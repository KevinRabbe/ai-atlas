# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **469 added test cases** and integrated work through **I27**. **Twenty-six provisional implementation-neutral principles** survive their current promotion gates.

No fixed A/B/C/D architecture family is selected as a universal whole-system architecture. Their useful mechanisms increasingly behave like organizational modes that can activate at different scopes and timescales.

## What the experiments are converging toward

Current evidence repeatedly supports these distinctions:

- scope follows coupling, responsibility and causal extent;
- state follows expected future value, recoverability and semantic validity;
- optional work follows marginal value under shared scarcity;
- material complements/substitutes require interaction-aware allocation;
- sharing follows reusable regularity while interference earns isolation;
- execution follows state change until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- authority follows independent current invariants, not confidence or historical permission;
- verification follows the failure layer that can still invalidate the result;
- publication state, process phase and state value are not interchangeable;
- external execution fact and permission to execute again are separately grounded;
- surviving bytes do not imply surviving semantics after crash/reorganization;
- record count does not equal independent evidence;
- source identity does not equal source quality;
- source quality does not equal source dependence;
- **evidence independence itself may be unknown, scoped, stale, learned and actively tested**;
- shared/common-mode dependence and directional derivation are different relations;
- absence of observed co-failure does not prove independence outside the observed distribution;
- relation state should be materialized only where its expected assurance value pays for it.

## Current executable architecture hypothesis

```text
stable typed semantic identities
  subjects / source evidence / publication provenance
  current authority / resource ownership
        |
        +--> adaptive ownership topology
        +--> overlapping non-owning coordination scopes
        +--> operational directional dependencies
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocator
        ↓
EVIDENCE PLANE
  exact source identity
  exact provenance where known
  learned source quality
  common-mode EvidenceDependenceModel
      scoped + observation-supported
  directional EvidenceDerivationModel
      where inheritance changes marginal evidence
        ↓
effective failure groups
        ↓
claim aggregation without record-count inflation
        ↓
consequence-sensitive assurance allocation
        ↓
PREPARE non-authoritative candidate state
        ↓
version + publication-provenance + current-authority fence
        ↓
PUBLISH coherent authoritative state
        |
        +--> external effect path
        |       effect-specific execution evidence
        |       current authority for every fresh/retry attempt
        |       unresolved status when exact execution cannot be known
        ↓
semantic crash recovery
        ↓
old-epoch forwarding + typed transient recovery
  hot state -> currentness / source rematerialization
  credit -> exact causal identity / source replay
        ↓
observe → versioned causal credit → staged appropriately-scoped update
```

This is **not** yet a frozen final architecture.

## Publication, crash recovery and external effects

I13–I19 establish that consequential state change is not one mutation with one moment.

**PS-024 — failure-isolated consequential transition publication** separates non-authoritative preparation from authoritative publication when partial visibility can violate invariants. Crash recovery follows publication provenance/base fencing rather than process phase. State value alone may not identify which transition produced it.

**PS-025 — externally grounded effect recovery / execution-authority separation** distinguishes:

```text
external execution evidence -> did the old effect happen?
current capability authority -> may a new/retry effect happen now?
```

Local intent, past approval and process phase establish neither external execution nor current permission.

## Typed recovery instead of opaque snapshot restoration

I22/I23 extend recovery to source-backed hot state and delayed causal credit.

Approximate I23 means:

| policy | utility/episode | stale hot | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

Typed recovery asks whether a state object's **meaning** survived the transition, not merely whether its bytes did.

## From known lineage to learned dependence

I05C/I17 first show that multiple agreeing records can still be one failure lineage. I20/I21 then use one assurance controller across external and metacognitive claims.

I24 removes exact lineage IDs from the learner. Hidden upstream relationships change while visible source identities stay fixed. Learned dependence beats both assuming all sources independent and assuming all are correlated.

I25 adds the required causal falsifier: hard tasks make unrelated evaluators fail together. Raw co-failure therefore cannot prove shared ancestry.

This promotes:

