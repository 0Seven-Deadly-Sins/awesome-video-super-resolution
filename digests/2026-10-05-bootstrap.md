# 4K 视频超分论文周报 · 2026-10-05 · 首次部署

重点：4K/UHD、生成式视频超分、时序一致性与高效流式推理。

本次读取 19 篇论文元数据，核验 19 篇；精选 8 篇。基础阅读列表不会伪装成本周新论文。

## 代码已发布

### [ReCaVSR: One-Step Streaming Diffusion Video Super-Resolution with Recycled Latents and Learned Cache Routing](https://arxiv.org/abs/2609.37831)

- 发布：2026-09-29；预印本/录用未核验
- 推荐依据：本周/近期新论文；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/kopperx/ReCaVSR)；许可证：Apache-2.0；实现文件：23
- 关注度：5 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2609.37831) / [证据 2](https://github.com/kopperx/ReCaVSR/blob/main/README.md)

作者摘要摘录（英文）：

> Real-time diffusion-based video super-resolution (VSR) is in high demand for online streaming, yet stringent latency requirements often compromise generative fidelity. We propose ReCaVSR, a Wan2.2-based, one-step framework for streaming VSR that builds on two observations: recycled SR latents retain local temporal context, reducing the need for full historical Key-Value (KV) caches; and individual transformer layers benefit from distinct temporal scopes. ReCaVSR combines three complementary designs: (i) layer-wise cache routing with recycled SR latents: each DiT layer learns its KV-cache temporal scope under a cache budget and exports a static inference schedule, while recycled SR latents propagate local context by conditioning each new block on the model's own preceding predictions. (ii) 

### [RelayVSR: Large-Small Model Collaboration for Efficient Real-World Video Super-Resolution](https://arxiv.org/abs/2609.37850)

- 发布：2026-09-29；预印本/录用未核验
- 推荐依据：本周/近期新论文；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/kopperx/RelayVSR)；许可证：Apache-2.0；实现文件：19
- 关注度：3 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2609.37850) / [证据 2](https://github.com/kopperx/RelayVSR/blob/main/README.md)

作者摘要摘录（英文）：

> Large generative models can recover realistic detail in real-world video super-resolution (VSR), but processing an entire video with them is computationally expensive. In this work, we present RelayVSR, a streaming VSR framework built on the Sparse Generative Relay mechanism. A large generative model generates reference latents for sparse keyframes, while a lightweight VSR network uses these references and low-resolution video to super-resolve every frame. The lightweight VSR network, implemented as a Dual-Memory Video Transformer, reuses keyframe information across frames and updates recent video context, supporting first-keyframe conditioning and dual-endpoint conditioning with bounded lookahead. However, errors in shared keyframes can propagate and accumulate across output frames, makin

### [FlashVSR: Towards Real-Time Diffusion-Based Streaming Video Super-Resolution](https://arxiv.org/abs/2510.12747)

- 发布：2025-10-14；CVPR 2026（作者来源标注）
- 推荐依据：基础阅读列表；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/OpenImagingLab/FlashVSR)；许可证：Apache-2.0；实现文件：176
- 关注度：1889 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2510.12747) / [证据 2](https://zhuang2002.github.io/FlashVSR) / [证据 3](https://github.com/OpenImagingLab/FlashVSR/blob/main/README.md)

作者摘要摘录（英文）：

> Diffusion models have recently advanced video restoration, but applying them to real-world video super-resolution (VSR) remains challenging due to high latency, prohibitive computation, and poor generalization to ultra-high resolutions. Our goal in this work is to make diffusion-based VSR practical by achieving efficiency, scalability, and real-time performance. To this end, we propose FlashVSR, the first diffusion-based one-step streaming framework towards real-time VSR. FlashVSR runs at approximately 17 FPS for 768x1408 videos on a single A100 GPU by combining three complementary innovations: (i) a train-friendly three-stage distillation pipeline that enables streaming super-resolution, (ii) locality-constrained sparse attention that cuts redundant computation while bridging the train-te

### [SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training](https://arxiv.org/abs/2506.05301)

- 发布：2025-06-05；ICLR 2026（作者来源标注）
- 推荐依据：基础阅读列表；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/ByteDance-Seed/SeedVR)；许可证：Apache-2.0；实现文件：73
- 关注度：1383 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2506.05301) / [证据 2](https://iceclear.github.io/projects/seedvr2/) / [证据 3](https://github.com/ByteDance-Seed/SeedVR/blob/main/readme.md)

作者摘要摘录（英文）：

> Recent advances in diffusion-based video restoration (VR) demonstrate significant improvement in visual quality, yet yield a prohibitive computational cost during inference. While several distillation-based approaches have exhibited the potential of one-step image restoration, extending existing approaches to VR remains challenging and underexplored, particularly when dealing with high-resolution video in real-world settings. In this work, we propose a one-step diffusion-based VR model, termed as SeedVR2, which performs adversarial VR training against real data. To handle the challenging high-resolution VR within a single step, we introduce several enhancements to both model architecture and training procedures. Specifically, an adaptive window attention mechanism is proposed, where the wi

### [SeedVR: Seeding Infinity in Diffusion Transformer Towards Generic Video Restoration](https://arxiv.org/abs/2501.01320)

- 发布：2025-01-02；ICLR 2026（作者来源标注）
- 推荐依据：基础阅读列表；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/ByteDance-Seed/SeedVR)；许可证：Apache-2.0；实现文件：73
- 关注度：1383 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2501.01320) / [证据 2](https://iceclear.github.io/projects/seedvr/) / [证据 3](https://github.com/ByteDance-Seed/SeedVR/blob/main/readme.md)

作者摘要摘录（英文）：

> Video restoration poses non-trivial challenges in maintaining fidelity while recovering temporally consistent details from unknown degradations in the wild. Despite recent advances in diffusion-based restoration, these methods often face limitations in generation capability and sampling efficiency. In this work, we present SeedVR, a diffusion transformer designed to handle real-world video restoration with arbitrary length and resolution. The core design of SeedVR lies in the shifted window attention that facilitates effective restoration on long video sequences. SeedVR further supports variable-sized windows near the boundary of both spatial and temporal dimensions, overcoming the resolution constraints of traditional window attention. Equipped with contemporary practices, including causa

### [Stream-DiffVSR: Low-Latency Streamable Video Super-Resolution via Auto-Regressive Diffusion](https://arxiv.org/abs/2512.23709)

- 发布：2025-12-29；ECCV 2026（作者来源标注）
- 推荐依据：新开源/更新资源；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/jamichss/Stream-DiffVSR)；许可证：Apache-2.0；实现文件：33
- 关注度：317 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2512.23709) / [证据 2](https://jamichss.github.io/stream-diffvsr-project-page/) / [证据 3](https://github.com/jamichss/Stream-DiffVSR/blob/main/README.md)

作者摘要摘录（英文）：

> Diffusion-based video super-resolution (VSR) methods deliver strong perceptual quality but are often unsuitable for latency-sensitive scenarios due to reliance on future frames and expensive multi-step denoising. We propose Stream-DiffVSR, a causally conditioned diffusion framework for efficient online VSR. Operating strictly on past frames, Stream-DiffVSR integrates a four-step distilled denoiser for fast inference, an Auto-regressive Temporal Guidance (ARTG) module that injects motion-aligned cues during latent denoising, and a lightweight temporal-aware decoder with a Temporal Processor Module (TPM) to enhance detail and temporal coherence. Unlike chunk-wise streaming inference, our strictly frame-by-frame causal design avoids sequence-level waiting, substantially reducing time-to-first

### [DOVE: Efficient One-Step Diffusion Model for Real-World Video Super-Resolution](https://arxiv.org/abs/2505.16239)

- 发布：2025-05-22；NeurIPS 25（作者来源标注）
- 推荐依据：基础阅读列表；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/zhengchen1999/DOVE)；许可证：Apache-2.0；实现文件：53
- 关注度：223 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2505.16239) / [证据 2](https://github.com/zhengchen1999/DOVE/blob/main/README.md)

作者摘要摘录（英文）：

> Diffusion models have demonstrated promising performance in real-world video super-resolution (VSR). However, the dozens of sampling steps they require, make inference extremely slow. Sampling acceleration techniques, particularly single-step, provide a potential solution. Nonetheless, achieving one step in VSR remains challenging, due to the high training overhead on video data and stringent fidelity demands. To tackle the above issues, we propose DOVE, an efficient one-step diffusion model for real-world VSR. DOVE is obtained by fine-tuning a pretrained video diffusion model (i.e., CogVideoX). To effectively train DOVE, we introduce the latent-pixel training strategy. The strategy employs a two-stage scheme to gradually adapt the model to the video super-resolution task. Meanwhile, we de

### [SparkVSR: Interactive Video Super-Resolution via Sparse Keyframe Propagation](https://arxiv.org/abs/2603.16864)

- 发布：2026-03-17；ECCV 2026（作者来源标注）
- 推荐依据：基础阅读列表；高分辨率相关，未确认 4K 证据；来源关联与实现文件已核验。
- 开源：代码已发布；[作者仓库](https://github.com/taco-group/SparkVSR)；许可证：Apache-2.0；实现文件：75
- 关注度：742 stars，较上次核验 +0（仅作热度信号）。
- 复现边界：作者页面列有模型/权重链接，未验证下载；未运行实验；4K 实际显存、耗时与效果需进一步验证。
- 核验来源：[证据 1](https://arxiv.org/abs/2603.16864) / [证据 2](https://sparkvsr.github.io/) / [证据 3](https://github.com/taco-group/SparkVSR/blob/main/README.md)

作者摘要摘录（英文）：

> Video Super-Resolution (VSR) aims to restore high-quality video frames from low-resolution (LR) estimates, yet most existing VSR approaches behave like black boxes at inference time: users cannot reliably correct unexpected artifacts, but instead can only accept whatever the model produces. In this paper, we propose a novel interactive VSR framework dubbed SparkVSR that makes sparse keyframes a simple and expressive control signal. Specifically, users can first super-resolve or optionally a small set of keyframes using any off-the-shelf image super-resolution (ISR) model, then SparkVSR propagates the keyframe priors to the entire video sequence while remaining grounded by the original LR video motion. Concretely, we introduce a keyframe-conditioned latent-pixel two-stage training pipeline 

[Awesome 仓库](https://github.com/0Seven-Deadly-Sins/awesome-video-super-resolution-4k) · [历期周报](https://github.com/0Seven-Deadly-Sins/awesome-video-super-resolution-4k/tree/main/digests)

索引将在 SMTP 接受本邮件后更新。stars 不等于论文质量；公开代码、开放许可证、模型权重与实测 4K 能力分别判断。
