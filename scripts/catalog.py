"""Render and validate a bibliography with one primary topic per paper."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOPICS = [
    ("alignment", "时序对齐与特征传播 / Alignment and Propagation", "帧间对齐、长距离传播与时序状态。"),
    ("architecture", "Transformer 与状态空间架构 / Sequence Architectures", "面向视频重建的序列建模架构。"),
    ("generative", "扩散先验与生成式超分 / Diffusion-based VSR", "多步扩散、视频生成先验与细节合成。"),
    ("onestep", "单步扩散与蒸馏 / One-step Diffusion and Distillation", "将生成式超分压缩为单步或少步推理。"),
    ("gan", "对抗生成式超分 / GAN-based VSR", "以对抗学习恢复感知细节。"),
    ("realworld", "真实退化、盲超分与自监督 / Real-world and Blind VSR", "未知退化、真实噪声、域泛化和自监督学习。"),
    ("spacetime", "时空联合与任意倍率 / Space-time and Arbitrary-scale SR", "空间分辨率与帧率联合提升，连续或非整数倍率。"),
    ("efficiency", "高效、流式与模型压缩 / Efficient and Streaming VSR", "在线推理、边缘部署、量化、轻量化及计算复用。"),
    ("compression", "压缩域与传输鲁棒性 / Compression and Delivery", "编码信息、压缩退化、丢包及流媒体传输。"),
    ("guided", "参考、文本引导与交互 / Guided and Interactive VSR", "稀疏关键帧、参考信息、文本提示和用户控制。"),
    ("events", "事件相机视频超分 / Event-guided VSR", "融合 RGB 视频与事件信号进行空间或时空超分。"),
    ("faces", "人脸视频超分与修复 / Face Video SR", "人脸细节、身份一致性和时序稳定性。"),
    ("joint", "联合去模糊、弱光与物理退化 / Joint Restoration", "超分与去模糊、低照度、红外或湍流恢复联合建模。"),
    ("domains", "专用场景与模态 / Domain-specific VSR", "医学、卫星、全景、实时渲染、深度及显微视频。"),
    ("benchmarks", "数据集与评测 / Datasets and Benchmarks", "支持视频超分研究的数据集和评测基准。"),
]
FIELDS = {"id", "title", "venue", "year", "category", "tags", "summary", "paper_url", "pdf_url", "code_url", "project_url", "arxiv_id", "venue_status", "resource_status"}


def normalized_title(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def validate(papers):
    ids, titles = set(), set()
    for p in papers:
        if set(p) != FIELDS:
            raise ValueError("Catalog contains unexpected or missing bibliographic fields")
        if p["id"] in ids or normalized_title(p["title"]) in titles:
            raise ValueError("Duplicate paper")
        ids.add(p["id"])
        titles.add(normalized_title(p["title"]))
        if p["category"] not in {key for key, _, _ in TOPICS}:
            raise ValueError("Unknown topic")
        if not isinstance(p["year"], int) or p["year"] < 2000:
            raise ValueError("Invalid year")
        if p["venue_status"] not in {"verified", "preprint"}:
            raise ValueError("Invalid publication status")
        if p["venue_status"] == "preprint" and p["venue"] != "arXiv":
            raise ValueError("Unverified venue attribution")
        if p["resource_status"] not in {"author-linked", "promised", "not-found"}:
            raise ValueError("Invalid resource status")
        for key in ["paper_url", "pdf_url", "code_url", "project_url"]:
            url = p[key]
            if url and (not url.startswith("https://") or re.search(r"\s", url)):
                raise ValueError("Invalid source URL")
        if not p["paper_url"] or not p["title"] or not isinstance(p["tags"], list):
            raise ValueError("Incomplete bibliography")


def render(papers):
    validate(papers)
    counts = Counter(p["category"] for p in papers)
    accepted = sum(p["venue_status"] == "verified" for p in papers)
    text = """# Awesome Video Super-Resolution

A categorized collection of video super-resolution papers, author implementations, datasets and benchmarks.

视频超分辨率文献合集，涵盖传统重建、生成式超分、真实退化、时空联合超分、流式部署与专用场景。输出分辨率不作为收录限制。

集中整理 **2024 年至今**的相关顶会工作；正式录用以官方论文集或会议页面为依据，近期预印本另行标注。范围与检索入口见 [收录说明](docs/COVERAGE.md)。

"""
    text += "目前收录 **%d 篇**：**%d 篇会议论文**、**%d 篇预印本**，按 **%d 个方向**编排。每篇只出现一次，交叉特征列为补充标签。\n\n" % (len(papers), accepted, len(papers) - accepted, sum(bool(counts[key]) for key, _, _ in TOPICS))
    text += "`Code` 表示作者提供的仓库链接，资源是否完整请以作者说明为准；`待发布` 表示明确的发布计划；`—` 表示尚未找到作者公开代码链接，不等同于确定闭源。\n\n## Contents\n\n"
    for key, label, _ in TOPICS:
        if counts[key]:
            text += "- [%s](#%s) · %d\n" % (label, key, counts[key])
    text += "- [Contributing](CONTRIBUTING.md)\n\n"
    for key, label, description in TOPICS:
        rows = [p for p in papers if p["category"] == key]
        if not rows:
            continue
        text += '<a id="%s"></a>\n\n## %s\n\n%s\n\n' % (key, label, description)
        text += "| Paper | Venue | Focus / Tags | Resources |\n| --- | --- | --- | --- |\n"
        for p in sorted(rows, key=lambda p: (-p["year"], p["venue_status"] != "verified", p["venue"], p["title"])):
            links = []
            if p["code_url"]:
                links.append("[待发布](%s)" % p["code_url"] if p["resource_status"] == "promised" else "[Code](%s)" % p["code_url"])
            elif p["resource_status"] == "promised":
                links.append("待发布")
            if p["project_url"]:
                links.append("[Project](%s)" % p["project_url"])
            if p["pdf_url"]:
                links.append("[PDF](%s)" % p["pdf_url"])
            focus = p["summary"] + ("<br>" + ", ".join(p["tags"]) if p["tags"] else "")
            venue = p["venue"] + " " + str(p["year"]) + (" · 预印本" if p["venue_status"] == "preprint" else "")
            text += "| [%s](%s) | %s | %s | %s |\n" % (p["title"].replace("|", "\\|"), p["paper_url"], venue, focus.replace("|", "\\|"), " · ".join(links) if links else "—")
        text += "\n"
    text += "## Contributing\n\n欢迎补充遗漏论文、作者资源链接和分类修正。请提供原始来源，并按 [贡献说明](CONTRIBUTING.md) 更新文献数据。\n"
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    papers = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
    text = render(papers)
    target = ROOT / "README.md"
    if args.check:
        if target.read_text(encoding="utf-8") != text:
            raise SystemExit("README is out of sync with the catalog")
        print("Catalog and rendered bibliography are consistent (%d papers)" % len(papers))
    else:
        target.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
