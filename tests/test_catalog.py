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

    def test_arxiv_identity_deduplicates_renamed_versions(self):
        paper = next(p for p in self.papers if p['arxiv_id'])
        renamed = dict(paper, id='renamed-record', title='A Completely Renamed Video Super-Resolution Paper')
        with self.assertRaisesRegex(ValueError, 'arXiv identity'):
            catalog.validate([paper, renamed])

    def test_plus_method_extension_is_not_erased_by_title_normalization(self):
        self.assertNotEqual(catalog.normalized_title('EvTexture: Video Super-Resolution'), catalog.normalized_title('EvTexture++: Video Super-Resolution'))

    def test_publication_types_do_not_mislabel_journals_as_conferences(self):
        rendered = catalog.render(self.papers)
        overview = next(line for line in rendered.splitlines() if line.startswith('目前收录'))
        for kind, label in [('conference', '会议论文'), ('journal', '期刊论文'), ('workshop', ' Workshop 论文'), ('preprint', '预印本')]:
            count = sum(p['publication_type'] == kind for p in self.papers)
            self.assertIn('**%d 篇%s**' % (count, label), overview)
        wrong = dict(self.papers[0], venue_status='preprint', venue='arXiv', publication_type='journal')
        with self.assertRaisesRegex(ValueError, 'disagree'):
            catalog.validate([wrong])

    def test_year_index_contains_each_paper_once(self):
        rendered = catalog.render_years(self.papers)
        self.assertEqual((ROOT / 'docs/BY_YEAR.md').read_text(encoding='utf-8'), rendered)
        for p in self.papers:
            self.assertEqual(1, rendered.count('](' + p['paper_url'] + ')'))

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

    def test_renamed_official_paper_upgrades_the_same_arxiv_record(self):
        preprint = dict(self.papers[0], id='stable-id', title='Early Video Super-Resolution Title', venue='arXiv', venue_status='preprint', publication_type='preprint', arxiv_id='2501.12345')
        source = {'venue': 'CVPR', 'year': 2026, 'kind': 'links', 'url': 'https://example.org/index'}
        accepted = dict(preprint, title='Renamed Video Super-Resolution Title', venue='CVPR', venue_status='verified', publication_type='conference', paper_url='https://example.org/accepted')
        with patch.object(refresh, 'new_record', return_value=accepted):
            papers, additions, _ = refresh.refresh([preprint], [source], loader=lambda url: '<a href="/accepted">' + accepted['title'] + '</a>')
        self.assertEqual(1, len(papers))
        self.assertEqual(0, additions)
        self.assertEqual('stable-id', papers[0]['id'])
        self.assertEqual('verified', papers[0]['venue_status'])
        self.assertEqual(accepted['title'], papers[0]['title'])

    def test_broad_inverse_problem_title_requires_super_resolution_evidence(self):
        source = {"venue": "CVPR", "year": 2026}
        with patch.object(refresh, "fetch", return_value='<div id="abstract">We solve video camera-control inpainting.</div>'):
            self.assertIsNone(refresh.new_record("Video Inverse Problem Solver", "https://example.org/paper", source))
        with patch.object(refresh, "fetch", return_value='<div id="abstract">We solve video super-resolution.</div><a href="https://github.com/template/site">Template</a>'):
            record = refresh.new_record("Video Inverse Problem Solver", "https://example.org/paper", source)
            self.assertEqual("", record["code_url"])

    def test_vsr_acronym_does_not_establish_video_super_resolution(self):
        source = {"venue": "ICML", "year": 2026}
        aliases = ["Zero-AVSR: Audio-Visual Speech Recognition", "AutoVSR: Visual-to-Symbolic Reasoning", "Multi-Speaker VSR"]
        with patch.object(refresh, "fetch", return_value='<div id="abstract">We solve visual speech recognition and symbolic reasoning.</div>'):
            for title in aliases:
                self.assertIsNone(refresh.new_record(title, "https://example.org/paper", source))

    def test_video_derived_sisr_and_video_quality_plus_image_sr_are_excluded(self):
        self.assertFalse(refresh.vsr_scope('VCISR: Blind Single Image Super-Resolution With Video Compression Synthetic Data', 'We evaluate SISR on video super-resolution datasets.'))
        self.assertFalse(refresh.vsr_scope('Short-form UGC Video Quality Assessment and Enhancement', 'Track1 evaluates video quality. Track2 studies single-image super-resolution.'))
        self.assertFalse(refresh.vsr_scope('Short-form UGC Video Quality Assessment and Enhancement', 'We study image super-resolution. The primary objective is to improve short-form UGC video quality.'))
        self.assertTrue(refresh.vsr_scope('Real-Time Single Image and Video Super-Resolution Using Sub-Pixel Convolution', 'We upscale videos.'))
        self.assertTrue(refresh.vsr_scope('DiTVR: Zero-Shot Diffusion Transformer for Video Restoration', 'Video restoration aims to reconstruct high-quality video sequences, addressing tasks such as super-resolution, denoising and deblurring.'))


if __name__ == "__main__":
    unittest.main()
