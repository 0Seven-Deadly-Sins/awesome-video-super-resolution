#!/usr/bin/env python3
"""Codex reviews evidence; Python validates, emails and publishes. No silent fallback."""
import argparse
import datetime as dt
import html.parser
import json
import os
import re
import signal
import subprocess
from pathlib import Path

import weekly as w


class VisibleText(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav"}:
            self.hidden += 1
        if tag in {"p", "div", "section", "h1", "h2", "h3", "li"} and not self.hidden:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def excerpt(p):
    result = {"basis": "仅摘要与资源", "text": "", "source": p["paper_url"]}
    if not re.fullmatch(w.ID_RE, p["id"]):
        return result
    try:
        raw = w.get("https://arxiv.org/html/" + p["id"], attempts=1, timeout=20)
        parser = VisibleText()
        parser.feed(raw)
        text = w.clean(" ".join(parser.parts))
        if len(text) > 3000 and w.norm(p["title"]) in w.norm(text[:4000]):
            result = {"basis": "正文节选与资源", "text": text[:28000], "source": "https://arxiv.org/html/" + p["id"]}
    except Exception:
        pass
    return result


def packet_path():
    return w.ROOT / "work/agent/packet.json"


def prepare(bootstrap=False):
    cfg = w.load(w.ROOT / "config.json", {})
    state = w.load(w.ROOT / "data/state.json", {"sent": {}, "delivered": []})
    today = dt.datetime.now(w.TZ).date()
    date = today.isoformat() if bootstrap else (today - dt.timedelta(days=(today.weekday() - 2) % 7)).isoformat()
    period = "codex:" + ("bootstrap:" if bootstrap else "weekly:") + date
    if period in state["delivered"]:
        print("Codex digest already delivered this period")
        return False
    # Existing collector is reused as a broad source of evidence, not as final selector.
    subprocess.run([os.sys.executable, str(w.ROOT / "scripts/weekly.py"), "--dry-run", "--bootstrap"], check=True)
    papers = w.load(w.ROOT / "work/preview-papers.json", []) + w.load(w.ROOT / "work/preview-watchlist.json", [])
    cutoff = today - dt.timedelta(days=cfg["lookback_days"])
    candidates = []
    for p in papers:
        changed = state["sent"].get(p["id"]) and state["sent"][p["id"]] != w.fingerprint(p)
        recent = max(p.get("published", ""), p.get("updated", ""))[:10] >= cutoff.isoformat()
        due = bootstrap or changed or (not state["sent"].get(p["id"]) and (recent or p.get("resource_news") or p.get("pending_digest")))
        if due and (p["id"] not in cfg["already_read"] or changed):
            p["material_change"] = bool(changed)
            p["paper_excerpt"] = excerpt(p)
            candidates.append(p)
    # Baselines and sent papers remain context; only due candidates are eligible for this issue.
    packet = {"period": period, "date": date, "bootstrap": bootstrap, "collected_at": w.stamp(),
              "max_recommendations": cfg["max_recommendations"], "max_promised": cfg["max_promised"],
              "already_read_ids": cfg["already_read"], "already_sent_ids": list(state["sent"]),
              "sent_fingerprints": state["sent"],
              "candidates": candidates, "catalog": papers,
              "baseline_context": [{k: p.get(k) for k in ["id", "title", "paper_url", "abstract", "repo_url"]} for p in papers if p["id"] in cfg["already_read"]],
              "collector_status": w.load(w.ROOT / "work/preview-status.json", {})}
    # Model discoveries beyond this issue's bounded second pass are not forgotten.
    pending = w.load(w.ROOT / "data/ai-review.json", {}).get("discoveries", [])
    if pending:
        discover({"discoveries": pending}, packet)
    w.save(packet_path(), packet)
    print("Prepared %d candidates for Codex analysis" % len(candidates))
    return True


def execute_review(command, **options):
    prompt = options.pop("input")
    timeout = options.pop("timeout")
    # The npm launcher spawns a native CLI. Kill the entire process group on timeout.
    process = subprocess.Popen(command, stdin=subprocess.PIPE, start_new_session=os.name != "nt", **options)
    try:
        stdout, stderr = process.communicate(prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.communicate(timeout=10)
        raise RuntimeError("Codex analysis exceeded the 20-minute limit; no email sent") from None
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def run_review(packet, model, auth_home, output):
    # Run the model with only the packet, schema and prompt in an isolated working directory.
    isolated = w.ROOT / "work/agent/reviewer"
    isolated.mkdir(parents=True, exist_ok=True)
    prompt = (w.ROOT / "prompts/reviewer.md").read_text(encoding="utf-8")
    prompt += "\n\n本期请求与候选材料 JSON：\n" + json.dumps({k: v for k, v in packet.items() if k not in {"catalog", "collector_status", "sent_fingerprints"}}, ensure_ascii=False)
    output = output.resolve()
    schema = (w.ROOT / "schemas/review.json").resolve()
    task_environment = {k: v for k, v in os.environ.items() if k in {"PATH", "SystemRoot", "WINDIR", "TEMP", "TMP", "HOME", "USERPROFILE", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY"}}
    task_environment["CODEX_HOME"] = str(auth_home.resolve())
    cli = os.environ.get("CODEX_EXECUTABLE", "codex")
    effort = os.environ.get("VSR_REASONING_EFFORT", "xhigh")
    if effort not in {"low", "medium", "high", "xhigh", "max", "ultra"}:
        raise ValueError("Unsupported reasoning effort configuration")
    command = [cli, "exec", "--json", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only", "--disable", "shell_tool", "--disable", "plugins", "--disable", "unbounded_connection_retries", "--model", model,
               "-c", 'model_reasoning_effort="' + effort + '"', "-c", 'web_search="live"', "-c", 'shell_environment_policy.inherit="none"',
               "-c", 'agents.enabled=false', "-c", 'apps._default.enabled=false',
               "--output-schema", str(schema), "--output-last-message", str(output), "-"]
    result = execute_review(command, input=prompt, text=True, encoding="utf-8", env=task_environment, cwd=isolated,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1200)
    # Publish only counters, never raw tool text, model execution logs or credentials.
    counters = {"model": model, "reasoning_effort": effort, "web_searches": 0, "usage": {}}
    for line in getattr(result, "stdout", "").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "turn.completed":
            counters["usage"] = {k: v for k, v in event.get("usage", {}).items() if isinstance(v, int)}
        if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "web_search":
            counters["web_searches"] += 1
    metadata = w.load(w.ROOT / "work/agent/execution-meta.json", [])
    metadata.append(counters)
    w.save(w.ROOT / "work/agent/execution-meta.json", metadata)
    print("Codex execution counters: " + json.dumps(counters))
    # Do not put raw model/tool execution logs into public artifacts or CI logs.
    if result.returncode or not output.exists():
        # Classify failures without exposing raw logs, tokens, tool input or env values.
        log = (result.stderr + result.stdout).lower()
        reason = next((name for name, markers in [
            ("authentication", ["unauthorized", "token expired", "refresh token", "401"]),
            ("quota", ["usage limit", "quota", "rate limit", "429"]),
            ("invalid configuration", ["unexpected argument", "invalid schema", "not supported", "model not found", "error loading config", "reserved built-in", "unknown feature"]),
            ("network", ["connection", "timeout", "stream disconnected"])
        ] if any(marker in log for marker in markers)), "unclassified")
        print("Codex failure category: " + reason)
        # Show only a bounded error line, with current session token values removed.
        error_lines = [line for line in (result.stderr + result.stdout).splitlines() if re.match(r"(?i)^error(?: loading config\.toml)?:", line.strip())]
        if error_lines:
            detail = error_lines[-1]
            cache = w.load(auth_home / "auth.json", {})
            for value in cache.get("tokens", {}).values():
                if isinstance(value, str) and len(value) > 16:
                    detail = detail.replace(value, "[REDACTED]")
            detail = re.sub(r"eyJ[\w.-]+|Bearer\s+\S+", "[REDACTED]", detail)
            print("Codex error summary: " + detail[:350])
        raise RuntimeError("Codex analysis failed (exit %s); no rule-only email will be sent" % result.returncode)
    return w.load(output, {})


def validate_review(review, packet):
    required = {"weekly_summary", "selected_ids", "reviews", "discoveries"}
    if not isinstance(review, dict) or set(review) != required or not isinstance(review["selected_ids"], list):
        raise ValueError("Malformed Codex result")
    schema = w.load(w.ROOT / "schemas/review.json", {})["properties"]
    if not isinstance(review["weekly_summary"], str) or not review["weekly_summary"].strip():
        raise ValueError("Missing weekly analysis")
    for field in ["reviews", "discoveries"]:
        if not isinstance(review[field], list):
            raise ValueError("Malformed model records")
        item_schema = schema[field]["items"]
        for row in review[field]:
            if not isinstance(row, dict) or set(row) != set(item_schema["required"]):
                raise ValueError("Incomplete model record")
            for key, definition in item_schema["properties"].items():
                value = row[key]
                if definition["type"] == "string" and not isinstance(value, str):
                    raise ValueError("Invalid model text")
                if "enum" in definition and value not in definition["enum"]:
                    raise ValueError("Invalid model category")
                if definition["type"] == "array" and (not isinstance(value, list) or any(not isinstance(x, str) for x in value)):
                    raise ValueError("Invalid model source list")
    candidates = {p["id"]: p for p in packet["candidates"]}
    records = {r["id"]: r for r in review["reviews"]}
    if len(records) != len(review["reviews"]):
        raise ValueError("Duplicate model reviews")
    ids = review["selected_ids"]
    if any(not isinstance(aid, str) for aid in ids) or len(ids) != len(set(ids)) or len(ids) > packet["max_recommendations"]:
        raise ValueError("Duplicate or too many model recommendations")
    promised = 0
    for aid in ids:
        if aid not in candidates or aid not in records:
            raise ValueError("Model selected an unverified or unexplained paper")
        p, record = candidates[aid], records[aid]
        if p["open_status"] not in {"released", "promised"}:
            raise ValueError("Model selected a paper without verified open-source evidence")
        explanations = ["contribution", "why_read", "comparison", "evidence_quality", "limitations", "reproduction", "four_k", "reading_plan"]
        if record.get("decision") != "recommend" or any(not record[key].strip() for key in explanations) or not record.get("sources"):
            raise ValueError("Model recommendation lacks rationale or primary sources")
        if record.get("reading_basis") == "正文与资源":
            # Full reading coverage cannot be independently established from the response.
            record["reading_basis"] = p.get("paper_excerpt", {}).get("basis", "仅摘要与资源")
        if any(not isinstance(url, str) or not url.startswith("https://") for url in record["sources"]):
            raise ValueError("Invalid model source URL")
        primary = {p.get("paper_url"), p.get("repo_url"), "https://arxiv.org/html/" + aid, "https://arxiv.org/pdf/" + aid}
        if not any(url.rstrip("/") in primary for url in record["sources"]):
            raise ValueError("Recommendation has no verified paper/repository source")
        promised += p["open_status"] == "promised"
    if promised > packet["max_promised"]:
        raise ValueError("Too many promised-code papers")
    return [candidates[aid] for aid in ids], records


def discover(review, packet):
    fresh = {}
    hints = {}
    known = {p["id"]: p for p in packet["candidates"]}
    for d in review.get("discoveries", [])[:8]:
        aid = d.get("id", "")
        if re.fullmatch(w.ID_RE, aid) and (aid not in known or (known[aid]["open_status"] == "unconfirmed" and d.get("repo"))):
            hints[d["id"]] = d.get("repo", "") if re.fullmatch(r"[\w.-]+/[\w.-]+", d.get("repo", "")) else ""
    if hints:
        rows = w.arxiv({"id_list": ",".join(hints), "max_results": 8})
        for p in rows:
            # Semantic topic relevance is decided by Codex, rather than the title keyword gate.
            item = w.verify(p, w.stamp(), hints[p["id"]])
            prior = packet.get("sent_fingerprints", {}).get(p["id"])
            changed = bool(prior and prior != w.fingerprint(item))
            if p["id"] in packet["already_read_ids"] and not changed:
                continue
            if prior and not changed and not packet["bootstrap"]:
                continue
            item["material_change"] = changed
            item["paper_excerpt"] = excerpt(item)
            fresh[p["id"]] = item
    for p in fresh.values():
        packet["candidates"] = [x for x in packet["candidates"] if x["id"] != p["id"]] + [p]
        packet["catalog"] = [x for x in packet["catalog"] if x["id"] != p["id"]] + [p]
    return bool(fresh)


def analyze(model, auth_home):
    packet = w.load(packet_path(), {})
    if not packet:
        print("No prepared issue; nothing to analyze")
        return
    output = w.ROOT / "work/agent/review.json"
    review = run_review(packet, model, auth_home, output)
    # A second pass only occurs when the model discovers candidates absent from the packet.
    if discover(review, packet):
        w.save(packet_path(), packet)
        review = run_review(packet, model, auth_home, output)
    validate_review(review, packet)
    w.save(output, review)
    print("Codex review validated: %d selected papers" % len(review["selected_ids"]))


def render(selected, records, review, packet, model):
    text = "# 4K 视频超分论文周报 · " + packet["date"] + " · Codex 研究分析\n\n"
    text += "分析模型：" + model + "；联网检索与论文/资源分析。以下研究判断由模型生成，尚未人工复现实验。\n\n"
    text += review["weekly_summary"] + "\n\n"
    warnings = packet.get("collector_status", {}).get("warnings", [])
    if warnings:
        text += "检索降级说明：" + "；".join(str(x) for x in warnings) + "。本期覆盖可能不完整。\n\n"
    if not selected:
        text += "本期没有值得推荐且通过开源证据核验的新候选，不凑数。\n\n"
    for p in selected:
        r = records[p["id"]]
        p["digest_reason"] = r["priority"] + "：" + r["why_read"]
        text += "## [%s](%s) · %s\n\n" % (p["title"], p["paper_url"], r["priority"])
        text += "发布：%s；阅读依据：%s；模型分析置信度：%s。\n\n" % (p["published"][:10], r["reading_basis"], r["confidence"])
        for label, key in [("核心贡献", "contribution"), ("为什么值得读", "why_read"), ("与已读工作的关系", "comparison"), ("实验与证据", "evidence_quality"), ("局限与风险", "limitations"), ("复现可行性", "reproduction"), ("4K 相关证据", "four_k"), ("建议阅读顺序", "reading_plan")]:
            text += "**" + label + "**：" + r[key] + "\n\n"
        text += "自动核验：%s；许可证 %s；%d 个实现文件；%d stars；%s。\n\n" % (p["open_status"], p["license"], p["code_count"], p["stars"], p.get("weights_note", "权重未确认"))
        text += "原始来源：" + " / ".join("[来源 %d](%s)" % (i + 1, url) for i, url in enumerate(r["sources"])) + "\n\n"
    text += "[Awesome 仓库](https://github.com/" + w.load(w.ROOT / "config.json", {})["repository"] + ")\n"
    return text


def finish(model, dry_run=False):
    packet = w.load(packet_path(), {})
    if not packet:
        print("No new prepared issue")
        return
    review = w.load(w.ROOT / "work/agent/review.json", {})
    selected, records = validate_review(review, packet)
    body = render(selected, records, review, packet, model)
    preview = w.ROOT / "work/agent/preview.md"
    preview.write_text(body, encoding="utf-8")
    if dry_run:
        print("AI dry run complete; no email or public update")
        return
    state = w.load(w.ROOT / "data/state.json", {"sent": {}, "delivered": []})
    if packet["period"] in state["delivered"]:
        print("Issue already delivered; no duplicate")
        return
    cfg = w.load(w.ROOT / "config.json", {})
    w.send_mail(body, packet["date"], packet["bootstrap"], cfg["repository"], edition="Codex 研究分析")
    state["delivered"].append(packet["period"])
    for p in selected:
        state["sent"][p["id"]] = w.fingerprint(p)
    catalog = packet["catalog"]
    for p in catalog:
        p.pop("paper_excerpt", None)  # Full paper extracts stay temporary, not publicly republished.
        if p["id"] in records:
            p["ai_review"] = records[p["id"]]
            p["ai_review_model"] = model
            p["ai_review_generated_at"] = packet["collected_at"]
        if p["id"] in state["sent"]:
            p["pending_digest"] = False
    approved = [p for p in catalog if p["open_status"] in {"released", "promised"}]
    watch = [p for p in catalog if p["open_status"] not in {"released", "promised"}]
    w.save(w.ROOT / "data/state.json", state)
    w.save(w.ROOT / "data/papers.json", approved)
    w.save(w.ROOT / "data/watchlist.json", watch)
    w.save(w.ROOT / "data/ai-review.json", {"model": model, "period": packet["period"], "generated_at": w.stamp(), **review})
    w.save(w.ROOT / "data/status.json", {"checked_at": w.stamp(), "smtp_accepted": True, "period": packet["period"], "analysis_backend": "codex_subscription", "model": model, "warnings": packet.get("collector_status", {}).get("warnings", []), "executions": w.load(w.ROOT / "work/agent/execution-meta.json", [])})
    target = w.ROOT / "digests" / (packet["date"] + ("-bootstrap" if packet["bootstrap"] else "") + "-codex.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    w.update_readme(approved)
    print("AI digest accepted by SMTP; public updates prepared")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "analyze", "finish"])
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=os.environ.get("VSR_MODEL", "gpt-6-luna"))
    parser.add_argument("--auth-home", type=Path)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.bootstrap)
    elif args.phase == "analyze":
        if not args.auth_home:
            parser.error("analyze requires an isolated --auth-home")
        analyze(args.model, args.auth_home)
    else:
        finish(args.model, args.dry_run)


if __name__ == "__main__":
    main()
