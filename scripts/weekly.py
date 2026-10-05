#!/usr/bin/env python3
"""Evidence-first VSR watcher. Standard library; never executes discovered code."""
import argparse
import base64
import datetime as dt
import hashlib
import html
import ipaddress
import json
import math
import os
import re
import smtplib
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TZ = dt.timezone(dt.timedelta(hours=8))
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
ID_RE = r"\d{4}\.\d{4,5}"
REPO_RE = r"https://github\.com/([\w.-]+/[\w.-]+)"
OPEN_LICENSES = {"Apache-2.0", "MIT", "BSD-2-Clause", "BSD-3-Clause", "GPL-3.0", "GPL-2.0", "LGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC0-1.0", "Unlicense", "AGPL-3.0"}
PROMISE_RE = re.compile(r"(?:\b(?:our |the |all )?(?:source )?code\b.{0,60}\b(?:will be (?:made )?(?:available|released)|(?:coming|available) soon|to be released)\b|\b(?:we will|we plan to)\b.{0,40}\b(?:release|open.source)\b.{0,30}\bcode\b)", re.I)
CLOSED_RE = re.compile(r"(?:\bcode\b.{0,40}\b(?:will not|won.t|cannot|not planned to)\b.{0,30}\b(?:release|available)|\bclosed.source\b|\bno plans to release\b)", re.I)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp():
    return dt.datetime.now(TZ).isoformat(timespec="seconds")


def get(url, github=False, attempts=2, timeout=20):
    # Discovered project URLs must be public HTTPS names; no credentials travel there.
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("unsafe source URL")
    host = parsed.hostname.lower()
    if host in {"localhost", "metadata.google.internal"} or host.endswith((".local", ".internal")):
        raise ValueError("private source URL")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("literal IP source URL")
    headers = {"User-Agent": "awesome-vsr-4k/1.0 research literature watcher", "Accept": "application/json,text/html,application/atom+xml"}
    if github:
        if host != "api.github.com":
            raise ValueError("token destination must be GitHub API")
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = "Bearer " + token
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
                if github and urllib.parse.urlsplit(response.url).hostname != "api.github.com":
                    raise ValueError("unexpected GitHub redirect")
                return response.read(3_000_000).decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in {404, 410}:
                raise
            if attempt + 1 == attempts:
                raise RuntimeError("HTTP %d from %s" % (exc.code, host)) from None
        except (OSError, TimeoutError) as exc:
            if attempt + 1 == attempts:
                raise RuntimeError("network error from " + host) from None
        time.sleep(3 * (attempt + 1))


def gh(path):
    return json.loads(get("https://api.github.com/" + path, github=True))


def parse_feed(raw):
    root = ET.fromstring(raw)
    if root.find("a:entry/a:title", NS) is not None and root.find("a:entry/a:title", NS).text == "Error":
        raise RuntimeError("arXiv returned an error feed")
    papers = []
    for e in root.findall("a:entry", NS):
        aid = re.search(ID_RE, e.findtext("a:id", "", NS))
        if not aid:
            continue
        summary = clean(e.findtext("a:summary", "", NS))
        comment = clean(e.findtext("x:comment", "", NS))
        papers.append({"id": aid.group(), "title": clean(e.findtext("a:title", "", NS)),
                       "abstract": summary[:1200], "source_text": summary + " " + comment,
                       "authors": [clean(a.findtext("a:name", "", NS)) for a in e.findall("a:author", NS)],
                       "published": e.findtext("a:published", "", NS), "updated": e.findtext("a:updated", "", NS),
                       "paper_url": "https://arxiv.org/abs/" + aid.group(), "comment": comment})
    return papers


def arxiv(params):
    time.sleep(3.1)  # arXiv asks for at least three seconds between API calls.
    return parse_feed(get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)))


