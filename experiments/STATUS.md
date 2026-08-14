# Phase 10 Experimental Status

**Checkpoint: fifteen provisional design principles selected; composition testing is now the primary experimental strategy.**

## Implemented blocks

Core and promotion experiments:

- E01/E01B — coordination topology and shared scarcity;
- E02/E02B/E02C — transfer/interference and compute-matched conditional sharing;
- E03/E03B — current state, source evidence and revision;
- E04/E04B — typed representation/fidelity;
- E05/E05B — adaptive compute and value-of-search;
- E06 — hypothesis plurality;
- E07 — active evidence acquisition;
- E08/E08B — predictive-state breadth and online breadth adaptation;
- E09/E09B/E09C — staged persistence, volatility adaptation and noise-vs-change identification;
- E10/E10B — serial and branching delayed credit assignment;
- E11 — retrieval similarity vs temporal/causal/downstream applicability;
- E22/E22B — cross-resource substitution, capacity contention and quality drift;
- E23/E23B — constructive and empirical beyond-teacher discovery mechanics.

Integrated composition generations:

- **I01 — integrated epistemic organism:** memory conflict, ambiguity, active evidence, discovery staging and shared resource allocation;
- **I02 — adaptive integrated organism:** online resource-quality learning, conditional shared/private estimation and fallible learned assurance;
- **I03 — assurance composition:** verification granularity, evaluator independence under optimizer pressure and consequence-sensitive assurance allocation.

## Validation

This continuation added:

- E08B: 4 tests;
- I01: 5 tests;
- I02: 5 replicated tests;
- I03: 6 replicated tests;
- E10A: 5 replicated tests;
- E10B: 5 replicated tests.

The continuation's local suite is **30/30 passing**, taking the Phase-10 added-test history to **104 passing tests**. Runtime code remains Python 3.11+ stdlib-only.

---

# Latest composition findings

## E08B / PS-012 — adaptive state breadth

Across a hidden low-switch → high-switch → low-switch lifetime:

- always broad: net ~`0.9880`;
- always narrow: net ~`0.9797`;
- adaptive breadth: **~`0.9909`**.

The adaptive controller changes broad-state fraction approximately `0.0006 → 0.9903 → 0.0678` without receiving the hidden regime label.

## I01 — individually good principles do not contribute equally

30-seed net utility/task:

| variant | utility/task |
|---|---:|
| **integrated full** | **2.3589** |
| no plurality | 2.3418 |
| no active information | 2.0879 |
| similarity retrieval | 1.9437 |
| immediate consolidation | 1.8541 |
| independent/first-come allocation | 2.2756 |

Immediate visible-evaluator consolidation creates ~`54.6` false durable writes/run, demonstrating that a discovery failure becomes a persistent-memory failure when the result is reused.

## I02 — metacognition itself must be learned

Operation/resource quality changes through three hidden regimes and differs by task family.

30-seed lifetime utility/task:

| estimator | utility/task |
|---|---:|
| **conditional shared/private** | **1.3511** |
| all shared | 1.2659 |
| all private | 1.3316 |
| frozen initial quality | 1.3391 |

Frozen initial economics is strongest while its assumptions remain true and degrades sharply in the first drift regime (`~0.880` vs `~1.062` conditional).

Assurance result:

| verifier policy | utility/task | false durable writes/run | secondary checks/task |
|---|---:|---:|---:|
| **adaptive learned assurance** | **1.3511** | 0.433 | **0.02022** |
| primary only | 1.1281 | **12.10** | 0.00000 |
| uniform double | 1.3487 | 0.433 | 0.02132 |

The system learns an observable unsafe-primary-approval rate around `0.193` for the risky family and `0.060` for the safer family.

## I03 / PS-013 — evaluator independence

A shared evaluator exploit becomes increasingly likely to be found as candidate search pressure rises.

At search pressure `16`:

- single primary exploit acceptance: ~`0.434`;
- correlated double evaluator: ~`0.430`;
- independent double evaluator: **~`0.0176`**.

