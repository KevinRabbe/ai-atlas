# Computation, Complexity and Resource Bounds

## Required function

Turn information into useful decisions under finite time, memory, communication, energy and interaction budgets.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-CC-01 | There are precisely formulable computational problems that no general algorithm can solve; computability is a real boundary, not merely an engineering inconvenience. | O | E5 | F-S015 |
| F-CC-02 | Among computable problems, resource requirements differ qualitatively; reductions and complexity classes formalize that some solutions would imply unexpectedly powerful algorithms for many others. | O | E5 | F-S016 |
| F-CC-03 | Universal induction can be formulated by weighting computable hypotheses according to algorithmic simplicity, providing an important theoretical ideal. | O | E4 | F-S017, F-S018 |
| F-CC-04 | Universal search can provide asymptotic/constant-factor-style optimality relative to broad program classes, but the constants/search space can make it impractical. | O | E4 | F-S019 |
| F-CC-05 | Universal-agent formalisms combining algorithmic probability and sequential decision theory can be defined, but their ideal forms are uncomputable; computable approximations introduce severe resource dependence. | O | E4 | F-S020 |

## What seems established

### Formal universality is not a practical architecture

A universal formalism can be valuable because it isolates the assumptions needed for ideal induction or control. But if its exact solution is uncomputable, saying “use universal induction” does not specify an implementable intelligence. A practical system must decide **which parts of the hypothesis/action space deserve finite search**.

### Intelligence is necessarily resource-bounded

Even when the desired mapping exists and is computable, the relevant question is whether it can be found and executed within available time, memory, energy and communication. This makes compute allocation part of intelligence rather than merely an implementation detail.

### Amortization and search are complementary

A learned mapping spends resources earlier to make repeated future decisions cheap; online search spends resources later to adapt to the current instance. Neither dominates universally. The clean-sheet system will eventually need a theory for when reusable structure should be compiled into persistent state versus recomputed.

## Implications for later Atlas domains

- **Reasoning:** search depth/branching must be budgeted against expected value.
- **Memory:** stored results trade memory/bandwidth for recomputation.
- **Agents:** delegation introduces communication and coordination complexity.
- **Hardware:** arithmetic throughput alone is insufficient; data movement can dominate.
- **Self-improvement:** architecture search itself is a computational problem and needs a bounded evaluator/search loop.

## What is not established

- That the Turing-machine abstraction identifies the efficient physical substrate for intelligence.
- That worst-case complexity predicts typical real-world difficulty.
- That algorithmic description length is directly computable enough to serve as an operational objective.
- That one universal search strategy is competitive under realistic finite budgets.

## Clean-sheet restatement

The system must continually choose **which computations are worth performing now**, which results should be amortized or cached, which searches should be abandoned, and which approximations are adequate. Any architecture that ignores finite-resource scheduling is incomplete even if its idealized reasoning rule is optimal.

## Discriminating experiments

Build task distributions with controllable reuse and novelty. Under fixed lifetime compute, compare pure amortization, pure search and adaptive mixtures. Measure not only accuracy but total compute, latency, memory traffic, adaptation speed and opportunity cost.

## Failure modes

Invoking uncomputable ideals as implementable mechanisms; worst-case-only design; uncontrolled search explosion; recomputing reusable structure; storing everything despite retrieval/data-movement costs; treating more reasoning compute as free.
