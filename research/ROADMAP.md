# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis completed first passes on 2026-08-14. Targeted gap closure remains open.

Discovery/epistemic growth is explicit: human knowledge is bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 requires turning uncertainty into testable hypotheses and independently supported new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.**

## Phase 9 — Clean-sheet architecture

First-pass candidate generation completed on 2026-08-14. **Exit gate: PASS.** A/B/C/D remain useful reference organizations, but current Phase-10 evidence treats their mechanisms as conditional modes/scopes rather than mutually exclusive final systems.

## Phase 10 — Experimental reconstruction

**Active. Twenty-four reversible implementation-neutral principles survive their current promotion gates.** The validation history now contains **278 added test cases**.

The experimental strategy has progressed through:

1. isolated mechanism discrimination;
2. integrated epistemic/resource composition;
3. guarded self-improvement;
4. learned metacognition under imperfect feedback;
5. interaction-aware runtime allocation;
6. fixed architecture-family comparison;
7. adaptive organizational modes;
8. simultaneous scoped organization;
9. learned dynamic topology;
10. typed-state migration across topology epochs;
11. independent assurance for structural reconfiguration;
12. a persistent reusable typed-scope runtime API;
13. overlapping/non-owning coordination scopes;
14. directional dependency semantics;
15. partial-failure structural migration;
16. partial-failure singular ownership handoff;
17. version-fenced failure-isolated publication in the reusable runtime.

## Current architecture spine

```text
stable typed semantic identities
  subjects / evidence / provenance / sources
  authority versions / resource leases
        |
        +--> directional dependencies
        |
        +--> disjoint ownership topology
        |       dynamic split / merge
        |
        +--> overlapping non-owning coordination scopes
                temporary or persistent
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocation
        ↓
consequence-sensitive independent assurance
        ↓
PREPARE non-authoritative candidate state
        ↓
version + current-authority publication fence
        ↓
PUBLISH coherent topology / ownership / durable version
        ↓
retire old version / forward in-flight work
        ↓
observe → causal credit → staged appropriately-scoped update
```

The value allocator cannot manufacture epistemic, capability or publication authority.

## I06–I12 — architecture-scale composition

I06 shows that runtime operations such as fidelity, rematerialization, synchronization and intervention interact enough that a joint allocator (~`1.564` utility/task) beats independent operation controllers (~`1.355`).

AF01–AF03 and I07 show organizational mode, scope and membership can all be adaptive state when structural persistence pays for inference/switch/migration cost.

I08 gives dynamic scopes real typed state; I09 adds independent assurance before consequential reconfiguration under correlated evidence.

I10 creates the reusable `TypedScopeRuntime` so later stresses use common identity/authority/topology/event semantics.

I11 separates stable semantic ownership from overlapping coordination membership. I12 separates directional dependence from reciprocal/shared organization. The runtime therefore carries distinct typed relations rather than one generic module graph.

## I13 — partial topology migration failure

Naive in-place migration can fail after only part of the new topology becomes live. At 20% failure probability and ordinary event load it corrupts ~20% of migration attempts, loses ~3.96 events/migration and duplicates ~0.51.

Stop-world, staged and dual-version mechanisms isolate preparation from visible publication and keep those corruption metrics at zero in the family.

The mechanisms cross over with failure risk and live traffic: direct update can win when failure exposure is negligible; blocking can win when traffic is cheap to stop; staged publication wins at ordinary live load; dual-version handoff can win at very high live traffic.

## I13B — singular resource ownership handoff

The second family reproduces the same abstract boundary with a different invariant.

Make-before-break can expose two writers and duplicate work. Break-before-make can expose zero writer and lose work. Stop-world, staged lease publication and dual-read/single-write preserve singular write ownership.

Default 30-seed results favor staged/dual publication (~`0.770–0.774` utility/handoff) over make-before-break (~`0.562`) and break-before-make (~`0.385`).

## PS-024 — failure-isolated consequential transition publication

I13 + I13B satisfy the second-family promotion gate:

> **Prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish authority/ownership/topology only across a coherence boundary after required validation. Select direct, blocking, staged or dual-version publication according to failure risk, blast radius, live-work pressure and isolation cost.**

This is a semantic rule, not a selection of transactions, locks, consensus, blue/green deployment or another named implementation.

## I13C — reusable publication protocol

`PublicationProtocol` now encodes the rule explicitly:

- prepare topology/resource handoff without changing live authority/ownership;
- remember the topology epoch or lease version the candidate was prepared against;
- require sufficient independent assurance where consequence demands it;
- re-read current capability authority at publication time;
- reject stale prepared plans;
- publish the coherent version/lease change;
- discard without changing live state.

The protocol therefore handles two important races:

1. two topology plans prepared from epoch N cannot both publish after one advances to N+1;
2. a resource handoff prepared before a revocation cannot inherit the old permission at publish time.

## JEPA / E24

JEPA remains a candidate mechanism, not a commitment. E24 shows latent prediction can be efficient while passive predictive sufficiency fails under future objectives/interventions. Recoverable source evidence improves the compression/optionality frontier.

No JEPA-specific principle is selected.

## Current provisional selection count

**PS-001 through PS-024** are active reversible constraints.

## Next milestone — live handoff + revocation + crash recovery

### I14A — authority changes during staged/dual handoff

Run queued external work while:

- a topology/resource candidate is prepared;
- authority is revoked or granted mid-handoff;
- old and new versions may coexist briefly;
- events from old topology epochs remain in flight.

Required invariants:

- current categorical authority wins at execution/publication;
- no prepared copy can reactivate revoked authority;
- no duplicate external effect across versions;
- stale assurance/version tokens cannot publish after relevant authority/version changes.

### I14B — crash/restart between prepare and publish

Crash at different lifecycle points:

- before preparation complete;
- after preparation but before assurance;
- after assurance but before publication;
- immediately after publication before old-version cleanup.

Do **not** assume a write-ahead log/database first.

Compare the minimum persisted facts required to determine safely after restart whether to:

- discard the candidate;
- resume preparation;
- publish;
- retain the current old version;
- finish retiring an already-published old version.

Only if recovery cannot be solved from already-required version/semantic state should a new durable intent/log mechanism be added.

## Later targeted work

- partial migration of bounded caches and delayed credit traces;
- I05C correlated/adversarial evaluator audits and partially unresolved outcomes;
- nested/overlapping **ownership** only if non-owning coordination overlays prove insufficient;
- neural E24C only if predictive-objective geometry remains architecture-discriminating;
- hardware co-design only after transition/topology/fidelity laws are stable enough for substrate assumptions to be informative.

## Phase-10 substantial-completion condition

Before Phase 10 is considered substantially complete, the combined organism should show that:

- selected principles retain lifetime value under composition;
- learned metacontrol overhead does not consume the gains;
- authority/provenance remain stable under learned control, topology changes and multi-version handoffs;
- world/tool/evaluator/self uncertainty remain distinguishable;
- self-change uses independent refreshing evidence and scoped rollback/change;
- failures remain attributable enough to revise mechanisms;
- unsupported transitions can remain tentative/unresolved;
- crash/restart cannot turn prepared but unpublished state into accidental authority;
- the common executable runtime reproduces important boundaries without experiment-specific privileged semantics.

## Open targeted gap closure

Add literature only when it materially changes an active experimental/design decision. The Atlas optimizes discriminatory evidence, not source count.
