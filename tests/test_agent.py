import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("agent_weekly", ROOT / "scripts/agent_weekly.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def candidate(status="released"):
    return {"id": "2609.12345", "title": "Video Super-Resolution", "paper_url": "https://arxiv.org/abs/2609.12345", "repo_url": "https://github.com/author/model", "open_status": status, "published": "2026-09-30", "license": "MIT", "stars": 1, "code_count": 3, "repo": "author/model", "weights": [], "resolution": "未确认", "venue": "预印本"}


def result():
    schema = json.loads((ROOT / "schemas/review.json").read_text(encoding="utf-8"))
    row = {key: "分析内容" for key in schema["properties"]["reviews"]["items"]["required"]}
    row.update(id="2609.12345", decision="recommend", priority="建议阅读", confidence="中", reading_basis="仅摘要与资源", sources=["https://arxiv.org/abs/2609.12345"])
    return {"weekly_summary": "研究趋势", "selected_ids": [row["id"]], "reviews": [row], "discoveries": []}


def packet(p=None):
    return {"date": "2026-10-05", "period": "codex:bootstrap:2026-10-05", "bootstrap": True, "candidates": [p or candidate()], "catalog": [p or candidate()], "max_recommendations": 8, "max_promised": 2, "already_read_ids": [], "already_sent_ids": [], "sent_fingerprints": {}, "collector_status": {"warnings": ["One source unavailable"]}}


class AgentSafeguards(unittest.TestCase):
    def test_model_cannot_override_open_source_check(self):
        for status in ["closed", "unconfirmed"]:
            with self.assertRaisesRegex(ValueError, "open-source"):
                a.validate_review(result(), packet(candidate(status)))

    def test_model_cannot_invent_paper_or_duplicate_it(self):
        review = result()
        review["selected_ids"] = ["not-verified"]
        with self.assertRaises(ValueError):
            a.validate_review(review, packet())
        review["selected_ids"] = ["2609.12345", "2609.12345"]
        with self.assertRaises(ValueError):
            a.validate_review(review, packet())

    def test_missing_analysis_and_nonprimary_sources_rejected(self):
        review = result()
        del review["reviews"][0]["limitations"]
        with self.assertRaises(ValueError):
            a.validate_review(review, packet())
        review = result()
        review["reviews"][0]["sources"] = ["https://news.example.com/claim"]
        with self.assertRaisesRegex(ValueError, "verified"):
            a.validate_review(review, packet())

    def test_reading_coverage_not_overstated(self):
        review = result()
        review["reviews"][0]["reading_basis"] = "正文与资源"
        a.validate_review(review, packet())
        self.assertEqual("仅摘要与资源", review["reviews"][0]["reading_basis"])

    def test_discovery_cannot_resend_unchanged_paper(self):
        p = candidate()
        request = packet()
        request.update(bootstrap=False, candidates=[], sent_fingerprints={p["id"]: a.w.fingerprint(p)})
        review = result()
        review["discoveries"] = [{"id": p["id"], "repo": "author/model", "source_url": p["paper_url"], "why": "新发现"}]
        with patch.object(a.w, "arxiv", return_value=[p]), patch.object(a.w, "verify", return_value=p), patch.object(a, "excerpt"):
            self.assertFalse(a.discover(review, request))

    def test_smtp_failure_does_not_mark_delivered(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "schemas").mkdir()
            (root / "schemas/review.json").write_bytes((ROOT / "schemas/review.json").read_bytes())
            (root / "work/agent").mkdir(parents=True)
            a.w.save(root / "work/agent/packet.json", packet())
            a.w.save(root / "work/agent/review.json", result())
            a.w.save(root / "config.json", {"repository": "owner/repo"})
            with patch.object(a.w, "ROOT", root), patch.object(a.w, "send_mail", side_effect=RuntimeError("SMTP failed")):
                with self.assertRaisesRegex(RuntimeError, "SMTP failed"):
                    a.finish("model")
            self.assertFalse((root / "data/state.json").exists())
            self.assertFalse((root / "data/ai-review.json").exists())

    def test_model_subprocess_does_not_receive_deploy_or_mail_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "result.json"
            def run(*args, **kwargs):
                env = kwargs["env"]
                self.assertFalse({"GITHUB_TOKEN", "QQ_SMTP_PASS", "VSR_AUTH_KEY", "PUBLIC_DEPLOY_KEY"} & set(env))
                output.write_text(json.dumps(result()), encoding="utf-8")
                return type("Completed", (), {"returncode": 0})()
            secret_env = {key: "test-value" for key in ["GITHUB_TOKEN", "QQ_SMTP_PASS", "VSR_AUTH_KEY", "PUBLIC_DEPLOY_KEY"]}
            with patch.dict(a.os.environ, secret_env), patch.object(a.subprocess, "run", side_effect=run):
                a.run_review(packet(), "model", Path(folder), output)

    def test_partial_search_failure_remains_visible(self):
        selected, records = a.validate_review(result(), packet())
        self.assertIn("One source unavailable", a.render(selected, records, result(), packet(), "model"))


if __name__ == "__main__":
    unittest.main()
