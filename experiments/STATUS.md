# Phase 10 Experimental Status

**Checkpoint: twenty provisional design principles selected; composition + guarded self-improvement experiments are active. No Phase-9 architecture family is selected.**

## Implemented blocks

Core/promotion experiments now cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit, E11 retrieval, E12B verification granularity, E14/E14B capability authority, E15/E15B lineage diversity, E16 repair/change scope, E20/E20B self-change regression evidence, E22/E22B cross-resource metacontrol, and E23/E23B beyond-teacher discovery.

Integrated composition generations remain I01–I04, with **I04** testing one shared typed state-transition/resource allocator rather than one permanent controller per principle.

JEPA is explicitly registered as a candidate predictive-representation family. **E24 is specified but not implemented** and may lose against reconstruction/task-sufficient/recoverable-source alternatives.

## Validation

Phase 10 now has **150 added passing tests**. This continuation contributed 46 passing tests across I04, E12B, E14/E14B, E20/E20B, E15/E15B and E16. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Latest findings

## I04 — common allocation, typed authority

Across 30 seeds the typed shared kernel reaches ~`0.9758` utility/task versus ~`0.7846` for typed fixed silos and `-0.3494` for a flat scalar kernel. The flat kernel creates ~`194.1` false durable writes and ~`68.4` unsafe external effects/run. The shared typed kernel reallocates verification as workload changes.

**Interpretation:** common marginal-value/resource allocation can replace some separate controllers, but the allocation score cannot itself grant durable epistemic or external authority.

## E12B / PS-016 — failure-layer-targeted verification

Outcome-only leaves ~`0.1337` process harm; process-only leaves ~`0.1113` outcome harm. Uniform both checks cover both layers but cost 2 checks/task. Adaptive granularity gives best default utility (~`1.9877`) with ~`1.068` checks/task.

## E14/E14B / PS-017 — current revocable capability authority

Behavior-only categorical violations degrade under spoofing. Narrow exact authority gates keep categorical violations at zero while behavioral/contextual risk control remains necessary inside the authorized envelope.

When grants/revocations change, a static boundary suffers ~`1679.6` stale-authority violations/run. Always-live and versioned boundaries stay at zero; versioned authority refreshes on only ~`1.14%` of tasks and slightly beats always-live utility (`0.4573` vs `0.4399`).

## E20/E20B / PS-018 — rotating independent self-change evidence

A fixed hidden suite can become stale in both **coverage** and **timescale**.

- E20 state-space shift: fixed-hidden post-shift true capability ~`0.078`; rotating hidden ~`0.997`.
- E20B long-horizon shift: fixed-short hidden ~`0.095`; rotating horizons ~`0.942`.

Maximal adversarial testing is safer in the synthetic families but rejects substantially more useful changes and costs more assurance.

## E15/E15B / PS-019 — lineage diversity is priced option value

Stationary objective:

| policy | net performance |
|---|---:|
| **greedy incumbent** | **0.99275** |
| bounded archive | 0.98798 |

Switching objective:

| policy | net performance | first-10 after switch | best A | best B |
|---|---:|---:|---:|---:|
| greedy incumbent | 0.95620 | 0.79900 | 0.87129 | 1.00000 |
| **bounded archive** | **0.98040** | **0.95452** | **1.00000** | **1.00000** |

In E15B's deceptive landscape, greedy remains at local score 10 on 30/30 seeds; bounded diversity reaches global score 15 on 30/30 with equal candidate-evaluation budget.

## E16 / PS-020 — repair scope follows causal scope

Three causal regimes produce three different useful scopes:

| regime | local only | component only | structural only | adaptive scope |
|---|---:|---:|---:|---:|
| sparse isolated | **-0.06698** | -0.07512 | -0.11541 | -0.06989 |
| recurring component root | -0.49970 | -0.06297 | -0.09650 | **-0.05872** |
| shared systemic root | -0.61242 | -0.68739 | -0.09665 | **-0.06024** |

For the systemic root, adaptive scope makes only ~`5.33` structural changes/run versus ~`120.3` for structural-only. This promotes **PS-020 — evidence-scaled repair scope / minimal sufficient blast radius**.

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
20. PS-020 — evidence-scaled repair scope / minimal sufficient blast radius.

---

# Current architecture compression hypothesis

The experimental evidence increasingly points toward fewer primitives than the 20 principle labels:

`typed state/transition proposals -> shared marginal-value/resource allocator -> failure-layer assurance + current authority boundary -> execute -> observe -> causal credit -> staged/appropriately-scoped update`

Recurring laws:

- scope follows coupling/responsibility/causal extent;
- state follows future value and recoverability;
- optional work follows marginal value;
- sharing follows reusable structure;
- authority follows independent current evidence/invariants;
- verification follows residual failure layer;
- durable change requires stronger and refreshing evidence;
- self-improvement diversity is retained only while future option value pays for itself;
- repair blast radius expands only when evidence says the root cause is equally broad.

This remains a hypothesis, not a selected architecture.

## Next high-value work

1. **I05 — learned transition metadata:** learn more of I04's value, coupling, authority-risk and verifier-independence estimates rather than supplying them;
2. **E17 — mature structure:** fixed structure vs direct structural mutation vs generative/developmental organization, now under PS-018/PS-020 change governance;
3. E18/E19 only where they materially discriminate the emerging architecture;
4. **E24 JEPA** remains queued and rises in priority if predictive-state/representation becomes the bottleneck.

## Guardrail

Self-improvement remains inside the staged change protocol: independent/current capability authority, rotating independent regression evidence, scoped causal attribution, explicit rollback/reversibility where possible, and no proposal path may treat its own score as promotion authority.
