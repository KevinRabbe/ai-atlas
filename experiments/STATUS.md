# Phase 10 Experimental Status

**Checkpoint: twenty-three provisional design principles selected; composition + guarded self-improvement experiments are active. No Phase-9 architecture family is selected.**

## Implemented blocks

Core/promotion experiments now cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit, E11 retrieval, E12B verification granularity, E14/E14B capability authority, E15/E15B lineage diversity, E16 repair/change scope, E17/E17B structural organization, E18 execution timing, E19 fidelity allocation, E20/E20B self-change regression evidence, E22/E22B cross-resource metacontrol, E23/E23B beyond-teacher discovery, and **E24 predictive representation / JEPA mechanism discrimination**.

Integrated composition generations are **I01–I05**. I04 tests one shared typed state-transition/resource allocator; I05 makes key metacognitive estimates learned and revisable rather than supplied by oracle metadata.

JEPA remains an explicit candidate mechanism family, **not a selected architecture component**. E24 is now implemented and gives evidence both for latent predictive efficiency and against overly coarse/passive-only predictive sufficiency.

## Validation

Phase 10 now contains **184 added test cases**. The previous 178-test checkpoint was extended by E24 predictive representation: 6 tests.

The shell environment cannot clone GitHub because DNS resolution is unavailable there. Recent E17B/E18/E19/E24 numerical discriminators were first exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Latest findings

## E24 — predictive latent efficiency vs future/interventional sufficiency

E24 does not implement JEPA itself. It uses empirical predictive-feature objectives as a model-free proxy so the first discriminator isolates **what the representation objective preserves** rather than neural architecture details.

### Objective shift

| policy | initial balanced acc. | future balanced acc. | lifetime net | future hot width |
|---|---:|---:|---:|---:|
| raw reconstruction | 0.9601 | **0.8504** | 0.8332 | 24 |
| task sufficient | 0.9601 | 0.6280 | 0.7820 | 4 |
| **coarse latent target** | 0.9601 | **0.5000** | 0.7180 | **4** |
| dense latent target | 0.9601 | **0.8504** | 0.8752 | 10 |
| **latent + recoverable source** | 0.9601 | **0.8504** | **0.8797** | **5** |

The coarse latent is cheapest/best on the original objective but permanently omitted the lower-ranked factor required later. Dense latent keeps the factor; source-backed latent rematerializes it with less hot-state width.

### Passive prediction vs intervention

| policy | passive balanced acc. | intervention balanced acc. | lifetime net | intervention hot width |
|---|---:|---:|---:|---:|
| raw reconstruction | 0.9498 | **0.8989** | 0.8763 | 16 |
| task sufficient | 0.9498 | 0.5884 | 0.7571 | 4 |
| **coarse latent target** | 0.9498 | **0.4899** | 0.7078 | **4** |
| dense latent target | 0.9498 | **0.8989** | 0.8943 | 10 |
| **latent + recoverable source** | 0.9498 | **0.8989** | **0.9028** | **5** |

All policies look equally strong on passive prediction; coarse latent fails once an action-discriminating lower-predictability cue becomes relevant. Thus:

`passive predictive sufficiency != intervention/counterfactual sufficiency`.

No new JEPA principle is promoted. E24 mainly refines PS-012/PS-023: **predictive compression must optimize lifetime decision/intervention utility, with target breadth and recoverability treated as part of the objective.**

## E18 / PS-022 — event-scoped execution

Sparse dependency work favors event propagation over global ticking; version-coupled work requires scoped barriers. Eager synchronization wins again when consistent snapshots are nearly continuous.

## E19 / PS-023 — adaptive fidelity

Approximate state is efficient until its uncertainty can change consequential decisions. Adaptive precision/replay beats both uniform-low and uniform-high policies in threshold and accumulated-trajectory families.

## I05 — learned transition metacognition

The conditional learner takes a real hit after hidden operation/evaluator economics change, then recovers from ~0.517 immediately post-shift to ~0.740 in the final 100 batches. Frozen/global estimates do not recover as well. Categorical authority remains exact and external.

## E17/E17B / PS-021 — structural indirectness follows regularity

Repeated structural state and dependency topology reward compact generative rules; irregular/local organization requires direct/local override paths.

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

---

# Current architecture compression hypothesis

`typed state/transition proposals -> learned shared marginal-value/resource allocator -> failure-layer assurance + current authority boundary -> execute at scoped timing/fidelity -> observe -> causal credit -> staged/appropriately-scoped update`

Recurring laws:

- scope follows coupling/responsibility/causal extent;
- state follows future value and recoverability;
- optional work follows marginal value;
- sharing and structural indirectness follow reusable regularity;
- execution follows events until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- predictive compression is valid only relative to future/action-relevant distinctions and recoverability;
- authority follows independent current evidence/invariants;
- verification follows residual failure layer;
- durable change requires stronger and refreshing evidence;
- self-improvement diversity is retained only while future option value pays for itself;
- repair blast radius expands only when evidence says the root cause is equally broad;
- metacognitive estimates are themselves revisable state.

This remains a hypothesis, not a selected architecture.

## Next high-value work

1. **I05B — imperfect metacognitive feedback:** replace exact delayed research/tool audit outcomes with noisy, delayed, censored or partially missing evidence;
2. **I06 — composition of timing/fidelity/representation:** let E18/E19/E24 decisions compete inside the common allocator rather than remain separate controllers;
3. only then use end-to-end evidence to begin eliminating Phase-9 architecture families;
4. later neural E24C only if actual learned predictive-objective geometry remains architecture-discriminating after I06.

## Guardrail

Self-improvement remains inside the staged change protocol: independent/current capability authority, rotating independent regression evidence, scoped causal attribution, explicit rollback/reversibility where possible, and no proposal path may treat its own score as promotion authority.
