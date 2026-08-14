# Uncertainty and Decision

## Required function

Represent incomplete knowledge in a form that supports calibrated prediction, information gathering and decisions with asymmetric consequences.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-UD-01 | Calibration gives a testable relationship between stated probabilities and observed frequencies under suitable repeated-event conditions. | O | E5 | F-S025 |
| F-UD-02 | Strictly proper scoring rules incentivize reporting the forecaster's true predictive distribution in expectation and connect probabilistic prediction to entropy/divergence functions. | O | E5 | F-S026 |
| F-UD-03 | Distinguishing uncertainty associated with irreducible observation noise from uncertainty about model knowledge can improve uncertainty modeling in practical prediction tasks. | O | E3 | F-S027 |
| F-UD-04 | Approximate Bayesian methods can expose useful predictive uncertainty without exact Bayesian inference, though approximation quality is method- and regime-dependent. | O | E3 | F-S028 |
| F-UD-05 | In sequential allocation problems, optimal behavior must sometimes spend actions on information acquisition rather than immediate reward. | O | E5 | F-S031 |

## What seems established

### Confidence is not enough

A system can assign a large score to its chosen output while being systematically wrong. Useful uncertainty must be externally testable. Calibration and proper scoring provide two complementary tools: calibration asks whether probabilities match frequencies; proper scores make honest probabilistic forecasts optimal under the scoring rule.

### Uncertainty matters because decisions have different loss surfaces

The same predictive distribution can rationally produce different actions depending on the cost of errors, reversibility, information value and available fallback actions. Therefore uncertainty representation and decision policy should remain distinguishable.

### Some uncertainty can be reduced by acquiring information; some cannot

The aleatoric/epistemic distinction is not a complete ontology, but it captures an operational difference: if uncertainty can be reduced by computation, data, experiment, retrieval or interaction, the system may rationally allocate resources to reduce it. If it cannot, risk-aware action selection matters more.

## Clean-sheet restatement

The system needs to represent **what it expects, how uncertain that expectation is, what evidence could change it, and how much reducing uncertainty is worth before acting**.

This does not require committing to exact Bayesian inference as the implementation. It does require that uncertainty claims can be scored against reality and influence resource allocation/actions.

## Open questions

- What uncertainty representation remains tractable for high-dimensional structured outputs and long-horizon plans?
- How should uncertainty propagate through tool calls, retrieval, subagents and world-model rollouts?
- When is ensemble disagreement meaningful epistemic signal versus correlated shared error?
- How should model uncertainty and evaluator uncertainty interact?
- Can calibration survive continual learning and distribution shift without constant labeled feedback?

## Discriminating experiments

Give systems the option to answer, retrieve, simulate, ask, defer or run additional reasoning at explicit costs. Evaluate whether uncertainty predicts both error and the expected value of purchasing additional information/computation.

## Failure modes

Softmax/logit confidence treated as probability; calibrated averages hiding subgroup failures; uncertainty estimates that collapse under shift; costly information gathering with negligible decision value; ignoring correlated errors among supposedly independent evaluators.
