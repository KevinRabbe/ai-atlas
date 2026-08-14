# Hardware and Algorithm Co-Design

## Required function

Choose or create physical compute structures whose dataflow, memory hierarchy, communication and numeric primitives match the dominant operations of the intelligent system.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-HW-01 | The first TPU demonstrated large performance/energy gains from a domain-specific matrix-multiply engine and large explicitly managed on-chip memory on production neural workloads. | O | E4 | AS-S038 |
| AS-HW-02 | TPU v4 combines accelerator design with large-system interconnect and specialized sparse/embedding hardware, showing hardware specialization can occur at both chip and cluster level. | O | E3 | AS-S039 |
| AS-HW-03 | Horowitz's energy analysis establishes memory-system energy as a central constraint and motivates local/specialized computation. | O | E5 | AS-S026 |
| AS-HW-04 | FlashAttention generations demonstrate that algorithms can be redesigned around specific memory hierarchy, warp scheduling, asynchronous transfer and low-precision primitives without changing their high-level mathematical objective. | O | E4 | AS-S027, AS-S028, AS-S029 |
| AS-HW-05 | Sparse MoE systems show that irregular dynamic computation needs matching kernels/runtime support to realize theoretical savings. | O | E4 | AS-S023, AS-S024 |

## Co-design levels

1. **representation ↔ numerical format**
2. **operator ↔ accelerator primitive**
3. **state layout ↔ memory hierarchy**
4. **routing ↔ device placement/interconnect**
5. **model topology ↔ cluster topology**
6. **compiler/runtime ↔ dynamic computation graph**

A clean-sheet AI should not freeze the upper layer while pretending the lower ones are implementation details.

## But avoid hardware lock-in

Co-design can overfit a model to one accelerator generation. Therefore distinguish:

- fundamental physical constraints: locality, finite bandwidth, energy, propagation/synchronization;
- current technology constraints: tensor-core shapes, HBM capacity, GPU warp structure, network topology.

The final design should exploit current hardware where useful without confusing transient hardware details with intelligence requirements.

## Clean-sheet restatement

Select computation and physical realization jointly against a multi-objective frontier of capability, latency, throughput, memory, energy, manufacturability and programmability. Preserve abstraction boundaries only where their cost is justified by portability/modularity.

## Open questions

- Would an AI designed around persistent local state require a different accelerator than one designed around global attention?
- Can many heterogeneous small compute/memory islands beat a few giant matrix processors for adaptive modular intelligence?
- What should be near-memory or in-memory if parameter/state movement dominates energy?
- Can hardware expose efficient primitives for dynamic routing and variable-depth execution without losing utilization?

## Failure modes

Benchmark-specific ASIC design; poor programmability; stranded compute due to bandwidth; excessive data conversion; inflexible routing; architecture tied to obsolete hardware assumptions.