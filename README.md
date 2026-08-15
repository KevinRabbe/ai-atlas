# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **392 added test cases**, integrated work through **I23**, architecture-family comparisons **AF01–AF03**, and a persistent crash-aware typed runtime. **Twenty-five provisional implementation-neutral principles** survive their current promotion gates.

No fixed A/B/C/D architecture family is selected as a universal whole-system architecture. Their useful mechanisms increasingly behave like organizational modes that can be activated at different scopes and timescales.

## What the experiments are converging toward

The current evidence increasingly supports a smaller set of recurring laws:

- scope follows coupling, responsibility and causal extent;
- state follows expected future value, recoverability and semantic validity;
- optional work follows marginal value under shared scarcity;
- material complements/substitutes require interaction-aware allocation;
- sharing and structural indirectness follow reusable regularity;
- execution follows state change until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- predictive compression is sufficient only relative to future/action-relevant distinctions and recoverability;
- authority follows independent current invariants, not confidence or historical permission;
- verification follows the residual failure layer;
- **record count does not equal evidence independence**;
- state value does not necessarily identify which publication produced it;
- multi-step consequential change separates preparation from authoritative publication when partial visibility can violate invariants;
- crash recovery follows authoritative identity/provenance rather than local process phase;
- external execution fact and permission to execute again are separately grounded;
- transient cache/credit state is recovered only while future value and typed validity justify persistence/rematerialization/replay.

## Current executable architecture hypothesis

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
evidence-lineage structure
  lineage / staleness / resolves? / conflict
        + learned source-quality estimates
        ↓
consequence-sensitive assurance allocation
        ↓
PREPARE non-authoritative candidate state
        ↓
version + publication-provenance + current-authority fence
        ↓
PUBLISH coherent internal authoritative state
        |
        +--> external effect path
        |       effect-specific external evidence
        |       current authority for every fresh/retry attempt
        |       unresolved status if exact execution cannot be known
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

This is **not** yet a frozen final architecture.

## From architecture families to adaptive organization

I06 shows interacting runtime operations benefit from joint allocation. AF01–AF03 show A/B/C/D are not universal winners: their useful behavior tracks locality, coupling/scarcity, shared transfer and recurrence/variant option value.

AF02 learns organizational mode; AF03 lets different scopes use different modes; I07 learns scope membership itself. I08–I13 turn those laws into a reusable typed runtime with stable semantic identity, dynamic topology, overlapping coordination, directional dependencies, singular leases, epoch-routed events and failure-isolated publication.

## PS-024 — publication and crash recovery

I13/I13B show unfinished topology/resource changes can violate invariants if partially visible. I14 shows a local lifecycle phase cannot tell `already published but marker lost` from `not published`.

I18 adds exact attribution: numeric target version may not be knowable at preparation time, and another publication can independently produce the same target state. `PublicationProtocol` therefore stamps publication provenance into the same modeled authoritative change as resource/topology state.

The selected principle remains **PS-024 — failure-isolated consequential transition publication**. No WAL/database/journal/transaction technology is selected.

## PS-025 — external execution recovery

I15 shows local state cannot prove the external world already acted after crash. Receiver-recognized stable effect identity or exact reconciliation can remove ambiguity when the environment participates; non-identifiable physical effects may remain unresolved.

I16 separates:

```text
external execution evidence -> did it happen?
current capability authority -> may we try again now?
```

This promotes **PS-025 — externally grounded effect recovery / execution-authority separation**.

## I17 / I05C — copied evidence is one failure lineage

External receipts and verifier audits reproduce the same failure. Three copied records are not three independent observations, and raw majority can even pay for one independent check while still ignoring it.

Missing audit resolution is also not positive evidence. Taking more risk may still have positive expected value, but the epistemic state must not claim support that was never observed.

## I20 / I21 — one evidence-assurance substrate

`EvidenceLineageRegistry` represents lineage, staleness, whether an observation resolves the claim, and conflict. It does **not** assign truth/reliability.

`EvidenceAssuranceDecision` combines that structure with learned source-quality estimates, consequence/asymmetric harm and independent-check cost.

I20 applies the same policy to external-execution and metacognitive claims:

- record-count confidence: ~`3.062` utility/task, ~`1.438` harm;
- uniform independent: ~`3.585`, ~`0.733` harm, one check/task;
- **lineage-value:** ~`3.782`, ~`0.592` harm, ~`0.695` checks/task.

I21 routes this planning through `OrganismRecoveryCoordinator` rather than receiving already-trusted receipts.

## I22 / I23 — transient state and whole-lifecycle recovery

I22 shows source-backed hot state can be selectively persisted/rematerialized, while delayed credit requires stable causal identity/version or replayable history after structure changes.

I23 then combines topology publication, crash recovery, hot state, delayed credit, old-epoch events, authority revocation and stale/correlated external evidence in one lifecycle.

Approximate 30-seed means:

| policy | utility/episode | stale hot | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

The result is not merely `do not snapshot`. Safe discard loses useful cache/credit value. Typed recovery retains useful state by asking whether its **semantics** survived, not just its bytes.

## JEPA / E24

JEPA remains explicitly inside the Atlas as a candidate predictive-representation mechanism, not a selected component.

E24 shows that coarse predictive latent state can be efficient yet discard a future/action-relevant distinction. Dense predictive state or compact latent + recoverable source evidence preserves the option.

> Predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

The goal is an AI capable of expanding the shared knowledge frontier through independently verifiable discovery, not merely reproducing humanity's bootstrap knowledge.

## Current provisional selection count

**PS-001 through PS-025** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

## Next milestone

The next major uncertainty is **evidence-lineage inference itself**. Current experiments know which records share a failure lineage. A mature system often will not.

Next discriminate:

- exact supplied lineage metadata;
- similarity/count heuristics;
- learned correlation/causal lineage estimates;
- active lineage-discovery tests;
- unresolved independence when lineage cannot be established cheaply.

The key failure to expose is **false independence**: two sources appear separate but inherit the same hidden upstream failure.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions and typed organizational relationships under finite resources, with semantic boundaries strong enough that **confidence, record count, local phase, historical approval, publication state, evidence lineage, causal identity and current authority cannot impersonate one another**.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
