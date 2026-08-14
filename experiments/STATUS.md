# Phase 10 Experimental Status

**Checkpoint: twenty-three provisional design principles selected; composition has progressed through I12 plus the reusable typed-scope runtime. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **260 added test cases**.

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
- typed directional-dependency registry: 3.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Current architecture checkpoint

## I06 — interaction-aware runtime allocation

I06 puts high fidelity, source rematerialization vs broad hot state, synchronization and active intervention into one shared runtime budget.

30-seed learned-joint utility is ~`1.5640`/task versus ~`1.3549` factorized independent, ~`1.4096` uniform-safe and ~`0.4769` uniform-cheap.

**Result:** operation values cannot always be summed independently. Material complements/substitutes require interaction-aware allocation.

## AF01–AF03 / I07 — fixed architecture becomes adaptive organization

AF01 finds a Pareto frontier among canonical A/B/C/D embodiments rather than a universal fixed winner.

AF02 learns organizational mode from noisy observable structure: ~`1.5625` utility/step versus ~`1.5087` best fixed and ~`1.5762` oracle. It loses when regimes are too short to amortize identification/switching.

AF03 shows organizational mode must also be scoped: heterogeneous weakly coupled domains favor simultaneous local modes, while homogeneous tightly coupled domains favor global organization.

I07 removes predefined subsystem boundaries. Adaptive graph-derived scopes reach ~`1.0583` utility/step and ~`0.9045` pairwise scope accuracy versus `1.0270` static global and ~`1.0748` oracle at 120-step regimes. At 20-step regimes adaptive topology loses.

**Result:** organizational mode, scope and membership can all be revisable state, but plasticity has an economic timescale.

## I08 — typed state survives live topology changes

I08 puts exact evidence IDs/provenance, predictive source references, independent versioned authority, exact resource leases and delayed events behind dynamic split/merge operations.

30-seed means:

| runtime | utility/step | event misroutes | authority violations | provenance failures | rematerialization failures | duplicate resource exposure/step |
|---|---:|---:|---:|---:|---:|---:|
| static typed | 0.9957 | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| scope snapshot | 0.7770 | ~45.0 | ~4.53 | ~108.3 | ~97.0 | ~8.218 |
| typed stale-route | 1.0636 | ~45.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| **typed epoch** | **1.0744** | **0.0** | **0.0** | **0.0** | **0.0** | **0.000** |

The typed-epoch runtime forwards ~`46.9` delayed events/run across topology changes rather than losing their route.

**Result:** stable semantic identity is not the same state dimension as current organizational scope.

## I09 — topology changes need assurance under correlated evidence

A sustained false interaction source drops raw pairwise topology accuracy from ~`0.9061` to ~`0.8227`; simply raising the threshold still accepts ~`15.2` harmful migrations/run.

Selective independent checking reaches ~`0.9325` attacked accuracy with zero harmful accepted migrations in the matched family and uses ~`5.9` audit samples/step versus `33` for uniform checking.

Uniform assurance wins when independent evidence is cheap; selective assurance wins as audit cost rises.

**Result:** topology proposal evidence is not automatically topology-promotion evidence.

## I10 — persistent typed-scope organism API

I10 converts the architecture checkpoint into a reusable runtime protocol instead of another experiment-specific controller.

`TypedScopeRuntime` now exposes:

- exact evidence/source records and predictive rematerialization links;
- current versioned capability authority;
- singular versioned resource leases;
- typed transition proposals;
- interaction-aware bundle allocation;
- independent proposal-specific assurance tokens;
- staged/committed/rolled-back topology changes;
- topology epochs and exactly-once old-epoch event forwarding.

Eight semantic tests passed before publication.

A separate 900-step I10 integration scenario repeatedly changes topology and authority while work is in flight, rematerializes source-backed state and allocates complementary operation bundles. Across the local 20-seed validation it averages ~`6.1` topology epochs, ~`2.45` independently rejected structural proposals, ~`6.75` old-epoch forwards and ~`7.0` external effects blocked by current revocation. Every queued event is eventually processed and all tested semantic invariants remain true.

**Result:** later architecture experiments can now target one common executable protocol rather than silently redefining identity/authority/migration semantics.

