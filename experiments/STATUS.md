# Phase 10 Experimental Status

**Checkpoint: twenty-three provisional design principles selected; composition has progressed through I07 and architecture-level tests AF01–AF03. No fixed Phase-9 A/B/C/D family is selected.**

## Validation

Phase 10 now contains **217 added test cases**.

Recent additions:

- I06 integrated runtime allocation: 6 tests;
- AF01 matched fixed-family Pareto benchmark: 5 tests;
- AF02 adaptive organizational mode selection: 6 tests;
- AF03 simultaneous scoped organization: 5 tests;
- I07 dynamic scope formation: 5 tests.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent numerical discriminators were exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

## Implemented experimental surface

Core/promotion experiments cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit, E11 retrieval, E12B verification granularity, E14/E14B capability authority, E15/E15B lineage diversity, E16 repair/change scope, E17/E17B structural organization, E18 execution timing, E19 fidelity allocation, E20/E20B self-change regression evidence, E22/E22B cross-resource metacontrol, E23/E23B beyond-teacher discovery, and E24 predictive representation / JEPA mechanism discrimination.

Integrated composition generations now run through **I07**, with I05B as the imperfect-feedback metacognition branch.

JEPA remains an explicit candidate mechanism family, **not a selected architecture component**. E24 supports latent predictive efficiency but rejects overly coarse/passive-only predictive sufficiency.

---

# Latest architecture-level findings

## I06 — interaction-aware runtime allocation

I06 puts high fidelity, source rematerialization vs broad hot state, synchronization and active intervention into one shared runtime budget.

30-seed learned-joint utility is ~`1.5640`/task versus ~`1.3549` for factorized independent controllers, ~`1.4096` uniform-safe and ~`0.4769` uniform-cheap. The learned allocator suffers a real hidden-shift drop and later recovers.

**Result:** operation values cannot always be summed independently. Material complements/substitutes require interaction-aware allocation.

## AF01 — fixed architecture families form a Pareto frontier

Eight-seed utility means:

| scenario | A | B | C | D |
|---|---:|---:|---:|---:|
| sparse stationary | 1.6033 | 1.5991 | 1.5614 | **1.6098** |
| coupled switching | 1.3683 | 1.3704 | 1.3896 | **1.4435** |
| recurring mixed | 1.3953 | 1.3806 | **1.4797** | 1.4367 |

Different regimes reward different organization. Sparse rankings also change as explicit organization costs change. AF01 therefore does not justify selecting or eliminating a fixed family.

## AF02 — organization itself can be adaptive

AF02 removes the hidden regime label. The selector sees noisy observed coupling/conflict/transfer/recurrence cues plus its own realized reward history.

30-seed default:

| policy | utility/step | best-mode fraction |
|---|---:|---:|
| fixed A | 1.4834 | ~0.25 |
| fixed B | 1.4518 | ~0.25 |
| fixed C | 1.4394 | ~0.25 |
| fixed D | **1.5087** | ~0.25 |
| **adaptive** | **1.5625** | **0.9065** |
| oracle | **1.5762** | 1.0000 |

The learned selector uses B ~87% in local regimes, A ~91% under high coupling, C ~92% under high sharedness and D ~92% under recurrence.

**Falsifier:** at only 20 steps/regime, adaptive organization loses to the best fixed mode. Organizational plasticity earns itself only when expected regime persistence exceeds identification/switch/carrying cost.

## AF03 — organization should also be scoped

Four domains operate simultaneously.

- heterogeneous domains + cross-domain coupling `0.12`: scoped adaptive ~`1.5543`, global adaptive ~`1.4947`;
- homogeneous domains + coupling `0.80`: global adaptive ~`1.5711`, scoped adaptive ~`1.5537`.

In heterogeneous domains the scoped advantage decays continuously as cross-domain coupling rises and is essentially gone at coupling `1.0`.

**Result:** neither global organization nor maximal modularity is universal. Organizational scope expands with coupling.

