# Phase 10 Experimental Status

**Checkpoint: twenty-five provisional design principles selected; composition has progressed through I22 plus the reusable crash-aware typed organism runtime. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **377 added test cases**.

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
- I22 transient cache/credit recovery: 8.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Current architecture checkpoint

## I06–I13 — adaptive organization becomes typed executable state

I06 shows interacting runtime operations benefit from joint allocation (~`1.564` utility/task versus ~`1.355` factorized). AF01–AF03 and I07 show organizational mode, scope and membership can be adaptive when structural persistence pays for identification/switch/migration cost.

I08–I10 move exact evidence/provenance, predictive source references, versioned authority, singular leases and in-flight work through topology epochs and expose them through reusable `TypedScopeRuntime`.

I11 separates overlapping non-owning coordination from ownership. I12 separates one-way dependency from reciprocity/shared organization.

I13/I13B/I13C show consequential multi-step changes need a failure-isolated publication boundary when partial visibility can violate invariants. This promotes **PS-024 — failure-isolated consequential transition publication**.

## I14 — crash/restart is not a remembered phase

Across resource ownership and durable-knowledge promotion, old assurance replay or `phase + current recheck` remains only ~`0.59–0.62` correct in the synthetic crash distribution because it cannot distinguish `already published but marker lost` from `not published`, and can overwrite a newer superseding state.

Version/target-fenced recovery reaches exact modeled recovery. Any retry reacquires current validation/assurance; old approval is evidence history rather than standing authority.

## I15–I16 — external execution is a separate evidence plane

I15 shows local versioning cannot prove the outside world acted. Receiver-recognized stable effect identity or exact reconciliation can remove retry ambiguity when the environment participates. A non-identifiable physical effect cannot be made exact by a local UUID; ambiguous execution remains unresolved and retry/abstention is consequence-priced.

I16 separates historical execution evidence from current permission to act again. The separated policy reaches ~`0.969` utility with zero modeled duplicate effects, unauthorized retries and history errors.

This promotes **PS-025 — externally grounded effect recovery / execution-authority separation**.

## I17 — record count is not evidence independence

Three visible external receipts descend from one failure lineage. Correlated majority therefore behaves like one source (~`0.931` weighted harm). Buying an independent observation but letting the three copied records outvote it also wastes the check.

Uniform independent checking reduces default harm to ~`0.135`; selective checking uses ~`0.675` queries/task with ~`0.173` harm. Assurance-price sweeps reproduce PS-014: uniform checking wins while independent evidence is cheap, selective checking as it becomes expensive, and sufficiently costly checks can make trusting the imperfect primary source rational in low-enough consequence regimes.

## I18 — authoritative state identity is not publication attribution

Two crash-recovery assumptions fail:

1. a broader/global version allocator can make the exact numeric target version unknowable at prepare time;
2. another transition can independently produce the same state value.

Predicting `base+1` recognizes only ~`0.519` of completed publications in the first family. State value alone produces ~`0.088` false completion attribution in the same-target collision family. **Publication provenance** reaches exact modeled attribution in both.

Runtime hardening:

- `RecoveryRecord.target_version` is optional;
- `RecoveryObservation` may carry `current_publication_id`;
- `ResourceLease` can carry `publication_ref`;
- current topology carries `topology_publication_ref`;
- `PublicationProtocol` stamps provenance at the same modeled coherence boundary as the authoritative lease/epoch change.

## I19 — common crash-aware organism recovery

`OrganismRecoveryCoordinator` now derives recovery records from prepared topology/resource publications, observes authoritative runtime provenance, re-reads current authority for any retry, and routes external effects through PS-025.

The coordinator covers prepared, published, superseded, revocation-after-publish, unknown numeric target versions, topology recovery and unresolved non-identifiable external effects without privileged hidden experiment state.

## I05C + I17 — the same evidence failure appears internally and externally

I05C makes verifier-quality audit evidence correlated, stale and unavailable on some outcomes.

30-seed default calibration error:

- correlated majority: ~`0.079`;
- `majority + independent` with raw vote count: ~`0.078` despite paying for the independent audit;
- uniform independent: **~`0.048`**;
- selective independent: ~`0.050` with only ~`0.666` audit queries/task.

