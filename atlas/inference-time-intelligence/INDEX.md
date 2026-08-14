# Inference-Time Intelligence — Evidence Map

**Status:** first evidence pass in progress.

This area studies how a trained/adapted system allocates computation while solving a particular problem. The unit is not “reasoning tokens” or “agents”; it is an **inference operation with expected value and cost**.

## Research decomposition

1. [`01-deliberation-representation.md`](01-deliberation-representation.md) — intermediate computation and representational form.
2. [`02-search-sampling-verification.md`](02-search-sampling-verification.md) — branching, sampling, selection and verifiers.
3. [`03-compute-allocation-stopping.md`](03-compute-allocation-stopping.md) — how much compute to spend and when to stop.
4. [`04-tools-environment-execution.md`](04-tools-environment-execution.md) — external computation, APIs, code execution and interfaces.
5. [`05-external-context-recursion.md`](05-external-context-recursion.md) — context as environment and recursive decomposition.
6. [`06-delegation-subagents-multiagent.md`](06-delegation-subagents-multiagent.md) — parallel workers, specialists and communication.
7. [`07-harness-context-runtime.md`](07-harness-context-runtime.md) — harness/runtime policy as capability multiplier.
8. [`08-evaluator-evolutionary-loops.md`](08-evaluator-evolutionary-loops.md) — iterative generation under objective evaluation.
9. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions only.

## Shared evaluation axes

- task quality under fixed total inference cost;
- marginal gain from additional compute;
- sequential critical path vs parallel work;
- context/state growth;
- evaluator reliability/exploitability;
- tool/action latency and failure cost;
- communication/delegation overhead;
- recoverability and rollback;
- error propagation across branches/agents;
- token/FLOP/byte/wall-clock/energy cost;
- ability to terminate unproductive computation.

## Core separation

`problem decomposition != computation scheduling != model call != tool call != verification != memory update`

Current agent systems often fuse these into one loop. Clean-sheet design should evaluate each role separately.