# Improvement Surfaces and Attribution

## Required function

Determine what caused a weakness/opportunity and select the smallest mutation surface likely to improve it without unnecessary collateral change.

## Candidate mutation surfaces

- active context/state;
- retrieval/memory policy;
- prompts/instructions;
- executable skill/procedure;
- tool/interface;
- routing/scheduling;
- harness code;
- data/curriculum;
- evaluator/reward model;
- parameter-efficient deltas;
- shared weights;
- architecture/developmental program;
- hardware/compiler configuration.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SIA-AT-01 | Fixed-model performance can improve substantially from harness/context-policy changes alone. | O | E4 | SI-S001, SI-S002, SI-S003 |
| SIA-AT-02 | Joint harness + weight modification can outperform harness-only iteration on heterogeneous studied tasks, implying some weaknesses are not fully removable at one layer. | O | E2 | SI-S004 |
| SIA-AT-03 | Parameter-efficient and test-time adaptation from Phase 2 show useful changes need not always modify all shared weights. | O/I | E4 | prior Learning evidence |
| SIA-AT-04 | Architecture/hyperparameter search can improve capability by changing the learning/computational substrate rather than task weights alone. | O | E4 | SI-S007, SI-S008 |

## Improvement attribution problem

A failure such as “agent repeatedly misses relevant file” may be caused by:

- insufficient learned understanding;
- context truncation;
- bad retrieval query;
- tool interface;
- harness retry policy;
- memory corruption;
- evaluator error;
- task ambiguity.

Updating weights because the visible output was wrong can therefore target the wrong layer.

## Minimal-mutation principle

A useful hypothesis is:

> prefer the cheapest reversible mutation that addresses the diagnosed cause, then escalate scope only when evidence shows the local fix is insufficient.

This is not a law. A broader weight/architecture change may produce better transfer than repeated local patches. The point is to make scope a measured decision.

## Attribution evidence

Candidate signals include:

- execution traces and failure localization;
- counterfactual reruns with one component replaced;
- ablations;
- evaluator disagreement;
- hidden-state/monitor evidence;
- repeated failure clusters;
- controlled repair experiments;
- lifetime cost of local workaround versus durable integration.

## Clean-sheet restatement

Self-improvement needs a **mutation router**:

`observed failure/opportunity -> causal diagnosis -> candidate target layer(s) -> minimal intervention experiments -> validated mutation scope`.

This is analogous to credit assignment, but the variables are entire system components and persistence layers rather than individual parameters.

## Failure modes

Changing weights to repair a tool-interface problem; adding harness complexity to compensate for missing base capability; evaluator blamed for generator failure or vice versa; local patch accumulation; broad mutation without diagnosis; cross-layer interaction hidden by one-factor ablations; selecting the easiest-to-edit layer rather than the causal layer.
