"""Render and validate a bibliography with one primary topic per paper."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOPIC_GROUPS = [
    ("阅读与评测 / Reading and evaluation", [
        ("surveys", "综述与阅读指南 / Surveys", "视频超分辨率的技术综述、方法分类与研究进展。"),
        ("benchmarks", "数据集与评测 / Datasets and Benchmarks", "视频超分辨率数据集、评价指标与竞赛基准。"),
    ]),
    ("重建方法与架构 / Reconstruction methods and architectures", [
        ("classical", "传统重建与优化 / Classical Reconstruction", "基于运动估计、贝叶斯建模、稀疏表示与多帧优化的重建方法。"),
        ("cnn", "卷积重建与时空融合 / CNN Reconstruction", "基于卷积网络的多帧特征提取、时空融合与重建。"),
        ("alignment", "时序对齐与特征传播 / Alignment and Propagation", "帧间对齐、长程特征传播与时序状态建模。"),
        ("architecture", "Transformer 与状态空间模型 / Transformers and State Space Models", "面向视频重建的 Transformer、状态空间模型与其他序列架构。"),
    ]),
    ("生成式方法 / Generative methods", [
        ("gan", "对抗生成式超分 / GAN-based VSR", "通过对抗学习恢复视频纹理与感知细节。"),
        ("generative", "扩散先验与生成式超分 / Diffusion-based VSR", "基于多步扩散与视频生成先验的细节重建。"),
        ("onestep", "单步扩散与蒸馏 / One-step Diffusion and Distillation", "通过蒸馏与推理加速实现单步或少步生成式超分。"),
    ]),
    ("退化建模与任务扩展 / Degradations and task extensions", [
        ("realworld", "真实退化、盲超分与自监督 / Real-world and Blind VSR", "面向未知退化、真实噪声与域偏移的盲超分、自监督及适应方法。"),
        ("spacetime", "时空联合与任意倍率 / Space-time and Arbitrary-scale SR", "联合提升空间分辨率与帧率，或支持连续、非整数放大倍率。"),
        ("guided", "参考、文本引导与交互 / Guided and Interactive VSR", "利用参考帧、外部图像、文本提示或用户交互引导视频超分。"),
        ("joint", "联合视频修复 / Joint Video Restoration", "超分与去模糊、低照度、红外或湍流恢复的联合建模。"),
    ]),
    ("高效系统与视频传输 / Efficient systems and video delivery", [
        ("efficiency", "高效、流式与模型压缩 / Efficient and Streaming VSR", "面向在线推理、边缘部署与低计算开销的轻量化、量化及计算复用。"),
        ("compression", "压缩域与传输鲁棒性 / Compression and Delivery", "利用编码信息，或应对压缩退化、丢包与流媒体传输的超分方法。"),
    ]),
    ("专用场景与模态 / Applications and modalities", [
        ("events", "事件相机视频超分 / Event-guided VSR", "融合 RGB 视频与事件信号的空间或时空超分。"),
        ("faces", "人脸视频超分与修复 / Face Video SR", "面向人脸细节、身份一致性与时序稳定性的超分及联合修复。"),
        ("domains", "其他专用场景与模态 / Other Domains and Modalities", "面向医学、卫星、全景、实时渲染、深度及显微视频的超分方法。"),
    ]),
]
TOPICS = [topic for _, topics in TOPIC_GROUPS for topic in topics]
FIELDS = {"id", "title", "venue", "year", "category", "tags", "summary", "paper_url", "pdf_url", "code_url", "repository_url", "project_url", "arxiv_id", "venue_status", "resource_status", "publication_type"}


def normalized_title(title):
    return re.sub(r"[^a-z0-9]", "", title.lower().replace("+", "plus"))


def paper_sort_key(paper):
    title = re.sub(r"[\W_]+", " ", paper["title"].casefold()).strip()
    return (-paper["year"], title, paper["title"].casefold())


def validate(papers):
    ids, titles, arxiv_ids = set(), set(), set()
    for p in papers:
        if set(p) != FIELDS:
            raise ValueError("Catalog contains unexpected or missing bibliographic fields")
        if p["id"] in ids or normalized_title(p["title"]) in titles:
            raise ValueError("Duplicate paper")
        ids.add(p["id"])
        titles.add(normalized_title(p["title"]))
        if p["arxiv_id"]:
            if p["arxiv_id"] in arxiv_ids:
                raise ValueError("Duplicate arXiv identity")
            arxiv_ids.add(p["arxiv_id"])
        if p["category"] not in {key for key, _, _ in TOPICS}:
            raise ValueError("Unknown topic")
        if not isinstance(p["year"], int) or p["year"] < 1900:
            raise ValueError("Invalid year")
        if p["venue_status"] not in {"verified", "preprint"}:
            raise ValueError("Invalid publication status")
        if p["venue_status"] == "preprint" and p["venue"] != "arXiv":
            raise ValueError("Unverified venue attribution")
        if p["publication_type"] not in {"conference", "workshop", "journal", "preprint"}:
            raise ValueError("Invalid publication type")
        if (p["venue_status"] == "preprint") != (p["publication_type"] == "preprint"):
            raise ValueError("Publication type and verification status disagree")
        if p["resource_status"] not in {"author-linked", "repository-only", "promised", "not-found"}:
            raise ValueError("Invalid resource status")
        if p["resource_status"] == "repository-only" and not p["repository_url"]:
            raise ValueError("Repository-only status requires a repository URL")
        for key in ["paper_url", "pdf_url", "code_url", "repository_url", "project_url"]:
            url = p[key]
            if url and (not url.startswith("https://") or re.search(r"\s", url)):
                raise ValueError("Invalid source URL")
        if not p["paper_url"] or not p["title"] or not isinstance(p["tags"], list):
            raise ValueError("Incomplete bibliography")


def render(papers):
    validate(papers)
    counts = Counter(p["category"] for p in papers)
    kinds = Counter(p["publication_type"] for p in papers)
    text = """# Awesome Video Super-Resolution

