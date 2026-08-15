# Phase 10 Experimental Status

**Checkpoint: twenty-five provisional design principles selected; composition has progressed through I16 plus the reusable typed-scope runtime. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **308 added test cases**.

Architecture/composition additions since the 190-test metacognitive/JEPA checkpoint:

- I06 interaction-aware runtime allocation: 6 tests;
- AF01 fixed-family Pareto benchmark: 5;
- AF02 adaptive organizational mode: 6;
- AF03 simultaneous scoped organization: 5;
- I07 dynamic scope formation: 5;
- I08 typed dynamic-scope runtime: 6;
- I09 topology assurance: 6;
- I10 persistent typed-scope organism API: 8;
- I10 end-to-end API scenario: 5;
- I11 overlapping/cross-cutting scopes: 6;
- non-owning coordination-scope registry: 3;
- I12 directional dependencies: 6;
- typed directional-dependency registry: 3;
- I13 partial topology/structural commit: 6;
- I13B singular resource/service ownership handoff: 6;
- I13C publication-fence runtime semantics: 6;
- I14 crash/restart recovery: 6;
- minimal recovery protocol: 6;
- I15 external-effect crash ambiguity: 6;
- I16 execution-evidence / current-authority separation: 6;
- external-effect recovery protocol: 6.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Current architecture checkpoint

## I06–I12 — from common allocation to typed dynamic organization

I06 shows that fidelity, rematerialization, synchronization and intervention interact enough that a joint allocator (~`1.564` utility/task) beats independent operation controllers (~`1.355`).

AF01–AF03 and I07 show that organizational mode, organizational scope and scope membership can all be revisable state, but plasticity only pays when dependency structure persists long enough to amortize inference/switch/migration cost.

I08 puts exact evidence/provenance, predictive source references, versioned authority, singular resource leases and in-flight events behind topology epochs. The typed-epoch runtime reaches ~`1.0744` utility/step versus ~`0.9957` static typed topology while preserving the tested routing, authority, provenance, rematerialization and resource-uniqueness invariants.

I09 shows topology proposal evidence is not automatically topology-promotion evidence: under correlated spoofing, selective independent checking raises attacked pairwise topology accuracy to ~`0.933` with zero harmful accepted migrations in the matched family.

I10 converts those boundaries into reusable `TypedScopeRuntime`. I11 separates semantic ownership from overlapping non-owning coordination membership. I12 separates directional dependence from reciprocity/shared organization.

## I13 / I13B / I13C — publication is a typed transition boundary

I13 fails topology migration after a random subset of moves. At 20% failure probability and ordinary event load, naive in-place mutation corrupts ~20.2% of attempts, loses ~3.96 events and duplicates ~0.51. Stop-world, staged and dual-version mechanisms isolate unfinished state from authoritative routing and keep those modeled corruption metrics at zero.

I13B reproduces the boundary with singular resource ownership: make-before-break can expose two writers; break-before-make can expose zero writer. Failure-isolated mechanisms preserve singular write ownership.

I13C makes this executable through `PublicationProtocol`: topology epoch / lease-version fences, current-authority re-check, independent assurance and discard semantics prevent stale prepared plans from publishing.

### PS-024 — failure-isolated consequential transition publication

> **Prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish authority/ownership/topology only across a coherence boundary after required validation. Choose direct, blocking, staged or dual-version publication according to partial-failure risk, blast radius, live-work pressure and isolation cost.**

## I14 — crash/restart requires semantic publication identity, not a remembered phase

I14 crashes resource ownership and durable-knowledge promotion in five lifecycle states: prepared, assured, published-but-unmarked, published-and-marked, or superseded.

30-seed means:

| recovery policy | resource correct | knowledge correct | duplicate publish | superseded overwrite |
|---|---:|---:|---:|---:|
| old assurance replay | ~0.599 | ~0.594 | ~0.220 | ~0.160 |
| phase + current recheck | ~0.620 | ~0.620 | ~0.220 | ~0.160 |
| **version-fenced** | **1.000** | **1.000** | **0** | **0** |
| ideal atomic snapshot | **1.000** | **1.000** | **0** | **0** |

Old assurance replay additionally publishes after current resource revocation (~2.1%) or knowledge-source retraction (~2.6%). Current recheck fixes those authority/evidence failures but cannot tell `already published but marker lost` from `not published` and cannot prevent superseded overwrite.

`RecoveryRecord` therefore stores only the implementation-neutral semantics required to classify recovery:

