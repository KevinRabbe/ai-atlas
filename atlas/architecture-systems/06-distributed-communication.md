# Distributed Computation and Communication

## Required function

Scale capacity and computation beyond one device while preventing communication, synchronization, imbalance and failure handling from dominating useful work.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-DC-01 | Tensor/model parallelism enables models exceeding one-device capacity but introduces communication into layer execution. | O | E4 | AS-S033 |
| AS-DC-02 | Combining data, tensor and pipeline parallelism can scale training to thousands of accelerators, but configuration strongly changes bubbles, memory and communication efficiency. | O | E4 | AS-S034 |
| AS-DC-03 | ZeRO shows that optimizer/gradient/parameter replication is a systems choice rather than a fixed training requirement; partitioning redundant state can dramatically change feasible model scale. | O | E4 | AS-S032 |
| AS-DC-04 | Sparse expert systems introduce dynamic all-to-all communication and load imbalance; adaptive execution and block-sparse kernels can recover substantial efficiency. | O | E4 | AS-S022, AS-S023, AS-S024 |
| AS-DC-05 | Reconfigurable interconnect topology and hardware support for particular sparse operations can materially improve large-system efficiency. | O | E3 | AS-S039 |

## Important distinction

Parallelism has several independent purposes:

- **capacity parallelism** — fit parameters/state that exceed one device;
- **throughput parallelism** — process more independent work;
- **latency parallelism** — shorten the critical path of one task;
- **search/ensemble parallelism** — evaluate alternative computations;
- **specialist parallelism** — host heterogeneous capabilities.

Treating all of these as generic “more GPUs” hides different optimal communication patterns.

## Communication-aware architecture

A modular architecture may appear attractive semantically while becoming inefficient if every module boundary requires high-volume synchronization. Conversely, excessive parameter sharing can reduce communication while forcing irrelevant computation.

The design variable is therefore not merely modularity but **information crossing module/device boundaries per unit of useful progress**.

## Clean-sheet restatement

Partition computation so that most high-bandwidth interactions remain local; cross boundaries for information whose expected value justifies communication. Physical scheduling should be allowed to replicate, migrate or colocate modules independently of their semantic identity where possible.

## Metrics

- useful compute / communication byte;
- collective time / step time;
- synchronization critical path;
- straggler/tail utilization;
- replicated-state overhead;
- communication overlap;
- failure/recovery cost;
- quality per distributed joule and wall-clock second.

## Failure modes

All-reduce/all-to-all domination; pipeline bubbles; hot experts; topology mismatch; synchronization storms; tiny messages; replicated state explosion; network failures contaminating long-running learning.