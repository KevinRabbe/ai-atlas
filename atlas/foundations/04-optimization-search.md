# Optimization and Search

## Required function

Select useful parameters, programs, plans or actions from spaces too large to enumerate exhaustively.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-OS-01 | Stochastic approximation can converge using noisy local feedback, showing that exact objectives/gradients are not always required at each step. | O | E5 | F-S021 |
| F-OS-02 | Stochastic global-search procedures such as simulated annealing can trade additional exploration for escape from poor local configurations. | O | E4 | F-S022 |
| F-OS-03 | On separable logistic problems, gradient descent selects a max-margin direction despite the absence of an explicit max-margin regularizer. | O | E4 | F-S023 |
| F-OS-04 | Different optimization geometries can select different solutions from underdetermined sets of fitting solutions; optimizer choice can therefore act as implicit regularization. | O | E3 | F-S024 |
| F-OS-05 | No optimizer dominates uniformly over all objective classes covered by no-free-lunch assumptions; good search exploits structure. | O | E5 | F-S009 |

## What seems established

### Optimization is not necessarily a neutral transport mechanism

In an underdetermined problem there may be many solutions with similar training/objective value. The trajectory and geometry of the optimizer can systematically prefer some of them. Therefore “model + objective” does not fully specify what is learned; **the learning algorithm is part of the inductive bias**.

### Search requires a structure assumption

Local smoothness, decomposability, reusable substructure, informative heuristics, simulator fidelity, gradients, priors or evaluator quality all constrain where search effort should go. A search method that performs well is exploiting at least one such property.

### Exploration has an opportunity cost

Searching a wider space may find better solutions but delays exploitation and consumes compute. This appears both in parameter optimization and sequential decision problems. Later architecture work should account for expected value of computation rather than equating more search with more intelligence.

## Mechanism families to keep distinct

- local iterative improvement;
- gradient/pathwise optimization;
- stochastic/score-function optimization;
- population/evolutionary search;
- tree/graph search;
- program search;
- Bayesian/surrogate optimization;
- learned search policies and heuristics.

The Atlas should compare these by information requirements, parallelism, sample cost, memory, robustness to nonstationarity and capacity to exploit structure—not by fashion.

## Clean-sheet restatement

An intelligent system needs a **proposal-and-selection process** for spaces where exhaustive enumeration is impossible. The mechanism should exploit available structure, estimate the value of further exploration, and expose how its search bias changes the solutions it finds.

## Open questions

- Can a system learn which optimizer/search geometry matches a new problem online?
- When should search produce a one-off answer versus a reusable learned heuristic?
- How should evaluator uncertainty affect search breadth and stopping?
- What information should be shared between parallel search branches?
- Can learned optimizers adapt without becoming brittle to out-of-distribution objective geometry?

## Failure modes

Assuming the optimizer is neutral; premature exploitation; endless exploration; evaluator hacking; local objective improvement with global regressions; hidden compute amplification; search policies overfit to benchmark topology.
