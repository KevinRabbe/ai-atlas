# Model Architectures

## Required function

Provide a learnable computational substrate that transforms observations and internal state into useful representations, predictions, decisions or control signals.

## Status

**Coupled architecture/systems first evidence pass completed; not saturated.**

Detailed notes live under [`architecture-systems/`](architecture-systems/INDEX.md) because architecture cannot be evaluated independently of memory hierarchy, execution critical path and communication. The current pass covers information access/state, conditional routing, adaptive computation/writable memory, hybrid operators, IO/locality, distributed communication, precision, inference execution and hardware co-design.

## First-pass findings

1. **Information-access semantics are more fundamental than named blocks.** Direct address, bounded recurrent state and writable memory solve different access problems.
2. **Direct addressability versus compressed state is a genuine trade-off.** Better update rules move the frontier rather than removing it.
3. **Training and inference forms can differ.** Parallel/chunked training can coexist with recurrent decode.
4. **Conditional computation is not free capacity.** Sparse activation trades arithmetic for routing, storage, load balance and communication.
5. **Variable depth is viable but requires a stopping/value policy.** More internal steps are useful only when their expected value exceeds cost.
6. **Functional heterogeneity is increasingly credible.** Current hybrid systems show that local/direct access, recurrent state and sparse specialists can coexist effectively, but each mechanism must earn its complexity.
7. **Inference state is architectural.** KV/recurrent/latent/writable state can dominate long-context memory and bandwidth.

## Mechanism families still to deepen

Feed-forward networks; recurrence; attention; convolution; state-space/linear attention; memory-augmented networks; conditional computation; graph/message-passing networks; energy-based models; diffusion/generative dynamics; modular networks; neuro-symbolic hybrids; program interpreters; adaptive computation; test-time learning modules.

## Clean-sheet questions

- What information must remain directly addressable versus summarized into state?
- Which operations require content-dependent routing?
- What update algebra best prevents interference in bounded memory?
- Can active computation graph, precision and memory tier change with task difficulty?
- What is the minimum information that must cross specialist/module boundaries?
- Which properties are intelligence requirements versus accelerator conveniences?

## Anti-assumptions

Do not assume attention, recurrence, state-space models, sparse experts, homogeneous repeated blocks, differentiability, fixed depth, fixed precision or a single neural substrate are necessary. Treat each as evidence about computational properties.