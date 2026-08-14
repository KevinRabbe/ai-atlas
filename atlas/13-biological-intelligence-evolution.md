# Biological Intelligence, Development & Evolution

## Required function

Extract computational mechanisms from evolved nervous systems and developmental programs without treating biological fidelity as an objective.

Biology is included because evolution has already searched a vast design space under severe energy, communication, developmental and survival constraints. It is **evidence about possible mechanisms**, not a privileged blueprint for artificial intelligence.

## Scope

Synaptic plasticity; dendritic and compartmental computation; neuromodulation; eligibility traces; homeostasis; replay and consolidation; multi-timescale learning; sparse/event-driven signaling; developmental self-organization; gene-regulatory programs; genomic encoding; evolutionary changes in regulation and developmental timing.

Detailed notes live under [`biological-intelligence/`](biological-intelligence/INDEX.md).

## Anti-assumptions

Do not assume spikes, biological neurons, neurotransmitters, cortical columns, sleep, DNA, evolution, or any anatomical structure should be copied literally. Ask which problem each mechanism solves and whether a simpler artificial mechanism can provide the same function.

Do not infer optimality from existence. Evolution optimizes reproductive fitness under historical constraints, not benchmark intelligence, software maintainability or datacenter efficiency.

## First-pass questions

- Can local learning rules receive useful delayed global credit without end-to-end differentiability?
- Why does biological learning use multiple coupled plasticity and stabilization timescales?
- What computational value comes from dendritic compartmentalization inside a nominal neuron?
- Can replay/consolidation separate rapid acquisition from durable integration?
- Which aspects of sparse/event-driven signaling arise from fundamental communication/energy constraints?
- Does development suggest that complex architectures should be *grown/generated* from compact rules rather than explicitly specified?
- Which human evolutionary changes altered regulatory timing, cell-type programs or morphology rather than inventing entirely new computational primitives?

## Status

First evidence pass completed on 2026-08-14. Provisional implementation-neutral deductions are in [`biological-intelligence/PROVISIONAL_SYNTHESIS.md`](biological-intelligence/PROVISIONAL_SYNTHESIS.md).