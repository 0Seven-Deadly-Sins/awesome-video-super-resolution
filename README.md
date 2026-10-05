# Awesome Video Super-Resolution & 4K Generation

面向真实视频、影视素材与生成视频的超分辨率/修复，重点跟踪 4K/UHD、生成式 VSR、时序一致性、单步与流式推理。高分辨率直接生成作为邻近方向单列。

每周三北京时间 **09:17**，GitHub 托管的 Actions 运行 Codex CLI，使用 ChatGPT/Codex 订阅额度联网检索和分析论文，向配置的 QQ 邮箱发送中文研究周报，发信成功后更新本仓库。无需本地电脑在线或打开 Codex 应用，不使用按量计费的 OpenAI API 密钥。任务可能受 GitHub 排队或订阅额度影响。

Codex 判断贡献、实验支持、与已读工作的增量、局限、复现可行性与 4K 证据，并决定阅读顺序；程序独立核验作者来源、开源状态和去重。模型可补充规则检索遗漏的候选。模型分析失败会停止发信，不退回规则周报。运行编排与加密登录凭据放在私有仓库，本仓库公开分析代码、提示词及研究结果。

## 收录规则

- **已发布代码**：核验论文与作者仓库的关联，并检查仓库中存在实际实现文件；同时列出许可证。公开代码但许可证未知/受限会明确标记，不能据此认定自由使用。
- **明确承诺开源**：必须有作者原文承诺和来源链接，最多占每期 2 篇，独立分区；空仓库、`coming soon` 或项目网页本身不等于已经开源。
- **未确认 / 明确不开源**：不进入常规推荐；在观察清单中等待新证据。作者撤回开源承诺、删库或停止维护时记录状态变化。
- **可信度**表示来源关联与可复现资源证据强度，不保证论文结论正确。GitHub stars/增量是关注度指标，不等于研究质量。顶会信息注明来源，未核验录用的工作标为预印本。
- **4K**：区分作者明确提及的 4K/UHD 与泛称高分辨率；`4×` 并不代表 `4K`。没有运行 GPU 实验，不声称实测 4K 能力。

初始基础论文与本周新增论文分开。已读 StableVSR、MGLD-VSR、PS-SR 保留在索引，后续仅在代码发布等重要变化时再次推送。

## 论文索引

<!-- PAPERS:START -->
### 已发布代码

