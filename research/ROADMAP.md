# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis completed first passes on 2026-08-14. Targeted gap closure remains open.

Discovery/epistemic growth is explicit: human knowledge is bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 requires turning uncertainty into testable hypotheses and independently supported new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.**

## Phase 9 — Clean-sheet architecture

First-pass candidate generation completed on 2026-08-14. **Exit gate: PASS.** A/B/C/D remain useful reference organizations, but current Phase-10 evidence treats their mechanisms as conditional modes/scopes rather than mutually exclusive final systems.

## Phase 10 — Experimental reconstruction

**Active. Twenty-five reversible implementation-neutral principles survive their current promotion gates.** The validation history now contains **308 added test cases**.

The experimental strategy has progressed through:

1. isolated mechanism discrimination;
2. integrated epistemic/resource composition;
3. guarded self-improvement;
4. learned metacognition under imperfect feedback;
5. interaction-aware runtime allocation;
6. architecture-family Pareto comparison;
7. adaptive organizational modes/scopes/topology;
8. typed-state migration and structural assurance;
9. persistent reusable typed-scope runtime;
10. overlapping coordination and directional dependencies;
11. partial-failure topology/resource publication;
12. version-fenced failure-isolated publication;
13. crash/restart recovery from base/target semantic identity;
14. external-effect recovery across receiver-identifiable and non-identifiable environments;
15. separation of historical execution evidence from current capability authority.

## Current architecture spine

```text
stable typed semantic identities
  subjects / evidence / provenance / sources
  authority versions / resource leases
        |
        +--> directional dependencies
        +--> dynamic ownership topology
        +--> overlapping non-owning coordination scopes
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocation
        ↓
consequence-sensitive independent assurance
        ↓
PREPARE non-authoritative candidate state
        ↓
version / target / current-authority publication fence
        ↓
PUBLISH coherent internal authoritative version
        |
        +--> external effect path
        |       effect-specific external execution evidence
        |       current authority for every new/retry attempt
        |       unresolved state when execution cannot be identified
        ↓
crash recovery from semantic base/target identity
        ↓
observe → causal credit → staged appropriately-scoped update
```

The value allocator cannot manufacture epistemic, capability, publication or external-execution authority.

## I06–I13 — architecture-scale composition

I06 shows that runtime operations interact enough that joint allocation (~`1.564` utility/task) beats factorized control (~`1.355`). AF01–AF03 and I07 show organizational mode/scope/membership can all be adaptive when persistence pays for switching/migration. I08–I10 move stable semantic state through live topology and make that substrate reusable. I11/I12 split ownership, overlapping coordination and directional dependency into distinct relations.

I13/I13B expose partial visibility as a first-class failure mode. Naive topology mutation can leave mixed routing state; naive writer handoff can produce two writers or zero writer. Staged/blocking/dual-version mechanisms preserve invariants under different load/failure economics.

### PS-024 — failure-isolated consequential transition publication

> **Prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish authority/ownership/topology only across a coherence boundary after required validation. Select direct, blocking, staged or dual-version publication according to failure risk, blast radius, live-work pressure and isolation cost.**

`PublicationProtocol` implements prepared-against topology/lease versions, current-authority re-check and stale-plan rejection without selecting a storage/transaction technology.

## I14 — crash/restart around the publication fence

I14 tests resource ownership and durable-knowledge promotion across crashes in prepared, assured, published-but-unmarked, published-and-marked and superseded states.

Phase + old approval is insufficient. It cannot tell whether publication already became authoritative just before the crash and can overwrite newer state. Re-checking current authority/evidence prevents revoked/retracted retries but still cannot solve already-published or superseded ambiguity.

The minimum surviving semantics are currently:

```text
stable publication identity
expected base authoritative version
intended target version
target identity/digest
references needed to reacquire current validation
```

`RecoveryRecord` deliberately does not persist old approval as standing authority.

## I15 — crash ambiguity at an external side effect

Internal version fencing cannot prove that the external world already acted.

