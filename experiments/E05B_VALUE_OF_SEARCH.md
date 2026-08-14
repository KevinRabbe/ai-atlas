# E05B — Value-of-Computation in Costly Candidate Search

**Status:** second E05 family; preliminary 20-seed evidence.

## Why a second family

Original E05 uses repeated noisy evidence for one binary decision. E05B instead presents 6–26 candidate solutions with imperfect heuristic scores. Exact evaluation reveals a candidate's true value but incurs a configurable cost. The problem is therefore **how many alternatives are worth verifying before stopping**, not how many votes to sample.

## Variants

Fixed budgets evaluate the top 1, 3, 8 or 20 heuristic candidates and select the best exact value seen.

`adaptive_value_of_search` evaluates the leading candidate and then asks whether the next candidate's calibrated optimistic value could improve the current best enough to justify the exact-evaluation cost. Its stopping rule uses task value, heuristic uncertainty and current evaluation cost; it never receives a hidden difficulty label.

## 20-seed means

| exact-eval cost | adaptive net utility | adaptive regret | adaptive evals | best fixed utility |
|---:|---:|---:|---:|---:|
| 0.02 | **2.954** | 0.029 | 1.683 | 2.922 |
| 0.08 | **2.853** | 0.033 | 1.622 | 2.742 |
| 0.25 | **2.597** | 0.045 | 1.482 | 2.498 |
| 0.60 | 2.152 | 0.068 | 1.307 | 2.148 |

At the expensive 0.60 regime the adaptive policy is essentially tied with the best fixed one-evaluation policy; at cheaper regimes it spends additional evaluations selectively and exceeds the best tested fixed utility.

## Allocation behavior

At evaluation cost 0.25:

- low-noise heuristic tasks use ~1.04 evaluations on average;
- high-noise/ambiguous tasks use ~2.13;
- low-value tasks use ~1.38;
- high-value tasks use ~1.59.

As evaluation cost rises from 0.02 to 0.60, average work falls from ~1.68 to ~1.31 evaluations without changing the policy code.

## Interpretation

Together with E05's noisy-evidence family, E05B supports a broader rule than "use confidence thresholds": **inference work should be allocated according to expected marginal downstream value relative to its current cost**.

Difficulty, consequence/task value, uncertainty and resource price all change the useful stopping point. Unused budget can therefore be a correct outcome.

## Design-ledger implication

E05 now has two structurally different task families, task-difficulty variation and an independent computation-price sweep. DL-005 can move to a principle-level provisional selection: adaptive value-of-computation/stopping rather than one fixed inference budget. The exact value estimator remains open.

## Falsifier

The principle should be weakened if a fixed budget consistently matches adaptive lifetime utility once the policy must estimate uncertainty/cost/value under distribution shift, or if the overhead of estimating marginal value exceeds the saved computation on realistic workloads.
