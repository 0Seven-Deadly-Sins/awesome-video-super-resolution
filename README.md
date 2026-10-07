# Awesome Video Super-Resolution

A categorized collection of video super-resolution papers, author implementations, datasets and benchmarks.

视频超分辨率文献合集，涵盖传统重建、生成式超分、真实退化、时空联合超分、流式部署与专用场景。输出分辨率不作为收录限制。

本轮集中整理 **2024–2026 会议年份**的相关顶会工作；正式录用以官方论文集或会议页面为依据，近期预印本另行标注。范围与检索入口见 [收录说明](docs/COVERAGE.md)。

目前收录 **90 篇**：**87 篇会议论文**、**3 篇预印本**，按 **15 个方向**编排。每篇只出现一次，交叉特征列为补充标签。

`Code` 表示作者提供的仓库链接，资源是否完整请以作者说明为准；`待发布` 表示明确的发布计划；`—` 表示尚未找到作者公开代码链接，不等同于确定闭源。

## Contents

- [时序对齐与特征传播 / Alignment and Propagation](#alignment) · 4
- [Transformer 与状态空间架构 / Sequence Architectures](#architecture) · 1
- [扩散先验与生成式超分 / Diffusion-based VSR](#generative) · 16
- [单步扩散与蒸馏 / One-step Diffusion and Distillation](#onestep) · 9
- [对抗生成式超分 / GAN-based VSR](#gan) · 1
- [真实退化、盲超分与自监督 / Real-world and Blind VSR](#realworld) · 4
- [时空联合与任意倍率 / Space-time and Arbitrary-scale SR](#spacetime) · 7
- [高效、流式与模型压缩 / Efficient and Streaming VSR](#efficiency) · 14
- [压缩域与传输鲁棒性 / Compression and Delivery](#compression) · 2
- [参考、文本引导与交互 / Guided and Interactive VSR](#guided) · 3
- [事件相机视频超分 / Event-guided VSR](#events) · 10
- [人脸视频超分与修复 / Face Video SR](#faces) · 6
- [联合去模糊、弱光与物理退化 / Joint Restoration](#joint) · 5
- [专用场景与模态 / Domain-specific VSR](#domains) · 7
- [数据集与评测 / Datasets and Benchmarks](#benchmarks) · 1
- [Contributing](CONTRIBUTING.md)

<a id="alignment"></a>

## 时序对齐与特征传播 / Alignment and Propagation

帧间对齐、长距离传播与时序状态。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [LDIP: Long Distance Information Propagation for Video Super-Resolution](https://openaccess.thecvf.com/content/ICCV2025/html/Bernasconi_LDIP_Long_Distance_Information_Propagation_for_Video_Super-Resolution_ICCV_2025_paper.html) | ICCV 2025 | Long-distance feature propagation | [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Bernasconi_LDIP_Long_Distance_Information_Propagation_for_Video_Super-Resolution_ICCV_2025_paper.pdf) |
| [Semantic Lens: Instance-Centric Semantic Alignment for Video Super-resolution](https://ojs.aaai.org/index.php/AAAI/article/view/28321) | AAAI 2024 | Instance-centric semantic alignment | — |
| [Enhancing Video Super-Resolution via Implicit Resampling-based Alignment](https://openaccess.thecvf.com/content/CVPR2024/html/Xu_Enhancing_Video_Super-Resolution_via_Implicit_Resampling-based_Alignment_CVPR_2024_paper.html) | CVPR 2024 | Implicit resampling alignment | [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Xu_Enhancing_Video_Super-Resolution_via_Implicit_Resampling-based_Alignment_CVPR_2024_paper.pdf) |
| [Learning Truncated Causal History Model for Video Restoration](https://proceedings.neurips.cc/paper_files/paper/2024/hash/309fd617a4168d592e543690fbd094db-Abstract-Conference.html) | NeurIPS 2024 | Turtle; truncated causal history; includes VSR | [Code](https://github.com/Ascend-Research/Turtle) · [Project](https://kjanjua26.github.io/turtle/) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/309fd617a4168d592e543690fbd094db-Paper-Conference.pdf) |

<a id="architecture"></a>

## Transformer 与状态空间架构 / Sequence Architectures

面向视频重建的序列建模架构。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [VSRM: A Robust Mamba-Based Framework for Video Super-Resolution](https://openaccess.thecvf.com/content/ICCV2025/html/Tran_VSRM_A_Robust_Mamba-Based_Framework_for_Video_Super-Resolution_ICCV_2025_paper.html) | ICCV 2025 | Mamba sequence modeling<br>state-space | [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Tran_VSRM_A_Robust_Mamba-Based_Framework_for_Video_Super-Resolution_ICCV_2025_paper.pdf) |

<a id="generative"></a>

## 扩散先验与生成式超分 / Diffusion-based VSR

多步扩散、视频生成先验与细节合成。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [DTG-Restore: Training-Free Diffusion Refinement for Generative Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Yesiltepe_DTG-Restore_Training-Free_Diffusion_Refinement_for_Generative_Video_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Training-free diffusion refinement<br>diffusion, self/zero-shot | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Yesiltepe_DTG-Restore_Training-Free_Diffusion_Refinement_for_Generative_Video_Super-Resolution_CVPR_2026_paper.pdf) |
| [Rethinking Diffusion Model-Based Video Super-Resolution: Leveraging Dense Guidance from Aligned Features](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Rethinking_Diffusion_Model-Based_Video_Super-Resolution_Leveraging_Dense_Guidance_from_Aligned_CVPR_2026_paper.html) | CVPR 2026 | Dense guidance from aligned features<br>diffusion | [Code](https://github.com/tszssong/DGAF-VSR) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Xu_Rethinking_Diffusion_Model-Based_Video_Super-Resolution_Leveraging_Dense_Guidance_from_Aligned_CVPR_2026_paper.pdf) |
| [STCDiT: Spatio-Temporally Consistent Diffusion Transformer for High-Quality Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_STCDiT_Spatio-Temporally_Consistent_Diffusion_Transformer_for_High-Quality_Video_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Motion-aware reconstruction and anchor guidance<br>diffusion, spatiotemporal | [Code](https://github.com/JyChen9811/STCDiT) · [Project](https://jychen9811.github.io/STCDiT_page) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_STCDiT_Spatio-Temporally_Consistent_Diffusion_Transformer_for_High-Quality_Video_Super-Resolution_CVPR_2026_paper.pdf) |
| [LVTINO: LAtent Video consisTency INverse sOlver for High Definition Video Restoration](https://iclr.cc/virtual/2026/poster/10011196) | ICLR 2026 | Zero-shot consistency-model inverse solver<br>self/zero-shot | [Code](https://github.com/LATINO-PRO/LVTINO) · [Project](https://latino-pro.github.io/LVTINO/) · [PDF](https://iclr.cc/media/iclr-2026/Slides/10011196.pdf) |
| [SimpleGVR: A Simple Baseline for Latent-Cascaded Generative Video Super-Resolution](https://iclr.cc/virtual/2026/poster/10008775) | ICLR 2026 | Latent-cascaded generative upsampling | [Project](https://simplegvr.github.io/) · [PDF](https://iclr.cc/media/iclr-2026/Slides/10008775.pdf) |
| [Vivid-VR: Distilling Concepts from Text-to-Video Diffusion Transformer for Photorealistic Video Restoration](https://iclr.cc/virtual/2026/poster/10008888) | ICLR 2026 | DiT-based photorealistic restoration<br>diffusion | [Code](https://github.com/csbhr/Vivid-VR) |
| [WEVSR: Video Diffusion Generators for Real-World Video Super-Resolution with Wavelet-Enhanced VAE Encoder](https://proceedings.mlr.press/v306/chen26ce.html) | ICML 2026 | Wavelet-enhanced VAE encoder<br>diffusion | [Code](https://github.com/elvinyychen/WEVSR) · [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/chen26ce/chen26ce.pdf) |
| [PatchVSR: Breaking Video Diffusion Resolution Limits with Patch-wise Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2025/html/Du_PatchVSR_Breaking_Video_Diffusion_Resolution_Limits_with_Patch-wise_Video_Super-Resolution_CVPR_2025_paper.html) | CVPR 2025 | Patch-wise diffusion; scalable output<br>diffusion | [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Du_PatchVSR_Breaking_Video_Diffusion_Resolution_Limits_with_Patch-wise_Video_Super-Resolution_CVPR_2025_paper.pdf) |
| [SeedVR: Seeding Infinity in Diffusion Transformer Towards Generic Video Restoration](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_SeedVR_Seeding_Infinity_in_Diffusion_Transformer_Towards_Generic_Video_Restoration_CVPR_2025_paper.html) | CVPR 2025 | Diffusion Transformer; generic restoration<br>diffusion | [Code](https://github.com/ByteDance-Seed/SeedVR) · [Project](https://iceclear.github.io/projects/seedvr/) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_SeedVR_Seeding_Infinity_in_Diffusion_Transformer_Towards_Generic_Video_Restoration_CVPR_2025_paper.pdf) |
| [DiffVSR: Revealing an Effective Recipe for Taming Robust Video Super-Resolution Against Complex Degradations](https://openaccess.thecvf.com/content/ICCV2025/html/Li_DiffVSR_Revealing_an_Effective_Recipe_for_Taming_Robust_Video_Super-Resolution_ICCV_2025_paper.html) | ICCV 2025 | Complex degradations and temporal consistency | [Code](https://github.com/xh9998/DiffVSR) · [Project](https://xh9998.github.io/DiffVSR-project/) · [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Li_DiffVSR_Revealing_an_Effective_Recipe_for_Taming_Robust_Video_Super-Resolution_ICCV_2025_paper.pdf) |
| [STAR: Spatial-Temporal Augmentation with Text-to-Video Models for Real-World Video Super-Resolution](https://openaccess.thecvf.com/content/ICCV2025/html/Xie_STAR_Spatial-Temporal_Augmentation_with_Text-to-Video_Models_for_Real-World_Video_Super-Resolution_ICCV_2025_paper.html) | ICCV 2025 | Text-to-video diffusion priors<br>diffusion, spatiotemporal | [Code](https://github.com/NJU-PCALab/STAR) · [Project](https://nju-pcalab.github.io/projects/STAR) · [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Xie_STAR_Spatial-Temporal_Augmentation_with_Text-to-Video_Models_for_Real-World_Video_Super-Resolution_ICCV_2025_paper.pdf) |
| [Learning Spatial Adaptation and Temporal Coherence in Diffusion Models for Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2024/html/Chen_Learning_Spatial_Adaptation_and_Temporal_Coherence_in_Diffusion_Models_for_CVPR_2024_paper.html) | CVPR 2024 | SATeCo; spatial adaptation and temporal coherence<br>diffusion | [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Chen_Learning_Spatial_Adaptation_and_Temporal_Coherence_in_Diffusion_Models_for_CVPR_2024_paper.pdf) |
| [Upscale-A-Video: Temporal-Consistent Diffusion Model for Real-World Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2024/html/Zhou_Upscale-A-Video_Temporal-Consistent_Diffusion_Model_for_Real-World_Video_Super-Resolution_CVPR_2024_paper.html) | CVPR 2024 | Text-guided latent diffusion<br>diffusion | [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhou_Upscale-A-Video_Temporal-Consistent_Diffusion_Model_for_Real-World_Video_Super-Resolution_CVPR_2024_paper.pdf) |
| [Enhancing Perceptual Quality in Video Super-Resolution through Temporally-Consistent Detail Synthesis using Diffusion Models](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/1824_ECCV_2024_paper.php) | ECCV 2024 | StableVSR; temporally consistent diffusion<br>diffusion | [Code](https://github.com/claudiom4sir/StableVSR) · [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/01824.pdf) |
| [Motion-Guided Latent Diffusion for Temporally Consistent Real-world Video Super-resolution](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6048_ECCV_2024_paper.php) | ECCV 2024 | Motion-guided latent diffusion<br>diffusion | [Code](https://github.com/IanYeung/MGLD-VSR) · [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06048.pdf) |
| [SeeClear: Semantic Distillation Enhances Pixel Condensation for Video Super-Resolution](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f358b2a880adf34939d2d6f926e54d2a-Abstract-Conference.html) | NeurIPS 2024 | Semantic guidance and pixel condensation | [Code](https://github.com/Tang1705/SeeClear-NeurIPS24) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/f358b2a880adf34939d2d6f926e54d2a-Paper-Conference.pdf) |

<a id="onestep"></a>

## 单步扩散与蒸馏 / One-step Diffusion and Distillation

将生成式超分压缩为单步或少步推理。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [DUO-VSR: Dual-Stream Distillation for One-Step Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Lv_DUO-VSR_Dual-Stream_Distillation_for_One-Step_Video_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Dual-stream one-step distillation<br>online/streaming | [Code](https://github.com/cszy98/DUO-VSR) · [Project](https://cszy98.github.io/DUO-VSR/) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Lv_DUO-VSR_Dual-Stream_Distillation_for_One-Step_Video_Super-Resolution_CVPR_2026_paper.pdf) |
| [PS-SR: Pseudo-Single-Step Video Super-Resolution via Speculative Diffusion](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_PS-SR_Pseudo-Single-Step_Video_Super-Resolution_via_Speculative_Diffusion_CVPR_2026_paper.html) | CVPR 2026 | Speculative diffusion refinement<br>diffusion | [Code](https://github.com/HiDream-ai/PS-SR) · [Project](https://waq2001.github.io/) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_PS-SR_Pseudo-Single-Step_Video_Super-Resolution_via_Speculative_Diffusion_CVPR_2026_paper.pdf) |
| [ART-VSR: Adaptive Rectified Trajectories for One-Step Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/4653) | ECCV 2026 | One-step rectified trajectories | [Code](https://github.com/Roveer/ART_VSR) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/6876.pdf) |
| [Improved Adversarial Diffusion Compression for Real-World Video Super-Resolution](https://iclr.cc/virtual/2026/poster/10009266) | ICLR 2026 | AdcVSR; compressed one-step adversarial distillation<br>diffusion | — |
| [SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training](https://iclr.cc/virtual/2026/poster/10006682) | ICLR 2026 | One-step diffusion adversarial post-training<br>diffusion | [Code](https://github.com/ByteDance-Seed/SeedVR) · [Project](https://iceclear.github.io/projects/seedvr2/) · [PDF](https://iclr.cc/media/iclr-2026/Slides/10006682.pdf) |
| [RelayVSR: Large-Small Model Collaboration for Efficient Real-World Video Super-Resolution](https://arxiv.org/abs/2609.37850) | arXiv 2026 · 预印本 | Streaming / one-step generative VSR<br>online/streaming | [Code](https://github.com/kopperx/RelayVSR) · [PDF](https://arxiv.org/pdf/2609.37850) |
| [UltraVSR: Achieving Ultra-Realistic Video Super-Resolution with Efficient One-Step Diffusion Space](https://doi.org/10.1145/3746027.3755117) | ACM MM 2025 | One-step diffusion video super-resolution<br>diffusion | — |
| [DOVE: Efficient One-Step Diffusion Model for Real-World Video Super-Resolution](https://proceedings.neurips.cc/paper_files/paper/2025/hash/7b04ec5f2b89d7f601382c422dfe07af-Abstract-Conference.html) | NeurIPS 2025 | One-step diffusion adaptation<br>diffusion | [Code](https://github.com/zhengchen1999/DOVE) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/7b04ec5f2b89d7f601382c422dfe07af-Paper-Conference.pdf) |
| [One-Step Diffusion for Detail-Rich and Temporally Consistent Video Super-Resolution](https://proceedings.neurips.cc/paper_files/paper/2025/hash/fc28053a08f59fccb48b11f2e31e81c7-Abstract-Conference.html) | NeurIPS 2025 | DLoRAL; dual LoRA one-step restoration<br>diffusion | [Code](https://github.com/yjsunnn/DLoRAL) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/fc28053a08f59fccb48b11f2e31e81c7-Paper-Conference.pdf) |

<a id="gan"></a>

## 对抗生成式超分 / GAN-based VSR

以对抗学习恢复感知细节。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [VideoGigaGAN: Towards Detail-rich Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2025/html/Xu_VideoGigaGAN_Towards_Detail-rich_Video_Super-Resolution_CVPR_2025_paper.html) | CVPR 2025 | GAN-based detail synthesis | [Project](https://videogigagan.github.io/) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Xu_VideoGigaGAN_Towards_Detail-rich_Video_Super-Resolution_CVPR_2025_paper.pdf) |

<a id="realworld"></a>

## 真实退化、盲超分与自监督 / Real-world and Blind VSR

未知退化、真实噪声、域泛化和自监督学习。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [Self-supervised ControlNet with Spatio-Temporal Mamba for Real-world Video Super-resolution](https://openaccess.thecvf.com/content/CVPR2025/html/Shi_Self-supervised_ControlNet_with_Spatio-Temporal_Mamba_for_Real-world_Video_Super-resolution_CVPR_2025_paper.html) | CVPR 2025 | Self-supervision; ControlNet and Mamba<br>state-space, spatiotemporal, self/zero-shot | [Code](https://github.com/ssj9596/SCST) · [Project](https://ssj9596.github.io/scst-project/) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Shi_Self-supervised_ControlNet_with_Spatio-Temporal_Mamba_for_Real-world_Video_Super-resolution_CVPR_2025_paper.pdf) |
| [Blind Video Super-Resolution based on Implicit Kernels](https://openaccess.thecvf.com/content/ICCV2025/html/Zhu_Blind_Video_Super-Resolution_based_on_Implicit_Kernels_ICCV_2025_paper.html) | ICCV 2025 | Implicit spatially varying degradation kernels | [Code](https://github.com/QZ1-boy/BVSR-IK) · [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhu_Blind_Video_Super-Resolution_based_on_Implicit_Kernels_ICCV_2025_paper.pdf) |
| [NegVSR: Augmenting Negatives for Generalized Noise Modeling in Real-world Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/28942) | AAAI 2024 | Real-world noise modeling and negative augmentation | [Project](https://negvsr.github.io/) |
| [RealViformer: Investigating Attention for Real-World Video Super-Resolution](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/4277_ECCV_2024_paper.php) | ECCV 2024 | Artifact-aware attention | [Code](https://github.com/Yuehan717/RealViformer) · [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/04277.pdf) |

<a id="spacetime"></a>

## 时空联合与任意倍率 / Space-time and Arbitrary-scale SR

空间分辨率与帧率联合提升，连续或非整数倍率。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [Time Without Time: Pseudo-Temporal Representation for Space-Time Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Choi_Time_Without_Time_Pseudo-Temporal_Representation_for_Space-Time_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Pseudo-temporal pretraining<br>spatiotemporal | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Choi_Time_Without_Time_Pseudo-Temporal_Representation_for_Space-Time_Super-Resolution_CVPR_2026_paper.pdf) |
| [AVSR-Diff: Scale-Agnostic Diffusion Priors for Temporally Consistent Arbitrary-Scale Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/5371) | ECCV 2026 | Scale-agnostic diffusion priors<br>diffusion, arbitrary-scale | [Code](https://github.com/KAIST-VICLab/AVSR-Diff) · [Project](https://kaist-viclab.github.io/AVSR-Diff/) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/10243.pdf) |
| [Continuous Space-Time Video Super-Resolution with 3D Fourier Fields](https://iclr.cc/virtual/2026/poster/10008618) | ICLR 2026 | 3D Fourier fields; continuous space-time SR<br>arbitrary-scale, spatiotemporal | [Code](https://github.com/prs-eth/v3) · [Project](https://v3vsr.github.io/) |
| [BF-STVSR: B-Splines and Fourier---Best Friends for High Fidelity Spatial-Temporal Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2025/html/Kim_BF-STVSR_B-Splines_and_Fourier---Best_Friends_for_High_Fidelity_Spatial-Temporal_Video_CVPR_2025_paper.html) | CVPR 2025 | B-spline temporal and Fourier spatial representation<br>spatiotemporal | [Code](https://github.com/Eunjnnn/bfstvsr) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Kim_BF-STVSR_B-Splines_and_Fourier---Best_Friends_for_High_Fidelity_Spatial-Temporal_Video_CVPR_2025_paper.pdf) |
| [Arbitrary-Scale Video Super-resolution Guided by Dynamic Context](https://ojs.aaai.org/index.php/AAAI/article/view/28003) | AAAI 2024 | DCGU; dynamic context-guided upsampling<br>arbitrary-scale | — |
| [SAVSR: Arbitrary-Scale Video Super-Resolution via a Learned Scale-Adaptive Network](https://ojs.aaai.org/index.php/AAAI/article/view/28114) | AAAI 2024 | Scale-adaptive non-integer and asymmetric VSR<br>arbitrary-scale | [Code](https://github.com/Weepingchestnut/SAVSR) |
| [Arbitrary-Scale Video Super-Resolution with Structural and Textural Priors](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/7392_ECCV_2024_paper.php) | ECCV 2024 | ST-AVSR; arbitrary-scale spatial VSR<br>arbitrary-scale | [Code](https://github.com/shangwei5/ST-AVSR) · [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/07392.pdf) |

<a id="efficiency"></a>

## 高效、流式与模型压缩 / Efficient and Streaming VSR

在线推理、边缘部署、量化、轻量化及计算复用。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [QuantVSR: Low-Bit Post-Training Quantization for Real-World Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/37257) | AAAI 2026 | Low-bit diffusion quantization<br>diffusion, quantization | — |
| [FlashVSR: Towards Real-time Diffusion-Based Streaming Video Super Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Zhuang_FlashVSR_Towards_Real-time_Diffusion-Based_Streaming_Video_Super_Resolution_CVPR_2026_paper.html) | CVPR 2026 | One-step streaming diffusion<br>diffusion, online/streaming | [Code](https://github.com/OpenImagingLab/FlashVSR) · [Project](https://zhuang2002.github.io/FlashVSR/) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhuang_FlashVSR_Towards_Real-time_Diffusion-Based_Streaming_Video_Super_Resolution_CVPR_2026_paper.pdf) |
| [NanoVSR: Towards Real-Time Video Super-Resolution on Edge Devices](https://eccv.ecva.net/virtual/2026/poster/5988) | ECCV 2026 | Real-time edge deployment | [Code](https://github.com/filippawlicki/nanovsr) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/15115.pdf) |
| [Stream-DiffVSR: Low-Latency Streamable Video Super-Resolution via Auto-Regressive Diffusion](https://eccv.ecva.net/virtual/2026/poster/3212) | ECCV 2026 | Autoregressive streaming diffusion<br>diffusion, online/streaming | [Code](https://github.com/jamichss/Stream-DiffVSR) · [Project](https://jamichss.github.io/stream-diffvsr-project-page/) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/390.pdf) |
| [TAQ: Static-Deployable Temporal-Aware Quantization for Real-World Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/5539) | ECCV 2026 | Temporal-aware quantization<br>quantization | [Code](https://github.com/imaboybut/TAQ) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/11260.pdf) |
| [TRaM-VSR: Importance-Aware Token Routing and Merging for One-Step Diffusion Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/3546) | ECCV 2026 | Token routing and merging<br>diffusion | [待发布](https://github.com/Ree1s/TRaM-VSR) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/1923.pdf) |
| [Trajectory-aware Shifted State Space Models for Online Video Super-Resolution](https://iclr.cc/virtual/2026/poster/10009452) | ICLR 2026 | TS-Mamba; online state-space modeling<br>state-space, online/streaming | [Code](https://github.com/QZ1-boy/TS-Mamba) · [PDF](https://iclr.cc/media/iclr-2026/Slides/10009452_EX7lTZM.pdf) |
| [InfVSR: Toward Consistency-Driven Streaming Generative Video Super-Resolution](https://proceedings.mlr.press/v306/zhang26dm.html) | ICML 2026 | Consistency-driven streaming inference<br>online/streaming | [Code](https://github.com/Kai-Liu001/InfVSR) · [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhang26dm/zhang26dm.pdf) |
| [LSGQuant: Layer-Sensitivity Guided Quantization for One-Step Diffusion Real-World Video Super-Resolution](https://proceedings.mlr.press/v306/wu26g.html) | ICML 2026 | Layer-sensitive diffusion quantization<br>diffusion, quantization | [Code](https://github.com/zhengchen1999/LSGQuant) · [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/wu26g/wu26g.pdf) |
| [LiteVSR: Lightweight Adaptation of Frozen Diffusion Transformers for Video Super-Resolution](https://proceedings.mlr.press/v306/cao26n.html) | ICML 2026 | Lightweight diffusion Transformer adaptation<br>diffusion | [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/cao26n/cao26n.pdf) |
| [ReCaVSR: One-Step Streaming Diffusion Video Super-Resolution with Recycled Latents and Learned Cache Routing](https://arxiv.org/abs/2609.37831) | arXiv 2026 · 预印本 | Streaming / one-step generative VSR<br>diffusion, online/streaming | [Code](https://github.com/kopperx/ReCaVSR) · [PDF](https://arxiv.org/pdf/2609.37831) |
| [SwiftVR: Real-Time One-Step Generative Video Restoration](https://arxiv.org/abs/2606.09516) | arXiv 2026 · 预印本 | Streaming / one-step generative VSR<br>online/streaming | [Code](https://github.com/H-oliday/SwiftVR) · [PDF](https://arxiv.org/pdf/2606.09516) |
| [QBasicVSR: Temporal Awareness Adaptation Quantization for Video Super-Resolution](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c17f3035898a7044194fe45c5df6c6e8-Abstract-Conference.html) | NeurIPS 2025 | Temporal-aware low-bit VSR quantization<br>quantization | [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/c17f3035898a7044194fe45c5df6c6e8-Paper-Conference.pdf) |
| [Video Super-Resolution Transformer with Masked Inter&Intra-Frame Attention](https://openaccess.thecvf.com/content/CVPR2024/html/Zhou_Video_Super-Resolution_Transformer_with_Masked_InterIntra-Frame_Attention_CVPR_2024_paper.html) | CVPR 2024 | MIA-VSR; masked attention | [Code](https://github.com/CVL-UESTC/MIA-VSR) · [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhou_Video_Super-Resolution_Transformer_with_Masked_InterIntra-Frame_Attention_CVPR_2024_paper.pdf) |

<a id="compression"></a>

## 压缩域与传输鲁棒性 / Compression and Delivery

编码信息、压缩退化、丢包及流媒体传输。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [Compressed-Domain-Aware Online Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Compressed-Domain-Aware_Online_Video_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Compressed-domain guidance; online inference<br>online/streaming | [Code](https://github.com/sspBIT/CDA-VSR) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Compressed-Domain-Aware_Online_Video_Super-Resolution_CVPR_2026_paper.pdf) |
| [Mitigating Delivery Artifacts in Real-World Video Super-Resolution](https://doi.org/10.1145/3746027.3754989) | ACM MM 2025 | Robust VSR against streaming packet loss<br>online/streaming | — |

<a id="guided"></a>

## 参考、文本引导与交互 / Guided and Interactive VSR

稀疏关键帧、参考信息、文本提示和用户控制。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [TextOVSR: Text-Guided Real-World Opera Video Super-Resolution](https://openaccess.thecvf.com/content/CVPR2026/html/Chang_TextOVSR_Text-Guided_Real-World_Opera_Video_Super-Resolution_CVPR_2026_paper.html) | CVPR 2026 | Text-guided opera video | [Code](https://github.com/ChangHua0/TextOVSR) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Chang_TextOVSR_Text-Guided_Real-World_Opera_Video_Super-Resolution_CVPR_2026_paper.pdf) |
| [SparkVSR: Interactive Video Super-Resolution via Sparse Keyframe Propagation](https://eccv.ecva.net/virtual/2026/poster/5604) | ECCV 2026 | Sparse keyframe interaction and propagation | [Code](https://github.com/taco-group/SparkVSR) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/11646.pdf) |
| [Tiled Prompts: Overcoming Prompt Misguidance in Image and Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/4355) | ECCV 2026 | Spatially localized prompt guidance | [Project](https://bryanswkim.github.io/tiled-prompts/) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/5536.pdf) |

<a id="events"></a>

## 事件相机视频超分 / Event-guided VSR

融合 RGB 视频与事件信号进行空间或时空超分。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [Exploiting Blurry Representations for Event-guided Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/38081) | AAAI 2026 | BluR-EVSR; degradation-aware RGB-event fusion<br>events | — |
| [Seeing the Unseen: Zooming in the Dark with Event Cameras](https://ojs.aaai.org/index.php/AAAI/article/view/37478) | AAAI 2026 | Event-assisted low-light video super-resolution<br>events | — |
| [EvSTVSR: Event Guided Space-Time Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/32983) | AAAI 2025 | Event-guided alignment and space-time upsampling<br>spatiotemporal, events | [Code](https://github.com/zju-bmi-lab/EvSTVSR) |
| [Event-Enhanced Blurry Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/32438) | AAAI 2025 | Ev-DeblurVSR; event-guided deblurring and VSR<br>events | [Code](https://github.com/DachunKai/Ev-DeblurVSR) |
| [EvEnhancer: Empowering Effectiveness, Efficiency and Generalizability for Continuous Space-Time Video Super-Resolution with Events](https://openaccess.thecvf.com/content/CVPR2025/html/Wei_EvEnhancer_Empowering_Effectiveness_Efficiency_and_Generalizability_for_Continuous_Space-Time_Video_CVPR_2025_paper.html) | CVPR 2025 | Continuous space-time SR with events<br>arbitrary-scale, spatiotemporal, events | [Code](https://github.com/W-Shuoyan/EvEnhancer) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Wei_EvEnhancer_Empowering_Effectiveness_Efficiency_and_Generalizability_for_Continuous_Space-Time_Video_CVPR_2025_paper.pdf) |
| [Event-based Video Super-Resolution via State Space Models](https://openaccess.thecvf.com/content/CVPR2025/html/Xiao_Event-based_Video_Super-Resolution_via_State_Space_Models_CVPR_2025_paper.html) | CVPR 2025 | MamEVSR; RGB-event state-space fusion<br>state-space, events | [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Xiao_Event-based_Video_Super-Resolution_via_State_Space_Models_CVPR_2025_paper.pdf) |
| [DeblurSR: Event-Based Motion Deblurring under the Spiking Representation](https://ojs.aaai.org/index.php/AAAI/article/view/28293) | AAAI 2024 | Joint event reconstruction; includes VSR extension<br>events | — |
| [Asymmetric Event-Guided Video Super-Resolution](https://openreview.net/forum?id=zVgZfHRM3g) | ACM MM 2024 | AsEVSRN; asymmetric-resolution RGB-event fusion<br>events | [Code](https://github.com/zeyuxiao1997/AsEVSRN) |
| [Event-Adapted Video Super-Resolution](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/5857_ECCV_2024_paper.php) | ECCV 2024 | EATER; parameter-efficient event adaptation<br>events | [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05857.pdf) |
| [EvTexture: Event-driven Texture Enhancement for Video Super-Resolution](https://proceedings.mlr.press/v235/kai24a.html) | ICML 2024 | Event-driven texture enhancement<br>events | [Code](https://github.com/DachunKai/EvTexture) · [PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kai24a/kai24a.pdf) |

<a id="faces"></a>

## 人脸视频超分与修复 / Face Video SR

人脸细节、身份一致性和时序稳定性。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [DTI: Dynamic Trajectory Initialization for Generative Face Video Super-Resolution](https://eccv.ecva.net/virtual/2026/poster/5665) | ECCV 2026 | Face video; trajectory initialization | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/12117.pdf) |
| [TIGER: Taming Identity, Geometry, and Generative Priors for High-Quality Face Video Restoration](https://eccv.ecva.net/virtual/2026/poster/3384) | ECCV 2026 | Identity and geometry priors for face restoration | [Code](https://github.com/PixCtrol/Tiger) · [Project](https://yzhoulv.github.io/Tiger/) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/1221.pdf) |
| [Dynamic Content Prediction with Motion-aware Priors for Blind Face Video Restoration](https://openaccess.thecvf.com/content/CVPR2025/html/Xie_Dynamic_Content_Prediction_with_Motion-aware_Priors_for_Blind_Face_Video_CVPR_2025_paper.html) | CVPR 2025 | Motion-aware face content prediction | [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Xie_Dynamic_Content_Prediction_with_Motion-aware_Priors_for_Blind_Face_Video_CVPR_2025_paper.pdf) |
| [SVFR: A Unified Framework for Generalized Video Face Restoration](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_SVFR_A_Unified_Framework_for_Generalized_Video_Face_Restoration_CVPR_2025_paper.html) | CVPR 2025 | Face restoration and temporal consistency | [Code](https://github.com/wangzhiyaoo/SVFR) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_SVFR_A_Unified_Framework_for_Generalized_Video_Face_Restoration_CVPR_2025_paper.pdf) |
| [Dirichlet-Constrained Variational Codebook Learning for Temporally Coherent Video Face Restoration](https://openaccess.thecvf.com/content/ICCV2025/html/Chen_Dirichlet-Constrained_Variational_Codebook_Learning_for_Temporally_Coherent_Video_Face_Restoration_ICCV_2025_paper.html) | ICCV 2025 | DicFace; variational face codebooks | [Code](https://github.com/fudan-generative-vision/DicFace) · [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Chen_Dirichlet-Constrained_Variational_Codebook_Learning_for_Temporally_Coherent_Video_Face_Restoration_ICCV_2025_paper.pdf) |
| [Kalman-Inspired Feature Propagation for Video Face Super-Resolution](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/3752_ECCV_2024_paper.php) | ECCV 2024 | KEEP; Kalman-inspired face feature propagation | [Code](https://github.com/jnjaby/KEEP) · [Project](https://jnjaby.github.io/projects/KEEP/) · [PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/03752.pdf) |

<a id="joint"></a>

## 联合去模糊、弱光与物理退化 / Joint Restoration

超分与去模糊、低照度、红外或湍流恢复联合建模。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [HATIR: Heat-Aware Diffusion for Turbulent Infrared Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/38421) | AAAI 2026 | Infrared SR with atmospheric turbulence<br>diffusion | — |
| [Thermal Diffusion Matters: Infrared Spatial-Temporal Video Super-Resolution through Heat Conduction Priors](https://openaccess.thecvf.com/content/CVPR2026/html/Zhou_Thermal_Diffusion_Matters_Infrared_Spatial-Temporal_Video_Super-Resolution_through_Heat_Conduction_CVPR_2026_paper.html) | CVPR 2026 | THERIS; infrared space-time SR<br>diffusion, spatiotemporal | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhou_Thermal_Diffusion_Matters_Infrared_Spatial-Temporal_Video_Super-Resolution_through_Heat_Conduction_CVPR_2026_paper.pdf) |
| [VSRELL: A Simple Baseline for Video Super-Resolution and Enhancement in Low-Light Environment](https://openaccess.thecvf.com/content/CVPR2026/html/Hui_VSRELL_A_Simple_Baseline_for_Video_Super-Resolution_and_Enhancement_in_CVPR_2026_paper.html) | CVPR 2026 | Joint low-light enhancement and SR | [Code](https://github.com/373hdj/VSRELL) · [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Hui_VSRELL_A_Simple_Baseline_for_Video_Super-Resolution_and_Enhancement_in_CVPR_2026_paper.pdf) |
| [FMA-Net++: Motion- and Exposure-Aware Joint Video Super-Resolution and Deblurring](https://eccv.ecva.net/virtual/2026/poster/5366) | ECCV 2026 | Exposure-aware joint deblurring and SR | [Code](https://github.com/KAIST-VICLab/FMA-Net-PlusPlus) · [Project](https://kaist-viclab.github.io/fmanetpp_site/) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/10213.pdf) |
| [FMA-Net: Flow-Guided Dynamic Filtering and Iterative Feature Refinement with Multi-Attention for Joint Video Super-Resolution and Deblurring](https://openaccess.thecvf.com/content/CVPR2024/html/Youk_FMA-Net_Flow-Guided_Dynamic_Filtering_and_Iterative_Feature_Refinement_with_Multi-Attention_CVPR_2024_paper.html) | CVPR 2024 | Joint deblurring and super-resolution | [Code](https://github.com/KAIST-VICLab/FMA-Net) · [Project](https://kaist-viclab.github.io/fmanet-site) · [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Youk_FMA-Net_Flow-Guided_Dynamic_Filtering_and_Iterative_Feature_Refinement_with_Multi-Attention_CVPR_2024_paper.pdf) |

<a id="domains"></a>

## 专用场景与模态 / Domain-specific VSR

医学、卫星、全景、实时渲染、深度及显微视频。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [MambaOVSR: Multiscale Fusion with Global Motion Modeling for Chinese Opera Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/37261) | AAAI 2026 | Opera space-time VSR; Mamba fusion<br>state-space, spatiotemporal | — |
| [Spatio-Temporal Distortion Aware Omnidirectional Video Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/37215) | AAAI 2026 | STDAN; 360-degree video projection and temporal alignment<br>spatiotemporal | — |
| [SpatioTemporal Difference Network for Video Depth Super-Resolution](https://ojs.aaai.org/index.php/AAAI/article/view/38011) | AAAI 2026 | RGB-guided video depth SR | [Code](https://github.com/yanzq95/STDNet) |
| [Efficient Trajectory Space-Time Super-Resolution for Fast Live-cell Imaging](https://doi.org/10.1145/3746027.3754914) | ACM MM 2025 | T-STSR; fast subcellular space-time imaging<br>spatiotemporal | — |
| [Efficient Video Super-Resolution for Real-time Rendering with Decoupled G-buffer Guidance](https://openaccess.thecvf.com/content/CVPR2025/html/Zheng_Efficient_Video_Super-Resolution_for_Real-time_Rendering_with_Decoupled_G-buffer_Guidance_CVPR_2025_paper.html) | CVPR 2025 | RDG; G-buffer guided rendering | [Code](https://github.com/sunny2109/RDG) · [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Zheng_Efficient_Video_Super-Resolution_for_Real-time_Rendering_with_Decoupled_G-buffer_Guidance_CVPR_2025_paper.pdf) |
| [Hazy Low-Quality Satellite Video Restoration Via Learning Optimal Joint Degradation Patterns and Continuous-Scale Super-Resolution Reconstruction](https://openaccess.thecvf.com/content/CVPR2025/html/Ni_Hazy_Low-Quality_Satellite_Video_Restoration_Via_Learning_Optimal_Joint_Degradation_CVPR_2025_paper.html) | CVPR 2025 | Satellite video; haze and continuous scaling<br>arbitrary-scale | [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Ni_Hazy_Low-Quality_Satellite_Video_Restoration_Via_Learning_Optimal_Joint_Degradation_CVPR_2025_paper.pdf) |
| [MedVSR: Medical Video Super-Resolution with Cross State-Space Propagation](https://openaccess.thecvf.com/content/ICCV2025/html/Liu_MedVSR_Medical_Video_Super-Resolution_with_Cross_State-Space_Propagation_ICCV_2025_paper.html) | ICCV 2025 | Medical video; cross state-space propagation<br>state-space | [Code](https://github.com/CUHK-AIM-Group/MedVSR) · [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Liu_MedVSR_Medical_Video_Super-Resolution_with_Cross_State-Space_Propagation_ICCV_2025_paper.pdf) |

<a id="benchmarks"></a>

## 数据集与评测 / Datasets and Benchmarks

支持视频超分研究的数据集和评测基准。

| Paper | Venue | Focus / Tags | Resources |
| --- | --- | --- | --- |
| [ClearText-Video: A Large-Scale Text-Centric Video Dataset Bridging Video Restoration and Scene-Text Enhancement](https://eccv.ecva.net/virtual/2026/poster/3992) | ECCV 2026 | Text-centric video restoration benchmark | [Code](https://github.com/jinlong17/CTVid-Bench) · [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/4006.pdf) |

## Contributing

欢迎补充遗漏论文、作者资源链接和分类修正。请提供原始来源，并按 [贡献说明](CONTRIBUTING.md) 更新文献数据。
