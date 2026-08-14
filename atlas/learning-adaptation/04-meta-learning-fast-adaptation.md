# Meta-Learning and Fast Adaptation

## Required function

Use experience across tasks/environments to improve the *learning procedure itself*: initialization, update dynamics, inference algorithm, data acquisition or adaptation policy.

## Evidence

- **L-S007 — MAML:** an initialization can be optimized so that a few gradient updates on a new task produce strong adaptation.
- **L-S019 — general-purpose in-context meta-learning:** black-box sequence models can be meta-trained to implement learning algorithms in their forward pass across task distributions; accessible runtime state can become the limiting resource.
- **L-S020 — transformers as learned gradient-like meta-optimizers:** in controlled regression settings, trained attention mechanisms can implement transformations closely related to gradient descent and can learn refinements beyond plain GD.
- **L-S008/L-S009 — test-time learning:** adaptation can continue during deployment, either by updating model parameters or by treating mutable hidden state as a learned model.

## Important distinction

Meta-learning can optimize *how to change* without specifying that change must happen in durable weights.

Possible learned meta-objects include:

- initialization;
- optimizer/update rule;
- routing policy;
- retrieval policy;
- curriculum/data selector;
- stopping rule;
- consolidation threshold;
- architecture generator;
- uncertainty-to-action policy.

## Fast adaptation vs durable learning

A system can solve a new task temporarily using runtime state and only later decide whether to consolidate. This is attractive when tasks are numerous or transient because it prevents every episode from permanently mutating shared parameters.

## Clean-sheet hypothesis

A general system should learn a **change policy** that answers:

`what changed in the environment? -> what internal state should change? -> how much? -> for how long? -> what evidence would justify consolidation?`

This is broader than conventional meta-learning and remains a hypothesis.

## Failure modes

Meta-overfitting to training task distributions; learned update rules that exploit benchmark regularities; runtime state bottlenecks; adaptation instability; higher-order optimization cost; hidden changes that are hard to audit.