An externally recognized stable effect identity or exact effect-specific reconciliation removes retry ambiguity in the identifiable family. Their overhead only earns itself when duplicate/omission consequence is high enough.

A second physical/non-identifiable family demonstrates the hard boundary: if the environment cannot attribute observed state to this particular effect, noisy sensing cannot reconstruct exact history. Recovery must retain uncertainty and choose retry/abstention according to consequence.

## I16 — historical execution vs permission to execute again

Current capability authority and external execution evidence are separately grounded.

30-seed default means:

- authority-only: ~`-0.560` utility, ~32.4% duplicate effects, ~17.6% history error;
- evidence-only: ~`0.379` utility, ~9.8% unauthorized retries;
- revocation-erases-history: ~`0.705` utility, ~17.6% history error;
- **separated:** ~`0.969` utility, zero modeled duplicate, unauthorized-retry and history errors.

This promotes:

### PS-025 — externally grounded effect recovery / execution-authority separation

> **Local intent, phase state or past approval do not establish that an external effect occurred. Recover exact execution from sufficiently effect-specific external evidence or receiver-recognized identity; gate every fresh/retry effect by current authority. If exact execution cannot be identified, preserve an unresolved state and price retry versus abstention explicitly.**

This is a semantic rule, not a selection of an idempotency-key API, outbox, distributed transaction, remote receipt store or sensor technology.

## JEPA / E24

JEPA remains a candidate mechanism, not a commitment. E24 shows latent prediction can be efficient while passive predictive sufficiency fails under future objectives/interventions. Recoverable source evidence improves the compression/optionality frontier.

No JEPA-specific principle is selected.

## Current provisional selection count

**PS-001 through PS-025** are active reversible constraints.

## Next milestone — corrupt external execution evidence

The next discriminator should attack the evidence plane PS-025 now relies on.

Test effect recovery when receipts/observations are:

- delayed;
- stale;
- duplicated/correlated rather than independent;
- contradictory;
- partially unavailable;
- adversarially biased toward retry or completion.

Compare:

1. trust-one-source recovery;
2. confidence/majority aggregation;
3. effect-specific source precedence/provenance;
4. independent reconciliation purchased according to consequence;
5. unresolved-state retention when evidence conflict cannot be resolved cheaply.

Primary metrics:

- duplicate external effects;
- omitted effects;
- unauthorized retries;
- false historical completion;
- unresolved lifetime/cost;
- reconciliation spend;
- recovery latency.

The key falsifier is whether ordinary confidence aggregation can match typed provenance/independence-aware recovery after equal evidence cost.

## Integration after that discriminator

Move `RecoveryRecord` and `ExternalEffectProtocol` into the reusable organism execution lifecycle so later experiments do not get privileged recovery semantics.

Then return to:

- I05C correlated/adversarial evaluator audits with partially unresolved outcomes;
- bounded-cache and delayed-credit survival across structural recovery;
- nested/overlapping **ownership** only if non-owning coordination overlays prove insufficient;
- neural E24C only if predictive-objective geometry remains architecture-discriminating;
- hardware co-design only after transition/topology/fidelity/recovery laws are stable enough for substrate assumptions to be informative.

## Phase-10 substantial-completion condition

Before Phase 10 is considered substantially complete, the combined organism should show that:

- selected principles retain lifetime value under composition;
- learned metacontrol overhead does not consume the gains;
- authority/provenance remain stable under learned control, topology changes, multi-version handoffs and crash recovery;
- world/tool/evaluator/self uncertainty remain distinguishable;
- self-change uses independent refreshing evidence and scoped rollback/change;
- failures remain attributable enough to revise mechanisms;
- unsupported transitions can remain tentative/unresolved;
- crash/restart cannot turn prepared state or old approval into accidental authority;
- external effect recovery does not confuse local intent, historical execution and current capability permission;
- the common executable runtime reproduces these boundaries without experiment-specific privileged semantics.

## Open targeted gap closure

Add literature only when it materially changes an active experimental/design decision. The Atlas optimizes discriminatory evidence, not source count.