## I11 — ownership and coordination scope are different dimensions

Twelve components retain stable base ownership groups while cross-cutting work appears at different recurrence rates.

Sparse (~18% active):

- base partition: ~`1.1259` utility/step;
- forced disjoint repartition: ~`1.0898`;
- persistent overlap: ~`1.0635`;
- **temporary non-owning overlay: ~`1.1303`**.

Frequent (~90% active):

- base: ~`1.0540`;
- temporary overlay: ~`1.0756`;
- **persistent overlap: ~`1.1012`**.

Dense continuous coupling:

- **global scope: ~`1.5130`**;
- persistent overlap: ~`1.4980`;
- temporary overlay: ~`1.3800`.

**Result:** cross-cutting coordination may overlap semantic ownership without moving it; temporary vs persistent overlap is itself a recurrence/value allocation decision; dense enough coupling justifies merging scopes.

The runtime now has a separate **non-owning `CoordinationScopeRegistry`**. A subject may join multiple scopes; closing one cannot delete evidence/predictive state, transfer a lease or grant capability authority.

## I12 — dependencies are directional until reciprocity earns sharing

The learner observes noisy ordered interaction events through sparse one-way, reciprocal-cluster and mixed regimes.

30-seed default lifetime utility:

| policy | utility/step |
|---|---:|
| global scope | 0.7116 |
| directed links | 0.7034 |
| symmetric links | 0.6689 |
| **reciprocity adaptive** | **0.7394** |

In stationary sparse one-way structure, symmetric links represent ~`11.94` unsupported reverse relationships/step while directed/adaptive representations are effectively zero. In reciprocal structure, the adaptive representation collapses mutual links into shared scopes; in mixed structure it keeps reciprocal clusters shared while preserving one-way cross-cluster links.

At 20-step regimes the learned hybrid falls to ~`0.6369` while static global remains ~`0.7138`, again exposing the structural-identification timescale.

**Result:** one-way dependence does not justify reverse information flow or shared state. Reciprocity/coupling must earn the shared scope.

The runtime now also has a typed **`DependencyRegistry`** whose edges are explicitly directed and topology-independent. Reciprocity can be detected as evidence for coordination, but does not automatically create a shared scope, authority or ownership transfer.

---

# Current provisional selections

PS-001 through PS-023 remain active reversible constraints. I08–I12 do not add new principle numbers; they refine and compose the existing laws at architecture/runtime scale.

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
23. value/sensitivity-scaled fidelity allocation.

---

# Current executable architecture hypothesis

```text
stable typed semantic identities
  subjects / evidence / provenance / sources
  authority versions / resource leases
        |
        +--> directional dependency registry
        |
        +--> disjoint ownership topology
        |       + dynamic split/merge
        |
        +--> overlapping non-owning coordination scopes
                temporary or persistent
        ↓
typed transition proposals
        ↓
interaction-aware resource allocator
        ↓
consequence-sensitive independent assurance
        ↓
versioned execution / structural protocol
  execute / forward / stage / commit / rollback
        ↓
observe → causal credit → staged appropriately-scoped update
```

The strongest current inference is:

> **organization is not one graph with one meaning. Ownership, coordination, directional dependence, authority, provenance and resource identity are distinct typed relationships that may share stable identities but obey different update/assurance rules.**

This remains a falsifiable candidate architecture, not a final implementation selection.

## Next high-value work — I13 partial structural commit

I10 currently assumes a topology commit is atomic.

The next experiment should inject failures after only some migration steps have occurred and compare:

- naive in-place migration;
- stop-the-world copy/replace;
- staged transactional migration with version fence + rollback;
- possibly incremental dual-version handoff.

The experiment must preserve or measure:

- evidence/source reachability;
- resource lease uniqueness;
- current authority semantics;
- exactly-once in-flight events;
- topology epoch consistency;
- rollback/recovery cost and downtime.

A broad structural change is not safe merely because its final target topology is correct; the **transition path itself** must preserve invariants or provide recoverable staging.

## Guardrail

Self-improvement and topology change remain inside the staged change protocol: independent/current capability authority, sufficiently independent regression/assurance evidence, scoped causal attribution, explicit rollback/reversibility where possible, and no proposal path may treat its own score as promotion authority.
