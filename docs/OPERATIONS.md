# 云端运行与维护

## 部署

Python 3.11 标准库即可运行，没有 pip 依赖、LLM API 或持续在线服务器。GitHub 托管 Ubuntu runner 每周三 01:17 UTC（北京时间 09:17）启动，最长运行 30 分钟。

仓库 Actions Secrets：`QQ_SMTP_USER`、`QQ_SMTP_PASS`（QQ SMTP 授权码）、`QQ_MAIL_TO`。邮件地址和授权码不写进公开文件或日志。Secrets 在 GitHub 加密保存；仅 schedule/workflow_dispatch 会发信，PR 检查不读取邮箱 Secrets。

首次上线后通过 Actions → Weekly VSR digest → Run workflow 验证。`dry_run=true` 只检索和生成预览 artifact，不发邮件或提交数据。`bootstrap=true` 发初始阅读列表，正常周报只发未发送的近期论文和重要资源变化。人工运行同一周的任务默认不重复发信。

## 检索与证据

检索 arXiv 新提交与近期更新论文，保留 21 天重叠窗口以覆盖延迟索引；跟踪已有论文、未确认开源候选与 GitHub 新建/更新的相关研究仓库，回补首次检索遗漏。正式 proceedings-only 论文可人工在 seeds 中添加，自动检索不保证覆盖所有会议或中文来源。

项目网页只从论文元数据的链接展开。自动关联仓库必须有论文直接链接，或非 fork 仓库 README 的标题与论文完全匹配并声明官方实现；只匹配关键词或 stars 不能确认为官方。搜索发现的候选需回到 arXiv 核验元数据。实现文件、权重链接、许可证、来源地址、核验时间、仓库 stars 与一周增量分别记录。

排序优先 4K/UHD、生成式/扩散 VSR、已发布代码、有可识别开放许可证、作者仓库明确列出的顶会信息与关注度；其分数仅为可解释排序启发式。预印本不会因 stars 被标成已录用。新论文不设硬性 stars 下限，作者明确承诺但未发布的候选最多 2 篇。

周报使用中文解释推荐依据和复现边界，并附作者摘要摘录（英文，截断），不生成未经支持的实验数值。代码、许可证与权重是独立状态；链接存在不表示权重已验证可下载。不下载模型或执行 GPU 实验。

## 一致性与故障

顺序：检索 → 验证 → 生成周报 → SMTP 接受邮件 → 写入发送状态 → Git 提交与 push。SMTP 失败就停止，公开索引不先于邮件更新。全体新论文检索失败会使任务失败，不能伪装为“本周无新论文”；部分来源失败在周报显示降级说明。没有合格候选时仍发送清晰的空周报并更新运行状态。

按论文 ID 去重，重要变化指首次代码发布、开源状态/许可证/权重变化，不因 stars 数量改变重复推论文。周报最多 8 篇，未推送候选保留到后续期次；发送状态在 Git 中持久化。每周状态提交也避免公开仓库 60 天无活动导致定时停用。

SMTP 接受不等于收件箱到达。若邮件已接受但 Git push 随后失败，重跑可能重复一封；同一周固定 Message-ID 有助识别，但不承诺严格 exactly-once。失败时 GitHub Actions 标红并按账户通知设置提醒；可查看 artifact 中的周报后手动重跑。分支保护若禁止机器人直接写入，会导致 push 失败，需要允许 `github-actions[bot]` 写入或改为 PR 更新。

## 修改

筛选与查询在 `config.json`。新增人工核验的基础论文可添加 `{ "id": "arXiv ID", "repo": "owner/name" }`，其关联仍会重新核验，不能仅靠 seed 强行声称代码已发布。观察清单会每周复查，包括有明确开源承诺但未发代码的论文。人工修改 README 的自动区块以外内容会保留。

本地无发信检查：`python scripts/weekly.py --dry-run --bootstrap`。单元测试：`python -m unittest discover -s tests -v`。

停止：Actions 中 Disable workflow。更换邮箱：修改 Secrets 后手动 dry run/正常测试。无需重新打开 Codex。
