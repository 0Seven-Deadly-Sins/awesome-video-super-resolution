import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import catalog
import preprints


def feed(rows, total=None):
    entries = ''.join('<entry><id>http://arxiv.org/abs/%sv1</id><title>%s</title><summary>%s</summary><published>2026-10-10T00:00:00Z</published></entry>' % (aid, escape(title), escape(summary)) for aid, title, summary in rows)
    return '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:o="http://a9.com/-/spec/opensearch/1.1/"><o:totalResults>%d</o:totalResults>%s</feed>' % (len(rows) if total is None else total, entries)


class PreprintSources(unittest.TestCase):
    def test_no_code_or_4k_requirement_but_explicit_vsr_task_required(self):
        raw = feed([('2610.12345', 'Streaming Video Super-Resolution', 'We upscale videos to 720p.'),
                    ('2610.12346', 'Fast Video Restoration', 'Our method performs video super-resolution and denoising.'),
                    ('2610.12347', 'Native 4K Video Restoration', 'We denoise native 4K video.'),
                    ('2610.12348', 'AutoVSR', 'Visual speech recognition.')])
        papers = preprints.collect([], loader=lambda url: raw)
        self.assertEqual({'2610.12345', '2610.12346'}, {p['arxiv_id'] for p in papers})
        self.assertTrue(all(p['resource_status'] == 'not-found' for p in papers))

    def test_pagination_has_no_recommendation_batch_cap(self):
        pages = [feed([('2610.12345', 'Video Super-Resolution A', '')], 2), feed([('2610.12346', 'Video Super-Resolution B', '')], 2)]
        urls = []
        def load(url):
            urls.append(url)
            return pages.pop(0)
        with patch.object(preprints.time, 'sleep'):
            papers = preprints.collect([], loader=load)
        self.assertEqual(2, len(papers))
        self.assertIn('start=1', urls[1])

    def test_author_release_promise_is_annotated_without_inventing_a_repository(self):
        raw = feed([('2610.12345', 'High-Throughput Video Super-Resolution', 'Code will be released upon acceptance.')])
        paper = preprints.collect([], loader=lambda url: raw)[0]
        self.assertEqual('promised', paper['resource_status'])
        self.assertEqual('', paper['code_url'])
        self.assertEqual('efficiency', paper['category'])

    def test_existing_paper_id_and_conference_version_are_preserved(self):
        original = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))[0]
        raw = feed([('2610.12345', original['title'], ''), (original['arxiv_id'] or '2610.12346', 'Renamed Video Super-Resolution', '')])
        original = dict(original, arxiv_id=original['arxiv_id'] or '2610.12346')
        papers = preprints.collect([original], loader=lambda url: raw)
        self.assertEqual([original], papers)

    def test_source_failure_preserves_saved_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            path = root / 'data/catalog.json'
            content = (ROOT / 'data/catalog.json').read_bytes()
            path.write_bytes(content)
            with patch.object(catalog, 'ROOT', root), patch.object(sys, 'argv', ['preprints']), patch.object(preprints, 'collect', side_effect=OSError('HTTP 502')):
                preprints.main()
            self.assertEqual(content, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
