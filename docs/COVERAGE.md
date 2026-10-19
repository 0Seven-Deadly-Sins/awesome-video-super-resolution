# 收录范围与来源

本合集覆盖 **1991–2026 年**的视频超分研究，包含传统多帧重建、卷积重建、时序对齐与传播、Transformer/状态空间模型、生成式超分、空间与时间联合超分、参考引导，以及压缩、事件、深度、医学、卫星、人脸和全景等专用方向。相关综述、数据集和评测单独归类。代码、权重和输出分辨率均不构成收录门槛。

通用视频修复只在原始来源明确包含空间视频超分任务时收录。纯单图超分、纯插帧或时间维度超分、纯文生视频、视觉语音识别以及不包含空间超分的增强任务不纳入方法目录。对比实验使用视频数据，并不自动使单图方法成为 VSR 方法。

## 本次集中扩充

2026-10-19 完成跨年代集中扩充，合并同作预印本、正式版本和改题版本后，共 **459 篇**：209 篇会议、153 篇期刊、25 篇 Workshop、72 篇预印本，分为 **18 个方向**。可按 [研究方向](../README.md) 或 [发表年份](BY_YEAR.md) 浏览。

| 时段 | 条目数 |
| --- | ---: |
| 1991–2009 | 24 |
| 2010–2016 | 21 |
| 2017–2021 | 155 |
| 2022–2023 | 72 |
| 2024–2026 | 187 |

## 书目核验

- 会议与 Workshop：以官方论文集、会议页面或出版社的论文集条目确认题名、年份和会议类型；Workshop 与主会分别标注。
- 期刊：以出版社原始文章页、作者机构原文及出版社登记的 DOI 元数据核对题名、期刊和发表年份。出版社页面限制自动访问时，使用可核验的出版元数据与作者原文交叉确认。
- 预印本：以作者提交的 arXiv 原始记录核对题名、作者、摘要和首次提交年份。只有录用声明、尚未取得正式发表来源的条目保持预印本标注。
- 资源：作者论文、项目页或作者实现中的明确链接才标作作者资源。公开实现可能采用不同许可证或包含 p-code，具体形式以作者说明为准。

每篇指定一个主方向，交叉特征通过标签表达。相同 arXiv ID、相同题名和改题后的同作版本合并。独立期刊扩展如有明确新增方法或实验，可以保留并标注 `extended version`；仅因题名相近不删除不同论文。

## 资源复查（2026-10-19）

对原先缺少全文链接的 148 篇逐条比对出版社论文页、OpenAlex 可访问版本和作者 arXiv 记录，并实际检查 PDF 响应类型与题名。此次补入 30 个可访问的正式 PDF 或作者预印本全文；其余条目暂未找到可验证的全文副本，因此保留空链接，不用同名误配或第三方上传替代。当前 459 篇中有 339 篇提供 PDF 链接；336 条经 HTTP 内容类型检查确认返回 PDF，另 3 条遇到源站超时，但已由 arXiv、PMLR 或作者机构的原始来源确认是全文 PDF。

另对原先没有代码链接的条目检查 GitHub 仓库说明、目录和论文作者信息，补入 39 个与论文对应的作者实现。另有 6 篇找到了作者维护的相关仓库，但仓库当前没有该论文可用的实现；目录将其单独标为 `Repo`，明确写出作者承诺发布代码的记录另加 `待发布`。GitHub 上的第三方复现、同名项目和只在 README 中提及的相关工作均不计作作者代码。当前共 168 篇提供作者代码入口。

## 检索入口

本轮使用原始数据库检索、历年官方论文集扫描和参考文献追溯进行交叉查漏：

- [CVF Open Access](https://openaccess.thecvf.com/menu)：CVPR、ICCV、WACV 及有关 Workshop。早期按会议日分列的索引逐日读取；近期 NTIRE、AIM 等相关专题分别核查。
- [ECVA](https://www.ecva.net/papers.php)：ECCV 官方开放论文；另核查会议官方录用与出版社条目。
- [NeurIPS proceedings](https://proceedings.neurips.cc/)、[PMLR](https://proceedings.mlr.press/)、[OpenReview](https://openreview.net/)、[AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/issue/archive)、[IJCAI proceedings](https://www.ijcai.org/proceedings/) 和各会议官方页面。
- [arXiv API](https://info.arxiv.org/help/api/index.html)：组合检索 `video super-resolution`、`video super resolution`、`video upscaling`、`space-time super-resolution` 等题名变体，并按摘要确认实际任务。
- [Crossref](https://www.crossref.org/)：查验出版社登记的 DOI 书目信息；期刊范围包括 IEEE、ACM、Springer、Elsevier、IET 等相关出处。
- 作者大学主页、项目页及论文原文用于补证传统方法、改题论文和标题未明确写 VSR 的联合任务。

综述及 [Awesome-Super-Resolution](https://github.com/ChaofWang/Awesome-Super-Resolution)、[Awesome Video Enhancement](https://github.com/liuzhen03/awesome-video-enhancement) 等已有目录用于发现线索；条目的发表信息回到原始来源核验。每篇 Paper 链接提供具体出处。

## 后续维护

文献索引定期读取 `data/sources.json` 中的官方入口，并探测新会议年份。arXiv 采集分页检查最近 45 天首次提交的匹配论文，不设推荐篇数式的收录上限。期刊和历史遗漏条目也可按 [贡献说明](../CONTRIBUTING.md) 补入。

本轮覆盖面已扩展至经典方法和多个出版来源，题名同义表达、出版社访问限制及持续更新仍可能造成遗漏。来源访问失败会保留已有目录；欢迎提供原始证据补充或修正。
