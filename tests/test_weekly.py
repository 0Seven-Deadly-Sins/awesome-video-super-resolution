import datetime as dt
import importlib.util
import json
import tempfile
from types import SimpleNamespace
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("weekly", Path(__file__).resolve().parents[1] / "scripts/weekly.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


def paper(**kwargs):
    p = {"id": "2609.12345", "title": "Video Super-Resolution via Diffusion", "published": "2026-09-30", "updated": "2026-09-30", "open_status": "released", "repo": "author/model", "license": "MIT", "weights": [], "stars": 10, "resolution": "作者明确提及 4K/UHD（未实测）", "venue": "预印本/录用未核验"}
    p.update(kwargs)
    return p


class WatcherTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {"lookback_days": 21, "max_recommendations": 8, "max_promised": 2, "already_read": []}
        self.today = dt.date(2026, 10, 5)

    def test_closed_and_unknown_never_recommended(self):
        self.assertEqual([], w.select([paper(open_status="closed"), paper(id="x", open_status="unconfirmed")], {}, self.cfg, True, self.today))

    def test_recent_released_allowed_without_popularity(self):
        self.assertEqual(1, len(w.select([paper(stars=0)], {}, self.cfg, False, self.today)))

    def test_stars_and_check_date_do_not_trigger_duplicate(self):
        p = paper()
        state = {p["id"]: w.fingerprint(p)}
        p.update(stars=1000, checked_at="later")
        self.assertEqual([], w.select([p], state, self.cfg, False, self.today))

    def test_code_release_recommended_for_old_paper(self):
        p = paper(published="2024-01-01", updated="2024-01-01", open_status="promised")
        state = {p["id"]: w.fingerprint(p)}
        p["open_status"] = "released"
        self.assertEqual(1, len(w.select([p], state, self.cfg, False, self.today)))

    def test_promises_capped(self):
        papers = [paper(id=str(i), open_status="promised") for i in range(5)]
        self.assertEqual(2, len(w.select(papers, {}, self.cfg, False, self.today)))

    def test_backlog_survives_lookback(self):
        self.assertEqual(1, len(w.select([paper(published="2024-01-01", updated="2024-01-01", pending_digest=True)], {}, self.cfg, False, self.today)))

    def test_already_read_suppressed_until_material_change(self):
        p = paper()
        self.cfg["already_read"] = [p["id"]]
        self.assertEqual([], w.select([p], {}, self.cfg, True, self.today))
        old = w.fingerprint(p)
        p["weights"] = ["https://huggingface.co/author/model"]
        self.assertEqual(1, len(w.select([p], {p["id"]: old}, self.cfg, False, self.today)))

    def test_unrelated_image_sr_excluded(self):
        self.assertFalse(w.relevant(paper(title="4K Image Super-Resolution")))
        self.assertTrue(w.relevant(paper(title="4K Video Generation", source_text="4K")))

    def test_related_work_does_not_establish_official_repo(self):
        title = "Video Super-Resolution via Diffusion"
        self.assertFalse(w.heading_match("# Awesome list\nA list of Video Super-Resolution via Diffusion implementations", title))
        self.assertTrue(w.heading_match("# " + title + "\nOfficial implementation", title))

    def test_empty_repo_and_generic_coming_soon_not_released(self):
        p = paper(source_text="Dataset coming soon. https://github.com/author/model", paper_url="https://arxiv.org/abs/2609.12345", abstract="abstract", authors=[], comment="")
        mock = {"repo": "author/model", "repo_url": "https://github.com/author/model", "readme": "Dataset coming soon", "code_count": 0, "code_files": [], "license": "MIT", "stars": 0, "weights": [], "weights_note": "未知", "association": "direct", "evidence_url": "https://github.com/author/model", "archived": False}
        with patch.object(w, "repo_info", return_value=mock):
            result = w.verify(p, "now")
        self.assertEqual("unconfirmed", result["open_status"])
        self.assertNotIn("4K/UHD", result["resolution"])

    def test_explicit_code_promise_only(self):
        self.assertIsNotNone(w.PROMISE_RE.search("Our code will be released soon."))
        self.assertIsNone(w.PROMISE_RE.search("The dataset is coming soon."))

    def test_smtp_missing_secrets_fails(self):
        with patch.dict(w.os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                w.send_mail("body", "2026-10-05", False, "owner/repo")

    def test_smtp_failure_does_not_publish_or_mark_delivered(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = dict(self.cfg, repository="owner/repo", queries=["query"], seed_papers=[])
            (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
            original = "<!-- PAPERS:START -->original<!-- PAPERS:END -->"
            (root / "README.md").write_text(original, encoding="utf-8")
            p = paper(abstract="text", paper_url="https://arxiv.org/abs/2609.12345", category="视频超分/修复", confidence="核验", code_count=2, evidence=[], weights_note="未确认")
            args = SimpleNamespace(dry_run=False, bootstrap=True, initialize=False)
            with patch.object(w, "ROOT", root), patch.object(w.argparse.ArgumentParser, "parse_args", return_value=args), patch.object(w, "arxiv", return_value=[p]), patch.object(w, "gh", return_value={"items": []}), patch.object(w, "verify", return_value=p), patch.object(w.time, "sleep"), patch.object(w, "send_mail", side_effect=RuntimeError("SMTP failed")):
                with self.assertRaises(RuntimeError):
                    w.main()
            self.assertFalse((root / "data/state.json").exists())
            self.assertFalse((root / "data/papers.json").exists())
            self.assertEqual(original, (root / "README.md").read_text(encoding="utf-8"))

    def test_all_search_failures_are_not_an_empty_week(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = dict(self.cfg, repository="owner/repo", queries=["query"], seed_papers=[])
            (root / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
            args = SimpleNamespace(dry_run=False, bootstrap=False, initialize=False)
            with patch.object(w, "ROOT", root), patch.object(w.argparse.ArgumentParser, "parse_args", return_value=args), patch.object(w, "arxiv", side_effect=RuntimeError("search failed")), patch.object(w, "send_mail") as send:
                with self.assertRaisesRegex(RuntimeError, "All new-paper"):
                    w.main()
                send.assert_not_called()

    def test_direct_paper_evidence_survives_untrusted_seed_hint(self):
        p = paper(source_text="Code: https://github.com/author/model", paper_url="https://arxiv.org/abs/2609.12345", abstract="", authors=[], comment="")
        with patch.object(w, "repo_info", return_value=None) as verify:
            w.verify(p, "now", "author/model")
        self.assertTrue(verify.call_args.args[2])

    def test_author_project_code_link_and_repository_migration(self):
        title = "SeedVR2: One-Step Video Restoration"
        p = paper(title=title, source_text="Project page https://author.github.io/projects/seedvr2/", paper_url="https://arxiv.org/abs/2506.05301", authors=[])
        page = '<h1>' + title + '</h1><a href="https://github.com/new-owner/SeedVR">Code</a><a href="https://github.com/template/website">source code</a>'
        with patch.object(w, "get", return_value=page), patch.object(w, "repo_info", return_value=None) as check:
            w.verify(p, "now", "old-owner/SeedVR2")
        self.assertEqual("new-owner/SeedVR", check.call_args_list[0].args[0])
        self.assertTrue(check.call_args_list[0].args[2])
        self.assertNotIn("template/website", [call.args[0] for call in check.call_args_list])

    def test_html_headings_are_supported(self):
        self.assertTrue(w.heading_match('<h1>Video Super-Resolution via Diffusion</h1>\nOfficial implementation', "Video Super-Resolution via Diffusion"))


if __name__ == "__main__":
    unittest.main()
