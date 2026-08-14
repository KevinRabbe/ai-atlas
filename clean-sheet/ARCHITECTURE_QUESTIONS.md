# Architecture Questions

These are deliberately implementation-neutral.

## Cognitive computation

- What minimum operations are needed to transform observations and stored knowledge into useful actions?
- Which computations require learned approximation versus exact algorithms?
- Should a single substrate perform perception, prediction, planning and communication, or should they be specialized?

## Representation

- What internal representation maximizes useful information per unit compute and bandwidth?
- When is discreteness useful? When is continuity useful?
- Does human-readable language belong only at system boundaries?
- How can separate components exchange state without forcing lossy text serialization?

## Memory and learning

- What information should alter weights?
- What should remain rapidly editable external state?
- What constitutes an experience, fact, skill, heuristic, policy, model of another entity, or world-state belief?
- How should consolidation and forgetting work?

## Compute allocation

- How does the system estimate task difficulty and uncertainty?
- When should it stop thinking?
- When should it branch, search, simulate, retrieve, execute, delegate or recurse?
- How should compute budgets be allocated dynamically across heterogeneous resources?

## Prediction and world modeling

- What state must be predicted to evaluate actions before execution?
- How should uncertainty and model error propagate through imagined futures?
- When is a learned simulator preferable to direct interaction?

## Verification

- Which outputs can be objectively checked?
- How are uncheckable judgments handled?
- How can the system avoid optimizing against a flawed evaluator?

## Self-improvement

- Which layer should change first: active state, memory, skill, harness/routing policy, weights, or architecture?
- What evidence threshold justifies making an improvement persistent?
- How are regressions detected outside the optimization target?

## System organization

- What is the correct unit of modularity?
- What state should be shared versus isolated?
- How are components created, retired, specialized and merged?
- What does recursion mean when the recursive unit can contain an entire computational system?
