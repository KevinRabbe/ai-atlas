# E01B — Control Topology Under Shared Resource Contention

**Status:** second E01 task family; 20-seed preliminary follow-up.

## Why a second family

The first E01 benchmark uses dependency graphs. A control-topology conclusion should not survive merely because one representation of coupling favors it, so E01B removes prerequisite chains entirely and introduces a different coupling source: many independent tasks competing for a scarce verification resource.

Each task has a value, an estimated probability that its unverified answer is already correct, and a hidden realized correctness. Verification guarantees correctness but only a fixed number of tasks per batch can receive it.

## Policies

- `hierarchical_batch` — globally ranks expected verification gain and dispatches the scarce slots.
- `distributed_threshold` — tasks independently request verification; excess requests consume capacity in arrival order.
- `distributed_resource_auction` — tasks send local bids to the scarce resource, which arbitrates only that resource rather than installing a universal executive.

## 20-seed means

| verification slot fraction | policy | weighted correctness | allocation efficiency vs oracle | messages/task |
|---:|---|---:|---:|---:|
| 0.05 | hierarchical | 0.769 | 1.000 | 0.042 |
| 0.05 | local threshold | 0.754 | 0.483 | 0.706 |
| 0.05 | resource auction | 0.769 | 1.000 | 0.998 |
| 0.20 | hierarchical | 0.856 | 1.000 | 0.208 |
| 0.20 | local threshold | 0.811 | 0.613 | 0.706 |
| 0.20 | resource auction | 0.856 | 1.000 | 1.164 |
| 0.80 | hierarchical | 0.989 | 1.000 | 0.792 |
| 0.80 | local threshold | 0.978 | 0.959 | 0.706 |
| 0.80 | resource auction | 0.989 | 1.000 | 1.748 |

## Interpretation

The second family supports the same narrow pattern as dependency E01 without requiring the same architecture: **coordination becomes valuable when decisions are coupled through a shared constraint**.

Importantly, the resource-local auction matches the global allocator's selection quality in this benchmark. This is evidence against the false binary `global executive OR uncoordinated local agents`.

A stronger working hypothesis is now:

> coordination scope should track the scope of coupling: local where interactions are sparse, resource/domain-local where contention is localized, and broader only when dependencies themselves are broad.

This is still not a DL-001 selection because E22 must test whether the principle survives simultaneous substitution among different resource types and learned allocation policies.