## I07 — dynamic scope formation from noisy dependencies

I07 removes predefined domain boundaries. Twelve nodes move among three recurring hidden dependency partitions. The learner sees noisy pairwise interaction events and periodically splits/merges scopes, paying migration cost.

20-seed default:

| topology | utility/step | pairwise scope accuracy |
|---|---:|---:|
| global | 1.0270 | 0.2727 |
| local | 0.8950 | 0.7273 |
| fixed initial | 0.9760 | 0.7273 |
| **adaptive** | **1.0583** | **0.9045** |
| oracle | **1.0748** | 1.0000 |

With 120-step regimes adaptive scope formation beats every static topology after migration cost. At 20 steps/regime it falls to ~`0.9842`, below static global `1.0270`.

**Result:** topology membership itself can be revisable state, but topology plasticity only earns itself on timescales that amortize evidence/migration cost.

---

# Current provisional selections

1. PS-001 — typed hybrid boundary state;
2. PS-002 — staged adaptive persistence;
3. PS-003 — coupling-scoped coordination;
4. PS-004 — derived current belief with evidence linkage;
5. PS-005 — value-of-computation stopping;
6. PS-006 — consequence-sensitive hypothesis plurality;
7. PS-007 — value-driven active evidence acquisition;
8. PS-008 — verified epistemic frontier expansion;
9. PS-009 — conditional sharing with isolation fallback;
10. PS-010 — joint adaptive resource substitution under shared scarcity;
11. PS-011 — retrieval by expected applicability/downstream value;
12. PS-012 — adaptive predictive-state breadth / recoverable optionality;
13. PS-013 — failure-mode-independent assurance;
14. PS-014 — consequence/uncertainty/resource-sensitive assurance allocation;
15. PS-015 — causal/eligibility-scoped delayed credit;
16. PS-016 — failure-layer-targeted verification;
17. PS-017 — independent current/revocable capability authority;
18. PS-018 — rotating independent self-change regression evidence;
19. PS-019 — resource-priced lineage diversity / variant optionality;
20. PS-020 — evidence-scaled repair scope / minimal sufficient blast radius;
21. PS-021 — regularity-scaled structural encoding / local override fallback;
22. PS-022 — event-scoped execution with consistency-triggered synchronization;
23. PS-023 — value/sensitivity-scaled fidelity allocation.

No additional principle is created from AF01–AF03/I07 yet; they are composition-level evidence for how the existing laws organize a whole system.

---

# Current architecture compression hypothesis

```text
source/world evidence
      ↓
typed state + transition proposals
      ↓
learned interaction-aware value/resource allocation
      ↓
dynamic coupling scopes
      ├─ local/distributed organization where locality pays
      ├─ hierarchical arbitration where scarcity/coupling pays
      ├─ integrated/shared computation where transfer pays
      └─ variant preservation where recurrence/option value pays
      ↓
failure-layer assurance + current authority boundary
      ↓
execute at scoped timing / fidelity / state breadth
      ↓
observe → causal credit → staged appropriately-scoped update
```

The strongest new architecture inference is:

> **mode, scope and scope membership are all potentially adaptive state, but each form of plasticity must earn its identification, switching, carrying and migration costs.**

This remains a hypothesis, not a final selected architecture.

## Next high-value work

1. build the first **executable candidate architecture skeleton** around dynamic typed scopes rather than another abstract family benchmark;
2. make split/merge operations move real evidence references, predictive state, resource ownership, authority versions and in-flight events while preserving invariants;
3. then stress topology changes with stale/adversarial coupling evidence;
4. I05C remains queued for correlated/adversarial audit sources and partially unresolved outcomes;
5. neural E24C remains conditional on representation geometry still being architecture-discriminating.

## Guardrail

Self-improvement remains inside the staged change protocol: independent/current capability authority, rotating independent regression evidence, scoped causal attribution, explicit rollback/reversibility where possible, and no proposal path may treat its own score as promotion authority.