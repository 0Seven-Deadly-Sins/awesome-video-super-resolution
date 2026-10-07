"""Collect newly indexed VSR titles from official conference bibliographies."""
import argparse
import concurrent.futures
import datetime
import functools
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import urllib.robotparser

import catalog

DIRECT_TOPIC = re.compile(r"(?:video|space.?time|spatial.?temporal).*super.?resol|super.?resol.*video|video upscal|\b\w*VSR\b", re.I)
RELATED_TOPIC = re.compile(r"video.*(?:inverse problem|restor|enhanc)", re.I)


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


@functools.lru_cache(maxsize=1)
def neurips_robots():
    parser = urllib.robotparser.RobotFileParser("https://neurips.cc/robots.txt")
    parser.read()
    return parser


def fetch(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname == "neurips.cc" and parsed.path.startswith("/virtual/"):
        if not neurips_robots().can_fetch("VSR-bibliography/2.0", url):
            raise PermissionError("Source robots.txt disallows paper metadata retrieval")
    request = urllib.request.Request(url, headers={"User-Agent": "VSR-bibliography/2.0", "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(20000000).decode("utf-8", "replace")


def parse_index(raw, source):
    rows = []
    if source["kind"] == "pmlr":
        for block in raw.split('<div class="paper">')[1:]:
            title = re.search(r'<p class="title">(.*?)</p>', block, re.S)
            link = re.search(r'href="([^"]+)">abs</a>', block)
            if title and link:
                rows.append((clean(title.group(1)), link.group(1)))
    else:
        for href, label in re.findall(r'<a\b[^>]*href\s*=\s*["\x27]?([^\s>"\x27]+)["\x27]?[^>]*>(.*?)</a>', raw, re.S | re.I):
            if source["kind"] == "ecva" and ("eccv_%d" % source["year"]) not in href:
                continue
            rows.append((clean(label), urllib.parse.urljoin(source["url"], href)))
    return [(title, url) for title, url in rows if (DIRECT_TOPIC.search(title) or RELATED_TOPIC.search(title)) and len(title) < 250 and not re.search(r"3D Super|SuperGaussian", title, re.I)]


def topic(title):
    patterns = [("events", r"event"), ("faces", r"face"), ("joint", r"deblur|low.light|infrared|thermal|turbulen"),
                ("domains", r"medical|satellite|panoram|omnidirect|depth|render|cell"), ("spacetime", r"space.time|spatio.temporal|spatial.temporal|arbitrary.scale"),
                ("compression", r"compress|delivery|packet"), ("guided", r"text.guid|prompt|interactive|reference|keyframe"),
                ("efficiency", r"stream|online|efficient|lightweight|quantiz|edge|real.time|routing"), ("onestep", r"one.step|single.step|distill|speculative"),
                ("generative", r"diffusion|generative"), ("gan", r"GAN"), ("architecture", r"transformer|mamba|state.space")]
    return next((key for key, pattern in patterns if re.search(pattern, title, re.I)), "alignment")


def new_record(title, url, source):
    try:
        raw = fetch(url)
    except PermissionError:
        # A published official title is bibliographic evidence; restricted metadata stays blank.
        if not DIRECT_TOPIC.search(title):
            return None
        raw = ""
    abstract = re.search(r'<(?:div|p)\b[^>]*(?:id|class)=["\x27][^"\x27]*abstract[^"\x27]*["\x27][^>]*>(.*?)</(?:div|p)>', raw, re.S | re.I)
    if not abstract:
        abstract = re.search(r'<h[234][^>]*>\s*Abstract\s*</h[234]>\s*<p[^>]*>(.*?)</p>', raw, re.S | re.I)
    abstract_raw = abstract.group(1) if abstract else ""
    if not DIRECT_TOPIC.search(title):
        # Broad restoration and inverse-problem titles need an explicit SR task.
        if not re.search(r'super.?resol|upscal|low.resolution.*high.resolution', clean(abstract_raw), re.I):
            return None
    code_links = [href for href, label in re.findall(r'<a\b[^>]*href=["\x27]([^"\x27]+)["\x27][^>]*>(.*?)</a>', raw, re.S | re.I) if re.fullmatch(r'code|source code|implementation', clean(label), re.I)]
    repositories = re.findall(r'https://github\.com/([\w.-]+/[\w.-]+)', abstract_raw + " " + " ".join(code_links))
    repositories = [r.rstrip(".").removesuffix(".git") for r in repositories if not r.startswith("mlresearch/")]
    pdf = re.search(r'<meta[^>]*name=["\x27]citation_pdf_url["\x27][^>]*content=["\x27]([^"\x27]+)', raw)
    aid = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', raw)
    repo = repositories[0] if repositories else ""
    return {"id": hashlib.sha1(catalog.normalized_title(title).encode()).hexdigest()[:12], "title": title,
            "venue": source["venue"], "year": source["year"], "category": topic(title), "tags": [],
            "summary": "Video super-resolution", "paper_url": url, "pdf_url": html.unescape(pdf.group(1)) if pdf else "",
            "code_url": "https://github.com/" + repo if repo else "", "project_url": "", "arxiv_id": aid.group(1) if aid else "",
            "venue_status": "verified", "resource_status": "author-linked" if repo else "not-found"}


def current_sources(sources, year=None):
    """Probe official annual indexes as new conference years become available."""
    year = year or datetime.date.today().year
    latest = max(s["year"] for s in sources)
    result = list(sources)
    for y in range(latest + 1, year + 1):
        annual = [("CVPR", "https://openaccess.thecvf.com/CVPR%d?day=all" % y),
                  ("ICLR", "https://iclr.cc/virtual/%d/papers.html" % y),
                  ("ICML", "https://icml.cc/virtual/%d/papers.html" % y),
                  ("NeurIPS", "https://neurips.cc/Downloads/%d" % y)]
        annual += [("ICCV", "https://openaccess.thecvf.com/ICCV%d?day=all" % y)] if y % 2 else [("ECCV", "https://eccv.ecva.net/Conferences/%d/AcceptedPapers" % y)]
        result.extend({"venue": venue, "year": y, "kind": "links", "url": url} for venue, url in annual)
    return result


def refresh(papers, sources, loader=fetch):
    """An unavailable index cannot erase or truncate the existing collection."""
    known = {catalog.normalized_title(p["title"]): p for p in papers}
    candidates, warnings, successful = [], [], 0
    def read(source):
        try:
            return source, parse_index(loader(source["url"]), source), None
        except Exception as error:
            return source, [], type(error).__name__
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(read, sources))
    for source, rows, error in results:
        if error:
            warnings.append("%s %d: %s" % (source["venue"], source["year"], error))
            continue
        if not rows and any(p["venue"] == source["venue"] and p["year"] == source["year"] for p in papers):
            warnings.append("%s %d: index returned no known VSR titles" % (source["venue"], source["year"]))
            continue
        successful += 1
        for title, url in rows:
            existing = known.get(catalog.normalized_title(title))
            if existing and existing["venue_status"] == "preprint":
                existing.update(venue=source["venue"], year=source["year"], paper_url=url, venue_status="verified")
            elif existing is None:
                candidates.append((title, url, source))
    if not successful:
        raise RuntimeError("No conference index could be verified; catalog unchanged")
    additions = 0
    pending, queued = [], set()
    for title, url, source in candidates:
        key = catalog.normalized_title(title)
        if key in known or key in queued:
            continue
        queued.add(key)
        pending.append((title, url, source))
    def metadata(candidate):
        title, url, source = candidate
        try:
            return title, new_record(title, url, source), None
        except Exception as error:
            return title, None, type(error).__name__
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for title, record, error in pool.map(metadata, pending):
            if error:
                warnings.append("Paper metadata unavailable: %s (%s)" % (title, error))
            elif record is not None:
                known[catalog.normalized_title(title)] = record
                additions += 1
                print("Indexed addition: %s %d — %s" % (record["venue"], record["year"], title))
    result = sorted(known.values(), key=lambda p: (-p["year"], p["venue"], p["title"]))
    catalog.validate(result)
    return result, additions, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = catalog.ROOT / "data/catalog.json"
    papers = json.loads(path.read_text(encoding="utf-8"))
    sources = json.loads((catalog.ROOT / "data/sources.json").read_text(encoding="utf-8"))
    result, count, warnings = refresh(papers, current_sources(sources))
    for warning in warnings:
        print("::warning::" + warning)
    if not args.dry_run:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (catalog.ROOT / "README.md").write_text(catalog.render(result), encoding="utf-8")
    print("Bibliography refresh: %d additions, %d total; dry_run=%s" % (count, len(result), args.dry_run))


if __name__ == "__main__":
    main()
