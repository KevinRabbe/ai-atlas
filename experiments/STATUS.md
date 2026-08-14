# Phase 10 Experimental Status

**Checkpoint: Tier-1 complete; Tier-2 belief/information block implemented; eight provisional design principles selected on 2026-08-14.**

## Implemented probes

Tier-1: E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

Promotion/system follow-ups: E01B, E02B, E03B, E04B, E05B, E09B, E22.

Epistemic-growth/Tier-2 work now includes:

- `E23_DISCOVERY_LOOP` — constructive weak-teacher / independent-evaluator discovery;
- `E06_BELIEF_HYPOTHESES` — single belief versus consequence-sensitive hypothesis plurality;
- `E07_ACTIVE_INFORMATION` — passive/fixed/myopic versus value-driven active evidence acquisition;
- `E23B_CAUSAL_SCIENCE` — causal toy science requiring active interventions to resolve theories that passive teacher knowledge cannot distinguish.

## Validation

The new E06/E07/E23B group was executed locally with Python 3.11+ stdlib only.

**12 new Tier-2 tests pass locally** in this continuation. Combined with the earlier Phase-10 additions, the current local validation history contains **54 newly added passing unit tests** across the experimental reconstruction work.

Multi-seed sweeps now include:

- E01/E02/E04: 12 seeds;
- E01B: 20 seeds × verification-capacity regimes;
- E02B: 12 seeds × relatedness × data budgets;
- E03B: 20 seeds × source-retraction regimes;
- E04B: 20 seeds × score-distribution shifts;
- E05B: 20 seeds × evaluation-cost regimes;
- E09B: 30 seeds × alternating hidden volatility;
- E22: 30 seeds × resource-price regimes;
- E23: 30 seeds under exact and defective visible evaluators;
- E06: 20 seeds × observation-reliability regimes;
- E07: 20 seeds × probe-cost regimes;
- E23B: 30 seeds × experiment-cost regimes plus false-theory-consequence sweeps.

## New Tier-2 findings

### E06 — belief ambiguity

With four hidden worlds and noisy evidence, forcing the maximum-posterior world causes large wrong-commitment rates when evidence is weak. Preserving the full hypothesis set plus a safe action greatly improves utility in those regimes, while the gap narrows as observations become decisive.

20-seed means:

| reliability | single utility / wrong | multiple utility / wrong / safe |
|---:|---:|---:|
| 0.56 | -0.373 / 0.686 | 0.100 / 0.000 / 1.000 |
| 0.65 | -0.154 / 0.577 | 0.129 / 0.120 / 0.701 |
| 0.80 | 0.274 / 0.363 | 0.409 / 0.053 / 0.539 |
| 0.97 | 0.882 / 0.059 | 0.894 / 0.002 / 0.114 |

The causal second-family ablation gives both variants the same intervention. Preserving unresolved theories becomes better as the cost of a false theory rises; forced single commitment remains better when false claims are cheap. This establishes a real crossover rather than a universal preference for plurality.

### E07 — active information acquisition

The benchmark compares passive observation, always buying both probes, myopic one-step VOI and bounded two-step VOI.

A useful failure appeared during development: one-step VOI can reject a probe whose standalone value is low even though it unlocks a valuable second probe. The final benchmark therefore preserves myopic VOI as an explicit ablation.

20-seed means:

| probe cost | passive net | fixed net / queries | myopic net / queries | lookahead net / queries |
|---:|---:|---:|---:|---:|
| 0.02 | 0.124 | 1.062 / 2.000 | 1.062 / 2.000 | 1.062 / 2.000 |
| 0.08 | 0.124 | 0.942 / 2.000 | 0.877 / 1.617 | 0.942 / 2.000 |
| 0.20 | 0.124 | 0.702 / 2.000 | 0.161 / 0.069 | 0.702 / 1.986 |
| 0.60 | 0.124 | -0.098 / 2.000 | 0.124 / 0.000 | 0.183 / 0.612 |
| 2.00 | 0.124 | -2.898 / 2.000 | 0.124 / 0.000 | 0.124 / 0.000 |

The lookahead policy buys all information when it is cheap, becomes selective at intermediate prices and stops completely when probing is not worth its cost.

### E23B — causal empirical discovery

Three candidate causal theories are observationally indistinguishable under inherited/passive evidence. Interventions reveal different signatures.

30-seed means:

| experiment cost | teacher accuracy/net | fixed-one accuracy/net | active accuracy / experiments / unresolved / net |
|---:|---:|---:|---:|
| 0.01 | 0.338 / -0.324 | 0.672 / 0.334 | 1.000 / 1.662 / 0.000 / 0.983 |
| 0.05 | 0.338 / -0.324 | 0.672 / 0.294 | 1.000 / 1.662 / 0.000 / 0.917 |
| 0.20 | 0.338 / -0.324 | 0.672 / 0.144 | 1.000 / 1.662 / 0.000 / 0.668 |
| 0.60 | 0.338 / -0.324 | 0.672 / -0.256 | 0.000 / 0.000 / 1.000 / 0.000 |
| 1.00 | 0.338 / -0.324 | 0.672 / -0.656 | 0.000 / 0.000 / 1.000 / 0.000 |

At low/moderate cost the active system identifies the hidden theory exactly and crosses the passive teacher frontier. At high cost it performs no experiment and leaves the result unresolved instead of fabricating a theory.

## Provisional selections

The design ledger now contains eight reversible principle-level selections for the current experimental generation:

1. **PS-001 — typed hybrid boundary state**;
2. **PS-002 — staged adaptive persistence**;
3. **PS-003 — coupling-scoped coordination**;
4. **PS-004 — derived current belief with evidence linkage**;
5. **PS-005 — value-of-computation stopping**;
6. **PS-006 — consequence-sensitive hypothesis plurality**;
7. **PS-007 — value-driven active evidence acquisition**;
8. **PS-008 — verified epistemic frontier expansion**.

PS-008 is deliberately narrow: supervision/bootstrap knowledge may guide search without defining the ceiling, but novelty remains tentative and requires sufficiently independent evidence before durable promotion. The current E23/E23B systems do **not** claim new human knowledge.

## Still unresolved

- **DL-002 cognitive integration:** partial sharing still needs realized-compute matching.
- **DL-008 predictive-state breadth:** broad reconstruction versus decision-sufficient state remains open.
- **DL-011 memory retrieval objective:** similarity versus downstream decision value remains open experimentally.
- **DL-022 cross-resource metacontrol:** needs a second family with shared capacity and resource-quality drift.
- E09B still needs explicit disentanglement of observation noise from true environmental volatility.

## Next targets

1. compute-matched conditional sharing for E02B;
2. E22B with capacity contention + quality drift;
3. Tier-2 E08 predictive-state breadth and E11 retrieval objective;
4. E09B noise-versus-volatility disentanglement;
5. then assemble the next-generation organism from PS-001 through PS-008 and test whether the combined system retains the individual advantages without interaction regressions.

## Guardrail

The measuring instrument must remain simpler than the hypotheses it measures. Every provisional selection remains reversible, and novel output is never promoted to knowledge merely because the generator or its visible evaluator prefers it.
