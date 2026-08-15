# I26B — Directional Evidence Dependence / Derivation

**Status:** implemented PS-026 refinement. No new provisional principle.

## Question

I24–I26A represent shared failure ancestry mostly as a symmetric relation.

That is not sufficient for derived/copy evidence.

If source B usually copies source A but sometimes performs an independent correction, the relation is directional:

```text
A -> B
```

B inherits many of A's failures, but A does not inherit failures originating only in B.

The important epistemic asymmetry is:

```text
A agrees B      -> often inherited agreement; little marginal evidence
B disagrees A   -> possible independent correction; potentially high marginal evidence
```

An undirected `same lineage` bit cannot represent that difference.

## Environment

Four stable visible sources:

- `A`: upstream/base source, error probability `0.25`;
- `B`, `C`: derived sources;
- `D`: independent comparator, error probability `0.18`.

Each child B/C:

- copies A with probability `0.60`;
- independently re-checks with probability `0.40`;
- when re-checking, has error probability `0.03`.

So child errors are largely inherited from A, but the children sometimes repair A's mistakes.

A subset of claims later receives sufficiently independent resolution. The learned-direction policy receives only those outcomes, not the hidden derivation graph.

## Policies

### `record_count`

Counts A/B/C/D as four votes, with D breaking 2:2 ties.

### `symmetric_lineage`

Collapses A/B/C into one undirected lineage and compares that group with D.

This correctly refuses to count copied agreement as three independent votes but loses **where disagreement originated**.

### `directional_provenance`

Knows A is upstream of B/C and uses a simple provenance-aware rule:

- both children independently depart from A -> trust the shared child correction;
- exactly one child departs from A -> use independent D;
- both children agree A -> use A because the agreement is largely inherited.

### `learned_direction`

Starts with record-count aggregation. `DirectionalDependenceEstimator` learns directional error inheritance from resolved outcomes.

For candidate `parent -> child`, it asks whether:

1. child errors are disproportionately contained inside parent errors; and
2. parent is measurably less accurate than child, consistent with a child that can repair upstream mistakes.

Once both `A -> B` and `A -> C` are established, the policy uses the directional rule.

### `oracle`

Uses the exact generative probabilities and Bayesian likelihood for each observation pattern.

## Approximate 30-seed result

12,000 tasks/seed:

| policy | error rate | weighted harm/task | utility/task | error when child departs from A |
|---|---:|---:|---:|---:|
| record count | ~0.1249 | ~0.469 | ~1.867 | ~0.1792 |
| symmetric lineage | ~0.1813 | ~0.679 | ~1.028 | ~0.1792 |
| **directional provenance** | **~0.1184** | **~0.446** | **~1.960** | **~0.1419** |
| **learned direction** | **~0.1187** | **~0.447** | **~1.956** | **~0.1438** |
| Bayesian oracle | ~0.1116 | ~0.421 | ~2.062 | ~0.1031 |

The learned model typically establishes both A->B and A->C after roughly 600–700 tasks under 12% passive resolution; across a 100-seed prototype the 90th-percentile establishment time was below ~925 tasks.

The oracle gap is useful: direction is not the whole inference problem. It preserves important provenance information but does not replace calibrated probabilistic reasoning.

## Why symmetric lineage loses

The symmetric model correctly recognizes that A/B/C do not provide three independent failure modes.

But it then compresses away the relation that matters when one source changes its mind:

```text
A ---------> B
 \
  ---------> C

A=B=C   : inherited consistency
B!=A    : B may have generated new evidence
C!=A    : C may have generated new evidence
```

A cluster ID says only that the sources are related. It does not say which direction information and errors flow.

## Reusable architecture change

`EvidenceDerivationModel` is now separate from `EvidenceDependenceModel`.

### `EvidenceDependenceModel`

Represents symmetric/common failure ancestry and effective independence.

### `EvidenceDerivationModel`

Represents directional inheritance/derivation:

- parent -> child error inheritance;
- context-specific direction;
- inferred parent;
- directional children.

Neither model decides truth or grants epistemic authority.

Keeping them separate avoids an attractive but incorrect simplification:

```text
all evidence dependence = one undirected graph
```

## PS-026 refinement

PS-026 now has two relational forms:

1. **shared/common-mode dependence** — source observations may fail together;
2. **directional derivation/inheritance** — one source may inherit evidence/errors from another while retaining some independent correction path.

Evidence assurance should preserve whichever distinction changes marginal evidence value.

This is still a refinement of PS-026, not PS-027.

## Remaining falsifiers

- a child that adversarially hides copying by selectively disagreeing;
- multi-hop derivation A -> B -> C;
- cycles/mutual adaptation rather than acyclic derivation;
- direction that changes by claim domain or over time;
- sparse resolved outcomes where observational direction inference becomes unreliable;
- cases where explicit provenance is cheaper/more reliable than behavioral inference.

The next planned stress is adversarial **apparent independence**: correlated/derived sources intentionally decorrelate visible errors so passive dependence learning underestimates shared ancestry.
