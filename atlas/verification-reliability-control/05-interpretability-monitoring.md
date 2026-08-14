# Interpretability and Monitoring

## Required function

Extract diagnostic evidence from internal computation or runtime behavior that helps detect failure, localize causes and decide when additional checking or containment is warranted.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-IM-01 | Sparse autoencoders can recover many human-interpretable activation features at large scale, with measurable reconstruction/sparsity/explainability trade-offs. | O | E3 | V-S016 |
| V-IM-02 | Internal features can sometimes predict task-relevant failures before output, supporting diagnostic monitoring. | O | E2 | V-S017 |
| V-IM-03 | High predictive accuracy of an internal probe/feature does not guarantee that steering/intervening on that feature reliably corrects behavior. | O | E2 | V-S018 |
| V-IM-04 | Adversarial inputs can induce high-confidence failures in neural models, motivating monitoring under intentionally shifted/adversarial conditions rather than only ordinary validation. | O | E5 | V-S019 |

## Interpretability is evidence, not proof

A readable feature or circuit can support hypotheses such as:

- the model recognized a risky condition;
- a particular memory/tool result influenced the decision;
- an internal state changed before failure;
- a behavior appears to use an unexpected shortcut.

It does not establish complete causal understanding, absence of hidden features, or safety of the whole system.

## Monitoring levels

Useful monitoring can occur at multiple layers:

- inputs/untrusted-data provenance;
- internal activations/features;
- intermediate plans/state transitions;
- tool requests and permission use;
- memory writes/revisions;
- world-model prediction errors;
- evaluator disagreements;
- output/action effects;
- resource/recursion anomalies;
- changes to code, weights, policy or architecture.

No one layer observes every failure.

## Diagnostic vs control signal

A monitor can:

1. **diagnose** likely failure;
2. **trigger** stronger verification/escalation;
3. **block** an action if evidence is strong enough;
4. provide data for later learning.

Jumping directly from a correlational feature to irreversible intervention risks destroying correct behavior or creating a new failure mode.

## Adversarial robustness

Monitoring itself becomes part of the attack surface when a capable optimizer can learn what triggers alarms. Hidden/rotated monitors, independent evidence and effect-level checks can reduce reliance on one observable signal.

## Clean-sheet restatement

Interpretability should be treated as a **sensor into computation** with calibration, coverage and failure modes. It can improve observability of the system but should not be the sole authority for high-stakes safety decisions.

## Failure modes

Feature naming illusion; incomplete decomposition; probe learns correlation not causal mechanism; monitor distribution shift; steering correct feature causes collateral damage; monitor evasion; overwhelming false positives; safety argument built from a few interpretable examples; same model generates behavior and explains it post hoc.
