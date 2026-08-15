# Phase 10 Experimental Status

**Checkpoint: twenty-five provisional design principles selected; composition has progressed through I23 plus the reusable crash-aware typed organism runtime. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **392 added test cases**.

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
- I23 integrated crash/topology/evidence/transient recovery lifecycle: 8.

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

## I05C / I17 — correlated records are one evidence lineage

External receipts and verifier audits independently reproduce the same failure: raw record count does not equal independent evidence count.

I17 default external weighted harm:

- correlated majority: ~`0.931`;
- uniform independent: ~`0.135`;
- selective independent: ~`0.173` with only ~`0.675` checks/task.

I05C default verifier-calibration error:

- correlated majority: ~`0.079`;
- `majority + independent` with raw vote count: ~`0.078` despite paying for the independent audit;
- uniform independent: ~`0.048`;
- selective independent: ~`0.050` with ~`0.666` checks/task.

Missing audit resolution is not positive evidence. Treating missing audit as success can raise throughput in one synthetic regime, but worsens calibration and false durable writes.

## Shared evidence-lineage substrate

`EvidenceLineageRegistry` represents source/failure lineage, staleness, whether a record resolves the claim, and conflict across independent resolving lineages. It does not assign truth or reliability.

`EvidenceAssuranceDecision` combines that structure with separately learned quality estimates, consequence/asymmetric harm and independent-check cost, returning `use_current`, `acquire_independent` or `unresolved`.

## I20 / I21 — one assurance controller across external and metacognitive claims

30-seed I20 default:

| policy | utility/task | weighted harm | independent queries |
|---|---:|---:|---:|
| record-count confidence | ~3.062 | ~1.438 | 0 |
| stale-only | ~3.651 | ~0.798 | ~0.301 |
| uniform independent | ~3.585 | ~0.733 | 1.000 |
| **lineage-value** | **~3.782** | **~0.592** | **~0.695** |

The same policy lowers harm in both external-execution and metacognitive claims. I21 moves that planning inside `OrganismRecoveryCoordinator`, removing the privileged assumption that receipts arrive already interpreted.

## I22 — transient state recovery

### Source-backed hot/predictive cache

30-seed utility/item:

- persist all: ~`0.2314`, stale reuse ~`0.0694`;
- rematerialize: ~`0.3278`;
- discard: `0`, missed reuse ~`0.4202`;
- **adaptive:** ~`0.3335`, persisting ~`0.171` and rematerializing ~`0.301`, stale reuse ~`0.006`.

### Delayed causal-credit trace

30-seed utility/item:

- discard: `0`;
- unversioned positional restore: ~`0.6083`, false blame ~`0.1527`;
- versioned causal trace: ~`0.7073`, false blame `0`;
- source replay: ~`0.7073`, false blame `0`;
- **adaptive:** ~`0.7859`, mixing exact trace persistence and source replay.

`TransientStateRegistry` now implements the required typed metadata: source-backed hot state with source version/epoch/currentness semantics and delayed-credit records with stable transition identity/epoch/replay source.

## I23 — all recovery layers coexist

I23 combines in every episode:

- topology publication that may already have committed before crash;
- publication-provenance recovery;
- source-backed hot state from the old epoch;
- delayed credit from the old structure;
- an old-epoch external event;
- authority revocation during downtime;
- stale/correlated external receipts;
- independent reconciliation.

Approximate 30-seed composition means:

| policy | utility/episode | stale hot use | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

Typed external execution recovery still has small error because independent evidence itself is imperfect; the integration does not manufacture certainty. It nevertheless reduces combined duplicate/omission error materially versus trusting the correlated receipt snapshot.

The result is stronger than `do not snapshot`:

> **recovery must preserve semantic validity, not merely byte survival. Useful transient state can be selectively persisted/rematerialized/replayed without restoring stale authority, routes, cache values or causal pointers.**

---

# Current provisional selections

**PS-001 through PS-025** remain active reversible constraints. I17–I23 strengthen and compose existing principles; they do not justify new PS numbers.

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
evidence-lineage structure + learned source quality
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
        |       effect-specific evidence lineage
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

The architecture increasingly has one shared evidence/resource substrate while keeping exact semantic boundaries between provenance, reliability, truth/history, authority and state validity.

## Next high-value work

1. make **evidence-lineage relationships themselves uncertain/learned** rather than supplied as exact metadata;
2. test whether mistaken lineage inference can create false independence and whether active lineage-discovery evidence is worth buying;
3. only then decide whether evidence-lineage metadata belongs in stable exact state, learned approximate state, or both;
4. nested/overlapping **ownership** remains unearned while non-owning coordination overlays suffice;
5. neural E24C remains conditional on predictive-representation geometry becoming an architecture bottleneck.

## Guardrail

No proposal score, record count, stale assurance, prepared candidate, local phase marker, historical permission, missing audit, opaque snapshot, or unversioned transient pointer may manufacture current authority, external execution fact, independent evidence or causal attribution.
