# I26D — Large-Population Evidence-Dependence Scale

**Status:** implemented PS-026/PS-003/PS-012 composition stress. No new provisional principle.

## Question

PS-026 makes evidence dependence first-class relational state.

That creates an obvious scaling danger:

```text
N visible sources
      ↓
N(N-1)/2 possible pair relations
```

At 128 sources there are already 8,128 possible pairs.

I26D isolates the **state/resource economics** from the inference problem by assuming an exact provenance/dependency diagnostic is available at a price.

The question is:

> **Should the organism materialize the whole exact dependence graph, repeatedly query only active relations, or cache/expire only relation state that actually enters assurance decisions?**

## Environment

- 128 stable source identities;
- hidden groups of four sources share a relation;
- each decision uses only four sources, therefore six pair relations;
- 55% of panels contain one coupled source pair;
- the active 32-source pool changes halfway through the run;
- relation diagnostics are exact but cost `0.015` per queried pair;
- carrying one relation record costs `0.00002` per task;
- false independence on an active dependent pair incurs consequence-scaled assurance harm.

This is deliberately not another learning benchmark. It asks whether a dependence relation that can be known exactly is worth keeping globally.

## Policies

### `assume_independent`

Carries no relation state and pays harm when an active pair is actually dependent.

### `dense_exact`

Preloads all 8,128 possible pair relations and carries them for the full run.

### `query_every_time`

Carries no persistent relation graph but pays the exact diagnostic for all six active pairs on every task.

### `cache_forever`

Queries a relation only on first use and retains it forever.

### `scoped_ttl`

Queries on first use, refreshes active relation entries, and expires relations that have not participated in an assurance decision for 500 steps.

## Approximate 30-seed result

10,000 tasks/seed:

| policy | utility/task | relation cost/task | assurance harm/task | final relation state |
|---|---:|---:|---:|---:|
| assume independent | ~0.657 | 0 | ~0.343 | 0 |
| dense exact | ~0.825 | ~0.175 | 0 | 8,128 |
| query every time | ~0.910 | ~0.090 | 0 | 0 |
| cache forever | ~0.984 | ~0.016 | 0 | ~992 |
| **scoped TTL** | **~0.988** | **~0.012** | **0** | **~495** |

The active scoped cache therefore carries only about 6% of the full possible relation graph at the end of the run.

## Crossover

The TTL result is not universal.

When relation storage is deliberately made free, permanent caching can beat TTL because repeated diagnostics become the dominant cost.

So the result is not:

> `always expire relation state`

It is:

> **Carry dependence state only while expected reuse/assurance value exceeds acquisition + storage + staleness cost.**

That is the same resource law already observed for predictive/hot state, but now reproduced for evidence relations.

## Architecture consequence

PS-026 should not imply a universal dense source-dependence graph.

Dependence state can be:

- exact and durable when provenance is stable and frequently reused;
- learned and approximate when ancestry is inferred behaviorally;
- scoped by claim domain/context;
- materialized only for active/coupled evidence sets;
- expired/rematerialized when relation carrying cost exceeds expected reuse.

This composes directly with:

- PS-003 coupling-scoped coordination;
- PS-012 recoverable optionality;
- PS-014 value-priced assurance;
- PS-026 learned/causally-qualified dependence.

## I26 conclusion so far

The four I26 stresses now establish that evidence dependence can be:

1. **domain conditional** — I26A;
2. **directional/derived** — I26B;
3. **selectively hidden under distribution shift** — I26C;
4. **too large to materialize densely** — I26D.

The next integration step is to let the common evidence/assurance path combine:

- exact lineage/provenance where genuinely known;
- learned effective dependence where unknown;
- explicit unresolved dependence when neither is sufficient.
