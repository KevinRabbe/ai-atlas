# IO, Memory Hierarchy and Locality

## Required function

Execute useful computation while minimizing expensive movement of parameters, activations and persistent state across the memory hierarchy.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-IO-01 | Roofline analysis separates compute-bound from bandwidth-bound regimes using operational intensity; peak FLOPs alone cannot predict attainable performance. | O | E5 | AS-S025 |
| AS-IO-02 | Data movement can consume far more energy than arithmetic, making locality an energy as well as latency constraint. | O | E5 | AS-S026 |
| AS-IO-03 | FlashAttention computes exact attention faster by changing tiling/IO behavior rather than changing the mathematical attention result. | O | E4 | AS-S027 |
| AS-IO-04 | FlashAttention-2/3 show that work partitioning, occupancy, asynchrony and precision support materially change realized performance of the same broad operator. | O | E4 | AS-S028, AS-S029 |
| AS-IO-05 | PagedAttention/vLLM demonstrates that virtual-memory-style management of KV state can multiply serving throughput without changing model weights. | O | E4 | AS-S030 |

## Two complexity models are required

For each candidate operator record both:

### Abstract cost

- operation count / asymptotic work;
- persistent state growth;
- sequential dependency depth;
- theoretical communication requirements.

### Realized machine cost

- bytes moved at each memory level;
- arithmetic/operational intensity;
- kernel size and accelerator utilization;
- synchronization/barriers;
- cache/state fragmentation;
- communication collectives;
- numerical precision;
- latency distribution and batching behavior.

Optimizing the first while ignoring the second can produce a theoretically efficient mechanism that is slower in practice.

## Locality as an architectural property

Locality should not be treated only as a compiler optimization. The model determines which data must meet which computation. An architecture can create or destroy locality by its state layout, addressing scheme, routing policy and parameter sharing.

This suggests a clean-sheet question: **can representations be organized so that information likely to interact is physically and computationally near each other?**

## Clean-sheet restatement

Minimize the total cost of making required information available to required computation, rather than minimizing arithmetic in isolation. Treat movement, placement and reuse as first-class design variables.

## Open questions

- Can learned routing optimize semantic value and data locality jointly without collapsing specialization?
- What fraction of future AI workload is bandwidth-bound versus compute-bound at different batch/latency regimes?
- Can persistent internal state be structured around explicit memory tiers?
- When is recomputation cheaper than retaining/moving state?

## Failure modes

Low arithmetic intensity; cache thrashing; KV/state fragmentation; huge intermediate tensors; small irregular kernels; redundant state transfers; algorithmic improvements that regress wall-clock time.