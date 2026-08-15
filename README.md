# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **377 added test cases**, integrated work through **I22**, architecture-family comparisons **AF01–AF03**, and a persistent crash-aware typed runtime. **Twenty-five provisional implementation-neutral principles** survive their current promotion gates.

No fixed A/B/C/D architecture family is selected as a universal whole-system architecture. Their useful mechanisms increasingly behave like organizational modes that can be activated at different scopes and timescales.

## What the experiments are converging toward

The current evidence increasingly supports a smaller set of recurring laws:

- scope follows coupling, responsibility and causal extent;
- state follows expected future value, recoverability and validity after change;
- optional work follows marginal value under shared scarcity;
- material complements/substitutes require interaction-aware allocation;
- sharing and structural indirectness follow reusable regularity;
- execution follows state change until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- predictive compression is sufficient only relative to future/action-relevant distinctions and recoverability;
- authority follows independent current invariants, not confidence or historical permission;
- verification follows the residual failure layer;
- **record count does not equal evidence independence**;
- publication state value does not necessarily identify which transition produced it;
- multi-step consequential change separates preparation from authoritative publication when partial visibility can violate invariants;
- crash recovery follows authoritative base/version/target/publication provenance rather than local process phase;
- external execution fact and permission to execute again are separate evidence/authority questions;
- transient cache/credit state is recovered only while future value and semantic validity justify persistence/rematerialization/replay.

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
selective persist / rematerialize / replay of transient state
        ↓
observe → versioned causal credit → staged appropriately-scoped update
```

This is **not** yet a frozen final architecture.

## From architecture families to adaptive organization

I06 combines fidelity, source rematerialization/hot state, synchronization and intervention in one finite budget. Joint allocation reaches ~`1.564` utility/task versus ~`1.355` factorized control.

AF01–AF03 show A/B/C/D are not universal winners. Their useful behavior tracks locality, coupling/scarcity, shared transfer and recurrence/variant option value. AF02 learns organizational mode; AF03 lets different scopes use different modes; I07 learns scope membership itself.

I08–I13 turn those laws into a reusable typed runtime with stable semantic identity, dynamic topology, overlapping coordination, directional dependencies, singular leases, epoch-routed events and failure-isolated publication.

## PS-024 — publication and crash recovery

I13/I13B show unfinished topology/resource changes can violate invariants if partially visible. I14 shows a local lifecycle phase cannot tell `already published but marker lost` from `not published`.

I18 adds a deeper attribution result: exact numeric target version may not be knowable at preparation time, and another publication can independently produce the same target state. Recovery therefore distinguishes:

```text
what state is authoritative?
        !=
which publication produced it?
```

`PublicationProtocol` now stamps publication provenance at the same modeled coherence boundary as resource/topology authority. `RecoveryRecord.target_version` can be optional when publication provenance identifies the committed transition.

The selected principle remains **PS-024 — failure-isolated consequential transition publication**; no WAL/database/journal/transaction implementation is selected.

## PS-025 — external execution recovery

I15 shows local state cannot prove the external world already acted after a crash. Receiver-recognized stable effect identity or exact effect-specific reconciliation can remove ambiguity when the environment participates; non-identifiable physical effects may remain unresolved.

I16 then separates historical execution from current permission:

```text
external execution evidence -> did it happen?
current capability authority -> may we try again now?
```

This promotes **PS-025 — externally grounded effect recovery / execution-authority separation**.

## I17 / I05C — correlated evidence is one failure lineage

Three copied receipts or audits are not three independent observations.

I17 reproduces this for external execution; I05C reproduces it for the organism's own verifier-quality learning. Raw majority can even pay for one genuinely independent check and still ignore it by outvoting it with three copies from one source lineage.

Missing audit resolution is also not positive evidence. Treating it as success can raise throughput in one synthetic regime, but worsens calibration and increases false durable writes.

## I20 / I21 — one evidence-assurance substrate

`EvidenceLineageRegistry` represents lineage, staleness, whether an observation resolves the claim, and conflict. It does **not** assign truth/reliability.

`EvidenceAssuranceDecision` combines that structure with learned source-quality estimates, consequence/asymmetric harm and independent-check cost.

I20 applies the same policy to external-execution and metacognitive claims:

- record-count confidence: ~`3.062` utility/task, ~`1.438` harm;
- uniform independent: ~`3.585`, ~`0.733` harm, one check/task;
- **lineage-value:** ~`3.782`, ~`0.592` harm, ~`0.695` checks/task.

I21 moves that planning inside `OrganismRecoveryCoordinator`, removing the privileged assumption that external receipts arrive already interpreted as trustworthy.

## I22 — transient state across recovery

Source-backed hot/predictive state should not automatically survive a crash. Adaptive persistence/rematerialization reaches ~`0.3335` utility/item versus ~`0.3278` rematerialize-all and ~`0.2314` persist-all, while greatly reducing stale cache reuse.

Delayed credit has a different validity condition. Unversioned positional restoration creates ~`15.3%` false blame after structure changes; exact causal transition identity/version removes it. When exact trace persistence becomes expensive, retained source history can be replayed instead.

So recovery obeys the same value law as normal runtime, but **validity is typed**: currentness for cache, causal identity for credit.

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

Implement the minimal typed transient-state registry implied by I22:

- source-backed hot state with rematerialization reference + generation context;
- delayed credit eligibility tied to stable transition identity/version, optionally replayable from retained source history.

Then run a real topology/publication crash scenario where authoritative recovery, external evidence, hot-state recovery, in-flight events and delayed credit coexist.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions and typed organizational relationships under finite resources, with semantic boundaries strong enough that **confidence, record count, local phase, historical approval, publication state, evidence lineage, causal identity and current authority cannot impersonate one another**.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
