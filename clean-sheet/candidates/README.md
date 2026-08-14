# Phase 9 Candidate Architecture Families

These candidates are intentionally **different coherent bundles** of the unresolved choices. They all attempt to satisfy the same Phase-8 functional specification and invariants.

No candidate is selected. Candidate value is measured by what it teaches us about architectural boundaries.

## Candidate A — Hierarchical Adaptive System

A small hierarchy of metacontrol and specialized computational/state services. High-level state allocates operations/resources/assurance; lower-level processes perform representation, prediction, search, memory and action through typed contracts.

Primary hypothesis: explicit hierarchical allocation provides enough system-level coordination to justify its communication/meta-control overhead.

## Candidate B — Distributed Event-Driven Ecology

Many locally adaptive processes operate mostly on local state and exchange sparse typed events; global coordination is limited to shared constraints, evidence identity and escalation rather than a central cognitive executive.

Primary hypothesis: locality/asynchrony and distributed specialization outperform centralized coordination when communication is selective and global state is expensive.

## Candidate C — Integrated Predictive Core + External Evidence

A tightly integrated learned core maintains compact evolving state and performs most perception/prediction/operation selection internally, while exact/persistent evidence and high-assurance control remain externally addressable.

Primary hypothesis: integration reduces routing/communication overhead enough to outweigh compressed-state interference and reduced internal modularity.

## Candidate D — Developmental Variant System

A compact set of generative/update rules creates, specializes, retires and recombines computational structures over time; alternative system variants are retained and tested rather than maintaining one fixed mature organization.

Primary hypothesis: indirect structural generation and population diversity improve long-horizon adaptation/search enough to justify much higher assurance and architecture-management cost.

## Comparison rule

Candidate comparison must use matched:

- task/evidence streams;
- total compute and persistent-state budgets;
- interaction budget;
- assurance budget;
- available training experience;
- physical platform where practical.

Otherwise the architecture variable is confounded with scale/resources.

## Selection rule

Phase 9 does not select a final architecture from benchmark averages. It identifies:

1. which functions each organization implements naturally;
2. where each pays coordination/state/learning cost;
3. which unresolved design dimensions dominate outcomes;
4. the smallest experiments capable of distinguishing those choices.
