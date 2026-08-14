# Phase 10 Experimental Status

**Checkpoint: eleven provisional design principles selected; predictive-state breadth remains open after one family.**

## Implemented experimental blocks

- E01/E01B — coordination topology and shared scarcity;
- E02/E02B/E02C — transfer/interference and compute-matched conditional sharing;
- E03/E03B — current state, evidence history and revision;
- E04/E04B — typed representation/fidelity;
- E05/E05B — adaptive compute and value-of-search;
- E06 — hypothesis plurality;
- E07 — active evidence acquisition;
- E08 — predictive-state breadth / future-objective optionality;
- E09/E09B/E09C — staged persistence, volatility adaptation and noise-vs-change identification;
- E11 — retrieval similarity vs temporal/causal/downstream applicability;
- E22/E22B — cross-resource substitution, capacity contention and quality drift;
- E23/E23B — constructive and empirical beyond-teacher discovery mechanics.

## Validation

E08, E11 and E09C each add **4 passing local semantic tests**. Including earlier Phase-10 groups, the experimental reconstruction history now contains **74 newly added passing unit tests**. Runtime code remains Python 3.11+ stdlib-only.

## Latest findings

### E08 — state breadth is future-objective dependent

A 12-bit world is queried under objectives A/B. The benchmark prices hot-state rent, cold/source retention and rematerialization separately.

20-seed net-utility means:

| goal-switch probability | broad hot | narrow current-objective | source-recoverable hybrid |
|---:|---:|---:|---:|
| 0.00 | 0.976 | **0.994** | 0.990 |
| 0.02 | 0.976 | 0.820 | **0.989** |
| 0.10 | 0.976 | 0.759 | **0.983** |
| 0.20 | ~**0.976** | 0.751 | ~**0.976** |
| 0.50 | **0.976** | 0.746 | 0.953 |
| 0.80 | **0.976** | 0.744 | 0.931 |

No selection is promoted yet. The first family shows that decision sufficiency is relative to the expected future objective distribution: narrow state wins when goals are fixed, recoverable-source state wins under occasional changes, and broad hot state wins when reconstruction becomes constant.

### E11 — retrieval objective

Two families now separate semantic resemblance from applicability.

- In a stable corpus, similarity is cheapest because deeper checks do not change the correct answer.
- As exact-topic memories become stale, similarity accuracy falls from 1.0 to ~0 while temporal/applicability retrieval remains 1.0.
- In a separate surface-vs-causal family, similarity falls with surface/causal conflict while decision-value retrieval remains 1.0 by checking mechanism, outcome and verification.

This promotes **PS-011 — retrieval by expected applicability/downstream value**, while retaining similarity as a cheap candidate signal when it is a good proxy.

### E09C — noise vs true volatility

30-seed means:

| regime | single sensor | always corroborate | adaptive corroboration |
|---|---|---|---|
| stable + noisy | 0.901 acc / 198.5 false updates / 0.901 net | 0.993 / 0.33 / 0.987 | **0.988 / 9.53 / 0.983** |
| volatile + clean | **0.909 / 8.77 / 0.909** | 0.902 / 0.20 / 0.896 | **0.908 / 7.57 / 0.908**, second sensor ~10.6% |
| stable + clean | **0.997 / 0.00 / 0.997** | 0.997 / 0.00 / 0.991 | **0.997 / 0.00 / 0.996**, second sensor 10% |

A single observation channel can confound `world changed` with `sensor failed`. Independent corroboration resolves the ambiguity, but reading it constantly is wasteful. This closes the earlier PS-002 noise/volatility falsifier and couples persistence control to PS-006/PS-007.

## Current provisional selections

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
11. PS-011 — retrieval by expected applicability/downstream value.

No Phase-9 architecture family is selected.

## Next milestone

The project has enough individually supported principles to justify a shift in experimental strategy.

Next:

1. finish E08 with a second learned/dynamic predictive family;
2. build a **next-generation integrated organism** constrained by PS-001 through PS-011;
3. test interaction regressions and ablate each principle under matched lifetime resources;
4. only then continue into deeper verification, credit-assignment, self-improvement and physical-co-design decisions.

## Guardrail

The next integrated organism must not simply bolt eleven named modules together. It should discover the smallest mechanism boundaries that satisfy the selected functions, while every principle remains replaceable and falsifiable.
