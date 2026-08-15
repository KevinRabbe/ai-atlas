# Phase 10 Experimental Status

**Checkpoint: twenty-six provisional design principles selected; composition has progressed through I25 plus the reusable crash-aware typed organism and learned evidence-dependence substrate. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **412 added test cases**.

Architecture/composition additions since the 308-test I16 checkpoint:

- I17 correlated/stale external execution evidence: 6 tests;
- I18 publication-provenance recovery stress: 6;
- provenance-aware recovery protocol: 4;
- authoritative publication-provenance runtime integration: 6;
- I19 common organism recovery coordinator: 9;
- I05C correlated/partially-unresolved metacognitive audits: 6;
- typed evidence-lineage registry: 6;
- shared evidence-assurance API: 6;
- I20 cross-domain evidence assurance allocation: 6;
- I21 recovery/evidence-lineage integration: 6;
- I22 transient cache/credit recovery: 8;
- typed transient-state registry: 7;
- I23 integrated crash/topology/evidence/transient recovery lifecycle: 8;
- I24 hidden evidence-lineage inference: 7;
- I25 common-cause evidence-lineage confounding: 7;
- reusable learned evidence-dependence model: 6.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Current architecture checkpoint

## I06–I13 — adaptive organization becomes typed executable state

I06 shows interacting runtime operations benefit from joint allocation (~`1.564` utility/task versus ~`1.355` factorized). AF01–AF03 and I07 show organizational mode, scope and membership can be adaptive when structural persistence pays for identification/switch/migration cost.

I08–I10 move exact evidence/provenance, predictive source references, versioned authority, singular leases and in-flight work through topology epochs and expose them through reusable `TypedScopeRuntime`. I11 separates overlapping non-owning coordination from ownership. I12 separates directional dependence from reciprocity/shared organization.

I13/I13B/I13C show consequential multi-step changes need a failure-isolated publication boundary when partial visibility can violate invariants. This promotes **PS-024 — failure-isolated consequential transition publication**.

## I14–I19 — crash-aware publication and external execution

I14 shows a local process phase cannot distinguish `already published but marker lost` from `not published`, and old assurance cannot safely overwrite current revocation/retraction or newer state.

I15 shows local state cannot prove an external effect occurred. I16 separates historical execution evidence from permission to execute again, promoting **PS-025 — externally grounded effect recovery / execution-authority separation**.

I18 adds exact publication attribution: target numeric version may be unknown at preparation time and another transition can produce the same state value. `publication_ref` is therefore stamped into the same modeled coherence boundary as lease/topology authority. I19 composes those semantics through `OrganismRecoveryCoordinator`.

## I05C / I17 / I20 / I21 — shared evidence semantics

External receipts and verifier audits independently reproduce the same failure: raw record count does not equal independent evidence count.

`EvidenceLineageRegistry` represents known source/failure lineage, staleness, whether a record resolves the claim, and conflict across independent resolving lineages. `EvidenceAssuranceDecision` combines that structure with separately learned quality estimates, consequence/asymmetric harm and independent-check cost.

I20 then uses one assurance controller across both external-execution and metacognitive claims. At the default 30-seed sweep, lineage-aware value allocation reaches ~`3.782` utility/task versus ~`3.062` for record-count confidence, while using fewer independent checks than uniform checking. I21 moves that planning inside `OrganismRecoveryCoordinator`.

## I22 / I23 — typed transient recovery and whole-lifecycle composition

I22 separates source-backed hot/predictive state from delayed causal-credit state. Hot state may be cheaper to rematerialize than persist stale values; delayed credit needs stable causal identity or source replay rather than positional restoration.

I23 puts topology publication, crash recovery, old-epoch work, revocation, correlated external evidence, hot-state recovery and delayed credit into one lifecycle.

Approximate 30-seed composition means:

| policy | utility/episode | stale hot use | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

The result supports semantic recovery rather than byte-level process restoration as the architecture boundary.

## I24 — evidence dependence is not given metadata

I24 removes the assumption that source lineages are known.

Six stable visible sources share three hidden upstream failure processes. The learner only receives source outputs plus the subset of claims that later obtain sufficiently independent resolution. Midway through the run, the hidden upstream relationships change without changing source identities.

Approximate 30-seed result:

