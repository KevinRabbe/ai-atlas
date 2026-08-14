# Energy, Sparse Activity and Locality

## Required function

Perform useful computation under strong energy and communication constraints.

## Evidence

- **B-S015 — Attwell & Laughlin (2001):** a quantitative energy budget for mammalian grey matter found action potentials and postsynaptic signaling to be major energetic costs and argued that signaling energy constrains coding and activity levels.
- Dendritic evidence in the preceding notes shows substantial processing can occur locally before long-range output, reducing the need to interpret every biological operation as globally communicated.

## Clean-sheet restatement

Communication is expensive enough that **where computation happens and how often information is transmitted** can be as important as arithmetic count. This independently agrees with the Atlas systems evidence on HBM/network movement.

Biological spikes are one event-driven implementation. The general principle is not "use spiking networks"; it is:

> avoid moving/updating information when its expected utility is lower than the physical cost.

## Open questions

- When do event-driven/sparse representations beat dense vectorized computation on modern or future hardware?
- Can local state suppress unnecessary global communication without losing information required later?
- How should activity sparsity be optimized jointly with representation quality and hardware utilization?