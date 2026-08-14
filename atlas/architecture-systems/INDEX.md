# Architecture + Systems — Coupled Map

**Status:** first evidence pass in progress.

This area deliberately studies model architecture and execution systems together. A mathematically attractive operator that maps poorly to memory hierarchy, parallel hardware, communication topology or decoding workload may be a poor practical substrate; conversely, a hardware-friendly operator that destroys useful information is not intelligent computation.

## Research decomposition

1. [`01-information-access-state.md`](01-information-access-state.md) — direct addressability versus compressed recurrent state.
2. [`02-routing-sparsity.md`](02-routing-sparsity.md) — conditional computation, specialization and routing.
3. [`03-adaptive-compute-memory.md`](03-adaptive-compute-memory.md) — variable depth, writable memory and test-time adaptation.
4. [`04-hybrid-architectures.md`](04-hybrid-architectures.md) — why heterogeneous operators increasingly coexist.
5. `05-io-memory-hierarchy.md` — arithmetic intensity, locality and state movement.
6. `06-distributed-communication.md` — parallelism, synchronization and topology.
7. `07-precision-quantization.md` — numerical representation as an architecture/system variable.
8. `08-inference-execution.md` — serial decoding, caching, batching and speculation.
9. `09-hardware-codesign.md` — specialization and architecture/hardware co-design.
10. `PROVISIONAL_SYNTHESIS.md` — implementation-neutral deductions only.

## Shared evaluation axes

Every mechanism should be measured along at least:

- representational capability and task quality;
- training parallelism and critical path;
- inference/decode critical path;
- persistent state size and growth with sequence length;
- reads/writes across memory hierarchy;
- arithmetic intensity and kernel utilization;
- communication volume, synchronization and load balance;
- numerical precision requirements;
- ability to vary active computation with the input;
- ease of composition with external memory/tools;
- robustness under sequence length, scale and distribution shift.

## Anti-assumption

Do not optimize for FLOPs, parameter count, asymptotic complexity, GPU utilization or benchmark quality in isolation. Those are different projections of a coupled design surface.