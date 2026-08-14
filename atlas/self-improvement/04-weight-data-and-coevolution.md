# Weight, Data and Harness Co-Evolution

## Required function

Improve durable learned competence while accounting for the fact that the runtime/harness determines which experiences, failures and successful trajectories become future training data.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-WD-01 | SIA reports additional gains from updating both harness and weights compared with scaffold iteration alone across three heterogeneous domains. | O | E2 | SI-S004 |
| SI-WD-02 | Recursive Harness Self-Improvement explicitly frames harnesses as data-generating components whose traces can shape later foundation-model training. | I/O | E2 | SI-S003 |
| SI-WD-03 | Phase-2 evidence shows data generation/selection/ordering and parameter-update substrate jointly determine learned behavior. | I | E5 | prior Learning evidence |
| SI-WD-04 | Distillation demonstrates that behavior produced by expensive systems can be transferred into cheaper durable parameters, with information-loss trade-offs. | O | E4 | prior Learning evidence |

## Co-evolution loop

A realistic loop is:

`model -> harness/runtime -> actions/traces -> evaluator -> selected experience -> model update -> changed behavior -> new traces`.

This is a feedback system. Improving one part changes the data distribution seen by every later part.

## Why alternating one layer can fail

If the harness is poor, weight training may learn around avoidable interface/context defects. If weights are weak, harness search may accumulate increasingly complex workarounds. Joint optimization can therefore be useful, but it increases attribution difficulty and makes regression causes harder to identify.

## Trace quality as an objective

A harness should not be evaluated only on current task success. It can also be scored by whether its traces are:

- attributable/provenanced;
- diverse enough for learning;
- rich in informative failures;
- concise rather than duplicated;
- externally verifiable;
- safe to retain/train on;
- representative of desired future environments.

This creates a lifetime trade-off: a harness that is slightly slower now may generate much better future training data.

## Promotion to weights

Repeated patterns are candidates for parametric consolidation when:

- they are broadly reused;
- evidence is stable;
- runtime retrieval/tool overhead is repeated;
- the capability benefits from deep integration;
- interference/regression risk is acceptable;
- provenance/rollback requirements are satisfied.

Weight updates should not automatically erase the source skill/memory; the external version can remain as validation/provenance until confidence is high.

## Evaluator co-evolution risk

Updating the evaluator together with the agent can silently redefine success. Changes to reward/judge components require especially strong independent holdouts or trusted external criteria.

## Clean-sheet restatement

Model and runtime are coupled adaptive subsystems. Self-improvement should optimize **future competence and trace quality over a lifetime**, not treat today's harness and tomorrow's training set as independent.

## Failure modes

Feedback-loop collapse; training on self-generated errors; harness-induced dataset bias; evaluator drift; simultaneous changes hiding root cause; weights learn benchmark-specific scaffolding artifacts; distilled behavior loses uncertainty; self-generated data becomes increasingly homogeneous; reward model and agent collude through shared blind spots.
