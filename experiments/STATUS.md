# Phase 10 Experimental Status

**Checkpoint: twenty-three provisional design principles selected; composition + guarded self-improvement experiments are active. No Phase-9 architecture family is selected.**

## Implemented blocks

Core/promotion experiments now cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit, E11 retrieval, E12B verification granularity, E14/E14B capability authority, E15/E15B lineage diversity, E16 repair/change scope, E17/E17B structural organization, **E18 execution timing**, **E19 fidelity allocation**, E20/E20B self-change regression evidence, E22/E22B cross-resource metacontrol, and E23/E23B beyond-teacher discovery.

Integrated composition generations are **I01–I05**. I04 tests one shared typed state-transition/resource allocator; I05 makes key metacognitive estimates learned and revisable rather than supplied by oracle metadata.

JEPA is explicitly registered as a candidate predictive-representation family. **E24 is specified but not implemented** and may lose against reconstruction/task-sufficient/recoverable-source alternatives.

## Validation

Phase 10 now contains **178 added test cases**. The 166-test I05/E17 checkpoint was extended with:

- E18 execution timing: 6 tests;
- E19 fidelity allocation: 6 tests.

The shell environment could not clone GitHub because DNS resolution is unavailable there. The E17B/E18/E19 semantic assertions were executed independently in the local Python reasoning environment and passed; connector writes were verified on `main`. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Latest findings

## E18 / PS-022 — event-scoped execution + consistency-triggered synchronization

### Sparse event graph

| variant | utility/step | stale reads | operations/step | messages/step |
|---|---:|---:|---:|---:|
| sync global | 0.8560 | **0.0000** | 80.000 | 0.000 |
| async naive | 0.6671 | 0.2681 | **6.217** | 0.000 |
| **scoped event** | **0.9815** | **0.0000** | **8.699** | 5.699 |

Event-driven execution preserves exact dependency state while avoiding global idle work. Naive async misses dependent invalidations.

### Version-coupled snapshot

At 55% update / 30% snapshot-query demand:

| variant | utility/step | inconsistent queries | operations/step |
|---|---:|---:|---:|
| sync global | 0.2513 | **0.0000** | 26.492 |
| async naive | -0.3675 | 0.9991 | **4.417** |
| **scoped event + barrier** | **0.2624** | **0.0000** | **11.565** |

The scoped barrier coalesces several logical versions before materializing a common snapshot. But at ~90% snapshot demand eager sync becomes better (~0.8508 versus ~0.8202), establishing the synchronization-frequency crossover.

This promotes **PS-022 — event-scoped execution with consistency-triggered synchronization**.

## E19 / PS-023 — fidelity is a priced resource

### One-shot threshold decisions

| variant | utility/task | error rate | high-fidelity rate | fidelity cost |
|---|---:|---:|---:|---:|
| low | 1.6869 | 0.0626 | 0.0000 | **0.0100** |
| high | 2.2523 | **0.0000** | 1.0000 | 0.0800 |
| **adaptive** | **2.3057** | **0.0000** | **0.2082** | **0.0267** |

High-fidelity use rises from ~0.126 at consequence 1 to ~0.374 at consequence 6.

### Accumulated trajectory constraint

| variant | utility/episode | error rate | false-safe rate | exact replay rate |
|---|---:|---:|---:|---:|
| low | 0.4173 | 0.1072 | 0.0477 | 0.0000 |
| high | 0.7902 | **0.0000** | **0.0000** | 1.0000 |
| **adaptive** | **0.8434** | **0.0050** | **0.0020** | **0.4813** |

Exact replay rises with consequence (~0.380 at consequence 4 to ~0.572 at consequence 12). This promotes **PS-023 — value/sensitivity-scaled fidelity allocation**.

## I05 — learned transition metacognition

A hidden regime shift changes operation benefit, family-specific coordination value, visible-evaluator failure and secondary-verifier reliability. The conditional learner drops to ~0.517 immediately post-shift and recovers to ~0.740 in the final 100 batches, versus ~0.485 frozen and ~0.622 globally pooled. Categorical authority remains exact and external.

## E17/E17B / PS-021 — structural indirectness follows regularity

Repeated structural state and repeated dependency topology both reward a compact shared generative rule; irregular/local structure punishes always-global mutation. Adaptive indirect encoding retains local override/isolation and therefore keeps the repeated-structure advantage without paying the global-mutation penalty on irregular tasks.

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
22. **PS-022 — event-scoped execution with consistency-triggered synchronization**;
23. **PS-023 — value/sensitivity-scaled fidelity allocation.**

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
- authority follows independent current evidence/invariants;
- verification follows residual failure layer;
- durable change requires stronger and refreshing evidence;
- self-improvement diversity is retained only while future option value pays for itself;
- repair blast radius expands only when evidence says the root cause is equally broad;
- metacognitive estimates are themselves revisable state.

This remains a hypothesis, not a selected architecture.

## Next high-value work

1. **E24 JEPA predictive representation:** now the largest explicitly specified representation discriminator; compare latent target prediction against reconstruction, task-sufficient prediction and recoverable-source alternatives under objective shift/intervention;
2. **I05B:** degrade metacognitive feedback from exact delayed audit to noisy/partial/censored outcomes;
3. integrate E18/E19 into a future I06 kernel to test whether timing/fidelity decisions can share the common allocator without unstable feedback loops;
4. architecture-family elimination only after those composition tests provide end-to-end evidence.

## Guardrail

Self-improvement remains inside the staged change protocol: independent/current capability authority, rotating independent regression evidence, scoped causal attribution, explicit rollback/reversibility where possible, and no proposal path may treat its own score as promotion authority.
