# Systems, Efficiency & Hardware

## Required function

Realize useful intelligence under finite memory capacity, bandwidth, latency, energy, communication and hardware constraints.

## Status

**Coupled architecture/systems first evidence pass completed; not saturated.**

See [`architecture-systems/`](architecture-systems/INDEX.md) and its provisional synthesis. Systems concerns are intentionally researched together with model architecture because the model defines data movement, state growth, routing and critical paths.

## First-pass findings

1. **FLOPs are not machine cost.** Bandwidth, locality, synchronization and kernel utilization can dominate.
2. **Data movement is an architectural cost.** Exact mathematical work can be accelerated dramatically by changing IO scheduling alone.
3. **Persistent inference state matters as much as weights.** Cache/state representation controls long-context capacity, batching and bandwidth.
4. **Sparse compute shifts bottlenecks.** Routing and communication can erase arithmetic savings without matching kernels/runtime.
5. **Distributed scale has multiple purposes.** Capacity, throughput, latency, search and specialist parallelism have different optimal communication patterns.
6. **Precision is a system/architecture variable.** Low-bit representations can move the efficiency frontier, but sensitivity and accumulating state error must be measured.
7. **Hardware/software co-design works.** Domain-specific accelerators and hardware-aware kernels can produce large gains, but transient hardware details must not become clean-sheet axioms.

## Required dual accounting

Every candidate mechanism should report:

### Abstract complexity

operations; state growth; dependency depth; theoretical communication.

### Realized complexity

bytes moved by memory tier; communication; synchronization; utilization; kernel granularity; precision; batching behavior; latency distribution; energy.

## Clean-sheet questions

- Which computation is truly expensive in each workload regime: arithmetic, movement, synchronization or serialization?
- What state belongs physically closest to what computation?
- Can semantic routing and physical placement be decoupled?
- When does recomputation beat caching?
- What primitives would we ask hardware to implement if the AI architecture were not predetermined by current GPUs?

## Anti-assumptions

Do not assume GPUs, dense matrix multiplication, current tensor-core datatypes, HBM, Ethernet/InfiniBand-style cluster topology or conventional von-Neumann separation are permanent requirements. Also do not ignore them when measuring what is practical today.