def relevant(p):
    title = p["title"].lower().replace("-", " ")
    return (("video" in title and any(x in title for x in ["super resolution", "restoration", "upscal"]))
            or re.search(r"\bvsr\b", title) is not None
            or (any(x in title for x in ["video generation", "video synthesis"])
                and re.search(r"\b4k\b|\buhd\b|high.resolution|ultra.high", p.get("source_text", ""), re.I)))


def heading_match(readme, title):
    # Bibliography/related-work full-title matches do not establish an official repo.
    head = readme[:4000]
    headings = [line for line in head.splitlines() if re.match(r"\s*(?:#{1,3}\s|>\s|\*\*|<h[1-3]\b)", line, re.I)]
    return any(norm(title) in norm(line) for line in headings) and bool(re.search(r"official|implementation|our (?:paper|work)|authors?:|^>.*", head, re.I | re.M))


def repo_info(repo, paper, trusted=False):
    meta = gh("repos/" + repo)
    readme_obj = gh("repos/" + repo + "/readme")
    readme = base64.b64decode(readme_obj["content"]).decode("utf-8", "replace")
    if meta.get("fork"):
        return None
    # trusted means a direct paper-to-repository link, not merely a search match.
    if not trusted:
        headings = " ".join(line for line in readme[:5000].splitlines() if re.match(r"\s*(?:#{1,3}\s|>\s|\*\*|<h[1-3]\b)", line, re.I))
        title_linked = norm(paper["title"]) in norm(headings)
        author_matches = sum(norm(author) in norm(readme[:5000]) for author in paper.get("authors", []) if len(norm(author)) > 5)
        official_claim = re.search(r"official|code for.{0,50}paper", meta.get("description") or "", re.I)
        if not (heading_match(readme, paper["title"]) or (title_linked and (author_matches >= 2 or official_claim))):
            return None
    tree = gh("repos/" + repo + "/git/trees/" + urllib.parse.quote(meta["default_branch"]) + "?recursive=1")
    paths = [x["path"] for x in tree.get("tree", []) if x.get("type") == "blob"]
    code = [x for x in paths if x.endswith((".py", ".cpp", ".cu", ".ipynb")) and not re.search(r"(^|/)(docs|assets|website|third_party|vendor)/", x)]
    lic = (meta.get("license") or {}).get("spdx_id") or "未知"
    if lic == "NOASSERTION":
        lic = "自定义/未识别"
    weights = sorted(set(re.findall(r"https://(?:huggingface\.co|drive\.google\.com|pan\.baidu\.com|onedrive\.live\.com)/[^\s<>\"')]+", readme)))[:6]
    # A generic HF project or a base model link isn't evidence of this model's weights.
    weight_lines = [line for line in readme.splitlines() if re.search(r"(?:pre.?trained|checkpoint|weights|models|ckpt|预训练)", line, re.I) and re.search(r"https://(?:huggingface\.co|drive\.google\.com|pan\.baidu\.com|onedrive\.live\.com)", line)]
    return {"repo": meta["full_name"], "repo_url": meta["html_url"], "stars": meta["stargazers_count"],
            "archived": meta.get("archived", False), "license": lic, "code_files": code[:8],
            "code_count": len(code), "weights": weights if weight_lines else [],
            "weights_note": "作者页面列有模型/权重链接，未验证下载" if weight_lines else "未确认该方法权重",
            "readme": readme, "venue_text": meta.get("description") or "", "evidence_url": meta["html_url"] + "/blob/" + meta["default_branch"] + "/" + readme_obj.get("path", "README.md"),
            "association": "论文/作者项目直接链接仓库" if trusted else "README 首部完整标题与官方实现声明/论文作者相符"}


def text_urls(text):
    return [x.rstrip(".,;)］】") for x in re.findall(r"https://[^\s<>\"']+", html.unescape(text))]