| 论文 | 日期 / 会议 | 4K 证据 | 代码 / 许可证 | 关注度 | 模型研究判断 |
| --- | --- | --- | --- | --- | --- |
| [RelayVSR: Large-Small Model Collaboration for Efficient Real-World Video Super-Resolution](https://arxiv.org/abs/2609.37850) | 2026-09-29 / 预印本/录用未核验 | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/kopperx/RelayVSR) / Apache-2.0 | 3 ★ | [必读 · 高](data/papers.json) |
| [ReCaVSR: One-Step Streaming Diffusion Video Super-Resolution with Recycled Latents and Learned Cache Routing](https://arxiv.org/abs/2609.37831) | 2026-09-29 / 预印本/录用未核验 | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/kopperx/ReCaVSR) / Apache-2.0 | 5 ★ | [必读 · 高](data/papers.json) |
| [NanoVSR: Towards Real-Time Video Super-Resolution on Edge Devices](https://arxiv.org/abs/2607.10495) | 2026-07-11 / ECCV 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/filippawlicki/nanovsr) / MIT | 52 ★ | [跳过 · 高](data/papers.json) |
| [SwiftVR: Real-Time One-Step Generative Video Restoration](https://arxiv.org/abs/2606.09516) | 2026-06-08 / 预印本/录用未核验 | 作者明确提及 4K/UHD（未实测） | [代码](https://github.com/H-oliday/SwiftVR) / Apache-2.0 | 111 ★ | [必读 · 高](data/papers.json) |
| [PS-SR: Pseudo-Single-Step Video Super-Resolution via Speculative Diffusion](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_PS-SR_Pseudo-Single-Step_Video_Super-Resolution_via_Speculative_Diffusion_CVPR_2026_paper.pdf) | 2026-06-01 / CVPR 2026（作者来源标注） | 作者明确提及 4K/UHD（未实测） | [代码](https://github.com/HiDream-ai/PS-SR) / Apache-2.0 | 30 ★ | 待分析 |
| [SparkVSR: Interactive Video Super-Resolution via Sparse Keyframe Propagation](https://arxiv.org/abs/2603.16864) | 2026-03-17 / ECCV 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/taco-group/SparkVSR) / Apache-2.0 | 742 ★ | [建议阅读 · 高](data/papers.json) |
| [Stream-DiffVSR: Low-Latency Streamable Video Super-Resolution via Auto-Regressive Diffusion](https://arxiv.org/abs/2512.23709) | 2025-12-29 / ECCV 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/jamichss/Stream-DiffVSR) / Apache-2.0 | 317 ★ | [建议阅读 · 高](data/papers.json) |
| [FlashVSR: Towards Real-Time Diffusion-Based Streaming Video Super-Resolution](https://arxiv.org/abs/2510.12747) | 2025-10-14 / CVPR 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/OpenImagingLab/FlashVSR) / Apache-2.0 | 1889 ★ | [观察 · 高](data/papers.json) |
| [InfVSR: Toward Consistency-Driven Streaming Generative Video Super-Resolution](https://arxiv.org/abs/2510.00948) | 2025-10-01 / ICML 26（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/Kai-Liu001/InfVSR) / 自定义/未识别 | 61 ★ | [必读 · 高](data/papers.json) |
| [SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training](https://arxiv.org/abs/2506.05301) | 2025-06-05 / ICLR 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/ByteDance-Seed/SeedVR) / Apache-2.0 | 1383 ★ | [建议阅读 · 高](data/papers.json) |
| [DOVE: Efficient One-Step Diffusion Model for Real-World Video Super-Resolution](https://arxiv.org/abs/2505.16239) | 2025-05-22 / NeurIPS 25（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/zhengchen1999/DOVE) / Apache-2.0 | 223 ★ | [观察 · 中](data/papers.json) |
| [SeedVR: Seeding Infinity in Diffusion Transformer Towards Generic Video Restoration](https://arxiv.org/abs/2501.01320) | 2025-01-02 / ICLR 2026（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/ByteDance-Seed/SeedVR) / Apache-2.0 | 1383 ★ | [跳过 · 高](data/papers.json) |
| [Motion-Guided Latent Diffusion for Temporally Consistent Real-world Video Super-resolution](https://arxiv.org/abs/2312.00853) | 2023-12-01 / ECCV 2024（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/IanYeung/MGLD-VSR) / 自定义/未识别 | 166 ★ | 待分析 |
| [Enhancing Perceptual Quality in Video Super-Resolution through Temporally-Consistent Detail Synthesis using Diffusion Models](https://arxiv.org/abs/2311.15908) | 2023-11-27 / ECCV 2024（作者来源标注） | 高分辨率相关，未确认 4K 证据 | [代码](https://github.com/claudiom4sir/StableVSR) / MIT | 180 ★ | 待分析 |

### 作者明确承诺，待开源

| 论文 | 日期 / 会议 | 4K 证据 | 代码 / 许可证 | 关注度 | 模型研究判断 |
| --- | --- | --- | --- | --- | --- |

<!-- PAPERS:END -->

## 周报与运行状态

- [历期周报](digests/)
- [机器可读论文数据](data/papers.json)
- [观察清单](data/watchlist.json)
- [最近运行状态](data/status.json)
- [最近一次模型分析](data/ai-review.json)
- [研究分析提示词](prompts/reviewer.md)
- [部署、筛选与维护说明](docs/OPERATIONS.md)
- [公开代码检查](https://github.com/0Seven-Deadly-Sins/awesome-video-super-resolution-4k/actions)

欢迎通过 Issue/PR 补充论文和官方开源证据。自动脚本不会执行候选仓库中的代码。