- stable publication identity;
- expected base authoritative version;
- intended target version;
- target identity/digest;
- references needed to reacquire current validation.

It intentionally does **not** persist an `approved=true` bit as authority. A retry must satisfy current validation/assurance again.

## I15 — local recovery stops at the external-world boundary

I15 tests an effect whose authoritative fact is outside the organism.

### Externally identifiable ledger/service

Default duplicate penalty `4`, missed penalty `1`:

| policy | utility | duplicate | missed |
|---|---:|---:|---:|
| blind retry | ~-1.161 | ~0.540 | 0 |
| **stable externally recognized identity** | **~0.9825** | **0** | **0** |
| exact external reconciliation | ~0.9580 | **0** | **0** |
| abstain | ~0.8398 | 0 | ~0.160 |

The result has a cost/consequence crossover. With identity cost `0.10`, reconciliation cost `0.15` and duplicate harm only `0.01`, blind retry (~0.995) is cheaper than carrying exact recovery semantics (~0.930 stable identity). Once duplicate consequence rises, exact external grounding earns its cost.

### Non-identifiable physical effect

When the environment cannot recognize this effect identity, only a noisy aggregate sensor is available. Exact recovery is impossible in the model: sensor reconciliation leaves both duplicate (~5.8%) and omitted (~3.9%) effects.

When duplicate harm dominates, abstention/risk-sensitive no-retry is rational. When omission harm dominates, retry after sufficiently negative sensor evidence becomes rational. The state remains epistemically unresolved rather than being forced into a false exact history.

## I16 — execution evidence and execution authority are separate

I16 adds current capability revocation to external recovery.

30-seed means:

| policy | utility | duplicate | unauthorized retry | history error |
|---|---:|---:|---:|---:|
| authority only | ~-0.560 | ~0.324 | 0 | ~0.176 |
| evidence only | ~0.379 | 0 | ~0.098 | 0 |
| revocation erases history | ~0.705 | 0 | 0 | ~0.176 |
| **separated** | **~0.969** | **0** | **0** | **0** |

The surviving semantics are:

```text
external execution evidence
        -> did the old effect happen?

current capability authority
        -> may a NEW attempt be issued now?
```

A revocation cannot rewrite a historical effect as absent, and an old effect/receipt cannot authorize a new retry.

### PS-025 — externally grounded effect recovery / execution-authority separation

> **Local intent, phase state or past approval do not establish that an external effect occurred. Recover exact execution from sufficiently effect-specific external evidence or receiver-recognized identity; gate every new/retry effect by current capability authority. When exact external execution cannot be identified, retain an unresolved state and price retry versus abstention by explicit consequence rather than fabricating certainty.**

The selected object is the semantic boundary, not an HTTP idempotency key, outbox, distributed transaction, receipt database or sensor technology.

---

# Current provisional selections

**PS-001 through PS-025** are active reversible constraints. PS-024 covers failure-isolated internal consequential publication; PS-025 covers the point where execution authority/fact lives outside the organism.

---

# Current executable architecture hypothesis

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
version/current-authority publication fence
        ↓
PUBLISH coherent internal authoritative version
        |
        +--> if external effect:
        |       external effect identity/evidence
        |       + current authority for any new attempt
        |       + unresolved state if execution cannot be identified
        ↓
retire old version / forward in-flight work
        ↓
observe → causal credit → staged appropriately-scoped update
```

The strongest new inference is:

> **Crash recovery cannot be derived from local process phase. Internal authority is recovered from version + identity; external execution is recovered from external effect-specific evidence. Past approval is evidence history, never standing authority to retry.**

This remains a falsifiable candidate architecture, not a final implementation.

## Next high-value work

1. attack external execution evidence itself with delayed, stale, correlated and contradictory sources; measure when independent reconciliation earns its cost;
2. integrate `RecoveryRecord` and external-effect recovery decisions into the reusable organism runtime rather than leaving them as side protocols;
3. return to I05C correlated/adversarial evaluator audits with partially unresolved outcomes—the same evidence-identity problem now appears in metacognition;
4. test bounded-cache / delayed-credit survival across structural recovery;
5. neural E24C remains conditional on representation geometry still being architecture-discriminating.

## Guardrail

Self-improvement, topology/resource publication and external effect recovery remain typed transitions. No proposal score, stale assurance, prepared candidate, local phase marker or historical permission may manufacture current authority or external execution fact.
