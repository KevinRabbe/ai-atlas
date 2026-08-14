# Architecture + Systems — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

These are implementation-neutral deductions from the coupled architecture/systems evidence map. They are constraints and hypotheses for later clean-sheet design, not a selection of Transformer, RNN, SSM, MoE, GPU, or any other named implementation.

## P-AS01 — Information-access semantics should determine the memory mechanism

Past information can be retained as directly addressable items, compressed recurrent state, writable external state, or mixtures. Each has different capability and cost. No current evidence supports one access mechanism as universally optimal.

**Confidence:** high.

## P-AS02 — Direct addressability and bounded state form a real trade-off

Direct access preserves flexible lookup but grows retained state/work; bounded recurrent state offers cheap incremental execution but must compress, overwrite and manage interference. Better update rules move the frontier but do not erase the distinction.

**Confidence:** high.

## P-AS03 — Training and inference need not use the same execution form

Several sequence mechanisms admit highly parallel/chunked training and recurrent incremental inference. Therefore recurrent state does not imply fully serial training, and training-friendly execution need not dictate decode state representation.

**Confidence:** high.

## P-AS04 — Conditional computation trades arithmetic for routing and movement

Sparse activation can decouple stored capacity from active arithmetic, but routing, load balance, parameter storage, communication and kernel efficiency become first-class costs.

**Confidence:** high.

## P-AS05 — Semantic routing, compute allocation and physical scheduling are distinct problems

The capability best suited to an input need not be physically located where executing it is cheapest. Clean-sheet systems should avoid unnecessarily binding semantic specialization to static device placement.

**Confidence:** medium-high.

## P-AS06 — Variable computation is a capability only when stopping is controlled

Adaptive depth/recurrent refinement can spend more compute on harder inputs. Without a mechanism estimating the marginal value of additional work, variable depth can simply create instability or waste.

**Confidence:** medium.

## P-AS07 — Data movement is part of algorithmic cost

Memory hierarchy and communication can dominate time and energy. Two mathematically equivalent computations can have very different machine cost depending on locality, tiling, state layout and reuse.

**Confidence:** very high.

## P-AS08 — Abstract complexity and realized machine complexity must be recorded separately

Operation count, asymptotic sequence complexity and state growth are necessary but insufficient. Bytes moved, synchronization, kernel shape, utilization, precision, batching and communication determine realized cost.

**Confidence:** very high.

## P-AS09 — Persistent inference state is a first-class architectural variable

KV caches, recurrent states, compressed latent states and writable memories can dominate long-running inference memory and bandwidth. State representation should be evaluated as seriously as parameter representation.

**Confidence:** high.

## P-AS10 — Numerical precision is an allocatable resource

Current quantization evidence shows that sensitivity is non-uniform and that low precision can preserve substantial capability when algorithm/training and hardware are matched. A single global precision is a convention, not a proven requirement.

**Confidence:** high for non-uniformity; medium for dynamic precision allocation.

## P-AS11 — Architecture and physical execution should be co-designed, but physical accidents must be labeled

Locality, bandwidth, energy and communication are fundamental physical constraints. GPU warp sizes, a specific tensor-core datatype, HBM generation or cluster topology are transient implementation constraints. The Atlas must exploit the latter without promoting them to laws of intelligence.

**Confidence:** high.

## P-AS12 — Functional heterogeneity is plausible; architecture soup is not

Attention/retrieval, recurrent state, writable memory, conditional specialists and iterative computation solve partly different problems. Hybrid systems repeatedly improve practical frontiers, suggesting that a single homogeneous block may be unnecessarily restrictive. But every extra mechanism adds optimization/runtime/interface cost and must earn its role by ablation.

**Confidence:** medium-high.

---

## Emerging substrate model

The evidence suggests evaluating a computational substrate as a mapping:

`required information interaction -> representation/state -> operation -> physical placement -> realized cost -> downstream utility`

rather than as a named neural block.

A useful future capacity description may need multiple axes:

- stored parametric capacity;
- active computation per decision;
- addressable working/persistent state;
- memory bandwidth and locality;
- communication volume;
- sequential critical-path depth;
- adaptive-compute range;
- precision/fidelity;
- external-memory/tool bandwidth.

No scalar replacement for parameter count is established yet.

## Strong anti-conclusions

This pass does **not** justify any of the following:

- “attention is obsolete”;
- “linear/recurrent models are the final architecture”;
- “hybrids are always better”;
- “MoE gives free capacity”;
- “FLOPs measure AI cost”;
- “low precision is always harmless”;
- “current GPUs should define the clean-sheet architecture.”

## Most important experiment family

Build matched small models where the same functional requirement is moved between mechanisms while controlling total resource envelopes. For example, allocate long-range information access between direct attention, recurrent state and explicit retrieval while measuring:

1. task quality and generalization;
2. exact/associative recall and state tracking;
3. training compute and wall-clock time;
4. decode latency and throughput;
5. persistent state bytes;
6. HBM/cache traffic;
7. energy where measurable;
8. robustness as sequence length and hardware change.

This is more informative for clean-sheet design than comparing unrelated flagship models.