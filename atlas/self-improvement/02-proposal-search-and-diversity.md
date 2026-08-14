# Proposal Search, Populations and Diversity

## Required function

Generate and select improvement candidates without collapsing prematurely onto one local path whose weaknesses become inherited by every future version.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-PS-01 | Population-based training can jointly adapt parameters/hyperparameter schedules during training and outperform fixed hand-selected schedules in studied settings. | O | E4 | SI-S006 |
| SI-PS-02 | Darwin Gödel Machine improves coding agents through an archive/tree of self-modified descendants rather than maintaining only one incumbent path. | O | E3 | SI-S005 |
| SI-PS-03 | AlphaEvolve-style proposal + automated evaluation + evolutionary retention can discover useful algorithms and production optimizations. | O | E4 | SI-S009 |
| SI-PS-04 | AlphaTensor found many distinct correct algorithms and could optimize them for different hardware objectives, showing value in retaining solution diversity. | O | E4 | SI-S010 |

## Why one lineage is fragile

Greedy self-improvement:

`current best -> mutate -> keep if score improves -> repeat`

can lose stepping stones that are temporarily worse on the current metric but enable later improvements. It also makes every future version inherit a hidden defect introduced early.

Population/archive approaches preserve:

- alternative architectures;
- different tool/harness strategies;
- specialists;
- failed-but-informative branches;
- candidates optimized for different resource/risk profiles.

## Diversity must be useful

Random variation is not inherently valuable. Candidate diversity should target dimensions where correlated failure is costly:

- different reasoning/control strategy;
- different state/memory representation;
- different tool path;
- different optimization history;
- different evaluator assumptions;
- different resource profile.

## Multi-objective frontier

One scalar “fitness” can erase important trade-offs. A self-improving system may need a Pareto archive across:

`quality / compute / latency / memory / robustness / calibration / safety / generality / maintainability`.

A candidate can be worth retaining even if it is not globally best on one number.

## Open-endedness vs controlled search

Open-ended improvement increases discovery potential but also expands evaluation burden and attack surface. Search-space growth should therefore remain coupled to assurance capacity: broader mutations require stronger independent tests and containment.

## Clean-sheet restatement

Self-improvement is partly a search problem over **system variants**, and diversity is a hedge against local optima and correlated regressions. Selection should preserve promising alternative lineages until evidence is strong enough to prune them.

## Failure modes

Premature convergence; benchmark monoculture; archive explosion; diversity with no functional difference; retaining unsafe variants without containment; fitness dominated by one metric; mutation operators unable to reach structural changes; stepping stones discarded by greedy selection; evaluator bias copied into every lineage.
