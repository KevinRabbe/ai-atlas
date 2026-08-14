# E19 — Fidelity Allocation: Uniform Exact vs Approximate vs Adaptive Precision

**Status:** implemented and tested. Two structurally different families support a narrow DL-019 promotion.

## Question

Should every numerical/learned state transition use maximum fidelity, should approximation be applied uniformly for efficiency, or should precision itself be a priced resource?

The clean-sheet question is:

> **When is approximation error small enough to tolerate, and when can that error change a sufficiently consequential downstream decision that higher fidelity earns its cost?**

Exact identity, provenance, authority and other categorical side semantics remain governed separately by PS-001/PS-017. E19 concerns tolerant numerical/computational state.

## Family A — one-shot threshold decisions

A continuous hidden value determines a binary action around a decision boundary. Low fidelity quantizes the value to step `0.25`; high fidelity reads the exact value. Task consequence varies independently.

Variants:

- `low` — quantized decision only;
- `high` — exact decision on every task;
- `adaptive` — begin with low fidelity and buy exact computation only when the quantization interval overlaps the decision boundary or higher consequence makes a wider uncertainty band worth resolving.

### 30-seed result

| variant | net utility/task | error rate | high-fidelity rate | mean fidelity cost |
|---|---:|---:|---:|---:|
| low | 1.6869 | 0.0626 | 0.0000 | **0.0100** |
| high | 2.2523 | **0.0000** | 1.0000 | 0.0800 |
| **adaptive** | **2.3057** | **0.0000** | **0.2082** | **0.0267** |

Adaptive exact-computation rate rises with consequence:

- consequence 1: ~`0.1258`;
- consequence 3: ~`0.1247`;
- consequence 6: ~`0.3740`.

The extra fidelity is therefore spent where approximation can plausibly change a more consequential decision rather than uniformly.

## Family B — long-horizon accumulated constraint

A 40–100 step trajectory accumulates noisy increments. A safety decision depends on whether the true state ever crosses a limit. Low fidelity rounds the running state each step, so approximation error can compound over the trajectory. Raw increments remain recoverable source evidence, allowing an exact replay when the approximate trajectory approaches the constraint boundary.

Variants:

- `low` — rounded state throughout;
- `high` — exact state throughout;
- `adaptive` — maintain cheap approximate state, estimate a horizon/consequence-sensitive uncertainty margin, and replay exact retained increments only when the approximate trajectory lies close enough to the limit.

### 30-seed result

| variant | net utility/episode | error rate | false-safe rate | high-fidelity/replay rate |
|---|---:|---:|---:|---:|
| low | 0.4173 | 0.1072 | 0.0477 | 0.0000 |
| high | 0.7902 | **0.0000** | **0.0000** | 1.0000 |
| **adaptive** | **0.8434** | **0.0050** | **0.0020** | **0.4813** |

Exact replay rate rises with consequence:

- consequence 4: ~`0.3802`;
- consequence 8: ~`0.4920`;
- consequence 12: ~`0.5723`.

The family also shows why fidelity is not purely a local property: a tiny rounding error can be harmless in one step and consequential after repeated accumulation.

## Cross-family conclusion

Both universal policies lose for different reasons:

`uniform low fidelity -> cheap but decision-sensitive/accumulated approximation errors become costly`

`uniform high fidelity -> accurate but spends exact computation where it cannot change the decision`

The surviving rule is:

> **Allocate fidelity according to decision sensitivity, uncertainty propagation, consequence and recoverability. Use cheap approximate state while its plausible error cannot change enough downstream value; escalate or rematerialize higher fidelity when that condition fails.**

This links PS-001 typed representation, PS-005 value-of-computation, PS-012 recoverable optionality and PS-014 consequence-sensitive assurance without collapsing their authority semantics into numerical precision.

## Proposed principle

**Value/sensitivity-scaled fidelity allocation.**

Fidelity is a resource dimension. Approximation is acceptable only while its bounded/estimated effect on downstream decisions remains below the value of the additional precision required to resolve it.

This does not select a numeric format, quantizer, mixed-precision library, neural precision schedule or hardware architecture.

## Falsifiers

- precision-switching/replay overhead exceeds saved arithmetic or memory traffic;
- approximation error is too poorly bounded for adaptive fidelity to know when escalation is needed;
- low-frequency catastrophic errors dominate expected-utility estimates and require uniformly exact computation in a domain;
- hardware executes uniform high precision more efficiently than mixed/adaptive control once batching/vectorization is included;
- retained source evidence needed for rematerialization costs more than always-high state;
- approximation changes learning dynamics or representation geometry in ways not captured by local decision error.
