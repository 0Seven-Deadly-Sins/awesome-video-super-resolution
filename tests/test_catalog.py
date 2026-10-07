import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import catalog
import refresh


class BibliographyIntegrity(unittest.TestCase):
    def setUp(self):
        self.papers = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))

    def test_complete_collection_matches_rendered_readme(self):
        rendered = catalog.render(self.papers)
        self.assertEqual((ROOT / "README.md").read_text(encoding="utf-8"), rendered)
        for p in self.papers:
            self.assertEqual(1, rendered.count("](" + p["paper_url"] + ")"))

    def test_unexpected_personal_state_is_rejected(self):
        for key in ["unrelated_metadata", "personal_state"]:
            papers = copy.deepcopy(self.papers)
            papers[0][key] = "unexpected"
            with self.assertRaises(ValueError):
                catalog.validate(papers)

    def test_duplicate_preprint_and_conference_version_rejected(self):
        duplicate = dict(self.papers[0], id="another-id", venue="arXiv", venue_status="preprint")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            catalog.validate(self.papers + [duplicate])

    def test_unverified_acceptance_cannot_be_labeled_as_conference(self):
        papers = copy.deepcopy(self.papers)
        papers[0]["venue_status"] = "preprint"
        with self.assertRaisesRegex(ValueError, "attribution"):
            catalog.validate(papers)

    def test_source_failure_cannot_erase_collection(self):
        source = {"venue": "CVPR", "year": 2026, "kind": "links", "url": "https://example.org/index"}
        def offline(url):
            raise OSError("unavailable")
        with self.assertRaises(RuntimeError):
            refresh.refresh(self.papers, [source], loader=offline)
        self.assertEqual(len(self.papers), len(json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))))

    def test_additions_are_not_limited_to_a_batch_size(self):
        source = {"venue": "CVPR", "year": 2026, "kind": "links", "url": "https://example.org/index"}
        raw = "".join('<a href="/paper%d">New Video Super-Resolution Method %d</a>' % (i, i) for i in range(12))
        def record(title, url, src):
            return dict(self.papers[0], id=catalog.normalized_title(title), title=title, paper_url=url)
        with patch.object(refresh, "new_record", side_effect=record):
            papers, additions, warnings = refresh.refresh(self.papers, [source], loader=lambda url: raw)
        self.assertEqual(12, additions)
        self.assertEqual(len(self.papers) + 12, len(papers))
        self.assertFalse(warnings)

    def test_publisher_and_unquoted_ecva_index_formats(self):
        ecva = {"venue": "ECCV", "year": 2024, "kind": "ecva", "url": "https://www.ecva.net/papers.php"}
        raw = '<a href=papers/eccv_2024/html/1.php>Arbitrary-Scale Video Super-Resolution</a>'
        self.assertEqual(1, len(refresh.parse_index(raw, ecva)))
        raw = '<div class="paper"><p class="title">Video Super-Resolution via Events</p><a href="https://proceedings.mlr.press/v235/x.html">abs</a>'
        self.assertEqual(1, len(refresh.parse_index(raw, dict(ecva, kind="pmlr"))))

    def test_official_acceptance_upgrades_preprint_without_duplicate(self):
        preprint = dict(self.papers[0], venue="arXiv", venue_status="preprint")
        source = {"venue": "CVPR", "year": 2026, "kind": "links", "url": "https://example.org/index"}
        raw = '<a href="/accepted">' + preprint["title"] + '</a>'
        papers, additions, warnings = refresh.refresh([preprint], [source], loader=lambda url: raw)
        self.assertEqual(1, len(papers))
        self.assertEqual(0, additions)
        self.assertEqual("verified", papers[0]["venue_status"])
        self.assertEqual("CVPR", papers[0]["venue"])
        self.assertEqual(preprint["summary"], papers[0]["summary"])
        self.assertFalse(warnings)

    def test_new_conference_years_are_probed_automatically(self):
        source = {"venue": "CVPR", "year": 2026, "kind": "links", "url": "https://example.org/index"}
        sources = refresh.current_sources([source], 2028)
        self.assertEqual({2026, 2027, 2028}, {s["year"] for s in sources})
        self.assertTrue(any(s["venue"] == "ICCV" and s["year"] == 2027 for s in sources))
        self.assertFalse(any(s["venue"] == "ICCV" and s["year"] == 2028 for s in sources))

    def test_broad_inverse_problem_title_requires_super_resolution_evidence(self):
        source = {"venue": "CVPR", "year": 2026}
        with patch.object(refresh, "fetch", return_value='<div id="abstract">We solve video camera-control inpainting.</div>'):
            self.assertIsNone(refresh.new_record("Video Inverse Problem Solver", "https://example.org/paper", source))
        with patch.object(refresh, "fetch", return_value='<div id="abstract">We solve video super-resolution.</div><a href="https://github.com/template/site">Template</a>'):
            record = refresh.new_record("Video Inverse Problem Solver", "https://example.org/paper", source)
            self.assertEqual("", record["code_url"])


if __name__ == "__main__":
    unittest.main()
