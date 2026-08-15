# I27 — Learned Dependence Inside the Common Assurance Path

**Status:** implemented integration checkpoint. No new provisional principle.

## Why this integration was necessary

I24–I26 showed that evidence dependence can be unknown, scoped, directional, selectively hidden and expensive to materialize.

But the common recovery API still had two privileged assumptions:

1. every evidence source arrived with an exact lineage ID;
2. an external caller supplied `current_label` and `estimated_current_error` before lineage-aware assurance ran.

The second gap was especially dangerous. An upstream majority vote could count ten copied records as ten independent confirmations, convert them into `99.99% confidence`, and then hand that already-corrupted confidence to an otherwise correct lineage-aware assurance controller.

I27 closes both gaps.

## 1. Exact lineage is optional

`EvidenceLineageRegistry.register_source()` now accepts:

```text
source identity: required
exact lineage:   optional
```

Unknown source names are **not** counted as independent by default.

Without a learned model, multiple unknown sources remain in one conservative unresolved-dependence component.

With `EvidenceDependenceModel`, exact provenance and learned relations are combined:

- exact same lineage can never be split by behavioral learning;
- learned positive dependence can collapse otherwise distinct/unknown sources;
- learned independence separates unknown sources only after enough resolved observation support;
- an untrained below-threshold score remains `independence unresolved`, not `independent`.

`EvidenceSummary` now exposes both unknown and unresolved-dependence source counts.

## 2. Dependence confidence requires evidence support

The initial reusable model had a subtle bug:

```text
no history
→ covariance score near zero
→ below dependence threshold
```

That numerical result is not evidence of independence.

`EvidenceDependenceModel` now tracks decayed resolved-observation support. Relation confidence is:

```text
threshold-distance confidence
×
observation support
```

An explicit bounded probe can still set relation confidence to 1 for its validity window.

This prevents prior/default values from manufacturing independent evidence.

## 3. Effective evidence view

`EvidenceLineageRegistry.effective_view()` exposes the current non-stale records plus an effective source-group mapping after:

- exact lineage/provenance;
- learned dependence;
- context scope;
- minimum independence-confidence requirement;
- conservative unresolved dependence.

It remains non-owning and does not copy evidence payloads.

## 4. Binary evidence aggregation happens after grouping

`aggregate_binary_evidence()` combines one contribution per effective failure group.

Within one group:

- repeated/copy records do not multiply evidence;
- the lowest-error resolving source represents the group;
- equal-quality contradictory records leave that group ambiguous.

Across effective independent groups, the current small implementation uses source-error-weighted log odds.

This is an experimental aggregator, not a selection of Naive Bayes as the final epistemic calculus.

### Precision sanity check

If source error is 10%:

```text
4 copied agreeing records, one failure lineage
    -> estimate remains ~10% error

2 genuinely independent agreeing lineages
    -> estimate falls below ~2% error

2 unknown source names, no dependence evidence
    -> estimate remains ~10%, not <2%
```

This is the intended semantic boundary.

## 5. Organism recovery now consumes raw evidence

`OrganismRecoveryCoordinator` can carry an `EvidenceDependenceModel` and now exposes:

`plan_external_execution_evidence_from_sources(...)`

The method performs:

```text
raw current external records
        ↓
effective lineage/dependence view
        ↓
binary evidence aggregation
        ↓
current label + estimated error
        ↓
shared EvidenceAssuranceDecision
```

This closes the privileged-caller gap.

## Semantic tests

The integration tests pin that:

- unknown source names do not avoid a needed independent check;
- sufficiently supported learned independence can lower aggregate error and avoid an unnecessary check;
- learned dependence keeps agreeing unknown sources one effective group;
- exact copy lineage overrides a behavioral attempt to split it;
- independent contradiction remains unresolved / requests another failure mode;
- arbitrarily many copied records cannot enter through the aggregation layer as false precision.

## Current architecture consequence

The evidence plane now separates four different questions:

```text
1. Which record/source is this?                 exact identity
2. How reliable is this source?                 learned quality
3. Which failures/evidence does it share?       learned/exact dependence
4. What does the effective evidence imply?      aggregation + assurance
```

No one layer is allowed to impersonate another.

## What remains open

Directional derivation from I26B is represented by `EvidenceDerivationModel` but is not yet consumed by the generic binary aggregator. A child correction can carry more marginal evidence than inherited agreement, so simple symmetric grouping is still lossy in that family.

That is now a concrete future integration problem rather than a hidden assumption.

Large-scale relation-state selection also remains policy/resource dependent; I26D argues against materializing a universal dense graph by default.
