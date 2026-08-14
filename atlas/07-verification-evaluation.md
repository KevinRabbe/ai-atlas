# Verification & Evaluation

## Required function

Estimate whether outputs, intermediate states, plans and actions are correct or useful strongly enough to guide search, learning and self-improvement.

## Mechanism families to map

Unit/integration tests; formal proof; theorem provers; static analysis; simulators; reward functions; learned reward/evaluator models; process supervision; outcome supervision; cross-model critique; self-consistency; calibration; adversarial testing; red teaming; property-based testing; human oversight.

## Central distinction

Generation quality and evaluation quality are separate resources. A weak generator with a strong objective evaluator can support search; a powerful generator with an exploitable evaluator can optimize toward failure.

## Early evidence anchors

Self-consistency demonstrates value from aggregating independent candidate paths. Formal theorem-proving systems provide machine-checkable feedback. AlphaEvolve demonstrates iterative proposal plus automated evaluation and selection in domains with objective metrics. Self-Harness explicitly gates self-modifications through regression testing.

## Clean-sheet questions

- Which claims/actions are objectively verifiable and which remain judgment calls?
- How can evaluator uncertainty be represented and propagated?
- When should multiple independent evaluators be required?
- How do we prevent Goodhart/evaluator gaming during long optimization loops?
- Can evaluation target internal process properties without forcing human-readable reasoning?
- What regression suite is sufficient before a self-change becomes persistent?
