# E22 — Cross-Resource Metacontrol Under Changing Economics

**Status:** first E22 family; preliminary 30-seed evidence.

## Question

Can a system learn which computational/resource substrate is useful for a task and then **substitute among resources when their prices change**, rather than optimizing compute, memory, observation and verification independently?

## Resources

Four resource classes are represented:

- memory;
- internal compute;
- new observation;
- high-confidence verification.

There are four visible task types and three task-value levels. Each resource has an unknown task-type-dependent reliability. Policies learn those reliabilities only from outcomes of resources they actually use.

The environment has three price regimes. Resource competence stays fixed while economics change:

1. memory/compute inexpensive; observation and verification expensive;
2. observation becomes cheap while memory becomes expensive;
3. verification becomes cheap enough to compete on high-value tasks.

All policies receive 1,000 warm-up tasks in regime 0, then 2,000 measured tasks per price regime.

## Policies

- `adaptive_cross_resource` — one learned quality table plus current resource prices; chooses the highest estimated expected utility with small exploration.
- `frozen_initial_economics` — learns the same quality information but continues scoring resources with regime-0 prices after economics change.
- `resource_local_bids` — each resource owns the same local quality estimate and sends a current-price bid to an arbiter. It therefore represents explicit resource-local state + coordination rather than one shared table.

No policy receives the hidden reliability matrix.

## 30-seed means

### Regime 0 — original economics

Adaptive and frozen policies are intentionally equivalent: mean expected utility ~0.874 and regret ~0.081. Adaptive choices are roughly 56.5% memory, 38.5% compute, 4% observation and 1% verification.

### Regime 1 — observation becomes cheap

| policy | accuracy | spend/task | regret | expected utility |
|---|---:|---:|---:|---:|
| adaptive | 0.866 | 0.534 | **0.038** | **0.858** |
| frozen economics | 0.843 | 1.030 | 0.619 | 0.277 |
| resource-local bids | 0.866 | 0.534 | **0.038** | **0.858** |

Adaptive resource mix becomes ~6% memory, 16% compute, **77% observation**, 1% verification.

### Regime 2 — verification becomes cheap

| policy | accuracy | spend/task | regret | expected utility |
|---|---:|---:|---:|---:|
| adaptive | 0.903 | 0.718 | **0.026** | **0.816** |
| frozen economics | 0.848 | 0.869 | 0.391 | 0.451 |
| resource-local bids | 0.903 | 0.718 | **0.026** | **0.816** |

Adaptive resource mix becomes ~18% memory, 23% compute, 26% observation and **33% verification**.

Mean post-shift regret is therefore ~0.032 for adaptive metacontrol versus ~0.505 for frozen resource economics.

## Coordination result

`resource_local_bids` produces the same resource choices/quality as the shared adaptive controller in this benchmark, but pays about **4.84 messages per task** and ~7.68 logical controller operations per measured task versus no explicit messages and ~4 controller operations for the compact shared implementation.

This is not evidence that centralized state is universally better. It shows that if resource knowledge is already tiny and colocated, explicit distribution only adds overhead; E01/E01B already show regimes where locality removes much larger communication costs.

## Cross-domain implication

The result supports the Atlas organizing hypothesis at a higher level: intelligence is not only "how much inference compute?" but **which resource should be spent at all**. Resource prices and expected usefulness can change the best operation without changing the underlying task.

## Design-ledger implication

- DL-022 gains direct evidence that cross-resource allocation should respond to substitution/current economics rather than fixed independent budgets, but this is only one task family and should not yet be selected.
- Combined with E01/E01B, E22 completes the originally specified decisive evidence for DL-001's narrow principle: coordination scope should track coupling/resource scope instead of being globally centralized or universally local.

The next E22 family should add simultaneous capacity contention and resource-quality drift so a controller must trade information acquisition, task value and shared scarcity at once.
