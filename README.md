# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **412 added test cases**, integrated work through **I25**, architecture-family comparisons **AF01–AF03**, and a persistent crash-aware typed runtime plus learned evidence-dependence substrate. **Twenty-six provisional implementation-neutral principles** survive their current promotion gates.

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
- record count does not equal evidence independence;
- **evidence independence itself may be unknown, stale, learned and actively tested**;
- raw co-failure is not enough to prove shared ancestry because common causes can correlate independent sources;
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
source identity + known provenance where available
        + learned source-quality estimates
        + revisable EvidenceDependenceModel
            context-conditioned failure relations
            optional provenance/dependency probes
        ↓
effective independent evidence structure
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

`EvidenceLineageRegistry` represents known lineage, staleness, whether an observation resolves the claim, and conflict. It does **not** assign truth/reliability.

`EvidenceAssuranceDecision` combines that structure with learned source-quality estimates, consequence/asymmetric harm and independent-check cost.

I20 applies the same policy to external-execution and metacognitive claims:

- record-count confidence: ~`3.062` utility/task, ~`1.438` harm;
- uniform independent: ~`3.585`, ~`0.733` harm, one check/task;
- **lineage-value:** ~`3.782`, ~`0.592` harm, ~`0.695` checks/task.

I21 routes this planning through `OrganismRecoveryCoordinator` rather than receiving already-trusted receipts.

## I22 / I23 — transient state and whole-lifecycle recovery

I22 shows source-backed hot state can be selectively persisted/rematerialized, while delayed credit requires stable causal identity/version or replayable history after structure changes.

I23 combines topology publication, crash recovery, hot state, delayed credit, old-epoch events, authority revocation and stale/correlated external evidence in one lifecycle.

Approximate 30-seed means:

| policy | utility/episode | stale hot | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

The result is not merely `do not snapshot`. Safe discard loses useful cache/credit value. Typed recovery retains useful state by asking whether its **semantics** survived, not just its bytes.

## I24 — hidden evidence-lineage inference

I24 removes the convenient assumption that failure-lineage IDs are supplied exactly.

Six stable source identities share three hidden upstream failure processes. The organism sees only source outputs plus claims that later receive sufficiently independent resolution. At the midpoint, the hidden dependencies change while the visible source identities stay the same.

Approximate 30-seed result:

| policy | utility/task | weighted harm | independent audits/task |
|---|---:|---:|---:|
| assume source-count independence | ~4.157 | ~0.296 | ~0.277 |
| assume all sources correlated | ~4.002 | ~0.331 | ~0.865 |
| **learn hidden dependence** | **~4.196** | **~0.232** | ~0.437 |
| learned + active dependency probe | ~4.194 | **~0.221** | ~0.423 |
| oracle dependence | ~4.213 | ~0.216 | ~0.408 |

The passive learner recovers the hidden pair relationships, loses accuracy when upstream dependencies change, and relearns them. A value-priced explicit dependency/provenance probe accelerates recovery only where that relation can alter assurance behavior.

## I25 / PS-026 — evidence dependence needs causal qualification

Raw co-failure has a dangerous confounder: unrelated evaluators can fail together simply because the same task is difficult.

I25 adds a global hard-task common cause to a second hidden-lineage family. Conditioning the dependence model on a noisy observed difficulty context improves utility and reduces unnecessary audits; controlled dependency probes reduce harm further.

Approximate 10-seed result:

| policy | utility/task | weighted harm | independent audits/task |
|---|---:|---:|---:|
| raw co-failure | ~4.116 | ~0.296 | ~0.433 |
| **difficulty-conditioned** | **~4.149** | ~0.294 | **~0.337** |
| conditioned + active probe | ~4.145 | **~0.277** | ~0.335 |
| oracle dependence | ~4.165 | ~0.281 | ~0.337 |

This promotes:

> **PS-026 — learned / causally qualified evidence dependence:** treat independence between evidence sources as uncertain, revisable relational state. Do not infer independent failure modes from record count, source names, agreement or raw co-failure alone. Infer dependence from outcome/provenance/intervention evidence while conditioning on plausible common causes, and buy explicit dependency evidence when uncertainty about independence materially changes assurance value.

`EvidenceDependenceModel` is the current small executable substrate. It is **not** a selection of covariance clustering, causal discovery, provenance graphs or another mature dependence-learning implementation.

## JEPA / E24

JEPA remains explicitly inside the Atlas as a candidate predictive-representation mechanism, not a selected component.

E24 shows that coarse predictive latent state can be efficient yet discard a future/action-relevant distinction. Dense predictive state or compact latent + recoverable source evidence preserves the option.

> Predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

The goal is an AI capable of expanding the shared knowledge frontier through independently verifiable discovery, not merely reproducing humanity's bootstrap knowledge.

PS-026 matters directly here: ten apparently different confirmations are not ten independent experiments if they inherit the same hidden assumption, dataset, instrument or derivation.

## Current provisional selection count

**PS-001 through PS-026** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

## Next milestone

The next evidence-dependence stresses should test:

- **domain-conditional dependence** — two sources may share failure ancestry for one claim family but not another;
- **directional dependence** — copied/derived source B may depend on A without A depending on B;
- adversarial sources that intentionally decorrelate visible mistakes while sharing hidden ancestry;
- sparse feedback and large source populations where pairwise modeling may cost more than it saves.

The next integration step is to let the common assurance path consume learned dependence directly, using exact lineage metadata only when it is genuinely known.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions and typed organizational relationships under finite resources, with semantic boundaries strong enough that **confidence, record count, source identity, evidence dependence, local phase, historical approval, publication state, causal identity and current authority cannot impersonate one another**.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
