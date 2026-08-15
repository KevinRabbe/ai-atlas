# I28A — Direction-Aware Generic Evidence Aggregation

**Status:** implemented PS-026 integration discriminator. No new provisional principle.

## Question

I27 closes record-count inflation for symmetric/common-mode failure groups.

I26B shows a remaining loss: an upstream source and its derived children can share failures while the children still retain independent correction paths.

A symmetric group answers:

```text
these records share a failure mode
```

but cannot answer:

```text
is this child agreement merely inherited,
or did the child depart from upstream and create new evidence?
```

I28A asks what minimum aggregation semantics preserve that marginal evidence.

## Environment

Five sources:

- `A`: upstream source, error `0.25`;
- `B`, `C`: derived children;
- `D`: independent source, error `0.18`;
- `E`: independent source, error `0.22`.

Each child:

- copies A with probability `0.60`;
- independently re-checks with probability `0.40`;
- when re-checking, error is `0.03`.

Only 12% of claims later receive independent resolution. Source quality, conditional child behavior and derivation direction are therefore learned online rather than supplied as hidden labels to the learned policy.

## Policies

### `independent_quality`

Uses learned individual source quality but treats all five observations as independent.

### `symmetric_group`

Analogue of the current generic effective-group aggregator:

- A/B/C become one common-mode group;
- D and E remain independent groups;
- one best-quality resolving source represents A/B/C.

This avoids record-count inflation but discards derivation direction.

### `inheritance_discount`

Keeps all sources but gives every child a fixed reduced weight because it is derived.

This tests the tempting rule:

> derived evidence always contributes less.

### `novelty_weighted`

Uses directional provenance conditionally:

- child agrees parent -> strong inherited-agreement discount;
- child departs parent -> full child contribution.

No conditional generative model is learned.

### `learned_directional`

Uses `EvidenceDerivationModel` to infer A->B and A->C from resolved outcomes.

Once direction is established, it also learns child correctness conditioned on whether the parent was correct:

```text
P(child correct | parent correct)
P(child correct | parent wrong)
```

and uses those conditional likelihoods with independently learned A/D/E quality.

Before derivation direction is sufficiently supported, it falls back to symmetric grouping rather than manufacturing direction.

### `oracle`

Uses the exact hidden generative probabilities.

It is an information ceiling, not a candidate implementation.

## Approximate 30-seed result

12,000 tasks/seed; late metrics begin after task 4,000.

| policy | error rate | Brier | utility/task | child-departure error |
|---|---:|---:|---:|---:|
| independent quality | ~0.139 | ~0.106 | ~1.67 | ~0.257 |
| symmetric group | ~0.091 | ~0.075 | ~2.39 | ~0.162 |
| fixed inheritance discount | ~0.114 | ~0.084 | ~2.05 | ~0.279 |
| **novelty weighted** | **~0.082** | ~0.066 | **~2.51** | ~0.114 |
| learned directional | ~0.094 | **~0.068 lifetime** | ~2.35 | **~0.101** |
| oracle | ~0.074 | ~0.059 | ~2.65 | ~0.064 |

The learned conditional policy pays an early learning cost. Its late-horizon behavior is more informative:

| policy | late error | late Brier | late child-departure error |
|---|---:|---:|---:|
| symmetric group | ~0.091 | ~0.075 | ~0.160 |
| novelty weighted | **~0.080** | ~0.066 | ~0.101 |
| **learned directional** | ~0.083 | **~0.062** | **~0.065** |
| oracle | ~0.074 | ~0.059 | ~0.064 |

The learned derivation model establishes both A->B and A->C after roughly 650 tasks on average in the prototype; the observed maximum across the 30-seed sweep remained below 1,000 tasks.

## What this falsifies

### `derived source -> fixed discount`

False in this family.

A child that merely repeats upstream should add little. The same child can become highly informative precisely when it disagrees upstream.

The fixed child discount performs particularly badly on departure cases because it discounts the correction too.

### `shared failure family -> collapse to one source`

Also incomplete.

Symmetric collapse is substantially safer than independent record counting, but it cannot preserve where novel evidence originated.

## Architecture implication

The marginal value of derived evidence depends on **relation + observation state**:

```text
parent -> child

child == parent
    -> likely inherited consistency
    -> low marginal evidence

child != parent
    -> possible independent transform/check/correction
    -> potentially high marginal evidence
```

So generic evidence aggregation needs more than:

```text
source quality
+ symmetric failure group
```

when directional derivation exists.

It needs enough directional state to distinguish inherited agreement from source-originated novelty.

## Why no aggregator is selected yet

The simple novelty heuristic has the best lifetime decision error in this specific family.

The learned conditional model has better late probability calibration and nearly oracle-level late performance specifically on child departures.

The oracle remains materially better overall.

Therefore I28A does **not** justify selecting:

- fixed novelty weights;
- conditional likelihood tables;
- Bayesian networks;
- a particular derivation graph representation.

It only establishes the semantic need to preserve conditional marginal evidence through derivation.

## PS-026 refinement

PS-026 now means that evidence relation state can affect not just **how many independent groups exist**, but **how each observation changes the claim relative to its upstream evidence**.

Direction matters when derivation creates this asymmetry.

## Next discriminator

I28B should test multi-hop derivation:

```text
A -> B -> C
```

Local edge semantics may or may not compose safely.

Questions:

- if C agrees A but differs B, what evidence is actually new?
- does local parent-child discounting double-count or erase information?
- is stable root/source provenance needed across the full path?
- can a downstream correction survive multiple inherited transformations?

That experiment determines whether pairwise directional edges are enough or whether evidence needs path-level provenance.