def verify(p, now, repo_hint="", old=None):
    source_text = p.get("source_text", "")
    candidates = [(r.rstrip("."), True) for r in re.findall(REPO_RE, source_text)]
    evidence = [{"url": p["paper_url"], "kind": "paper"}]
    # Follow project links explicitly supplied in the paper metadata, not arbitrary references.
    for url in text_urls(source_text):
        if candidates:
            break
        host = urllib.parse.urlsplit(url).hostname or ""
        if host.endswith(".github.io") or (host not in {"github.com", "arxiv.org", "doi.org", "huggingface.co"} and "project" in url.lower()):
            try:
                page = get(url, attempts=1, timeout=12)
                page_text = clean(re.sub(r"<[^>]+>", " ", page))
                # Require the current paper title in the project page.
                if norm(p["title"]) in norm(page_text):
                    # Author-linked page + current paper title + an explicit Code link.
                    for href, label in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', page, re.I | re.S):
                        repo_match = re.match(REPO_RE, href)
                        if repo_match and re.fullmatch(r"(?:code|github|implementation|official code|code repository)", clean(re.sub(r"<[^>]+>", " ", label)), re.I):
                            candidates.append((repo_match.group(1).rstrip("."), True))
                    source_text += " " + page_text
                    evidence.append({"url": url, "kind": "author_project"})
            except Exception:
                pass
            if len(evidence) >= 3:
                break
    if repo_hint:
        candidates.append((repo_hint, False))
    if old and old.get("repo"):
        candidates.append((old["repo"], False))
    if not candidates:
        try:
            q = '"' + p["title"].split(":")[0][:80] + '" in:name,description,readme fork:false'
            found = gh("search/repositories?" + urllib.parse.urlencode({"q": q, "per_page": 4, "sort": "stars"}))
            candidates.extend((r["full_name"], False) for r in found.get("items", []))
        except Exception:
            pass
    info = None
    checked = set()
    failed = False
    # A supplied hint must never suppress stronger direct-paper evidence for the same repo.
    candidates = [(repo, any(t for r, t in candidates if r == repo)) for repo, _ in candidates]
    for repo, trusted in candidates[:10]:
        if repo in checked:
            continue
        checked.add(repo)
        try:
            item = repo_info(repo, p, trusted)
            if item and (not info or item["code_count"] > info["code_count"]):
                info = item
            if info and info["code_count"]:
                break
        except urllib.error.HTTPError as exc:
            if exc.code not in {404, 410}:
                failed = True
        except Exception:
            failed = True
    if failed and old and old.get("repo") and not info:
        # Transient API errors cannot turn known published code into an unknown status.
        retained = dict(old)
        retained["verification_warning"] = "本次仓库核验失败，保留上次核验状态"
        return retained
    text = source_text + " " + (re.split(r"\n#{1,3}\s+(?:References|Acknowledg|Related)", info["readme"], flags=re.I)[0][:10000] if info else "")
    promise = PROMISE_RE.search(source_text)
    if info:
        # For repo promises use relevant header/news, not bibliographies.
        promise = promise or PROMISE_RE.search(info["readme"][:6000])
    closed = CLOSED_RE.search(source_text) or (CLOSED_RE.search(info["readme"][:6000]) if info else None)
    if info and info["code_count"] and not closed:
        state = "released"
    elif closed:
        state = "closed"
    elif promise:
        state = "promised"
    else:
        state = "unconfirmed"
    p = dict(p)
    p.pop("source_text", None)
    p.update({"open_status": state, "checked_at": now, "evidence": evidence,
              "promise_note": clean(promise.group()) if promise else "",
              "resolution": "作者明确提及 4K/UHD（未实测）" if re.search(r"\b4k\b|\buhd\b|3840\s*[x×]\s*2160", text, re.I) else "高分辨率相关，未确认 4K 证据",
              "category": "直接高分辨率视频生成" if re.search(r"video (generation|synthesis)", p["title"], re.I) and not re.search(r"restoration|super.resolution", p["title"], re.I) else "视频超分/修复"})
    if info:
        p.update({k: v for k, v in info.items() if k != "readme"})
        p["evidence"].append({"url": info["evidence_url"], "kind": "author_repository"})
        p["stars_delta"] = info["stars"] - (old.get("stars", info["stars"]) if old else info["stars"])
    else:
        p.update({"repo": "", "stars": 0, "stars_delta": 0, "license": "未知", "code_count": 0, "weights": [], "weights_note": "未确认权重"})
    # Venue is explicitly attributed to the author repository/metadata; not inferred from dates.
    venue = re.search(r"\b(CVPR|ICCV|ECCV|ICLR|NeurIPS|ICML|AAAI)\s*['’]?\s*(20\d{2}|\d{2})\b", (info.get("venue_text", "") + " " + info["readme"][:4000] if info else "") + " " + p.get("comment", ""), re.I)
    p["venue"] = (venue.group(1) + " " + venue.group(2) + "（作者来源标注）") if venue else "预印本/录用未核验"
    p["confidence"] = "来源关联与实现文件已核验" if state == "released" else "仅作者开源承诺，尚未发布" if state == "promised" else "证据不足"
    return p