| policy | utility/task | weighted harm | independent audits/task | lineage probes/task |
|---|---:|---:|---:|---:|
| record count / assume independent | ~4.157 | ~0.296 | ~0.277 | 0 |
| assume all correlated | ~4.002 | ~0.331 | ~0.865 | 0 |
| **learned lineage** | **~4.196** | **~0.232** | ~0.437 | 0 |
| learned + active probe | ~4.194 | **~0.221** | ~0.423 | ~0.238 |
| oracle lineage | ~4.213 | ~0.216 | ~0.408 | 0 |

The passive learner reaches ~`0.980` pair-relation accuracy before the hidden shift, drops to ~`0.664` immediately after it, then recovers to ~`0.925`. Value-priced explicit dependency probes accelerate that recovery and reduce harm, but are not universally worth their cost.

## I25 — raw co-failure is confounded by task difficulty

I25 attacks I24's obvious causal weakness. Eight evaluators have hidden shared ancestry, but hard tasks also raise error rates across **all** evaluators. Unrelated evaluators therefore co-fail because of a common task cause.

A raw co-failure model mistakes some of that broad correlation for shared ancestry. Conditioning dependence learning on a noisy observable difficulty context improves utility and cuts unnecessary audits.

Approximate 10-seed result:

| policy | utility/task | weighted harm | independent audits/task | dependency probes/task |
|---|---:|---:|---:|---:|
| raw co-failure | ~4.116 | ~0.296 | ~0.433 | 0 |
| **difficulty-conditioned** | **~4.149** | ~0.294 | **~0.337** | 0 |
| conditioned + active probe | ~4.145 | **~0.277** | ~0.335 | ~0.217 |
| oracle lineage | ~4.165 | ~0.281 | ~0.337 | 0 |

The second family falsifies `persistent co-failure => shared lineage`. Dependence evidence must be interpreted relative to plausible common causes.

`EvidenceDependenceModel` now provides a reusable implementation-neutral substrate for:

- stable source identity;
- context-conditioned residual co-failure;
- revisable pairwise dependence estimates;
- bounded explicit dependence probes;
- effective source-component formation.

It does not decide truth and does not replace source-reliability learning.

### PS-026 — learned / causally qualified evidence dependence

> **Treat independence between evidence sources as uncertain, revisable relational state. Do not infer independent failure modes from record count, source names, agreement or raw co-failure alone. Infer dependence from outcome/provenance/intervention evidence while conditioning on plausible common causes, and acquire explicit dependency evidence when uncertainty about independence can materially change assurance value.**

The selected object is the semantic requirement that **evidence independence itself can be unknown and learned/tested**, not covariance clustering, causal-discovery algorithms, provenance graphs or a specific diagnostic mechanism.

---

# Current provisional selections

**PS-001 through PS-026** are active reversible constraints.

PS-013 says additional assurance matters only to the extent it adds sufficiently different failure modes. PS-026 now removes the hidden assumption that those failure-mode relationships are always known beforehand.

---

# Current executable architecture hypothesis

```text
stable typed semantic identities
  subjects / source evidence / publication provenance
  authority versions / resource leases
        |
        +--> directional dependencies
        +--> dynamic ownership topology
        +--> overlapping non-owning coordination scopes
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocator
        ↓
source identity + learned source quality
        +
revisable evidence-dependence model
  context-conditioned co-failure
  provenance / controlled dependency evidence
        ↓
effective independent evidence structure
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
        |       unresolved status when execution cannot be identified
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

The architecture increasingly treats relations themselves—organization, authority, provenance, causal credit and now evidence dependence—as typed, revisable state rather than incidental metadata.

## Next high-value work

1. test **domain-conditional and directional evidence dependence**: two sources may share failure modes only for some claim families, and dependence need not be symmetric in derived/copy relationships;
2. attack PS-026 with adversarial sources that intentionally decorrelate visible errors while sharing hidden ancestry;
3. test sparse-feedback / large-source-population regimes where pairwise dependence learning may cost more than it saves;
4. then integrate learned dependence directly into the common `EvidenceLineageRegistry`/assurance path rather than using exact lineage IDs as the default interface;
5. nested/overlapping **ownership** remains unearned while non-owning coordination overlays suffice;
6. neural E24C remains conditional on predictive-representation geometry becoming an architecture bottleneck.

## Guardrail

No proposal score, record count, source name, raw agreement, raw co-failure, stale assurance, prepared candidate, local phase marker, historical permission, missing audit, opaque snapshot or unversioned transient pointer may manufacture current authority, external execution fact, independent evidence or causal attribution.
