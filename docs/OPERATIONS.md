# 云端运行与维护

## 运行位置与时间

私有仓库 `0Seven-Deadly-Sins/vsr-paper-agent` 的 GitHub 托管 Ubuntu Actions 每周三 01:17 UTC（北京时间 09:17）运行，最长 60 分钟。公开仓库保存研究代码和结果，私有仓库保存编排与加密登录缓存。电脑关机或 Codex 应用关闭不影响运行。

默认 Codex CLI `0.160.0`，模型 `gpt-6.1-sol`、high reasoning、live web search，使用 ChatGPT/Codex 订阅额度。可用模型与用量受账户权限限制，不保证永久免费或永久免维护。私有 Actions 的分钟数也受 GitHub 账户计划限制。模型可通过私有仓库变量 `VSR_MODEL` 调整。

## 模型与证据

流程：21 天重叠窗口的 arXiv/作者仓库检索 → 作者来源与实际实现核验 → Codex 联网补查、分析论文 → 对新增发现独立核验，必要时再分析一次 → 结构化结果校验 → SMTP 发信 → 公开仓库更新。

候选收集规则用于发现与证据约束，最终研究价值和阅读优先级由 Codex 判断。模型分析核心贡献、与 StableVSR/MGLD-VSR/PS-SR 的关系、实验支持程度、局限、复现条件、4K 证据与阅读建议。提示词在 `prompts/reviewer.md`，输出规范在 `schemas/review.json`。模型没有人工复现实验；正文不可访问时标明依据范围，正文节选不等于完整阅读。

项目网页从论文元数据的链接展开。仓库关联须有论文/作者来源，或非 fork 仓库的论文标题与官方实现声明。空仓库、项目页或泛称 coming soon 不等于代码已发布。公开代码、许可证、权重和实测 4K 能力分别判断。`4×` 不是 `4K`，stars 不等于论文质量。模型不能绕过这些约束推送未确认开源或明确闭源论文。

每期最多 8 篇，明确承诺开源但尚未发布的最多 2 篇。已发送论文仅在代码、权重、许可证等实质变化时再推送；已读论文同样处理。初始 AI 周报可以重评历史基础论文并标明发布日期。模型可发现标题规则遗漏的 arXiv 论文；仅有会议论文而没有 arXiv 的工作目前需手动添加到 seeds，不保证完整覆盖。

## 登录与凭据

使用为本任务独立登录的 ChatGPT 会话，避免与桌面 Codex 共用刷新状态。私有仓库 Secrets 包含 `VSR_AUTH_KEY`、`PUBLIC_DEPLOY_KEY`、`QQ_SMTP_USER`、`QQ_SMTP_PASS`、`QQ_MAIL_TO`。

CLI 登录缓存通过 Fernet 认证加密保存于私有仓库 `.auth/codex.enc`；密钥单独存于 Actions Secret。每次在 runner 临时目录解密，CLI 自行刷新，随后将变化重新加密保存。刷新保存步骤在分析失败时也执行。并发组将同一会话串行运行。认证流程依据 [OpenAI 的 CI/CD 登录说明](https://learn.chatgpt.com/docs/auth/ci-cd-auth)。

模型子进程不接收 SMTP 密码、GitHub Token、加密密钥或发布私钥；候选代码不会被执行。公开仓库写入使用只对该仓库有效的 deploy key。登录明文、原始执行日志和论文完整节选不会上传到 artifact 或公开仓库。Artifact 仅保留分析 JSON 与周报预览。

## 失败与维护

模型登录失效、订阅额度不足、分析失败或 JSON 不合格会使 Actions 失败，不静默退回规则周报。所有新论文检索失败同样报错；部分失败在邮件显示覆盖降级。可查看私有仓库 Actions 的报错分类与预览。若登录被撤销或无法刷新，需要重新完成独立登录并更新加密缓存。

SMTP 失败不会写入公开发送状态。SMTP 接受不等于邮件已进收件箱。邮件接受后若发布失败，重跑可能重复；固定期次和 Message-ID 便于识别，但不保证严格 exactly-once。没有合格的新候选时发送有模型判断的简短空周报，不凑数。

公开旧规则任务应停用；正常发送只由私有 `Codex VSR research digest` 工作流执行。人工 Run workflow：`dry_run=true` 执行真实模型但不发邮件/发布；`bootstrap=true` 生成初始 AI 阅读列表。已投递的同一期不会重复运行。

GitHub 可能对长期无活动的定时任务停用。公开仓库每次周报会提交运行状态；私有 runner 若长时间未刷新凭据或修改代码，应检查 schedule 是否仍启用。

调整检索、已读记录与数量上限使用 `config.json`。模型研究标准使用提示词。验证：`python -m unittest discover -s tests -v`；本地收集预览：`python scripts/agent_weekly.py prepare --bootstrap`。停止运行在私有仓库 Actions 中 Disable workflow。更换邮箱修改私有 Secrets。