Treating missing audit resolution as success can raise throughput in this synthetic regime, but worsens calibration and increases false durable writes. Missing resolution therefore is **not positive evidence**, even when taking more risk can have positive expected value.

## Shared evidence-lineage substrate

`EvidenceLineageRegistry` now represents source-lineage, staleness, whether a record resolves a claim, and conflict across independent resolving lineages. It does not assign truth or reliability.

`EvidenceAssuranceDecision` consumes that structure plus learned source-quality estimates, consequence/asymmetric harm and independent-check cost, returning:

- `use_current`;
- `acquire_independent`;
- `unresolved`.

This keeps provenance structure, reliability learning and resource allocation as distinct semantics.

## I20 — one assurance allocator across two claim domains

I20 applies the same lineage-aware value rule to external-execution claims and metacognitive verifier claims.

30-seed default:

| policy | utility/task | weighted harm | independent queries |
|---|---:|---:|---:|
| record-count confidence | ~3.062 | ~1.438 | 0 |
| stale-only | ~3.651 | ~0.798 | ~0.301 |
| uniform independent | ~3.585 | ~0.733 | 1.000 |
| **lineage-value** | **~3.782** | **~0.592** | **~0.695** |

The same policy lowers per-family harm from ~`1.248 -> 0.599` for external execution and ~`1.629 -> 0.585` for metacognitive claims.

No new principle is needed: this is executable cross-domain support for PS-004/006/007/013/014/025.

## I21 — recovery now plans evidence acquisition itself

`OrganismRecoveryCoordinator` can query `EvidenceLineageRegistry` and the shared assurance layer before interpreting external execution evidence.

It can now distinguish:

```text
use current evidence
acquire another independent failure lineage
preserve unresolved execution state
```

before PS-025 decides historical completion versus a possible new retry. This removes the previous privileged `already interpreted receipt` step.

## I22 — transient cognitive state across recovery

### Source-backed hot/predictive cache

30-seed utility/item:

- persist all: ~`0.2314`, with ~`0.0694` stale reuse;
- rematerialize from stable source: ~`0.3278`;
- discard: `0` with ~`0.4202` missed reuse;
- **adaptive:** ~`0.3335`, persisting ~`0.171` and rematerializing ~`0.301` of items, with stale reuse only ~`0.006`.

### Delayed causal-credit traces

30-seed utility/item:

- discard: `0`, all delayed credit lost;
- unversioned positional restore: ~`0.6083`, false blame ~`0.1527`;
- versioned causal trace: ~`0.7073`, false blame `0`;
- source replay: ~`0.7073`, false blame `0`;
- **adaptive:** ~`0.7859`, mixing exact trace persistence (~`0.745`) and source replay (~`0.255`).

The recovery-validity condition is typed: cache asks whether information is current/recoverable; credit asks whether historical causal identity remains a legitimate learning target.

---

# Current provisional selections

**PS-001 through PS-025** remain active reversible constraints. I17–I22 strengthen and compose existing principles; they do not justify new PS numbers.

---

# Current executable architecture hypothesis

```text
stable typed semantic identities
  subjects / evidence / provenance / sources
  authority versions / resource leases / publication provenance
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
selectively persist / rematerialize / replay transient state
        ↓
observe → causal credit → staged appropriately-scoped update
```

The architecture increasingly has one shared evidence/resource substrate while keeping exact semantic boundaries between provenance, reliability, truth/history, authority and state validity.

## Next high-value work

1. implement the minimal typed transient-state registry implied by I22 instead of restoring opaque runtime snapshots;
2. stress evidence-lineage quality when lineage relations themselves are uncertain or learned incorrectly;
3. test delayed credit/hot-state recovery inside a real topology/publication crash scenario rather than the isolated I22 families;
4. nested/overlapping **ownership** remains unearned while non-owning coordination overlays suffice;
5. neural E24C remains conditional on predictive-representation geometry becoming an architecture bottleneck.

## Guardrail

No proposal score, record count, stale assurance, prepared candidate, local phase marker, historical permission, missing audit, or unversioned transient pointer may manufacture current authority, external execution fact, independent evidence or causal attribution.
