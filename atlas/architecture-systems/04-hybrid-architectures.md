# Hybrid and Heterogeneous Architectures

## Required function

Compose different information-processing mechanisms when no single operator dominates across capability, state, latency, memory and hardware efficiency.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-HY-01 | Griffin combines local attention with gated linear recurrence and reports Transformer-competitive quality with better inference characteristics in evaluated regimes. | O | E2 | AS-S014 |
| AS-HY-02 | Jamba interleaves Transformer attention, Mamba-style state-space layers and MoE, demonstrating large-scale viability of a heterogeneous stack. | O | E2 | AS-S015 |
| AS-HY-03 | Kimi Linear reports a hybrid of linear attention and MLA that outperforms its matched full-MLA baseline while sharply reducing long-context KV-cache usage in its experiments. | O | E2 | AS-S017 |
| AS-HY-04 | Modern linear/recurrent work repeatedly retains some direct/local attention because bounded state and direct retrieval have complementary strengths. | I | E3 | AS-S014, AS-S015, AS-S017, AS-S018 |
| AS-HY-05 | Hardware-efficient architecture depends on operator mix: an asymptotically cheaper operator can still underutilize accelerators, while strategically retaining dense kernels can improve realized performance. | I | E3 | AS-S013, AS-S016, AS-S027, AS-S028, AS-S029 |

## Why hybrids matter conceptually

The evidence does **not** establish that today's hybrid recipes are optimal. It establishes something more useful: architectural functions need not be implemented by one homogeneous repeated block.

Potentially separable functions include:

- local pattern processing;
- exact/content-addressed retrieval;
- compressed temporal state;
- long-term writable memory;
- conditional specialist computation;
- iterative reasoning;
- routing/control.

If these functions have different computational requirements, forcing them into one operator may be an accidental constraint.

## Danger: architecture soup

Hybridization is not automatically good. Adding mechanisms can increase:

- optimization interference;
- kernel fragmentation;
- state-management complexity;
- synchronization;
- compiler/runtime complexity;
- difficulty attributing failures.

Each component must earn its role through a distinct required function and measurable Pareto improvement.

## Clean-sheet restatement

Prefer **functional heterogeneity with explicit interfaces** over named-block heterogeneity. Start from required operations and only then choose whether multiple mechanisms are justified.

## Discriminating experiments

1. Under fixed training/inference cost, ablate each operator family and measure which task properties lose capability.
2. Replace a hybrid component with extra capacity of another component to distinguish function from mere parameter count.
3. Measure system-level utilization and bytes moved, not only validation loss.
4. Test whether the optimal mixture changes with hardware, sequence length and workload latency target.

## Failure modes

Cargo-cult layer mixing; duplicated capability; cross-module representation mismatch; performance hidden by unequal training budgets; architecture tuned to one accelerator generation.