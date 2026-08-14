# Biological Intelligence — Provisional Synthesis

**Status: evidence-derived hypotheses and constraints, not architecture.**

## P-B01 — Learning and stabilization can be separate coupled processes

Biological circuits combine associative plasticity with homeostatic regulation. This suggests that the mechanism maximizing task improvement need not also be responsible for keeping the system in a stable operating regime.

**Confidence:** high for biological separation; artificial advantage remains to test.

## P-B02 — Credit can be factorized across space and time

Local events can leave temporary eligibility state that is later converted into durable change by delayed modulatory/evaluative signals. This demonstrates one workable solution to delayed credit without retaining a complete differentiable history.

**Confidence:** high biologically; medium as a scalable AI principle.

## P-B03 — A nominal compute unit can contain internal hierarchy

Dendritic compartments show that useful nonlinear computation can occur locally before network-level communication. Point-neuron abstractions therefore discard a potentially important locality/computation dimension.

**Confidence:** high for dendritic computation; medium for artificial design consequences.

## P-B04 — Plasticity benefits from multiple timescales

Rapid changes, eligibility/tagging, consolidation and slow homeostasis operate on different timescales. A single permanent update timescale is not a biological requirement and may not be an optimal artificial one.

**Confidence:** high biologically; artificial partition is open.

## P-B05 — Offline processing can transform experience without new environment interaction

Replay during offline states provides evidence that experience can be revisited and temporally reorganized after collection. Artificial systems should test whether idle compute is better spent on consolidation, counterfactual replay, distillation or evaluator-driven revision.

**Confidence:** medium; specific causal role varies by memory system.

## P-B06 — Energy pressure favors selective activity and local processing

Neural signaling is energetically costly. This reinforces the systems principle that communication and state movement are first-class costs and supports investigation of event-driven/selective computation.

**Confidence:** high for the physical pressure, not for any specific sparse code.

## P-B07 — Complex mature structure can be generated indirectly

Brain development is produced by compact inherited regulatory information interacting with local developmental dynamics and environment; the mature structure is not explicitly enumerated in the genome.

**Confidence:** high as a biological observation/inference.

**AI hypothesis:** indirect generative architecture encodings may search/adapt more efficiently than direct full-graph specification.

## P-B08 — Evolution often changes regulation rather than replacing primitives

Human/mammalian brain evolution includes substantial changes in enhancer activity, gene-regulatory timing, cell-state programs and morphology while reusing conserved biological machinery.

**Confidence:** high for regulatory contribution; no claim that it explains cognition alone.

## P-B09 — Heterogeneous context-dependent learning rules are viable

Plasticity rules vary by synapse, location, cell type and modulatory context. A clean-sheet learner need not assume one uniform update law everywhere.

**Confidence:** high biologically; artificial benefit unproven.

## Emerging cross-domain hypothesis

The biological evidence aligns with a system organized around **local cheap adaptation, sparse/global coordination signals, and slower consolidation/stability processes**. This could reduce communication and credit-assignment cost while allowing heterogeneous modules to specialize.

This remains a hypothesis. It must compete experimentally against end-to-end dense optimization, not be preferred because it resembles a brain.

## Most valuable experiments later

1. Compare full backpropagation against local eligibility + delayed evaluator signals under fixed compute/memory and identical tasks.
2. Compare immediate permanent updates with fast tentative state + replay + consolidation.
3. Compare point modules with internally compartmentalized modules at equal total parameters/FLOPs/bytes moved.
4. Compare directly optimized architectures with compact generative/developmental encodings under equal search budgets.
5. Add independent homeostatic controllers to continual learners and measure stability/plasticity/forgetting rather than short-task loss only.