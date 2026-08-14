# Inference Execution, Caching and Speculation

## Required function

Turn a trained computational substrate into low-latency/high-throughput behavior without wasting expensive model evaluations or memory bandwidth.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-IE-01 | Autoregressive token generation imposes a serial dependency across output positions for standard next-token decoding. | O | E5 | AS-S002, AS-S031 |
| AS-IE-02 | Speculative decoding can use a cheaper approximate model to propose several steps that the target verifies in parallel while preserving the target distribution. | O | E4 | AS-S031 |
| AS-IE-03 | KV-cache layout/management can change achievable batching and throughput by multiples. | O | E4 | AS-S030 |
| AS-IE-04 | MQA/GQA/MLA reduce repeated inference-state bandwidth by sharing/compressing key/value representations. | O | E4 | AS-S005, AS-S006, AS-S007 |
| AS-IE-05 | Recurrent/linear mechanisms can have constant-size incremental state, changing decode memory behavior relative to KV-cached full attention. | O | E4 | AS-S010, AS-S011, AS-S013, AS-S016, AS-S017 |

## Critical-path view

Inference efficiency should distinguish:

- **prefill** — ingest available context, often parallel and compute-heavy;
- **decode** — produce/decide successive actions, often latency/bandwidth-bound;
- **verification** — check candidate outputs/actions;
- **state update** — write persistent or recurrent state;
- **external waits** — tools, networks, environment feedback.

An architecture optimized for training/prefill can be poor at interactive decoding.

## Generalization beyond tokens

Speculation expresses a broader systems principle:

> execute cheap approximate work ahead of an expensive serial bottleneck, then verify efficiently.

The same pattern could apply to planning, tool calls, simulation branches, memory retrieval or specialist routing—not only text tokens.

## Clean-sheet restatement

Design the inference path around the true action/decision critical path. Cache or speculate reusable work when its expected saved cost exceeds storage, invalidation and verification overhead.

## Metrics

Time-to-first-useful-result; steady-state latency; throughput; persistent bytes per live task; energy/result; accepted speculative work / proposed work; cache hit and invalidation rate; tail latency.

## Failure modes

Cache growth; stale caches; speculation with low acceptance; batch scheduling that destroys interactive latency; optimizing tokens/s while degrading useful task progress/s.