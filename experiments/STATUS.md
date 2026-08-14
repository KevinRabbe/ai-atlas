# Phase 10 Experimental Status

**Checkpoint: twenty-four provisional design principles selected; composition has progressed through I13C plus the reusable typed-scope runtime. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **278 added test cases**.

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
- I13C publication-fence runtime semantics: 6.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Current architecture checkpoint

## I06–I12 — from common allocation to typed dynamic organization

I06 shows that runtime operations such as fidelity, rematerialization, synchronization and intervention interact enough that a joint allocator (~`1.564` utility/task) beats independent operation controllers (~`1.355`).

AF01–AF03 and I07 then show that organizational mode, organizational scope and scope membership can all be revisable state, but plasticity only pays when dependency structure persists long enough to amortize inference/switch/migration cost.

I08 puts exact evidence/provenance, predictive source references, versioned authority, singular resource leases and in-flight events behind real topology epochs. The typed-epoch runtime reaches ~`1.0744` utility/step versus ~`0.9957` static typed topology while preserving zero tested failures across event routing, authority, provenance, rematerialization and resource uniqueness.

I09 shows topology proposal evidence is not automatically topology-promotion evidence: under correlated spoofing, selective independent checking raises attacked pairwise topology accuracy to ~`0.933` with zero harmful accepted migrations in the matched family.

I10 converts those boundaries into the reusable `TypedScopeRuntime`, with exact semantic records, typed proposals, interaction-aware allocation, independent assurance, staged scope change/rollback and topology-epoch event forwarding.

I11 separates semantic ownership from coordination membership. Sparse cross-cutting work favors temporary non-owning overlays; frequent recurrence can justify persistent overlap; dense continuous coupling justifies one merged/global scope. `CoordinationScopeRegistry` therefore supports overlapping non-owning memberships without transferring evidence, leases or authority.

I12 separates one-way dependence from reciprocity. Sparse directional work should not create reverse flow; reciprocal clusters can earn shared scopes; mixed regimes use both. `DependencyRegistry` stores explicit one-way relationships over stable subject identities.

## I13 — partial topology/structural publication failure

I13 fails migration after a random subset of 12 subject moves.

Default 30-seed result, 20% failure probability and event rate 8:

| mechanism | net utility/migration | corrupt rate | lost events | duplicate events | downtime |
|---|---:|---:|---:|---:|---:|
| naive in-place | 2.860 | ~0.202 | ~3.96 | ~0.51 | 0.000 |
| stop-world replace | 3.241 | **0.000** | **0.000** | **0.000** | ~1.299 |
| **staged transaction** | **3.310** | **0.000** | **0.000** | **0.000** | ~0.402 |
| dual-version handoff | 3.291 | **0.000** | **0.000** | **0.000** | **0.000** |

The mechanisms cross over with failure risk and live traffic:

- essentially zero failure + very low traffic: direct live change is cheapest;
- high failure + low traffic: blocking replacement can be rational;
- high live traffic: dual-version handoff can earn its extra temporary state.

## I13B — singular ownership handoff reproduces the boundary

This second family changes one exact resource/service writer rather than topology.

Naive make-before-break can leave two writers; break-before-make can leave zero writer.

Default 30-seed result, 20% failure and request rate 10:

| mechanism | utility/handoff | ownership violation | duplicate writes | lost requests | downtime |
|---|---:|---:|---:|---:|---:|
| make-before-break | 0.5621 | ~0.065 | ~0.780 | 0.000 | 0.000 |
| break-before-make | 0.3846 | ~0.064 | 0.000 | ~5.142 | 0.000 |
| stop-world transfer | 0.6841 | **0.000** | **0.000** | **0.000** | ~1.080 |
| staged lease fence | 0.7704 | **0.000** | **0.000** | **0.000** | ~0.120 |
| **dual-read / single-write** | **0.7743** | **0.000** | **0.000** | **0.000** | **0.000** |

High-failure/high-live-traffic conditions favor dual-read/single-write; zero-failure/low-traffic can make direct handoff cheapest.

## PS-024 — failure-isolated consequential transition publication

I13 + I13B meet the second-family promotion gate.

> **Prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish authority/ownership/topology only across a coherence boundary after required validation. Choose direct, blocking, staged or dual-version publication according to partial-failure risk, blast radius, live-work pressure and isolation cost.**

The selected object is the failure-isolation boundary between **preparation** and **authoritative publication**, not transactions, locks, consensus, blue/green deployment or another named implementation.

## I13C — publication protocol is now explicit in the runtime

`PublicationProtocol` hardens the reusable runtime with version fences:

- preparation does not change live topology/resource ownership;
- a topology candidate records the epoch it was prepared against;
- a resource handoff records the lease version it was prepared against;
- publication rejects stale topology/lease plans;
- current authority is re-read at publication, so revocation after preparation blocks the handoff;
- consequential publication still requires independent assurance;
- discard leaves the live state unchanged.

A specific concurrency bug is now prevented: two topology changes staged at epoch N cannot both publish. Once one advances the topology epoch, the other is stale.

---

# Current provisional selections

PS-001 through PS-024 are active reversible constraints:

1. typed hybrid boundary state;
2. staged adaptive persistence;
3. coupling-scoped coordination;
4. derived current belief with evidence linkage;
5. value-of-computation stopping;
6. consequence-sensitive hypothesis plurality;
7. value-driven active evidence acquisition;
8. verified epistemic frontier expansion;
9. conditional sharing with isolation fallback;
10. joint adaptive resource substitution under shared scarcity;
11. retrieval by expected applicability/downstream value;
12. adaptive predictive-state breadth / recoverable optionality;
13. failure-mode-independent assurance;
14. consequence/uncertainty/resource-sensitive assurance allocation;
15. causal/eligibility-scoped delayed credit;
16. failure-layer-targeted verification;
17. independent current/revocable capability authority;
18. rotating independent self-change regression evidence;
19. resource-priced lineage diversity / variant optionality;
20. evidence-scaled repair scope / minimal sufficient blast radius;
21. regularity-scaled structural encoding / local override fallback;
22. event-scoped execution with consistency-triggered synchronization;
23. value/sensitivity-scaled fidelity allocation;
24. **failure-isolated consequential transition publication**.

---

# Current executable architecture hypothesis

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
interaction-aware value/resource allocator
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

The strongest current inference is:

> **organization is not one graph with one meaning, and consequential change is not one mutation with one moment. Typed relationships evolve through prepared, validated and coherently published versions while stable identity/authority/provenance survive the reorganization.**

This remains a falsifiable candidate architecture, not a final product implementation.

## Next high-value work

1. run simultaneous **authority revocation during staged/dual topology and service handoff** with in-flight work, now through `PublicationProtocol`;
2. inject crash/restart between prepare and publish to test recovery of prepared-but-unpublished candidates;
3. persist publication intent/log state only if crash recovery proves it is required rather than assuming a database/WAL;
4. then return to I05C correlated/adversarial evaluator audits and partially unresolved outcomes;
5. neural E24C remains conditional on representation geometry still being architecture-discriminating.

## Guardrail

Self-improvement, topology change and resource ownership change remain inside the staged publication protocol: current capability authority, sufficiently independent assurance, version fences, rollback/discard where possible, and no proposal path may treat its own score or stale prepared state as publication authority.