A categorized collection of video super-resolution (VSR) papers, covering classical reconstruction, deep learning, generative methods, datasets and benchmarks.

视频超分辨率文献合集，按研究方向整理综述、方法、数据集与评测工作，涵盖经典重建、深度学习、生成式超分及专用场景。收录正式发表论文与预印本，不限输出分辨率；代码或权重是否公开不影响收录。

"""
    text += "目前收录 **%d 篇**文献，年份跨度为 **%d–%d 年**，涵盖 **%d 个研究方向**。其中包括 **%d 篇会议论文**、**%d 篇期刊论文**、**%d 篇 Workshop 论文**、**%d 篇预印本**。\n\n" % (len(papers), min(p["year"] for p in papers), max(p["year"] for p in papers), sum(bool(counts[key]) for key, _, _ in TOPICS), kinds["conference"], kinds["journal"], kinds["workshop"], kinds["preprint"])
    text += "[研究方向 / Topics](#contents) · [发表年份 / By year](docs/BY_YEAR.md) · [收录范围 / Scope](docs/COVERAGE.md) · [参与贡献 / Contributing](CONTRIBUTING.md)\n\n"
    text += '<a id="contents"></a>\n<a id="browse-by-research-direction"></a>\n\n## 目录 / Contents\n\n'
    text += "分类按研究主题编排；**编号对应正文分类，括号内为该类文献篇数**。\n\n"
    numbers = {key: number for number, (key, _, _) in enumerate(TOPICS, 1)}
    for heading, topics in TOPIC_GROUPS:
        if not any(counts[key] for key, _, _ in topics):
            continue
        text += "### %s\n\n" % heading
        for key, label, _ in topics:
            if counts[key]:
                text += "- [%02d. %s](#%s)（%d 篇）\n" % (numbers[key], label, key, counts[key])
        text += "\n"
    text += '''<a id="reading-notes"></a>

## 阅读说明 / Reading notes

- **分类**：每篇文献只列入一个主方向，交叉特征在研究要点与标签中补充。分类顺序不代表重要性或推荐排名。
- **排序**：各分类内按年份从新到旧排列；同年按论文标题的字母顺序排列，忽略大小写与标点。年份索引采用相同规则。 / Newest year first; titles A–Z within each year, ignoring case and punctuation.
- **版本**：同一工作的预印本与正式发表版本合并。正式版本采用发表年份，预印本采用首次提交年份；会议、期刊、Workshop 与预印本依据原始来源分别标注。
- **全文**：点击论文标题进入原始论文页；`PDF` 优先提供可访问的出版社全文或作者预印本。

| 资源标记 / Label | 含义 / Meaning |
| --- | --- |
| `PDF` | 论文全文，可能是正式版本或作者预印本 / Full text, including author preprints |
| `Code` | 已核实的作者实现或代码入口 / Author-provided implementation |
| `Repo` | 已核实的作者仓库，暂未找到可用实现 / Author repository without a verified usable implementation |
| `Project` | 作者项目主页 / Author project page |
| `待发布` | 作者明确承诺发布代码 / Code release explicitly promised by the authors |
| `—` | 暂未找到可核验的附加资源链接 / No verified additional resource link found |

'''
    for key, label, description in TOPICS:
        rows = [p for p in papers if p["category"] == key]
        if not rows:
            continue
        text += '<a id="%s"></a>\n\n## %02d. %s\n\n%s\n\n' % (key, numbers[key], label, description)
        text += "| 年份 / Year | 论文 / Paper | 出处 / Venue | 研究要点 / Focus | 资源 / Links |\n| --- | --- | --- | --- | --- |\n"
        for p in sorted(rows, key=paper_sort_key):
            links = []
            if p["pdf_url"]:
                links.append("[PDF](%s)" % p["pdf_url"])
            if p["code_url"]:
                links.append("[待发布](%s)" % p["code_url"] if p["resource_status"] == "promised" else "[Code](%s)" % p["code_url"])
            elif p["resource_status"] == "promised":
                links.append("待发布")
            if p["repository_url"]:
                links.append("[Repo](%s)" % p["repository_url"])
            if p["project_url"]:
                links.append("[Project](%s)" % p["project_url"])
            tags = [tag for tag in p["tags"] if tag != p["category"]]
            focus = p["summary"] + ("<br>Tags: " + ", ".join(tags) if tags else "")
            venue = p["venue"] + (" · Preprint" if p["venue_status"] == "preprint" else "")
            if p["publication_type"] == "workshop" and not re.search(r'workshop', p["venue"], re.I):
                venue += " · Workshop"
            text += "| %d | [%s](%s) | %s | %s | %s |\n" % (p["year"], p["title"].replace("|", "\\|"), p["paper_url"], venue.replace("|", "\\|"), focus.replace("|", "\\|"), " · ".join(links) if links else "—")
        text += "\n[↑ 返回目录 / Back to contents](#contents)\n\n"
    text += "## 参与贡献 / Contributing\n\n欢迎补充遗漏文献、完善作者资源链接或提出分类修正。请提供可核验的原始来源，并按 [贡献说明](CONTRIBUTING.md) 更新文献数据。\n\nContributions are welcome: add missing papers, improve author resource links, or suggest category corrections with primary sources. Please follow the [contribution guide](CONTRIBUTING.md).\n"
    return text


def render_years(papers):
    validate(papers)
    counts = Counter(p["year"] for p in papers)
    text = "# 按发表年份浏览\n\n[按研究方向浏览](../README.md) · [收录说明](COVERAGE.md)\n\n"
    text += "按年份从新到旧排列，同年按论文标题的字母顺序排列，忽略大小写与标点。正式版本使用经核验的发表年份，预印本使用首次提交年份；括号内为该年文献篇数。\n\n"
    text += "\n".join("- [%d](#%d)（%d 篇）" % (year, year, counts[year]) for year in sorted(counts, reverse=True)) + "\n\n"
    for year in sorted(counts, reverse=True):
        text += "## %d\n\n" % year
        for p in sorted((p for p in papers if p["year"] == year), key=paper_sort_key):
            label = p["venue"] + (" · 预印本" if p["publication_type"] == "preprint" else "")
            if p["publication_type"] == "workshop" and not re.search(r'workshop', p["venue"], re.I):
                label += " · Workshop"
            text += "- [%s](%s) — %s\n" % (p["title"], p["paper_url"], label)
        text += "\n"
    return text


def write_indexes(papers):
    (ROOT / "README.md").write_text(render(papers), encoding="utf-8")
    (ROOT / "docs/BY_YEAR.md").write_text(render_years(papers), encoding="utf-8")


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
        if (ROOT / "docs/BY_YEAR.md").read_text(encoding="utf-8") != render_years(papers):
            raise SystemExit("Year index is out of sync with the catalog")
        print("Catalog and rendered bibliography are consistent (%d papers)" % len(papers))
    else:
        write_indexes(papers)


if __name__ == "__main__":
    main()
