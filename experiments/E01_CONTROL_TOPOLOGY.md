# E01 — Hierarchical vs Distributed Operation Allocation

**Status:** first model-free implementation; preliminary multi-seed evidence only.

## Question

Does explicit global/hierarchical metacontrol justify its dispatch/serialization cost, or can local event-driven policies allocate operations more cheaply without losing task coherence?

## Synthetic task model

Each task exposes noisy local cues for four possible operations: retrieve, verify, observe and search. The hidden task state determines which operations are actually required. Operations can also have prerequisite edges. Dependency graphs are acyclic and their density is manipulated directly.

All policies receive the same cues, prices and dependency graph.

## Variants

### `hierarchical_global`

A central allocator reads all cues, selects candidate operations with the same cue/price threshold used by local policies, computes full prerequisite closure and dispatches selected operations. This buys globally coherent dependency handling but pays explicit centralized decision and dispatch cost.

### `distributed_r1`

Each operation makes its own local activation decision. Active operations can request prerequisites across one communication round. This minimizes central coordination but cannot resolve dependency chains deeper than its communication horizon.

### `distributed_r3`

Same local mechanism, but up to three dependency-propagation rounds are allowed. This tests whether local control can recover global coherence by spending additional messages rather than installing a global controller.

## Measured

Success rate; utility; selected operations; missed/unnecessary escalations; messages; logical operations; tail failure rate on highly coupled tasks.

## Preliminary 12-seed result

Each seed uses 1,000 tasks.

| dependency density | hierarchical success | distributed r1 | distributed r3 | hierarchical msgs/task | r1 msgs/task | r3 msgs/task |
|---:|---:|---:|---:|---:|---:|---:|
| 0.04 | 0.788 | 0.787 | 0.788 | 1.559 | 0.062 | 0.063 |
| 0.35 | 0.817 | 0.773 | 0.817 | 2.055 | 0.545 | 0.599 |
| 0.72 | 0.847 | 0.779 | 0.847 | 2.522 | 1.109 | 1.194 |

This is a crossover rather than a winner: sparse/local problems let distributed control match task success with dramatically less communication; one-round local coordination degrades as dependency chains become denser; extra local message rounds recover the hierarchical success rate in this toy environment while remaining cheaper in message count.

## What this does not establish

It does not prove that three local rounds dominate a hierarchical controller. Tasks are small, communication latency is logical rather than hardware-measured, and the benchmark has not yet been repeated on a structurally different allocation problem.

No Phase-9 design-ledger choice should be promoted from this result yet.

## Next discriminators

Vary communication latency/price independently of operation price; introduce asynchronous/stale local state; use a second allocation task family; compare learned allocation policies after the deterministic benchmark is understood.
