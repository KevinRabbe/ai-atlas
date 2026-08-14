# Model Architectures

## Required function

Provide a learnable computational substrate that transforms observations and internal state into useful representations, predictions, decisions or control signals.

## Mechanism families to map

Feed-forward networks; recurrence; attention; convolution; state-space models; memory-augmented networks; conditional computation / mixture-of-experts; graph networks; energy-based models; diffusion/generative dynamics; modular networks; neuro-symbolic hybrids; program interpreters; adaptive computation; test-time learning modules.

## Early evidence anchors

Transformers established that attention-only sequence models could outperform recurrent/convolutional baselines while enabling high parallelism. Sparse MoE work established that total parameter capacity and active compute can be decoupled. Mamba demonstrated a selective state-space alternative with linear sequence scaling in tested regimes. Titans explores learned neural memory updated at test time.

These results show that architecture is a trade space among information access, state persistence, conditional computation, parallelism, memory movement and learnability—not a contest over one named block.

## Clean-sheet questions

- What information must be globally addressable versus compressed into state?
- Which operations need content-dependent routing?
- How much persistent state should live inside the learned substrate?
- Can architecture change its own active computation graph based on the problem?
- What is the minimum communication required among specialized modules?
- Which architecture properties arise from GPU convenience rather than intelligence requirements?