> **PS-026 — learned / causally qualified evidence dependence:** treat independence between evidence sources as uncertain, revisable relational state. Do not infer independent failure modes from record count, source names, agreement or raw co-failure alone. Infer dependence from outcome/provenance/intervention evidence while conditioning on plausible common causes, and acquire explicit dependency evidence when uncertainty about independence can materially change assurance value.

## I26A — dependence is scoped

The same source pair can be dependent in one claim domain and independent in another.

A global relation graph reaches only ~`0.80` pair-relation accuracy in the matched synthetic family. Domain-scoped dependence reaches ~`0.98`, reduces audits from ~`0.55` to ~`0.39` per task and raises utility from ~`4.15` to ~`4.22`.

So PS-026 is a **typed/scoped relation**, not one universal graph.

## I26B — dependence can be directional

Derived sources may inherit upstream errors but sometimes independently correct them.

Approximate error rates:

| policy | total error | error when child departs upstream |
|---|---:|---:|
| record count | ~0.125 | ~0.179 |
| symmetric collapse | ~0.181 | ~0.179 |
| **directional provenance** | **~0.118** | **~0.142** |
| **learned direction** | **~0.119** | **~0.144** |
| Bayesian oracle | ~0.112 | ~0.103 |

`EvidenceDerivationModel` therefore stays separate from common-mode `EvidenceDependenceModel` for now. Agreement may be inherited; downstream disagreement may be the genuinely new evidence.

## I26C — apparent independence can be distribution-limited

B/C look independent on ordinary resolved history, then use a shared hidden failure path only on rare unresolved high-consequence frontier cases.

Passive co-failure learning then fails by construction. Treating the pair as dependent everywhere protects the frontier but destroys ordinary diversity. A scoped provenance/stress diagnostic preserves ordinary performance while reducing frontier error from ~`0.38` to ~`0.12`.

So:

```text
no observed dependence
!= structural independence
!= independence under future distribution shift
```

## I26D — dependence does not imply a dense N² graph

At 128 sources there are 8,128 possible pair relations, while each decision touches only six.

Approximate utility/task:

- assume independent: ~`0.657`;
- dense exact graph: ~`0.825`;
- query active pairs every time: ~`0.910`;
- cache forever: ~`0.984`;
- **scoped TTL relation state:** ~`0.988`.

The scoped policy ends with ~495 active relation records rather than 8,128. When storage is made nearly free, permanent caching can win, so no fixed cache technology is selected.

## I27 — dependence is now inside the common assurance path

The evidence runtime no longer requires every source to arrive with an exact lineage ID.

`EvidenceLineageRegistry` now combines:

- exact lineage where genuinely known;
- learned positive dependence;
- learned independence only after sufficient observation support;
- unresolved dependence where neither is justified.

An untrained below-threshold covariance score is **not** confidence in independence.

`aggregate_binary_evidence()` then combines one contribution per effective failure group using separately supplied source-quality estimates.

Sanity boundary for 10%-error sources:

```text
4 copied agreeing records / one failure group -> ~10% error
2 independent agreeing groups              -> <2% error
2 unknown names / unsupported dependence   -> ~10% error
```

`OrganismRecoveryCoordinator` can now consume raw external records and derive the current execution label/error **after** effective grouping, so record-count false precision cannot sneak in through an upstream caller.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

PS-026 matters directly: ten nominally different confirmations are not ten independent experiments if they inherit the same hidden assumption, dataset, instrument, derivation path or frontier failure mode.

## Current provisional selection count

**PS-001 through PS-026** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

No PS-027 is selected by I26/I27. Those experiments refine and compose PS-026.

## Next milestone

The highest-value open evidence problem is now **direction-aware aggregation**.

I26B proves that symmetric collapse can destroy useful child-correction information, but the generic aggregator currently consumes only effective symmetric failure groups. The next step is to integrate directional derivation without turning `parent -> child` into a simplistic discard rule, then stress:

- multi-hop derivation A -> B -> C;
- cycles/mutual adaptation;
- sparse/delayed truth;
- changing derivation by claim domain;
- whether one unified causal evidence model actually beats the current separated common-mode + directional representations.

JEPA/E24 remains a candidate representation mechanism, not a selected component. Neural E24C remains conditional on representation geometry becoming an architecture bottleneck.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
