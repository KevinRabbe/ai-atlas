# Clean-Sheet Architecture

This directory begins **after** research synthesis reaches sufficient coverage.

## The forgetting protocol

Before designing a component:

1. State the required function without implementation names.
2. State inputs, outputs, invariants and resource constraints.
3. List the evidence-backed properties a solution needs.
4. Deliberately remove assumptions inherited from current AI stacks.
5. Generate at least three mechanistically different candidate solutions where uncertainty permits.
6. Compare them by capability, information loss, compute, memory, bandwidth, latency, learning dynamics, robustness and testability.
7. Record why a candidate is selected in `DESIGN_LEDGER.md`.

Examples of forbidden shortcuts during the first pass:

- 'Use a Transformer because LLMs use Transformers.'
- 'Use text for reasoning because chain-of-thought works.'
- 'Use a vector database because agents need memory.'
- 'Use many agents because multi-agent systems are powerful.'
- 'Use RLM recursion because recursion is the next level.'

Each of those may eventually be selected—but only after the underlying requirement independently leads there.

## Principle

The goal is not novelty. If the evidence leads back to an existing mechanism, keep it. The goal is to ensure that it survives reconstruction for a reason rather than inheritance by default.
