# E23B — Causal Toy Science Discovery

**Status: implemented, tested and swept; synthetic discovery evidence only.**

## Purpose

E23's first family tested constructive discovery on a deceptive search landscape. E23B tests a different regime: **empirical discovery where passive knowledge is insufficient and the system must choose interventions to learn which world it inhabits.**

## World

Three causal theories produce the same inherited passive observation, so the teacher's corpus cannot distinguish them. Two interventions have different deterministic signatures under the three theories.

The teacher commits to one inherited explanation without new experiments.

Compared variants:

1. `teacher_passive` — fixed inherited theory;
2. `fixed_experiment` — perform one fixed intervention, then force one compatible theory;
3. `fixed_experiment_multi` — perform the same intervention but preserve an unresolved theory set when evidence is insufficient;
4. `active_hypothesis_science` — preserve candidate theories, choose the next discriminating intervention by expected utility, and stop unresolved when experiments cost more than the expected knowledge value.

## Validation

**5 E23B-specific unit tests pass**, including beyond-teacher identification, fixed-vs-active experiment choice, same-intervention ambiguity handling, bounded experiment count and high-cost abstention.

Together with E06/E07, **12 new Tier-2 tests pass locally** in this continuation.

## 30-seed experiment-cost sweep

| experiment cost | teacher accuracy / net | fixed-one accuracy / net | active accuracy / experiments / unresolved / net |
|---:|---:|---:|---:|
| 0.01 | 0.338 / -0.324 | 0.672 / 0.334 | 1.000 / 1.662 / 0.000 / 0.983 |
| 0.05 | 0.338 / -0.324 | 0.672 / 0.294 | 1.000 / 1.662 / 0.000 / 0.917 |
| 0.20 | 0.338 / -0.324 | 0.672 / 0.144 | 1.000 / 1.662 / 0.000 / 0.668 |
| 0.60 | 0.338 / -0.324 | 0.672 / -0.256 | 0.000 / 0.000 / 1.000 / 0.000 |
| 1.00 | 0.338 / -0.324 | 0.672 / -0.656 | 0.000 / 0.000 / 1.000 / 0.000 |

At low/moderate experiment cost the active system moves beyond the passive teacher frontier and identifies the hidden theory exactly. At sufficiently high cost it does **not** fabricate a theory; it records the state as unresolved.

## What this adds to E23

The first E23 family showed:

`teacher frontier -> diverse search -> independent verification -> beyond-teacher constructive result`.

E23B adds:

`bootstrap theories -> unresolved ambiguity -> choose intervention -> new evidence from world -> update hypotheses -> verified empirical belief`.

The two families therefore test different ways human/bootstrap knowledge can stop being the epistemic ceiling:

- search can expose implications/constructions absent from demonstrations;
- interaction can supply genuinely missing information that no amount of internal reasoning can infer from the current evidence.

## Limits

The candidate theories and hidden truth are benchmark-defined. This is **not new human scientific knowledge**. It tests the control semantics required before attempting open-ended empirical discovery.
