# Systems, Efficiency & Hardware

## Required function

Realize useful intelligence under finite memory capacity, bandwidth, latency, energy, communication and hardware constraints.

## Mechanism families to map

Dense vs conditional computation; memory hierarchy; attention/state-space/recurrent complexity; KV-state management; batching; caching; speculative decoding; quantization; kernels; compiler optimization; parallel/distributed training; topology-aware routing; heterogeneous accelerators; storage/compute co-design; neuromorphic and non-von-Neumann approaches.

## Early evidence anchors

Sparse MoE demonstrates conditional parameter activation. Switch Transformer exposes both scaling benefits and communication/training challenges. FlashAttention shows that IO complexity and memory movement can dominate nominal arithmetic complexity. PagedAttention/vLLM shows that memory-management policy alone can materially change serving throughput. Mamba demonstrates that sequence-processing alternatives can achieve linear sequence scaling while retaining competitive modeling capability in tested regimes.

## Clean-sheet questions

- Which computation is actually expensive: arithmetic, memory movement, synchronization or serialization?
- Should architecture be designed around hardware, hardware around architecture, or co-evolved?
- What state should live closest to compute?
- When does modular/distributed intelligence lose more to communication than it gains from specialization?
- What metric should replace raw parameter count for system capacity?
