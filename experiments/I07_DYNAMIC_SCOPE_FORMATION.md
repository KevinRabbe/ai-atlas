# I07 — Dynamic Scope Formation from a Changing Dependency Graph

**Status:** implemented topology-level composition experiment. No new provisional principle is added; I07 tests PS-003/020/021/022 at architecture scale.

## Question

AF03 still receives four predefined subsystem boundaries.

I07 removes those boundaries. The system receives a noisy interaction stream over twelve components and must infer:

- which components should stay local;
- which should share a coordination scope;
- when a scope should split;
- when several scopes should merge;
- whether the expected benefit of reorganization exceeds migration cost.

The system is never shown the true partition.

## Environment

Twelve nodes move among three recurring hidden dependency partitions, each containing three four-node coupling groups.

For every node pair:

- if they are truly coupled, an interaction event occurs with probability `0.65`;
- otherwise, an event occurs with probability `0.04`.

The adaptive system maintains decayed pairwise coupling evidence and periodically forms connected scopes from sufficiently supported edges.

The hidden partition changes repeatedly. Migration is explicitly priced when a node's scope membership changes.

## Policies

1. **global:** all nodes permanently share one scope;
2. **local:** every node stays isolated;
3. **fixed initial:** preserve the first correct three-scope partition forever;
4. **adaptive:** infer the coupling graph from noisy events and periodically split/merge scopes;
5. **oracle:** use the true current partition and pay the same migration price.

## Default 20-seed result

Six cycles, three recurrent partitions/cycle, 120 steps/partition:

| policy | utility/step | pairwise scope accuracy | migrations/run |
|---|---:|---:|---:|
| global | 1.0270 | 0.2727 | 0.0 |
| local | 0.8950 | 0.7273 | 0.0 |
| fixed initial | 0.9760 | 0.7273 | 0.0 |
| **adaptive** | **1.0583** | **0.9045** | ~39.1 |
| oracle | **1.0748** | 1.0000 | ~17.0 |

The learned topology closes most of the oracle gap and beats every static topology after migration cost.

It reorganizes more often than the oracle because noisy/lagging evidence creates extra corrections. That gap is real overhead, not hidden from the metric.

## Falsifier — topology plasticity also has a timescale

A targeted 10-seed duration sweep with default migration cost:

| hidden partition duration | global static | adaptive | adaptive - global |
|---:|---:|---:|---:|
| 20 | **1.0270** | 0.9842 | **-0.0428** |
| 80 | 1.0270 | **1.0500** | +0.0230 |
| 120 | 1.0270 | **1.0582** | +0.0312 |

When the graph changes every 20 steps, inference lag and migration dominate; the static global topology is better.

As structural persistence increases, adaptive scope formation earns its identification/migration cost.

This independently reproduces AF02's temporal result at the **topology** level:

> **plasticity should be allocated on a timescale where expected structural persistence exceeds evidence-acquisition, switching and migration cost.**

## Why global and local both fail in different ways

A permanent global scope captures every true dependency but also groups many unrelated pairs, paying interference/coordination cost.

Permanent local scopes avoid false grouping but miss every real cross-node dependency.

A fixed initially-correct partition becomes stale after the dependency graph reorganizes.

The adaptive topology attempts to preserve only the currently evidenced coupling scope.

## Emerging architecture rule

AF01–AF03 + I07 now suggest that architecture topology itself can be represented as revisable state:

```text
noisy interaction evidence
        |
estimated dependency graph
        |
value of grouping / separating
        |
current scopes
   |          |
 split      merge
   \          /
    migration cost
         |
 scoped organizational modes
```

This is more specific than "modular AI" or "distributed agents."

The boundary is conditional:

> **components should share organization only while their coupling/regularity makes the benefit of shared state/control greater than boundary, interference and migration cost.**

## Relation to existing principles

I07 does not need a new PS number because it composes existing rules:

- **PS-003:** coordination scope follows coupling;
- **PS-010:** shared resource coupling is jointly allocated;
- **PS-020:** change blast radius follows inferred causal scope;
- **PS-021:** shared structure earns itself from reusable regularity;
- **PS-022:** execution/synchronization scope follows consistency coupling.

What is new is the architecture-level composition: **scope membership itself becomes learned/revisable state.**

## Remaining gaps

I07 still simplifies several hard problems:

- every pair receives an observation opportunity each step;
- dependency evidence is symmetric and pairwise;
- scopes are disjoint rather than overlapping/nested;
- migration does not yet move real predictive/memory/authority state;
- no in-flight asynchronous work crosses a split/merge;
- authority/provenance constraints are not yet exercised during topology changes;
- graph edges are noisy but not adversarially spoofed.

## Next

The next integrated architecture checkpoint should put **real typed state** behind the dynamic topology:

1. memory/evidence ownership;
2. predictive state and source references;
3. resource arbitration;
4. authority versions;
5. in-flight event work;
6. regression evidence for structural changes.

A split/merge must then preserve those invariants rather than merely changing group labels.

That is the point where the Atlas can begin turning the current laws into an executable candidate architecture rather than another organizational benchmark.