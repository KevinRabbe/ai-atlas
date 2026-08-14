# E02 — Integrated vs Heterogeneous Computation

**Status:** first matched-parameter online-learning probe; preliminary multi-seed evidence only.

## Question

When does shared integrated computation earn its coupling, and when does explicit specialization reduce interference enough to justify routing boundaries?

## Why this probe uses a learned model

The E02 hypothesis is specifically about shared learned structure and update interference. A deterministic specialist-vs-general-algorithm comparison would bake the answer into the implementation, so this probe uses the smallest useful learned system: online linear binary tasks implemented with Python stdlib only.

## Matched capacity

Default: 3 task families, 6 input dimensions, integrated rank 2.

`specialists = 6 × 3 = 18 parameters`

`integrated = (6 × 2) + (3 × 2) = 18 parameters`

`integrated_shared_low_rank` uses a shared low-rank representation updated by every task. `heterogeneous_specialists` gives each task independent six-parameter state and counts a routing message for each handoff.

## Task structure

A hidden `sharedness` parameter controls how similar the true task rules are. Training is intentionally imbalanced toward task 0 so transfer can matter for lower-data tasks.

The experiment also performs a local rule-shift repair on task 0 after training and measures the effect on tasks 1/2. This makes shared-state interference observable.

## Preliminary 12-seed result

Each seed uses 1,200 training examples, 300 held-out examples per task and 80% of training traffic on task 0.

| sharedness | integrated accuracy | specialists accuracy | integrated cross-task interference after task-0 shift | specialist interference |
|---:|---:|---:|---:|---:|
| 0.98 | 0.977 | 0.958 | 0.199 | 0.000 |
| 0.75 | 0.907 | 0.962 | 0.140 | 0.000 |
| 0.15 | 0.759 | 0.952 | 0.060 | 0.000 |

The useful result is the crossover: very highly shared tasks can benefit from integrated transfer at equal parameter count; as task rules diverge, the rank-constrained shared state becomes a bottleneck; local adaptation can alter unrelated tasks through shared state while isolated specialists contain that update by construction.

The current integrated factorization also performs more arithmetic per update, while specialists pay an explicit routing message. Those costs are reported rather than hidden.

## Important limitation

This is not evidence that an integrated predictive core in general behaves like a rank-2 linear factorization. It is controlled evidence that sharing has both transfer value and an interference surface, and that the optimum moves with task relatedness.

## Next discriminators

Nonlinear/compositional task family; matched realized compute as well as parameter count; partially shared specialists; learned routing; update-locality mechanisms inside an otherwise integrated substrate; resource-regime shift before design-ledger promotion.
