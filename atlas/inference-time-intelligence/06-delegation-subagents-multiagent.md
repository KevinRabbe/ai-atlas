# Delegation, Subagents and Multi-Agent Computation

## Required function

Split inference work across multiple independent or specialized computational workers when parallelism, diversity or capability specialization outweighs coordination cost.

## Evidence

- **I-S012 — Recursive Agent Harnesses:** fine-grained child harnesses improved a fixed parent coding-agent baseline on a long-context benchmark, providing evidence that tool-capable delegation can add capability beyond a bare model call.
- **I-S016 — systematic multi-agent debate study:** debate showed conditional rather than universal advantages over strong self-agent test-time scaling; effects depended on difficulty/model capability and could worsen some safety behavior.
- **I-S018 — Mixture-of-Agents:** layered aggregation of outputs from multiple language models improved several response-quality benchmarks, showing heterogeneous model outputs can sometimes provide complementary signal.

## Delegation value sources

Delegation can help through distinct mechanisms:

1. **parallelism** — independent subproblems reduce critical path;
2. **context isolation** — each worker sees only relevant state;
3. **specialization** — different models/tools/policies match different tasks;
4. **diversity** — partially independent candidate generation reduces correlated errors;
5. **verification separation** — one worker produces while another checks;
6. **fault containment** — failures can be localized to a branch.

## Coordination costs

- task decomposition;
- duplicated context/setup;
- message/token transfer;
- inconsistent assumptions;
- aggregation;
- synchronization/tail latency;
- correlated model errors masquerading as consensus;
- recursive worker explosion.

## Clean-sheet restatement

“Agent count” is not a capacity metric. The useful quantity is roughly:

`net delegation value = parallel/specialist/diversity gain - decomposition/communication/integration cost`.

A single model called five times and five genuinely heterogeneous specialists are different computational regimes even if both are called “multi-agent.”

## Scheduling question

A root controller should estimate whether a subproblem is:

- separable;
- independently verifiable;
- sufficiently large to justify worker startup;
- likely to benefit from different capability/tooling;
- latency-sensitive;
- safe to execute concurrently.

## Failure modes

Consensus of correlated errors; duplicated work; stale shared state; task fragmentation; communication flooding; worker competition; aggregation bottleneck; recursive fan-out; lowest-quality worker contaminating synthesis.