def fingerprint(p):
    important = {k: p.get(k) for k in ["open_status", "repo", "license", "weights", "archived"]}
    return hashlib.sha256(json.dumps(important, sort_keys=True).encode()).hexdigest()[:16]


def rank(p):
    score = 40 if p["open_status"] == "released" else 10
    score += 20 if "4K/UHD" in p["resolution"] else 0
    score += 8 if re.search(r"diffusion|generative|one.step|streaming", p["title"], re.I) else 0
    score += 8 if p.get("license") in OPEN_LICENSES else 0
    score += 5 if "作者来源" in p.get("venue", "") else 0
    score += min(10, math.log10(p.get("stars", 0) + 1) * 3)
    return score


def select(papers, sent, config, bootstrap, today):
    eligible = []
    cutoff = today - dt.timedelta(days=config["lookback_days"])
    for p in papers:
        previous = sent.get(p["id"])
        changed = previous and previous != fingerprint(p)
        recent = max(p.get("published", ""), p.get("updated", ""))[:10] >= cutoff.isoformat()
        # A newly released code repository for an older paper remains news.
        release_news = p.get("resource_news", False)
        if p["open_status"] not in {"released", "promised"}:
            continue
        if p["id"] in config.get("already_read", []) and not changed:
            continue
        if (bootstrap and not previous) or changed or (not previous and (recent or release_news or p.get("pending_digest"))):
            p["digest_reason"] = "资源状态更新" if changed else "本周/近期新论文" if recent else "新开源/更新资源" if release_news else "基础阅读列表" if bootstrap else "上期候选回补"
            eligible.append(p)
    eligible.sort(key=lambda p: (p.get("digest_reason") == "本周/近期新论文", rank(p), p.get("published", "")), reverse=True)
    out, promised = [], 0
    for p in eligible:
        if p["open_status"] == "promised":
            if promised >= config["max_promised"]:
                continue
            promised += 1
        out.append(p)
        if len(out) == config["max_recommendations"]:
            break
    return out


def markdown(p):
    label = {"released": "代码已发布", "promised": "作者明确承诺开源", "unconfirmed": "开源未确认", "closed": "不推荐：闭源"}[p["open_status"]]
    reasons = [p.get("digest_reason", p["category"]), p["resolution"], p["confidence"]]
    return ("### [%s](%s)\n\n" % (p["title"], p["paper_url"]) +
            "- 发布：%s%s；%s\n" % (p["published"][:10], "（" + p["date_note"] + "）" if p.get("date_note") else "", p["venue"]) +
            "- 推荐依据：" + "；".join(reasons) + "。\n" +
            "- 开源：%s；[作者仓库](%s)；许可证：%s；实现文件：%s\n" % (label, p.get("repo_url", p["paper_url"]), p["license"], p["code_count"]) +
            "- 关注度：%s stars，较上次核验 %+d（仅作热度信号）。\n" % (p["stars"], p.get("stars_delta", 0)) +
            "- 复现边界：%s；未运行实验；%s。\n" % (p.get("weights_note", "未确认权重"), "仓库已归档" if p.get("archived") else "4K 实际显存、耗时与效果需进一步验证") +
            ("- 开源承诺：%s（作者原文片段，尚未发布）。\n" % p["promise_note"] if p["open_status"] == "promised" else "") +
            "- 核验来源：" + " / ".join("[证据 %d](%s)" % (i + 1, e["url"]) for i, e in enumerate(p["evidence"])) + "\n\n" +
            "作者摘要摘录（英文）：\n\n> " + p.get("abstract", "暂无摘要")[:800] + "\n\n")


