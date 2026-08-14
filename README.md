# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The purpose of this repository is **not** to document today's implementations and then assemble them into another conventional AI stack. The purpose is to extract the underlying mechanisms, empirical results, constraints, failure modes, and open questions across AI and adjacent fields; separate evidence from implementation habit; and then use that knowledge to derive clean-sheet architectures.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

After a research area has been mapped, synthesis restates the problem in implementation-neutral terms and asks what computational function is actually required. Named model blocks, reasoning methods, memory products, agent frameworks, biological mechanisms, learning algorithms, verifier products, self-improvement frameworks and current hardware are evidence/candidates—not axioms.

## Repository layers

- `atlas/` — mechanism-centric evidence and domain syntheses.
- `sources/` — primary/original source registries.
- `research/` — roadmap, claims, contradictions and failure modes.
- `synthesis/` — cross-domain deductions and required functions.
- `clean-sheet/` — implementation-free specification and competing architecture candidates.
- `experiments/` — model-free experimental organism for discriminating architecture choices.

## Current research state

First-pass evidence/synthesis is complete for:

- Foundations.
- Architecture + systems/hardware.
- Biological intelligence, development & evolution.
- Learning & adaptation.
- Inference-time intelligence.
- Persistent intelligence.
- Verification, reliability & control.
- Self-improvement.
- Machine-native representation & communication gap closure.
- Objective uncertainty & metareasoning gap closure.

Then the project deliberately crossed the clean-sheet boundary:

- **Phase 7 cross-domain synthesis:** complete to first-pass depth.
- **Phase 8 forget implementations:** complete; exit gate passed.
- **Phase 9 competing architecture families:** complete to first-pass depth; no architecture selected.
- **Phase 10 experimental reconstruction:** active.

## What the synthesis currently says

Five allocation problems recur across otherwise different areas:

1. **compute allocation** — what operation should run next, where and for how long;
2. **information allocation** — what remains active/addressable, what is abstracted and what can be forgotten;
3. **change allocation** — what state should change, at what scope and for how long;
4. **assurance allocation** — how much independent evidence/restriction a proposed transition needs;
5. **exploration/design allocation** — how much resource goes to the current best path versus alternatives and system variants.

The organizing hypothesis is that practical intelligence may be understood as adaptive selection of state transitions under uncertain world state and uncertain objectives, with finite physical resources and consequence-dependent assurance. This remains a falsifiable hypothesis, not a definition of intelligence.

## Clean-sheet reconstruction

Phase 8 produced a specification independent of current AI implementation names:

- semantic state classes;
- functional contracts;
- evidence/belief/provenance/authority semantics;
- lifetime physical resource model;
- system invariants;
- consequence-sensitive assurance/change protocol;
- unresolved experimental design choices;
- evidence traceability and falsifiers.

Phase 9 then derived four deliberately competing organizations from the same specification:

1. **Hierarchical Adaptive System** — explicit hierarchical allocation around specialized processes.
2. **Distributed Event-Driven Ecology** — locally adaptive processes with sparse coordination.
3. **Integrated Predictive Core + External Evidence** — tight cognitive integration with explicit evidence/authority boundaries.
4. **Developmental Variant System** — computational organization itself can grow/reorganize through versioned variant search.

None is currently preferred. `clean-sheet/EXPERIMENT_MATRIX.md` defines matched experiments intended to decide which architectural boundaries actually earn their cost.

## Experimental reconstruction

Phase 10 starts model-free so architecture results are not confounded by pretrained model behavior.

The first implemented probes are:

- **E03:** direct-address history versus compressed current state versus a hybrid state policy;
- **E05:** fixed versus adaptive computation on tasks with hidden difficulty/evidence quality.

The experiment package is Python 3.11+, has no runtime dependencies, emits machine-readable results and instruments logical operation/read/write/sample cost.

```bash
cd experiments
python -m pip install -e .
python -m unittest discover -s tests -v

ai-atlas-lab memory --seed 7
ai-atlas-lab adaptive-compute --seed 7
```

## Evidence discipline

Every important claim distinguishes:

1. **Observation** — directly measured or reported.
2. **Inference** — conclusion supported by observations.
3. **Hypothesis** — plausible proposition requiring testing.
4. **Design choice** — an engineering decision, not a scientific fact.

Negative results, replications, contradictory evidence, scaling limits and failure cases are first-class knowledge. Architecture decisions remain versioned and falsifiable.

## End goal

Produce a defensible answer to:

> If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?

The eventual architecture must be traceable back to evidence and survive matched experiments against credible alternatives.
