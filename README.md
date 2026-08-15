# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **308 added test cases**, integrated work through **I16**, architecture-family comparisons **AF01–AF03**, and a persistent reusable architecture substrate. **Twenty-five provisional implementation-neutral principles** survive their current promotion gates.

No fixed A/B/C/D architecture family is selected as a universal whole-system architecture. Their useful mechanisms increasingly behave like organizational modes that can be activated at different scopes and timescales.

## What the experiments are converging toward

The current evidence increasingly supports a smaller set of recurring laws:

- scope follows coupling, responsibility and causal extent;
- state follows expected future value and recoverability;
- optional work follows marginal value under shared scarcity;
- material complements/substitutes require interaction-aware allocation;
- sharing and structural indirectness follow reusable regularity;
- execution follows state change until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- predictive compression is sufficient only relative to future/action-relevant distinctions and recoverability;
- authority follows independent current evidence/invariants, not confidence alone;
- verification follows the residual failure layer;
- durable change requires stronger and refreshing evidence;
- organizational mode, scope and membership may themselves be adaptive state;
- ownership, coordination, directional dependence, authority, provenance and resource identity are different typed relationships;
- multi-step consequential change separates preparation from authoritative publication whenever partial visibility can violate invariants;
- crash recovery follows authoritative version/target identity rather than local process phase;
- **external execution fact and permission to execute again are separate evidence/authority questions.**

## Current executable architecture hypothesis

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
interaction-aware value/resource allocator
        ↓
consequence-sensitive independent assurance
        ↓
PREPARE non-authoritative candidate state
        ↓
version + target + current-authority publication fence
        ↓
PUBLISH coherent internal authoritative version
        |
        +--> external effect path
        |       externally grounded execution evidence
        |       current authority for every new/retry attempt
        |       unresolved status if exact execution cannot be known
        ↓
recover from semantic identity/version after crash
        ↓
observe → causal credit → staged appropriately-scoped update
```

This is **not** yet a frozen final architecture.

## I06–I13 — adaptive organization becomes an executable typed runtime

I06 combines fidelity, source rematerialization/hot state, synchronization and intervention in one finite budget. Learned joint allocation reaches ~`1.564` utility/task versus ~`1.355` for factorized independent controllers.

AF01–AF03 show that A/B/C/D behave as regime-dependent organizational modes. AF02 learns mode selection; AF03 shows multiple modes can coexist at different scopes; I07 learns scope membership itself from changing dependency evidence.

I08 migrates real typed state through topology epochs; I09 adds independent assurance under correlated topology evidence. I10 turns those semantics into reusable `TypedScopeRuntime`.

I11 separates overlapping coordination from ownership. I12 separates one-way dependency from reciprocity. I13/I13B show that unfinished consequential change cannot safely leak into authoritative topology/resource ownership when partial failure is meaningful.

This promotes **PS-024 — failure-isolated consequential transition publication**.

## I14 — crash recovery is not a phase flag

I14 crashes both resource ownership and durable-knowledge promotion around the publication fence.

A remembered `prepared/assured/published` phase fails because publication can become authoritative immediately before a crash while the local completion marker is lost. Across the synthetic 30-seed crash distribution, phase-based recovery is correct only ~`0.62` of the time and duplicates publication ~`0.22` of the time.

Version-fenced recovery reaches exact modeled recovery by retaining only the required semantics:

```text
stable publication identity
expected base authoritative version
intended target version + target identity/digest
references needed to reacquire current validation
```

Old approval is **not** persisted as standing authority. Any retry re-resolves current authority/evidence.

This strengthens PS-024 without selecting a WAL, database transaction, journal or event-sourcing implementation.

## I15 — local state cannot prove the external world acted

For an external service that recognizes a stable effect identity, deduplicated replay or exact reconciliation removes crash retry ambiguity. At the default high duplicate consequence, stable external identity reaches ~`0.9825` utility versus ~`-1.161` blind retry.

But the result is conditional: when duplicate harm is nearly zero and identity/reconciliation overhead is deliberately expensive, blind retry can be cheaper.

A second family removes the cooperative API assumption. A physical/non-identifiable effect can only be inferred through a noisy aggregate sensor. Exact history cannot be recovered: the system must retain uncertainty and choose retry versus abstention from consequence.

## I16 — execution evidence is not retry authority

I16 composes effect-specific external evidence with current capability revocation.

The separated policy reaches ~`0.969` utility with zero modeled duplicates, unauthorized retries and history errors. Conflating the two questions creates three different failures:

- authority-only recovery duplicates ~32.4% of ambiguous prior effects and misrecords ~17.6%;
- evidence-only recovery retries after revocation ~9.8% of the time;
- treating revocation as historical non-execution misrecords ~17.6% of already-applied effects.

This promotes:

> **PS-025 — externally grounded effect recovery / execution-authority separation:** local intent, phase state or past approval cannot establish that an external effect occurred. Determine exact execution from sufficiently effect-specific external evidence or receiver-recognized identity; gate every fresh/retry effect by current authority. If exact execution cannot be identified, preserve unresolved state and price retry versus abstention explicitly.

The selected object is the semantic boundary, not an HTTP idempotency key, outbox, distributed transaction, receipt database or sensor technology.

## JEPA / E24

JEPA remains explicitly inside the Atlas as a candidate predictive-representation mechanism, not a selected component.

E24 shows that coarse predictive latent state can be highly efficient yet discard a future/action-relevant distinction. Dense predictive state or compact latent + recoverable source evidence preserves the option.

> Predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

The goal is an AI capable of expanding the shared knowledge frontier through independently verifiable discovery, not merely reproducing humanity's bootstrap knowledge.

## Current provisional selection count

**PS-001 through PS-025** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

## Next milestone

The next stress attacks **external execution evidence itself**:

- delayed receipts;
- stale receipts;
- correlated/duplicated evidence sources;
- contradictory external observations;
- high-consequence cases where independent reconciliation may earn its cost.

Then the I14 recovery record and PS-025 external-effect protocol should be integrated into `TypedScopeRuntime`, so crash/recovery is part of the common organism rather than a side experiment.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions and typed organizational relationships under finite resources, with semantic boundaries strong enough that **confidence, local phase, historical approval and current authority cannot impersonate one another**.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
