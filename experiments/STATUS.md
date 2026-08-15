# Phase 10 Experimental Status

**Checkpoint: twenty-six provisional design principles selected; composition has progressed through I27 with a crash-aware typed organism, learned/scoped/directional evidence-dependence models and effective-lineage assurance aggregation. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **469 added test cases**.

Additions since the 412-test PS-026 checkpoint:

- I26A domain-conditional evidence dependence: 7 tests;
- reusable `EvidenceDependenceModel` context/confidence semantics: +5 tests;
- I26B directional evidence derivation: 7;
- reusable `EvidenceDerivationModel`: 6;
- I26C adversarial apparent independence: 7;
- I26D large-source dependence-state scale: 7;
- `EvidenceLineageRegistry` learned/unknown dependence integration: +5;
- effective-lineage binary evidence aggregation: 7;
- organism recovery with learned dependence + raw-evidence aggregation: 6.

The shell environment has previously been unable to clone GitHub because DNS resolution is unavailable there. Numerical discriminators are exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only. Do not interpret the committed test count as a claim that a fresh clean-checkout suite was executed in that shell.

---

# Current architecture checkpoint

## I06–I23 — typed adaptive organization, publication and recovery

I06 shows interacting runtime operations benefit from joint allocation. AF01–AF03 and I07 show organizational mode/scope/membership can all be adaptive when persistence pays for inference/switch/migration cost.

I08–I13 turn stable identities, dynamic topology, overlapping coordination, directional dependencies, leases, in-flight work and structural assurance into reusable typed runtime state. I13/I13B/I13C promote **PS-024 — failure-isolated consequential transition publication**.

I14–I19 make that runtime crash-aware: recovery follows authoritative publication provenance/base fencing rather than local phase, and external execution evidence remains separate from permission to issue a fresh/retry effect. I15/I16 promote **PS-025 — externally grounded effect recovery / execution-authority separation**.

I22/I23 extend recovery to source-backed hot state and delayed credit. In the integrated I23 lifecycle, typed recovery reaches ~`2.67` utility/episode with zero modeled stale-hot use, false credit, unauthorized old-event execution or duplicate publication attempts; opaque snapshot restoration falls to ~`-1.47`, while safe transient discard reaches ~`1.27` but loses useful state.

## I05C / I17 / I20 / I21 — evidence record count is not evidence independence

External receipts and verifier audits independently reproduce the same failure: multiple records can be one failure lineage.

`EvidenceLineageRegistry` initially represented exact known lineage/staleness/resolution/conflict. `EvidenceAssuranceDecision` then priced whether to use current evidence, acquire another failure mode or remain unresolved. I20 showed the same lineage-aware assurance rule can serve external and metacognitive claims.

This promoted no new principle by itself; it strengthened PS-013/014.

## I24 / I25 — PS-026: evidence independence may need to be learned

I24 removes exact lineage IDs from the learner. Hidden upstream relationships change while visible source identities stay constant.

Approximate 30-seed I24 means:

| policy | utility/task | weighted harm | independent audits/task |
|---|---:|---:|---:|
| source-count independence | ~4.157 | ~0.296 | ~0.277 |
| assume all correlated | ~4.002 | ~0.331 | ~0.865 |
| **learned dependence** | **~4.196** | **~0.232** | ~0.437 |
| learned + active probe | ~4.194 | **~0.221** | ~0.423 |
| oracle | ~4.213 | ~0.216 | ~0.408 |

I25 then adds a common-cause confounder: hard tasks make unrelated evaluators fail together. Raw co-failure therefore overstates shared ancestry; conditioning on a noisy difficulty context improves utility and reduces unnecessary audits.

Together they promote:

### PS-026 — learned / causally qualified evidence dependence

> **Treat independence between evidence sources as uncertain, revisable relational state. Do not infer independent failure modes from record count, source names, agreement or raw co-failure alone. Infer dependence from outcome/provenance/intervention evidence while conditioning on plausible common causes, and acquire explicit dependency evidence when uncertainty about independence can materially change assurance value.**

The selected object is the semantic requirement that evidence independence can itself be unknown/stale/learned/tested—not covariance clustering, causal discovery, provenance graphs or a particular diagnostic implementation.

## I26A — dependence is claim-scope conditional

The same six source identities have different hidden failure relations in external and metacognitive domains.

Approximate means:

| policy | utility/task | harm | audits/task | pair-relation accuracy |
|---|---:|---:|---:|---:|
| one global relation graph | ~4.146 | ~0.253 | ~0.547 | ~0.80 |
| **domain-scoped relation** | **~4.224** | **~0.225** | **~0.387** | ~0.98 |
| domain + active probe | ~4.225 | **~0.219** | ~0.395 | ~0.99 |
| oracle | ~4.226 | ~0.219 | ~0.398 | exact |

PS-026 is therefore refined: dependence is **typed/scoped relational state**, not necessarily one universal source-pair graph.

`EvidenceDependenceModel` now distinguishes global residual relation from context-specific relation and supports context-scoped probes.

## I26B — shared ancestry and directional derivation are different relations

I26B models an upstream source A and derived children B/C that usually copy A but sometimes independently correct it. D is an independent comparator.

Approximate 30-seed means:

| policy | error rate | error when child departs from A |
|---|---:|---:|
| record count | ~0.125 | ~0.179 |
| symmetric lineage collapse | ~0.181 | ~0.179 |
| **directional provenance** | **~0.118** | **~0.142** |
| **learned direction** | **~0.119** | **~0.144** |
| Bayesian oracle | ~0.112 | ~0.103 |

An undirected group can represent common-mode failure but loses **where evidence/errors flow**. Agreement downstream may be inherited; disagreement downstream may be the new evidence.

`EvidenceDerivationModel` therefore remains separate from symmetric `EvidenceDependenceModel`.

