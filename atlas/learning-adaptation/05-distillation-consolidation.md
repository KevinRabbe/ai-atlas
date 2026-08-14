# Distillation and Consolidation

## Required function

Convert expensive, redundant, temporary or externally generated competence into a cheaper durable representation when repeated future use justifies the conversion cost.

## Evidence

- **L-S015 — knowledge distillation:** behavior of an ensemble/large teacher can be transferred into a smaller deployable model, demonstrating that inference-time ensemble cost can be amortized into learned parameters.
- **L-S006 — DeepSeek-R1:** reasoning behavior from stronger models/RL-trained systems was distilled into smaller dense models with substantial retained capability, showing one modern form of capability compression across models.
- **Biological B-S013/B-S014:** synaptic tagging and replay provide a separate evidence family for staged stabilization and offline reuse of experience; these do not establish the artificial implementation but motivate timescale comparisons.

## General abstraction

Distillation is not only “make a smaller model.” It is a form of **compute amortization**:

`expensive process -> collect evaluated input/output/trajectory information -> learn cheaper reusable approximation`

The expensive source could be:

- ensemble;
- search/planning;
- recursive agents;
- external tools;
- simulator;
- verifier-filtered generation;
- larger specialist model;
- repeated retrieval procedure.

## Consolidation gate

Durable compilation should be favored when:

`expected repeated future savings + generalization benefit > consolidation/training cost + regression/interference risk`

The system should retain provenance linking consolidated competence back to evidence/evaluators where possible.

## Key distinction

Distillation can lose information. A student that matches teacher outputs on one distribution may fail to retain uncertainty, rare capabilities or causal procedure. Therefore consolidation should be regression-tested across the capability envelope, not accepted from average imitation loss.

## Clean-sheet question

Can a system measure recurring expensive computations and autonomously decide which ones deserve to be compiled into a faster skill, routing rule or weight update?

## Failure modes

Teacher error propagation; capability collapse outside distillation distribution; loss of uncertainty; hidden benchmark overfit; premature compilation of temporary behavior; catastrophic interference during consolidation.