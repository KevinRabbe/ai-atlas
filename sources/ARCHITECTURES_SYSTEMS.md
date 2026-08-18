# Architecture + Systems — Source Registry

Primary/original sources for the first coupled architecture/systems pass. IDs are referenced by `atlas/architecture-systems/`.

## Historical and architectural primitives

- **AS-S001** — Hochreiter & Schmidhuber (1997), *Long Short-Term Memory*. https://doi.org/10.1162/neco.1997.9.8.1735
- **AS-S002** — Vaswani et al. (2017), *Attention Is All You Need*. https://arxiv.org/abs/1706.03762
- **AS-S003** — Graves, Wayne & Danihelka (2014), *Neural Turing Machines*. https://arxiv.org/abs/1410.5401
- **AS-S004** — Graves (2016), *Adaptive Computation Time for Recurrent Neural Networks*. https://arxiv.org/abs/1603.08983

## Attention state and selective access

- **AS-S005** — Shazeer (2019), *Fast Transformer Decoding: One Write-Head is All You Need*. https://arxiv.org/abs/1911.02150
- **AS-S006** — Ainslie et al. (2023), *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. https://arxiv.org/abs/2305.13245
- **AS-S007** — DeepSeek-AI (2024), *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. https://arxiv.org/abs/2405.04434
- **AS-S008** — Yuan et al. (2025), *Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention*. https://arxiv.org/abs/2502.11089

## Recurrent, convolutional, state-space and linear alternatives

- **AS-S009** — Poli et al. (2023), *Hyena Hierarchy: Towards Larger Convolutional Language Models*. https://arxiv.org/abs/2302.10866
- **AS-S010** — Sun et al. (2023), *Retentive Network*. https://arxiv.org/abs/2307.08621
- **AS-S011** — Peng et al. (2023), *RWKV: Reinventing RNNs for the Transformer Era*. https://arxiv.org/abs/2305.13048
- **AS-S012** — Gu & Dao (2023), *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*. https://arxiv.org/abs/2312.00752
- **AS-S013** — Dao & Gu (2024), *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality (Mamba-2)*. https://arxiv.org/abs/2405.21060
- **AS-S014** — De et al. (2024), *Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models*. https://arxiv.org/abs/2402.19427
- **AS-S015** — Lieber et al. (2024), *Jamba: A Hybrid Transformer-Mamba Language Model*. https://arxiv.org/abs/2403.19887
- **AS-S016** — Lahoti et al. (2026), *Mamba-3: Improved Sequence Modeling using State Space Principles*. https://arxiv.org/abs/2603.15569
- **AS-S017** — Kimi Team et al. (2025), *Kimi Linear: An Expressive, Efficient Attention Architecture*. https://arxiv.org/abs/2510.26692
- **AS-S018** — Hatamizadeh, Choi & Kautz (2026), *Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention*. https://arxiv.org/abs/2605.22791

## Writable memory and adaptive inference

- **AS-S019** — Behrouz, Zhong & Mirrokni (2025), *Titans: Learning to Memorize at Test Time*. https://arxiv.org/abs/2501.00663
- **AS-S041** — Geiping et al. (2025), *Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach*. https://arxiv.org/abs/2502.05171

## Conditional computation and routing

- **AS-S020** — Dai et al. (2024), *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models*. https://arxiv.org/abs/2401.06066
- **AS-S021** — Zhou et al. (2022), *Mixture-of-Experts with Expert Choice Routing*. https://arxiv.org/abs/2202.09368
- **AS-S022** — Lepikhin et al. (2020), *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. https://arxiv.org/abs/2006.16668
- **AS-S023** — Gale et al. (2022), *MegaBlocks: Efficient Sparse Training with Mixture-of-Experts*. https://arxiv.org/abs/2211.15841
- **AS-S024** — Hwang et al. (2022), *Tutel: Adaptive Mixture-of-Experts at Scale*. https://arxiv.org/abs/2206.03382

## IO, memory hierarchy and kernels

- **AS-S025** — Williams, Waterman & Patterson (2009), *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. https://doi.org/10.1145/1498765.1498785
- **AS-S026** — Horowitz (2014), *Computing's Energy Problem (and What We Can Do About It)*. https://doi.org/10.1109/ISSCC.2014.6757323
- **AS-S027** — Dao et al. (2022), *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. https://arxiv.org/abs/2205.14135
- **AS-S028** — Dao (2023/2024), *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. https://arxiv.org/abs/2307.08691
- **AS-S029** — Shah et al. (2024), *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision*. https://arxiv.org/abs/2407.08608
- **AS-S030** — Kwon et al. (2023), *Efficient Memory Management for Large Language Model Serving with PagedAttention*. https://arxiv.org/abs/2309.06180

## Inference scheduling

- **AS-S031** — Leviathan, Kalman & Matias (2023), *Fast Inference from Transformers via Speculative Decoding*. https://proceedings.mlr.press/v202/leviathan23a.html

## Distributed training

- **AS-S032** — Rajbhandari et al. (2019), *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. https://arxiv.org/abs/1910.02054
- **AS-S033** — Shoeybi et al. (2019), *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. https://arxiv.org/abs/1909.08053
- **AS-S034** — Narayanan et al. (2021), *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM*. https://arxiv.org/abs/2104.04473
- **AS-S042** — Shing, Koyama & Akiba (2026), *DiffusionBlocks: Block-wise Neural Network Training via Diffusion Interpretation*. https://arxiv.org/abs/2506.14202 — decomposes residual-network training into independent local denoising objectives, changing active-memory and inter-block communication topology; current large-scale/frontier extrapolation remains unverified. Focused note: `sources/DIFFUSION_BLOCKWISE_TRAINING.md`.

## Precision

- **AS-S035** — Xiao et al. (2022), *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. https://arxiv.org/abs/2211.10438
- **AS-S036** — Lin et al. (2023), *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. https://arxiv.org/abs/2306.00978
- **AS-S037** — Ma et al. (2024), *The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits*. https://arxiv.org/abs/2402.17764

## Hardware co-design

- **AS-S038** — Jouppi et al. (2017), *In-Datacenter Performance Analysis of a Tensor Processing Unit*. https://arxiv.org/abs/1704.04760
- **AS-S039** — Jouppi et al. (2023), *TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning with Hardware Support for Embeddings*. https://arxiv.org/abs/2304.01433

## Additional system/architecture anchor

- **AS-S040** — DeepSeek-AI (2024), *DeepSeek-V3 Technical Report*. https://arxiv.org/abs/2412.19437

## Gaps before saturation

Expand primary evidence for: convolution/locality outside sequence language models; graph/message-passing architectures; energy-based and diffusion computation; neural cellular automata; learned program interpreters; dynamic sparse attention beyond current long-context studies; memory-capacity theory for linear/recurrent attention; associative-memory interference; near/in-memory compute; neuromorphic/event-driven hardware; chiplet/wafer-scale fabrics; optical/analog accelerators; fault tolerance; compiler/autotuning; communication lower bounds; empirical training-time activation/optimizer-state decomposition; local-objective/block-wise training at larger scales; and inference workloads beyond autoregressive language generation.