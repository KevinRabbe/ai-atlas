# Homeostasis and Stability

## Required function

Allow useful plastic change without pushing a learning system into saturation, inactivity, runaway feedback or catastrophic operating-point drift.

## Evidence

- **B-S003 — Turrigiano et al. (1998):** chronic changes in activity induced multiplicative-like scaling of synaptic response amplitudes, revealing a plasticity process that regulates overall activity rather than storing one association.
- Later experimental work has established multiple local and global homeostatic mechanisms; this pass keeps the original synaptic-scaling result as the primary anchor and treats broader mechanisms as an expansion target.

## Computational abstraction

Task learning and stability control are separable objectives:

`fast/task-directed plasticity + slower operating-point regulation`

The stabilizer need not undo relative learned structure. A global or local gain-control process can alter the operating envelope while preserving distinctions learned by another process.

## Atlas implication

Optimization systems should not assume the same objective/process must both **learn useful structure** and **keep the learner numerically/dynamically healthy**.

Potential artificial analogues include activation/weight homeostasis, adaptive normalization targets, resource-budget regulators, learning-rate controllers, routing-load regulation and regression gates.

## Failure modes

Overaggressive homeostasis can erase useful specialization; weak homeostasis permits instability; fixed setpoints can be wrong under regime change. Stability control itself may therefore need adaptation.