The second correlated evaluator adds cost without removing the relevant failure mode. This promotes **PS-013 — failure-mode-independent assurance**.

## I03 / PS-014 — assurance is a priced resource

Default assurance prices:

- implicit confidence-triggered self-check: ~`-0.982` utility/task;
- explicit adaptive assurance: ~`0.543`;
- uniform heavy verification: **~`0.635`**.

Uniform heavy checking is correctly better when assurance is cheap relative to error consequence.

When independent/process verification price scales to `1.5×`:

- explicit adaptive: **~`0.420`**;
- uniform heavy: ~`0.257`.

At `2×`:

- explicit adaptive: **~`0.294`**;
- uniform heavy: ~`-0.128`.

Together I02 + I03 promote **PS-014 — consequence/uncertainty/resource-sensitive assurance allocation**.

## I03 / E12 — verification granularity stays open

Outcome-only and process-only checks fail differently:

- outcome-only process-failure acceptance: ~`0.113`;
- process-only final-failure acceptance: ~`0.227`;
- uniform both reduces both but costs ~`0.400`/task;
- adaptive granularity produces the best first-family net (`~0.013`) at ~`0.329` verification cost/task.

DL-012 is intentionally **not promoted** until a structurally different task family reproduces the result.

---

# Credit assignment

## E10A — serial sparse delayed reward

Nine stages must all be correct before a final success signal appears.

30-seed means:

| policy | tail success | false blame/episode | delayed items/episode |
|---|---:|---:|---:|
| global trajectory | 0.189 | 4.038 | 9.000 |
| local diagnostics | **0.692** | 1.898 | **0.000** |
| eligibility hybrid | **0.692** | **0.537** | 2.186 |

A stage-count dry run shows the factorized advantage appears as outcome ambiguity grows: global credit is adequate around five stages and collapses as compositional depth rises.

## E10B / PS-015 — sparse causal scope

Two speculative five-stage branches execute, but only one causally determines the outcome.

| policy | tail success | inactive-branch updates | false blame | delayed items |
|---|---:|---:|---:|---:|
| global all branches | 0.533 | **5.0** | 1.380 | 10.000 |
| branch factorized | **0.812** | **0.0** | 0.878 | 5.000 |
| branch + eligibility | **0.812** | **0.0** | **0.147** | **1.123** |

E10A + E10B promote **PS-015 — causal/eligibility-scoped delayed credit**.

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
15. PS-015 — causal/eligibility-scoped delayed credit.

No Phase-9 architecture family is selected.

---

# What is converging

Composition is beginning to collapse several apparently separate mechanisms into common abstract rules:

- **scope follows coupling/responsibility** — control and credit widen only when dependencies do;
- **state follows future value** — breadth, persistence and retrieval depend on expected future use and recoverability;
- **work follows marginal value** — compute, sensing and assurance are allocatable rather than fixed budgets;
- **sharing follows reusable structure** — transfer is useful until interference outweighs it;
- **authority follows evidence** — confidence, novelty and correlated votes do not create epistemic authority;
- **durability demands stronger evidence** — persistent state changes have higher downstream consequence than temporary computation.

These may eventually become fewer architecture primitives than the fifteen PS entries suggest. Testing that collapse is now more important than accumulating additional isolated modules.

## Next high-value work

1. construct **I04**, where one typed state-transition/resource allocator tries to implement several PS rules rather than separate hand-coded controllers;
2. give it learned estimates for future value, coupling, verifier independence and credit eligibility;
3. test pairwise/multi-principle ablations and interaction regressions;
4. finish DL-012 with a second verification-granularity family;
5. then move into E14 capability boundaries and E20 self-change regression evidence before enabling deeper self-improvement experiments.

## Guardrail

The research organism is not an architecture merely because more mechanisms have been combined. Architecture selection waits until the composition experiments reveal which boundaries remain necessary under shared learned state, authority and resource control.