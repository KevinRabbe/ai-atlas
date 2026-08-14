# Phase 10 Experimental Status

**Checkpoint: sixteen provisional design principles selected; composition testing is the primary experimental strategy. No Phase-9 architecture family is selected.**

## Implemented blocks

Core/promotion experiments now cover E01/E01B coordination, E02/E02B/E02C sharing/interference, E03/E03B evidence/current state, E04/E04B representation, E05/E05B compute allocation, E06 ambiguity, E07 active information, E08/E08B predictive-state breadth, E09/E09B/E09C persistence, E10/E10B credit assignment, E11 retrieval, E12B workflow verification granularity, E14 capability boundaries, E22/E22B cross-resource metacontrol, and E23/E23B beyond-teacher discovery.

Integrated composition generations:

- **I01 — integrated epistemic organism**: memory conflict, ambiguity, active evidence, discovery staging and shared resources;
- **I02 — adaptive organism**: learned operation quality, conditional shared/private estimates and fallible assurance;
- **I03 — assurance composition**: process/outcome granularity, evaluator independence and assurance prices;
- **I04 — typed transition/resource kernel**: one common allocator with typed authority/durability/consequence boundaries.

JEPA is now explicitly registered as a candidate predictive-representation family. **E24 is specified, not implemented**, and is intentionally allowed to lose against reconstruction/task-sufficient/recoverable-source alternatives.

## Validation

The previous Phase-10 history contained **104 added passing tests**. This continuation adds:

- I04 transition kernel: 5 tests;
- E12B workflow granularity: 5 tests;
- E14 capability boundaries: 5 tests.

The continuation-local suite is **15/15 passing**, taking the Phase-10 added-test history to **119 passing tests**. Runtime experiment code remains Python 3.11+ stdlib-only.

---

# Latest composition findings

## I04 — common allocation works; flat authority does not

A hidden workload shift changes demand from cognition/observation toward research/external-effect tasks while all variants retain five total operation slots per batch.

30-seed means:

| variant | utility/task | false durable writes/run | unsafe external effects/run | authority violations/run |
|---|---:|---:|---:|---:|
| **typed shared kernel** | **0.9758** | 5.13 | **5.03** | **0.0** |
| typed fixed silos | 0.7846 | **2.67** | 6.57 | **0.0** |
| flat scalar kernel | **-0.3494** | **194.13** | **68.43** | **1144.7** |

The shared typed kernel reallocates verification from ~`0.1003`/task before the task-mix shift to ~`0.1546` afterward, while ordinary work allocation falls ~`0.3164 -> 0.2620`.

**Interpretation:** a common marginal-value/resource allocator can replace some separate controllers, but its score cannot also be the authority token for durable knowledge or consequential external effects.

## E12B / PS-016 — verification granularity

A multi-step workflow separates intermediate invariant violations from final-output corruption. An invalid intermediate transition may be repaired before the final output, and a valid process may still end in a corrupted result.

30-seed means:

| policy | utility/task | process harm | outcome harm | checks/task |
|---|---:|---:|---:|---:|
| process only | 1.6521 | **0.0050** | 0.1113 | 1.0000 |
| outcome only | 1.3030 | 0.1337 | **0.0042** | 1.0000 |
| uniform both | 1.8803 | **0.0053** | **0.0041** | 2.0000 |
| **adaptive granularity** | **1.9877** | 0.0226 | 0.0180 | **1.0684** |

Together with I03, this promotes **PS-016 — failure-layer-targeted verification**. Process/outcome/authority/provenance checks are not assumed substitutable merely because they all increase confidence.

## E14 — capability boundaries

Tasks separate exact categorical authorization from context-dependent action risk. Mid-lifetime, unauthorized privileged attempts become better at spoofing the behavioral risk cue.

30-seed means:

| policy | utility/task | invariant violations/run | contextual harms/run | blocked rate |
|---|---:|---:|---:|---:|
| behavior only | -2.2985 | 364.63 | **226.10** | 0.3100 |
| narrow hard only | -1.7620 | **0** | 795.90 | **0.0781** |
| broad hard | -1.3474 | **0** | 616.60 | 0.2798 |
| **hybrid** | **0.3530** | **0** | **226.10** | 0.3708 |

Behavior-only invariant violations rise ~`157.1 -> 207.5` after the spoof shift. A narrow hard boundary holds them at zero. Hard-only control still fails contextually; an over-broad hard boundary deletes legitimate capability. The strongest first-family result is therefore **narrow categorical enforcement + adaptive contextual control**. DL-014 remains open until changing delegation/revocation and boundary-failure cases are tested.

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
16. PS-016 — failure-layer-targeted verification.

---

# What is converging

The evidence increasingly compresses into fewer architecture laws than the provisional-principle count suggests:

- **scope follows coupling/responsibility**;
- **state follows future value and recoverability**;
- **work follows marginal value under shared scarcity**;
- **sharing follows reusable structure**;
- **authority follows evidence and typed invariants, not confidence alone**;
- **verification follows the residual failure layer**;
- **durability raises the evidence requirement**.

I04 suggests a candidate clean-sheet skeleton:

`typed state/transition proposals -> shared value/resource allocator -> layer-specific assurance/authority gate -> execute transition -> observe outcome -> scoped credit/update`

This remains a hypothesis, not a selected architecture.

## Next high-value work

1. **E14B** — changing delegation/revocation and boundary-maintenance failure;
2. **E20** — visible vs mixed-hidden vs rotating/adversarial regression evidence before deeper self-improvement;
3. **I05** — learn more of the I04 transition metadata (value, coupling, authority risk, verifier independence) rather than supplying it;
4. then E15/E16 self-improvement lineage/repair scope under the trusted-change protocol;
5. E24 JEPA predictive representation remains queued and should move up if I05 exposes a predictive-state bottleneck.

## Guardrail

Do not turn the common transition kernel into a universal scalar controller. The current evidence specifically supports shared allocation **while preserving typed authority, failure and durability semantics**.
