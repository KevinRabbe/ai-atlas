# Foundations — Evidence Map

This directory decomposes the Foundations domain into mechanism-level research notes. It is deliberately not organized around current AI products or architectures.

## Research questions

| Note | Function being studied |
|---|---|
| `01-induction-generalization.md` | Why can experience on observed cases support performance on unobserved cases? |
| `02-information-compression.md` | What can information theory say about useful representations, storage and communication? |
| `03-computation-complexity.md` | What can be computed, and what changes when time, memory and interaction are finite? |
| `04-optimization-search.md` | How are useful solutions selected from large possibility spaces? |
| `05-uncertainty-decision.md` | How should uncertain beliefs be represented, evaluated and used in decisions? |
| `06-causality-control.md` | What is required to predict interventions and act over time rather than merely predict observations? |
| `07-credit-assignment.md` | How can outcomes assign learning signal to earlier internal choices or actions? |
| `08-representation.md` | What makes an internal representation useful for prediction, transfer, recombination and control? |
| `09-resource-scaling.md` | How do data, compute, memory, bandwidth and interaction trade against one another? |
| `PROVISIONAL_SYNTHESIS.md` | Evidence-backed principles that survive implementation-neutral restatement. |

## Current status

**First evidence pass in progress. Not saturated.**

A note is not considered complete because it contains canonical papers. Saturation requires strong positive results, important counterexamples, alternative mechanisms, cost/scaling behavior, and unresolved discriminating experiments.

## Boundary rule

Foundational mathematics can tell us what is possible, impossible, or costly. It does **not** automatically tell us the best practical architecture. In particular:

- universal approximation does not imply practical learnability;
- universal induction does not imply computability;
- an information-theoretic optimum does not imply an efficient algorithm;
- asymptotic optimality does not imply good finite-budget behavior;
- a theorem under a distributional assumption must not be silently generalized beyond that assumption.
