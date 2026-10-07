# Contributing

收录范围包括空间视频超分、时空联合超分、任意倍率、真实退化、生成式超分及明确包含 VSR 任务的联合修复。事件、医学、人脸、深度和全景视频按专用方向标注。单图超分、纯插帧、纯文生视频、3D 场景超分和不涉及空间超分的画质增强不列为常规 VSR。

请在 `data/catalog.json` 中添加或修正条目，并提供官方会议论文页、出版社页面或作者原文。会议年份依据正式录用；只有作者声称录用而无会议来源的条目保持为预印本。Workshop、期刊和主会不能混用标签。

每篇指定一个主方向，通过 `tags` 表达交叉特征。代码链接优先使用原文或作者项目页指向的官方仓库；不得将第三方复现标为作者代码。未找到代码也可以收录，使用 `resource_status: not-found`。明确承诺发布可标为 `promised`，不要把空仓库当成可运行实现。

字段定义与可用分类见 `scripts/catalog.py`。运行 `python scripts/catalog.py` 生成 README，再运行 `python scripts/catalog.py --check` 和 `python -m unittest discover -s tests -v` 检查一致性。`data/sources.json` 保存官方索引入口，可为新会议年份补充入口。

修订论文沿用同一条目，避免同时列出同一工作的预印本和正式会议版本。链接应使用 HTTPS。欢迎提交更完整的作者链接、遗漏文献或分类依据。
