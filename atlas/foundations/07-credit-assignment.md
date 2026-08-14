# Credit Assignment

## Required function

Determine which earlier internal computations, parameters, choices or actions should change after observing an outcome.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-CA-01 | Reverse-mode error propagation can efficiently assign differentiable output error to hidden parameters in layered networks and learn useful internal features. | O | E5 | F-S033 |
| F-CA-02 | Temporal-difference methods can learn predictions incrementally by bootstrapping from later predictions, providing temporal credit without waiting for complete episodes. | O | E5 | F-S034 |
| F-CA-03 | Score-function/policy-gradient estimators can assign credit to stochastic actions from sampled rewards without differentiating through the environment. | O | E5 | F-S035 |
| F-CA-04 | These estimators have different information and variance properties; differentiability is powerful but is not a necessary condition for learning from consequences. | I | E5 | F-S033, F-S034, F-S035 |

## Credit assignment is broader than backpropagation

Backpropagation is a highly efficient answer when the computation is differentiable and the relevant forward trace is available. It should not be elevated into the abstract requirement. Real intelligent systems may contain nondifferentiable tools, discrete program choices, external environments, delayed outcomes, retrieval decisions and other components through which gradients are unavailable or undesirable.

The foundational requirement is more general: **construct an estimator or signal that links outcome differences to earlier changeable causes**.

## Several axes matter

### Pathwise versus sampled credit

If a differentiable causal path is known, pathwise derivatives can provide dense, low-variance local information. When only sampled outcomes are available, score-function estimators can remain valid but often require more samples or variance reduction.

### Immediate versus delayed credit

Bootstrapping methods trade bias/variance and can propagate value information before final outcomes arrive. Long delays increase ambiguity about which earlier decisions mattered.

### Local versus system-level credit

A component can improve its local loss while harming the complete system. Later self-improvement work must therefore distinguish local credit from end-to-end credit and include regression/evaluator gates.

## Clean-sheet restatement

Any adaptive system needs a way to estimate **which modifiable decisions causally contributed to useful or harmful outcomes, at what timescale, and with what uncertainty**. The estimator should exploit stronger feedback channels when available without assuming the entire world is differentiable.

## Open questions

- How should credit cross boundaries between neural computation, external tools, symbolic programs and human/environment feedback?
- Can hierarchical credit reduce variance by assigning responsibility first to modules/tasks and then internally?
- When should a failure update weights versus memory, skills, routing or a world model?
- How can delayed real-world outcomes update earlier decisions without corrupting unrelated capabilities?
- Can counterfactual evaluation provide lower-variance credit than raw trial-and-error?

## Discriminating experiments

Use the same modular agent with differentiable, sampled, verifier-based and counterfactual credit channels. Under fixed interaction cost, compare speed of improvement, variance, regressions and transfer of learned changes.

## Failure modes

Reward attribution to the wrong component; high-variance updates; bootstrapping from biased estimates; local-objective improvement with global capability loss; delayed feedback contaminating unrelated behavior; assuming gradient availability across external actions.
