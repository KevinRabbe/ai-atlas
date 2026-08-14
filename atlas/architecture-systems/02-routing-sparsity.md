# Conditional Computation, Routing and Sparsity

## Required function

Allocate expensive computation to the parts of a model/system most useful for the current input while allowing total stored capacity to exceed active computation.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-RS-01 | Sparse mixture-of-experts can increase total parameter capacity without proportional per-token arithmetic. | O | E4 | AS-S020, AS-S021, AS-S022 |
| AS-RS-02 | Expert granularity, shared experts and routing strategy materially affect specialization and quality. | O | E3 | AS-S020, AS-S021 |
| AS-RS-03 | Routing introduces load-balance and execution problems that can erase theoretical sparse-compute gains. | O | E4 | AS-S022, AS-S023, AS-S024 |
| AS-RS-04 | Hardware-aware sparse kernels can preserve dynamic routing without padding or token dropping and substantially improve realized throughput. | O | E3 | AS-S023 |
| AS-RS-05 | End-to-end sparse efficiency depends on mapping semantic routing to physical expert placement, communication and parallelism. | I | E4 | AS-S022, AS-S024 |

## Key distinction

There are at least three different routing problems:

1. **semantic routing** — which capability should process this information?
2. **compute-budget routing** — how much work is worth spending on it?
3. **physical routing** — where can that computation execute without creating communication or load bottlenecks?

Current MoE systems often couple these implicitly. A clean-sheet system should not assume they have the same optimum.

## Capacity is not free

Sparse activation reduces arithmetic but creates costs in:

- routing decisions;
- expert parameter storage;
- token permutation/dispatch;
- inter-device all-to-all traffic;
- load imbalance and stragglers;
- fragmented/small matrix operations;
- replicated shared experts or hot experts.

Therefore `total parameters / active parameters` is not an adequate efficiency measure.

## Beyond experts

Conditional computation can apply to more than FFN experts:

- attention heads or memory mechanisms;
- depth/number of recurrent steps;
- precision;
- external tools/models;
- verification effort;
- retrieval amount;
- simulation/search branches.

MoE is evidence for the broader principle, not the final form of routing.

## Clean-sheet restatement

The substrate should support **input-dependent activation of capabilities under an explicit resource budget**, while keeping semantic selection distinct from physical scheduling where possible.

## Discriminating experiments

- Compare fixed active FLOPs with varying routing granularity and communication topology.
- Measure quality, tail latency, bytes moved and idle device time—not just token-average FLOPs.
- Test whether learned semantic specialization remains beneficial when experts are dynamically relocated or replicated by the runtime.

## Failure modes

Expert collapse; redundant experts; hot experts; dropped tokens; router instability; communication domination; routing based on superficial features; specialists that fail outside their training niches.