## I26C — observational independence can fail under selective frontier shift

B/C look genuinely independent on ordinary tasks whose outcomes are resolved. On rare high-consequence frontier cases they switch to one hidden shared failure path; frontier outcomes are unavailable to passive dependence learning.

Approximate 30-seed means:

| policy | utility/task | weighted harm | ordinary error | frontier error |
|---|---:|---:|---:|---:|
| record count | ~0.858 | ~0.291 | ~0.032 | ~0.384 |
| passive history | ~0.858 | ~0.291 | ~0.032 | ~0.384 |
| always dependent | ~1.040 | ~0.246 | ~0.120 | ~0.124 |
| **frontier stress/provenance probe** | **~1.524** | **~0.124** | ~0.032 | **~0.124** |
| oracle | ~1.529 | ~0.124 | ~0.032 | ~0.124 |

So `no observed co-failure` means independence on the observed/resolved distribution—not structural independence under an unobserved frontier. Explicit provenance/intervention can have option value where coverage is weak and consequence high.

## I26D — dependence matters without requiring an N² graph

At 128 sources there are 8,128 possible pairs, while each decision touches six relations and the active 32-source pool changes midway.

Approximate 30-seed means:

| policy | utility/task | relation cost | assurance harm | final relation state |
|---|---:|---:|---:|---:|
| assume independent | ~0.657 | 0 | ~0.343 | 0 |
| dense exact graph | ~0.825 | ~0.175 | 0 | 8,128 |
| query every time | ~0.910 | ~0.090 | 0 | 0 |
| cache forever | ~0.984 | ~0.016 | 0 | ~992 |
| **scoped TTL** | **~0.988** | **~0.012** | 0 | **~495** |

When relation storage is made nearly free, permanent caching can beat TTL because re-querying dominates. The result is value/scoping, not mandatory expiry.

## I27 — learned dependence is now inside the common assurance path

I27 removes two remaining privileges.

### Exact lineage is optional

`EvidenceLineageRegistry.register_source()` no longer requires `lineage_id`.

- exact shared lineage cannot be split by behavioral learning;
- unknown names do not create independent evidence;
- learned positive dependence can collapse unknown/distinct sources;
- learned independence separates unknown sources only after sufficient resolved observation support;
- an untrained below-threshold covariance score remains **independence unresolved**.

`EvidenceDependenceModel` now includes observation-supported relation confidence.

### Confidence is aggregated after effective grouping

`aggregate_binary_evidence()` consumes source-quality estimates after exact/learned effective grouping.

Sanity boundary for 10%-error sources:

```text
4 agreeing copies / one failure lineage -> ~10% error
2 independent agreeing lineages        -> <2% error
2 unknown source names / no support    -> ~10% error
```

`OrganismRecoveryCoordinator.plan_external_execution_evidence_from_sources()` now runs:

```text
raw records
  -> effective provenance/dependence groups
  -> source-quality-weighted claim estimate
  -> shared assurance allocation
```

This prevents copied record count from re-entering as false precision through an upstream caller.

---

# Current provisional selections

**PS-001 through PS-026** are active reversible constraints.

PS-013 says assurance value comes from sufficiently different failure modes. PS-026 says the system may first need to determine whether those failure modes are actually independent and within what scope.

No PS-027 is promoted by I26/I27; these experiments refine and compose PS-026.

---

# Current executable architecture hypothesis

```text
stable typed semantic identities
  subjects / source evidence / publication provenance
  authority versions / resource leases
        |
        +--> dynamic ownership topology
        +--> non-owning coordination scopes
        +--> directional operational dependencies
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocator
        ↓
EVIDENCE STRUCTURE
  exact source identity
  exact provenance where known
  learned source quality
  symmetric/common-mode EvidenceDependenceModel
      scoped + observation-supported
  directional EvidenceDerivationModel
      where inheritance matters
        ↓
effective failure groups
        ↓
claim aggregation without record-count inflation
        ↓
consequence-sensitive assurance allocation
        ↓
PREPARE non-authoritative candidate state
        ↓
version / publication-provenance / current-authority fence
        ↓
PUBLISH internal authoritative state
        |
        +--> external effect path
        |       effect-specific execution evidence
        |       current authority for every new/retry attempt
        |       unresolved status when exact execution cannot be identified
        ↓
crash recovery from semantic identity/provenance
        ↓
old-epoch event forwarding + current authority recheck
        ↓
typed transient recovery
  hot state -> currentness / source rematerialization
  credit -> exact causal identity / source replay
        ↓
observe → versioned causal credit → staged appropriately-scoped update
```

## Strongest current evidence-plane inference

> **Evidence is not a bag of records. Its value depends on source quality, failure-mode dependence, derivation direction, scope/coverage and consequence. Those relations are themselves revisable state and should be materialized only where their expected assurance value pays for them.**

## Next high-value work

1. integrate I26B directional derivation into generic evidence aggregation without turning every derivation edge into a hard discard rule;
2. test multi-hop derivation A -> B -> C and cycles/mutual adaptation;
3. test learned dependence/derivation under sparse or delayed truth rather than exact post-hoc resolution;
4. then revisit whether a unified causal evidence graph is actually simpler/better than the current separate symmetric-dependence + directional-derivation models;
5. nested/overlapping **ownership** remains unearned while non-owning coordination overlays suffice;
6. neural E24C remains conditional on predictive-representation geometry becoming an architecture bottleneck.

## Guardrail

No proposal score, record count, source name, raw agreement, raw co-failure, unsupported below-threshold score, stale assurance, prepared candidate, local phase marker, historical permission, missing audit, opaque snapshot or unversioned transient pointer may manufacture current authority, external execution fact, independent evidence, claim confidence or causal attribution.
