# Phase 10 Experimental Status

**Checkpoint: twelve provisional design principles selected; first integrated composition organism implemented.**

## Implemented experimental blocks

- E01/E01B — coordination topology and shared scarcity;
- E02/E02B/E02C — transfer/interference and compute-matched conditional sharing;
- E03/E03B — current state, evidence history and revision;
- E04/E04B — typed representation/fidelity;
- E05/E05B — adaptive compute and value-of-search;
- E06 — hypothesis plurality;
- E07 — active evidence acquisition;
- E08/E08B — predictive-state breadth, optionality and online breadth adaptation;
- E09/E09B/E09C — staged persistence, volatility adaptation and noise-vs-change identification;
- E11 — retrieval similarity vs temporal/causal/downstream applicability;
- E22/E22B — cross-resource substitution, capacity contention and quality drift;
- E23/E23B — constructive and empirical beyond-teacher discovery mechanics;
- **I01 — first integrated epistemic organism**, combining multiple selected principles in one state-transition/resource loop.

## Validation

E08B adds **4 passing local semantic tests** and I01 adds **5 passing local composition tests**. Including earlier Phase-10 groups, the experimental reconstruction history now contains **83 newly added passing unit tests**. Runtime code remains Python 3.11+ stdlib-only.

## E08B — adaptive state breadth

E08A established a static frontier: narrow state wins with fixed goals, source-recoverable state wins with occasional objective switches, and broad hot state wins when switching/rematerialization becomes frequent.

E08B hides and changes the objective-switch rate. The controller estimates recent switching and expands/contracts hot state around the measured break-even between extra active-state rent and reacquisition cost.

30-seed means over low-switch → high-switch → low-switch segments:

| policy | net utility | cost/step | broad fraction | reacquisitions/run |
|---|---:|---:|---:|---:|
| always broad | 0.988000 | 0.012000 | 1.000 | 0.0 |
| always narrow | 0.979654 | 0.020346 | 0.000 | 765.1 |
| **adaptive breadth** | **0.990918** | **0.009082** | 0.353 | 51.4 |

Adaptive broad fraction by segment is approximately `0.0006 → 0.9903 → 0.0678` without access to the hidden regime labels.

This promotes **PS-012 — adaptive predictive-state breadth / recoverable optionality**.

## I01 — first composition checkpoint

I01 changes the research strategy from isolated mechanisms to interaction testing. One common epistemic state model contains exact identity/provenance, tentative/durable knowledge, rejected hypotheses, operation proposals, evidence links and shared resource capacities.

The mixed stream interleaves:

- stale/surface-conflicting memory decisions;
- ambiguous high-consequence actions;
- scarce exact observations;
- frontier/research candidates with a fallible visible evaluator;
- scarce independent verification;
- later reuse of durable learned knowledge.

### 30-seed means

| variant | net utility/task | safe rate | retrieval error | false durable writes/run |
|---|---:|---:|---:|---:|
| **integrated full** | **2.3589** | 0.0334 | 0.0124 | **0.0** |
| no plurality | 2.3418 | 0.0000 | 0.0252 | 0.0 |
| no active information | 2.0879 | 0.1713 | 0.0437 | 0.0 |
| similarity retrieval | 1.9437 | 0.0020 | 0.1079 | 0.0 |
| immediate consolidation | 1.8541 | 0.0332 | 0.0123 | **54.6** |
| independent allocation | 2.2756 | 0.0450 | 0.0086 | 0.0 |

The full organism averages about `0.248` deep retrievals/task, `0.196` probes/task and `0.072` independent verifications/task. Roughly `0.434` of later application decisions are served from durable learned knowledge after acquisition.

### Interaction findings

1. **Discovery governance becomes a memory problem.** False research conclusions are reused later; staged independent verification prevents that persistent contamination in this exact-verifier environment.
2. **Retrieval and observation substitute.** Removing applicability-aware retrieval pushes more decisions toward expensive probing.
3. **Plurality and evidence acquisition are complementary.** Plurality provides a safe fallback when uncertainty cannot economically be resolved; active information resolves it when the probe is worth its price.
4. **Task-local intelligence is insufficient under shared scarcity.** First-come allocation uses the same local expected gains but wastes scarce slots on lower-value tasks compared with joint ranking.

I01 is a **composition experiment, not a thirteenth principle and not an architecture-family selection**.

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
11. PS-011 — retrieval by expected applicability/downstream value;
12. **PS-012 — adaptive predictive-state breadth / recoverable optionality.**

No Phase-9 architecture family is selected.

## Next milestone — I02

The next integrated generation should stop assuming perfect hand-specified value estimates and an exact verifier.

Highest-value additions:

1. merge E08B adaptive breadth into the integrated lifetime;
2. learn operation quality/value online rather than reading benchmark reliabilities;
3. add conditional shared/private estimators from PS-009;
4. make verification fallible/correlated so assurance allocation and evaluator independence become active decisions;
5. introduce within-lifetime resource-price and environment shifts;
6. run pairwise interaction ablations, not only one-principle removals;
7. then proceed to E10/E12/E13/E21 using the integrated organism rather than isolated toy loops where possible.

## Guardrail

Composition is now the primary research target. The organism must remain simpler than the hypotheses it measures, every principle remains replaceable, and apparent gains from one subsystem must be checked for downstream regressions elsewhere.