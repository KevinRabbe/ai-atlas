# Harness, Context and Runtime Policy

## Required function

Control what information and capabilities the reasoning primitive receives, how actions are executed, how state persists, and how repeated inference steps are scheduled.

## Evidence

- **I-S007 — SWE-agent:** agent-computer interface changes materially affected coding-agent success while using a fixed underlying model family.
- **I-S013 — Meta-Harness:** automated search over harness code improved context-management, reasoning and coding tasks; one result improved online classification while using 4x fewer context tokens, and discovered harnesses transferred across held-out models in some tasks.
- **I-S014 — Self-Harness:** agents mined their own failure traces, proposed minimal harness changes and accepted them only after regression testing, improving held-out Terminal-Bench performance across three model families.
- **I-S015 — Recursive Harness Self-Improvement:** iterative harness refinement improved task performance while reducing inference cost in the evaluated synthetic research tasks, with gains attributed mainly to context/information flow rather than longer traces.

## Harness responsibilities

A harness may implement:

- context selection/compaction;
- memory retrieval/write policy;
- tool schemas and permissions;
- retry/error handling;
- subagent scheduling;
- model routing;
- reasoning budget;
- verification gates;
- event/trajectory logging;
- state recovery/branching;
- output formatting and user interaction.

These are computational decisions, not UI details.

## Why runtime can outperform weight changes

A harness can correct a model-specific failure by changing information access or action affordances without retraining the model. It is cheaper/reversible, but depends on the underlying model being capable of exploiting the new interface.

This mirrors Phase 2: runtime policy is another adaptation substrate with a different persistence/interference profile from weights.

## Self-modifying runtime

Harness self-improvement suggests an outer loop:

`collect traces -> identify recurrent failure -> propose minimal runtime change -> evaluate on regression suite -> accept/reject`.

The regression gate is essential. A change that fixes one trajectory can silently damage other task families.

## Clean-sheet restatement

The intelligent system should expose its **inference policy** as an explicit, testable, versioned component rather than burying all control behavior inside model weights/prompts.

## Failure modes

Harness overfitting; giant prompts that patch individual failures; hidden state divergence; interface churn; regression outside test set; permission escalation; context policies deleting crucial evidence; model-harness co-adaptation creating brittle coupling.