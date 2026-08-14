# E18 — Execution Timing: Global Ticks vs Event-Scoped Work vs Consistency Barriers

**Status:** implemented and tested. Two structurally different families support a narrow DL-018 promotion.

## Question

Should an intelligent system advance all components on a common synchronous schedule, execute only where state changes/events occur, or mix event-driven work with explicit synchronization boundaries?

The implementation-neutral question is:

> **How far can execution remain local and event-triggered before shared consistency requirements make synchronization worth its idle-work/latency cost?**

## Family A — sparse event graph

80 nodes receive three local external events per step. Each event invalidates the source plus two dependent nodes. Every step queries a sample of the graph.

Variants:

- `sync_global` — recompute all 80 nodes every step;
- `async_naive` — update only event sources; missed downstream invalidations are discovered lazily after stale reads;
- `scoped_event` — propagate the event through its actual dependency scope and recompute only affected nodes.

### 30-seed result

| variant | net utility/step | stale-read rate | operations/step | messages/step |
|---|---:|---:|---:|---:|
| sync global | 0.8560 | **0.0000** | **80.000** | 0.000 |
| async naive | 0.6671 | 0.2681 | **6.217** | 0.000 |
| **scoped event** | **0.9815** | **0.0000** | 8.699 | 5.699 |

Global ticking is correct but spends almost an order of magnitude more compute on unchanged nodes. Naive async is cheap but loses dependency consistency. Scoped event propagation preserves correctness while paying only for the changed dependency cone.

## Family B — version-coupled global snapshot

48 components share a logical configuration version. Updates arrive more frequently than globally consistent snapshots are requested. A query is valid only if all materialized components belong to the same current version.

Variants:

- `sync_global` — eagerly materialize every new version across all 48 components;
- `async_naive` — deliver a new version to only a subset of components and allow queries immediately;
- `scoped_event` — retain the new logical version cheaply, coalesce intermediate updates, and synchronize the full consistency scope only when a global snapshot is requested.

At the default 55% update rate and 30% query rate:

| variant | net utility/step | inconsistent-query rate | operations/step | messages/step |
|---|---:|---:|---:|---:|
| sync global | 0.2513 | **0.0000** | 26.492 | **0.000** |
| async naive | -0.3675 | 0.9991 | **4.417** | 4.417 |
| **scoped event + barrier** | **0.2624** | **0.0000** | **11.565** | 12.117 |

The scoped barrier remains exact while coalescing several updates into one materialization. About 0.806 barriers are required per query in this regime.

## Synchronization-frequency crossover

The event-scoped policy is not universally better. When globally consistent snapshots are requested almost continuously (`query_probability = 0.90`), the barrier must run so often that eager synchronization becomes cheaper:

- sync global: ~`0.8508` utility/step;
- scoped event + barrier: ~`0.8202`.

At query probability `0.10`, event-scoped execution is substantially cheaper (`~0.0815` vs `~0.0474`), and at `0.30` it still wins slightly (`~0.2624` vs `~0.2513`).

## Cross-family conclusion

The two families reject both universal extremes:

`always synchronous -> correct but wastes work when coupling is sparse/intermittent`

`always asynchronous -> cheap but can expose stale or mixed-version state`

The surviving rule is:

> **Execute on state-changing events while dependency/consistency scope is local; introduce synchronization only across the scope and at the time where a common version/barrier is actually required. If shared-consistency demand becomes continuous, eager synchronization can again be rational.**

This is a timing form of the broader Atlas result that scope follows coupling.

## Proposed principle

**Event-scoped execution with consistency-triggered synchronization.**

Execution timing should be determined by state change and dependency locality rather than a universal global clock. Synchronization/barriers are explicit priced operations whose scope/frequency expands with consistency coupling.

This does not select threads, actors, event loops, distributed systems, lockstep simulation or Phase-9 family B.

## Falsifiers

- event bookkeeping/message overhead erases sparse-work savings on realistic workloads;
- dependency propagation is too uncertain, causing hidden stale state that global ticks avoid;
- hardware/vectorization makes batch synchronous processing cheaper than sparse event dispatch despite idle logical work;
- barrier discovery itself requires global coordination as expensive as eager synchronization;
- asynchronous ordering creates nondeterminism/credit/provenance failures that dominate compute savings.
