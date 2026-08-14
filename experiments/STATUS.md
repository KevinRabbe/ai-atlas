# Phase 10 Experimental Status

**Checkpoint: nineteen provisional design principles selected; composition + guarded self-improvement experiments are active. No Phase-9 architecture family is selected.**

## Implemented blocks

Core/promotion experiments now cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit, E11 retrieval, E12B verification granularity, E14/E14B capability authority, E15/E15B lineage diversity, E20/E20B self-change regression evidence, E22/E22B cross-resource metacontrol, and E23/E23B beyond-teacher discovery.

Integrated composition generations remain I01–I04, with **I04** testing one shared typed state-transition/resource allocator rather than one permanent controller per principle.

JEPA is explicitly registered as a candidate predictive-representation family. **E24 is specified but not implemented** and may lose against reconstruction/task-sufficient/recoverable-source alternatives.

## Validation

The prior Phase-10 history contained **104 added passing tests**. This continuation adds:

- I04: 5;
- E12B: 5;
- E14: 5;
- E14B: 5;
- E20: 5;
- E20B: 5;
- E15 recurring-objective archive: 5;
- E15B deceptive stepping stones: 5.

The continuation-local suite is **40/40 passing**, taking the Phase-10 added-test history to **144 passing tests**. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Latest findings

## I04 — common allocation, typed authority

Across 30 seeds the typed shared kernel reaches ~`0.9758` utility/task versus ~`0.7846` for typed fixed silos and `-0.3494` for a flat scalar kernel. The flat kernel creates ~`194.1` false durable writes and ~`68.4` unsafe external effects/run because local score is allowed to masquerade as authority.

The typed shared kernel reallocates verification from ~`0.100`/task before a hidden workload shift to ~`0.155` afterward. **Allocation can unify; authority/durability/failure semantics cannot be flattened into the allocation score.**

## E12B / PS-016 — failure-layer-targeted verification

A workflow family separates intermediate invariant failure from final-output corruption. Outcome-only leaves ~`0.1337` process harm; process-only leaves ~`0.1113` outcome harm. Uniform both checks reduce both below 0.6% but require 2 checks/task. Adaptive granularity gives the best default utility (~`1.9877`) with ~`1.068` checks/task.

Together with I03 this promotes PS-016.

## E14/E14B / PS-017 — current revocable capability authority

E14 separates categorical authorization from contextual risk. Behavior-only produces ~`364.6` categorical violations/run and degrades after a spoofing shift; narrow hard authority holds categorical violations at zero but does not solve contextual danger. The hybrid is best.

E14B changes grants/revocations during the lifetime. A static hard boundary becomes stale (~`1679.6` violations/run). Always-live and versioned boundaries both stay at zero; the versioned design refreshes on only ~`1.14%` of tasks and slightly beats always-live utility (`0.4573` vs `0.4399`).

This promotes **PS-017 — independent current/revocable capability authority**.

## E20/E20B / PS-018 — rotating independent self-change evidence

E20 exposes state-space coverage drift: visible-only and fixed-hidden suites look nearly perfect before the shift, then fall to ~`0.034` and ~`0.078` real post-shift capability. Rotating current-distribution hidden evidence stays near **`0.997`** with ~`3.3` harmful accepted changes versus ~`85.9` fixed-hidden.

E20B reproduces the failure via timescale rather than state-space shift. Short/fixed-hidden tests fall to ~`0.070`/~`0.095` in long sessions; rotating horizons preserve ~`0.942`. Maximal adversarial horizons reach 1.0 here but reject ~`47.4` useful changes and cost more assurance.

This promotes **PS-018 — rotating independent self-change regression evidence**. The principle is refreshed independence/coverage, not permanent secrecy or universally maximal adversarial testing.

## E15/E15B / PS-019 — lineage diversity is option value

Family A uses two capabilities with destructive tradeoffs.

Stationary objective:

| policy | net performance |
|---|---:|
| **greedy incumbent** | **0.99275** |
| bounded archive | 0.98798 |

The archive correctly loses when alternatives never become useful.

Switching objective:

| policy | net performance | first-10 after switch | best A | best B |
|---|---:|---:|---:|---:|
| greedy incumbent | 0.95620 | 0.79900 | 0.87129 | 1.00000 |
| **bounded archive** | **0.98040** | **0.95452** | **1.00000** | **1.00000** |

Family B uses a deceptive landscape: local optimum score 10, global optimum 15, and all intermediate stepping stones score worse. Greedy remains at 10 on **30/30** seeds; bounded diversity reaches 15 on **30/30**, mean first arrival round ~`74.3`, with the same candidate-evaluation budget.

This promotes **PS-019 — resource-priced lineage diversity / variant optionality**.

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
19. PS-019 — resource-priced lineage diversity / variant optionality.

---

# Current architecture compression hypothesis

The evidence increasingly points toward fewer primitives than the 19 principle labels:

`typed state/transition proposals -> shared marginal-value/resource allocator -> failure-layer assurance + authority boundary -> execute -> observe -> causal credit -> staged update`

Recurring laws:

- scope follows coupling/responsibility;
- state follows future value/recoverability;
- optional work follows marginal value;
- sharing follows reusable structure;
- authority follows independent current evidence/invariants;
- verification follows residual failure layer;
- durable change requires stronger and refreshing evidence;
- self-improvement diversity is retained only while its future option value pays for itself.

This remains a hypothesis, not a selected architecture.

## Next high-value work

1. **E16 — repair/change scope:** local reversible patch vs isolated durable component change vs structural change under E20/PS-018 regression evidence;
2. **I05 — learned transition metadata:** make more I04 value/coupling/authority-risk/verifier-independence estimates learned rather than supplied;
3. then E17/E18/E19 only where they materially discriminate the emerging architecture;
4. **E24 JEPA** remains queued and rises in priority if predictive-state/representation becomes the bottleneck.

## Guardrail

Self-improvement experiments are now allowed only inside the staged change protocol: independent/current capability authority, rotating independent regression evidence, explicit rollback/reversibility where possible, and no self-change proposal path gets to treat its own score as promotion authority.
