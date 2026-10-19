"""Add recent VSR preprints from the official arXiv Atom API."""
import argparse
import datetime
import hashlib
import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET

import catalog
import refresh

NS = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
QUERY = '(ti:"video super-resolution" OR ti:"video super resolution" OR ti:"video upscaling" OR ti:"space-time super-resolution" OR ((ti:"video restoration" OR ti:VSR) AND abs:"super-resolution")) AND (cat:cs.CV OR cat:eess.IV OR cat:cs.LG)'


def collect(papers, loader=refresh.fetch, today=None):
    today = today or datetime.date.today()
    cutoff = today - datetime.timedelta(days=45)
    query = QUERY + ' AND submittedDate:[' + cutoff.strftime('%Y%m%d') + '0000 TO ' + today.strftime('%Y%m%d') + '2359]'
    result = list(papers)
    titles = {catalog.normalized_title(p['title']) for p in papers}
    ids = {p['arxiv_id'] for p in papers if p['arxiv_id']}
    start = 0
    while True:
        url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query': query, 'start': start, 'max_results': 100, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
        root = ET.fromstring(loader(url))
        if root.tag != '{' + NS['a'] + '}feed':
            raise ValueError('arXiv did not return an Atom feed')
        entries = root.findall('a:entry', NS)
        for entry in entries:
            title = refresh.clean(entry.findtext('a:title', '', NS))
            if title == 'Error':
                raise ValueError('arXiv returned an error feed')
            match = re.search(r'/(\d{4}\.\d{4,5})(?:v\d+)?$', entry.findtext('a:id', '', NS))
            if not match:
                continue
            aid = match.group(1)
            key = catalog.normalized_title(title)
            if aid in ids or key in titles:
                continue
            abstract = refresh.clean(entry.findtext('a:summary', '', NS))
            if not refresh.vsr_scope(title, abstract):
                continue
            published = entry.findtext('a:published', '', NS)
            year = int(published[:4])
            category = 'benchmarks' if re.search(r'dataset|benchmark|evaluating', title, re.I) else refresh.topic(title)
            promise = bool(re.search(r'\bcode\b.{0,60}\b(?:will be (?:made )?(?:available|released)|coming soon|to be released)\b', abstract, re.I))
            result.append({'id': hashlib.sha1(key.encode()).hexdigest()[:12], 'title': title,
                           'venue': 'arXiv', 'year': year, 'category': category, 'tags': [],
                           'summary': 'Video super-resolution preprint', 'paper_url': 'https://arxiv.org/abs/' + aid,
                           'pdf_url': 'https://arxiv.org/pdf/' + aid, 'code_url': '', 'project_url': '',
                           'arxiv_id': aid, 'venue_status': 'preprint', 'resource_status': 'promised' if promise else 'not-found', 'publication_type': 'preprint'})
            titles.add(key)
            ids.add(aid)
        start += len(entries)
        total = int(root.findtext('o:totalResults', str(start), NS))
        if not entries or start >= total:
            break
        time.sleep(3.1)
    catalog.validate(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    path = catalog.ROOT / 'data/catalog.json'
    papers = json.loads(path.read_text(encoding='utf-8'))
    try:
        result = collect(papers)
    except (OSError, ValueError, ET.ParseError) as error:
        print('::warning::arXiv preprint index unavailable (%s); existing bibliography preserved' % type(error).__name__)
        return
    if not args.dry_run:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        catalog.write_indexes(result)
    print('arXiv preprints: %d additions, %d total; dry_run=%s' % (len(result) - len(papers), len(result), args.dry_run))


if __name__ == '__main__':
    main()