def digest(selected, date, warnings, bootstrap, repo, stats):
    text = "# 4K 视频超分论文周报 · " + date + (" · 首次部署" if bootstrap else "") + "\n\n"
    text += "重点：4K/UHD、生成式视频超分、时序一致性与高效流式推理。\n\n"
    text += "本次读取 %d 篇论文元数据，核验 %d 篇；精选 %d 篇。基础阅读列表不会伪装成本周新论文。\n\n" % (stats["discovered"], stats["verified"], len(selected))
    if warnings:
        text += "检索/核验降级：" + "；".join(warnings) + "。本期覆盖不完整。\n\n"
    for category in ["released", "promised"]:
        items = [p for p in selected if p["open_status"] == category]
        if items:
            text += "## " + ("代码已发布" if category == "released" else "明确承诺开源，待发布") + "\n\n"
            text += "".join(markdown(p) for p in items)
    if not selected:
        text += "本期没有通过来源与开源证据筛选的未推送论文或重要资源更新，不凑数。已有论文仍会继续复查。\n\n"
    text += "[Awesome 仓库](https://github.com/" + repo + ") · [历期周报](https://github.com/" + repo + "/tree/main/digests)\n\n"
    text += "索引将在 SMTP 接受本邮件后更新。stars 不等于论文质量；公开代码、开放许可证、模型权重与实测 4K 能力分别判断。\n"
    return text


def send_mail(body, date, bootstrap, repo, edition=""):
    user, password, recipient = [os.environ.get(x, "") for x in ["QQ_SMTP_USER", "QQ_SMTP_PASS", "QQ_MAIL_TO"]]
    if not all([user, password, recipient]):
        raise RuntimeError("Missing QQ_SMTP_USER / QQ_SMTP_PASS / QQ_MAIL_TO secrets")
    message = EmailMessage()
    message["From"] = user
    message["To"] = recipient
    message["Subject"] = "4K 视频超分论文周报 · " + date + (" · " + edition if edition else "") + (" · 首次部署" if bootstrap else "")
    key = hashlib.sha256((repo + date + str(bootstrap) + edition).encode()).hexdigest()[:24]
    message["Message-ID"] = "<vsr-" + key + "@qq.com>"
    message.set_content(body)
    # Readable HTML without a markdown dependency; links remain clickable.
    escaped = html.escape(body)
    escaped = re.sub(r"\[([^\]]+)\]\((https://[^\s)]+)\)", r'<a href="\2">\1</a>', escaped)
    message.add_alternative('<html><body><div style="max-width:900px;font-family:Arial,sans-serif;white-space:pre-wrap;line-height:1.6">' + escaped + "</div></body></html>", subtype="html")
    with smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=45, context=ssl.create_default_context()) as server:
        server.login(user, password)
        refused = server.send_message(message)
        if refused:
            raise RuntimeError("SMTP refused at least one recipient")
    print("QQ SMTP accepted digest (recipient and credentials omitted)")


