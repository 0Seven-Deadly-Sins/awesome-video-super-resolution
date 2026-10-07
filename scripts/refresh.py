"""Collect newly indexed VSR titles from official conference bibliographies."""
import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

import catalog

TOPIC = re.compile(r"(?:video|space.?time|spatial.?temporal).*super.?resol|super.?resol.*video", re.I)


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def fetch(url):
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
    return [(title, url) for title, url in rows if TOPIC.search(title) and len(title) < 250 and not re.search(r"3D Super|SuperGaussian", title, re.I)]


def topic(title):
    patterns = [("events", r"event"), ("faces", r"face"), ("joint", r"deblur|low.light|infrared|thermal|turbulen"),
                ("domains", r"medical|satellite|panoram|omnidirect|depth|render|cell"), ("spacetime", r"space.time|spatio.temporal|spatial.temporal|arbitrary.scale"),
                ("compression", r"compress|delivery|packet"), ("guided", r"text.guid|prompt|interactive|reference|keyframe"),
                ("efficiency", r"stream|online|efficient|lightweight|quantiz|edge|real.time|routing"), ("onestep", r"one.step|single.step|distill|speculative"),
                ("generative", r"diffusion|generative"), ("gan", r"GAN"), ("architecture", r"transformer|mamba|state.space")]
    return next((key for key, pattern in patterns if re.search(pattern, title, re.I)), "alignment")


def new_record(title, url, source):
    raw = fetch(url)
    repositories = re.findall(r'https://github\.com/([\w.-]+/[\w.-]+)', raw)
    repositories = [r.rstrip(".").removesuffix(".git") for r in repositories if not r.startswith("mlresearch/")]
    pdf = re.search(r'<meta[^>]*name=["\x27]citation_pdf_url["\x27][^>]*content=["\x27]([^"\x27]+)', raw)
    aid = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', raw)
    repo = repositories[0] if repositories else ""
    return {"id": hashlib.sha1(catalog.normalized_title(title).encode()).hexdigest()[:12], "title": title,
            "venue": source["venue"], "year": source["year"], "category": topic(title), "tags": [],
            "summary": "Video super-resolution", "paper_url": url, "pdf_url": html.unescape(pdf.group(1)) if pdf else "",
            "code_url": "https://github.com/" + repo if repo else "", "project_url": "", "arxiv_id": aid.group(1) if aid else "",
            "venue_status": "verified", "resource_status": "author-linked" if repo else "not-found"}


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
            if catalog.normalized_title(title) not in known:
                candidates.append((title, url, source))
    if not successful:
        raise RuntimeError("No conference index could be verified; catalog unchanged")
    additions = 0
    for title, url, source in candidates:
        key = catalog.normalized_title(title)
        if key in known:
            continue
        try:
            known[key] = new_record(title, url, source)
            additions += 1
        except Exception as error:
            warnings.append("Paper metadata unavailable: %s (%s)" % (title, type(error).__name__))
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
    result, count, warnings = refresh(papers, sources)
    for warning in warnings:
        print("::warning::" + warning)
    if not args.dry_run:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (catalog.ROOT / "README.md").write_text(catalog.render(result), encoding="utf-8")
    print("Bibliography refresh: %d additions, %d total; dry_run=%s" % (count, len(result), args.dry_run))


if __name__ == "__main__":
    main()
