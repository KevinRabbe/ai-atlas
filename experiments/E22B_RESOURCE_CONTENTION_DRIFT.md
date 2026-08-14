# E22B — Cross-Resource Capacity Contention + Quality Drift

**Status: implemented, tested and swept.**

## Purpose

E22 showed that a system should substitute among memory, compute, observation and verification as their prices change. E22B adds two complications that make resource decisions genuinely coupled:

1. many tasks compete for scarce resource slots at the same time;
2. the actual competence/quality of each resource changes after deployment.

The question is whether local adaptation, joint capacity allocation, or both are required.

## Setup

Each round contains 12 heterogeneous tasks. Available slots are limited to:

- memory: 3;
- compute: 3;
- observation: 2;
- verification: 2.

All policies start calibrated to regime 0. Resource quality then changes twice. Current prices are visible to every policy, so E22B isolates **capacity coupling + quality drift** rather than repeating E22's stale-price test.

Compared variants form a 2×2 factorial:

- `frozen_independent` — stale quality model + capacity-blind task-local choices;
- `adaptive_independent` — learns chosen-resource quality but tasks still choose independently;
- `frozen_joint` — capacity-aware joint allocation but stale quality model;
- `adaptive_joint` — capacity-aware allocation + online quality adaptation.

Joint allocation pays an explicit four bid/message-equivalents per measured task.

## Validation

**4/4 E22B tests pass locally**:

- capacity-aware allocation reduces initial contention regret;
- quality adaptation improves post-drift joint regret;
- joint adaptation beats capacity-blind local adaptation after drift;
- coordination/message cost is reported explicitly.

## 30-seed sweep

Each cell reports `actual utility / reference regret / unserved rate` per task.

| policy | regime 0 | regime 1 | regime 2 | post-shift mean regret |
|---|---|---|---|---:|
| frozen independent | 0.731 / 0.218 / 0.326 | 0.455 / 0.379 / 0.292 | 0.428 / 0.395 / 0.296 | 0.387 |
| adaptive independent | 0.684 / 0.265 / 0.383 | 0.416 / 0.419 / 0.582 | 0.303 / 0.518 / 0.699 | 0.468 |
| frozen joint | 0.952 / 0.000 / 0.264 | 0.624 / 0.207 / 0.239 | 0.622 / 0.204 / 0.209 | 0.206 |
| **adaptive joint** | **0.903 / 0.042 / 0.294** | **0.781 / 0.052 / 0.407** | **0.704 / 0.121 / 0.474** | **0.086** |

The reference is a capacity-respecting assignment using the true current resource qualities, evaluated with the same greedy assignment rule. It is an experimental reference frontier, not a claim of globally optimal scheduling.

## Important failure mode

`adaptive_independent` is worse than `frozen_independent` after drift despite learning fresher local quality estimates.

Why: as a resource becomes attractive, many individually rational tasks rush toward it. Capacity fills in arrival order and other useful substitutions are missed. Better local preference estimates can therefore **increase contention** when allocation remains uncoordinated.

This is a direct systems-level example of the distinction between:

- learning local value;
- allocating across substitutes;
- coordinating shared scarcity.

## Interpretation

E22 + E22B jointly support a narrow principle:

> resource allocation should account for substitute operations jointly when their prices, competence or shared capacities change; local policies remain appropriate only while their choices are not materially coupled through common scarcity.

The exact centralized greedy allocator is not selected. A distributed/resource-local auction could implement the same coupling-scoped rule if it achieves comparable utility after communication/latency cost.

## Limits

- four fixed resource classes;
- simple EMA quality learning;
- known current prices;
- synthetic task values;
- no queues or deferred execution;
- no learned resource creation/removal.

The next generation should test the same principle with learned resource discovery and delayed/queued capacity rather than treating the resource menu as fixed forever.