def update_readme(papers):
    sections = []
    for status in ["released", "promised"]:
        subset = [p for p in papers if p["open_status"] == status]
        subset.sort(key=lambda p: p.get("published", ""), reverse=True)
        sections.append("### " + ("已发布代码" if status == "released" else "作者明确承诺，待开源") + "\n\n")
        sections.append("| 论文 | 日期 / 会议 | 4K 证据 | 代码 / 许可证 | 关注度 | 模型研究判断 |\n| --- | --- | --- | --- | --- | --- |\n")
        for p in subset:
            safe_title = p["title"].replace("|", "/")
            review = p.get("ai_review", {})
            judgment = "[%s · %s](data/ai-review.json)" % (review["priority"], review["confidence"]) if review else "待分析"
            sections.append("| [%s](%s) | %s / %s | %s | [代码](%s) / %s | %d ★ | %s |\n" % (safe_title, p["paper_url"], p["published"][:10], p["venue"], p["resolution"], p.get("repo_url", p["paper_url"]), p["license"], p["stars"], judgment))
        sections.append("\n")
    path = ROOT / "README.md"
    content = path.read_text(encoding="utf-8")
    content = re.sub(r"<!-- PAPERS:START -->.*?<!-- PAPERS:END -->", "<!-- PAPERS:START -->\n" + "".join(sections) + "<!-- PAPERS:END -->", content, flags=re.S)
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--initialize", action="store_true", help="write initial index without emailing, for deployment only")
    args = parser.parse_args()
    cfg = load(ROOT / "config.json", {})
    today = dt.datetime.now(TZ).date()
    # Stable weekly key prevents manual/retry sends on different days of the same week.
    week = today - dt.timedelta(days=(today.weekday() - 2) % 7)
    date = today.isoformat() if args.bootstrap else week.isoformat()
    state_path = ROOT / "data/state.json"
    state = load(state_path, {"sent": {}, "delivered": []})
    run_key = ("bootstrap:" if args.bootstrap else "weekly:") + date
    if run_key in state["delivered"] and not args.dry_run and not args.initialize:
        print("Already delivered this period; no duplicate email")
        return
    old_list = load(ROOT / "data/papers.json", []) + load(ROOT / "data/watchlist.json", [])
    old = {p["id"]: p for p in old_list}
    discovered, warnings, successes = {}, [], 0
    cutoff = today - dt.timedelta(days=cfg["lookback_days"])
    for i, query in enumerate(cfg["queries"]):
        print("Searching arXiv query %d" % (i + 1), flush=True)
        try:
            rows = arxiv({"search_query": "(" + query + ") AND lastUpdatedDate:[" + cutoff.strftime("%Y%m%d") + "0000 TO " + today.strftime("%Y%m%d") + "2359]", "sortBy": "lastUpdatedDate", "sortOrder": "descending", "max_results": 200})
            discovered.update({p["id"]: p for p in rows if relevant(p)})
            successes += 1
            print("arXiv query %d: %d records" % (i + 1, len(rows)), flush=True)
        except Exception as exc:
            warnings.append("arXiv 查询 %d 失败：%s" % (i + 1, type(exc).__name__))
    if not successes:
        raise RuntimeError("All new-paper arXiv searches failed; refusing a false empty digest")
    hints = {p["id"]: p["repo"] for p in cfg["seed_papers"]}
    # GitHub discovery recovers code releases for papers outside the arXiv lookback.
    resource_ids = set()
    for query in ['"video super-resolution" fork:false pushed:>=' + cutoff.isoformat(), '"4K" "video generation" fork:false created:>=' + cutoff.isoformat()]:
        print("Searching GitHub resource releases", flush=True)
        try:
            repos = gh("search/repositories?" + urllib.parse.urlencode({"q": query, "sort": "updated", "per_page": 12}))
            for repo in repos.get("items", []):
                try:
                    obj = gh("repos/" + repo["full_name"] + "/readme")
                    readme = base64.b64decode(obj["content"]).decode("utf-8", "replace")
                    # Main paper links only; avoid swallowing a related-work bibliography.
                    ids = re.findall(r"arxiv\.org/(?:abs|pdf)/(" + ID_RE + ")", readme[:2500])[:2]
                    for aid in ids:
                        resource_ids.add(aid)
                        hints.setdefault(aid, repo["full_name"])
                except Exception:
                    continue
        except Exception:
            warnings.append("GitHub 新资源检索降级")
    ids = sorted((set(hints) | set(old) | resource_ids) - set(discovered))
    for start in range(0, len(ids), 60):
        print("Refreshing %d known/watchlist papers" % len(ids[start:start + 60]), flush=True)
        try:
            rows = arxiv({"id_list": ",".join(ids[start:start + 60]), "max_results": 60})
            discovered.update({p["id"]: p for p in rows if relevant(p)})
        except Exception:
            warnings.append("已有论文/开源状态回查不完整")
    for manual in cfg.get("manual_papers", []):
        discovered[manual["id"]] = manual
        hints[manual["id"]] = manual["repo"]
    now = stamp()
    verified = {}
    for i, (aid, p) in enumerate(sorted(discovered.items())):
        item = verify(p, now, hints.get(aid, ""), old.get(aid))
        item["resource_news"] = aid in resource_ids and aid not in old
        verified[aid] = item
        print("Verified %d/%d %s: %s" % (i + 1, len(discovered), aid, item["open_status"]), flush=True)
        time.sleep(1.1)  # Respect GitHub search throttling.
    for aid, p in old.items():
        if aid not in verified:
            verified[aid] = p
    papers = [p for p in verified.values() if p["open_status"] in {"released", "promised"}]
    watchlist = [p for p in verified.values() if p["open_status"] not in {"released", "promised"}]
    selected = select(papers, state["sent"], cfg, args.bootstrap, today)
    selected_ids = {p["id"] for p in selected}
    # Retain deferred recommendations; they must not disappear when they age out.
    for p in papers:
        if p["id"] not in state["sent"] and (p["id"] in selected_ids or max(p.get("published", ""), p.get("updated", ""))[:10] >= cutoff.isoformat() or p.get("resource_news")):
            p["pending_digest"] = True
    stats = {"discovered": len(discovered), "verified": len(verified)}
    body = digest(selected, date, warnings, args.bootstrap, cfg["repository"], stats)
    preview = ROOT / "work/preview.md"
    preview.parent.mkdir(parents=True, exist_ok=True)
    preview.write_text(body, encoding="utf-8")
    if args.dry_run:
        save(ROOT / "work/preview-papers.json", papers)
        save(ROOT / "work/preview-watchlist.json", watchlist)
        save(ROOT / "work/preview-status.json", {"warnings": warnings, **stats})
        print("Dry run: %d recommendations; no email or persistent state mutation" % len(selected))
        return
    if not args.initialize:
        send_mail(body, date, args.bootstrap, cfg["repository"])
        for p in selected:
            state["sent"][p["id"]] = fingerprint(p)
            p["pending_digest"] = False
        for p in papers:
            if p["id"] in cfg.get("already_read", []):
                state["sent"].setdefault(p["id"], fingerprint(p))
        state["delivered"].append(run_key)
        state["delivered"] = state["delivered"][-104:]
        digest_path = ROOT / "digests" / (date + ("-bootstrap" if args.bootstrap else "") + ".md")
        digest_path.parent.mkdir(parents=True, exist_ok=True)
        digest_path.write_text(body, encoding="utf-8")
        save(state_path, state)
    save(ROOT / "data/papers.json", sorted(papers, key=lambda p: p["published"], reverse=True))
    save(ROOT / "data/watchlist.json", sorted(watchlist, key=lambda p: p["published"], reverse=True))
    save(ROOT / "data/status.json", {"checked_at": now, "smtp_accepted": not args.initialize, "period": run_key, "warnings": warnings, **stats})
    update_readme(papers)
    print("Index prepared after " + ("initialization" if args.initialize else "SMTP acceptance"))


if __name__ == "__main__":
    main()
