# Local Objectives and Training Decomposition

Status: focused implementation-neutral synthesis. **No architecture or training method is selected.**

## Question

Does a system that must learn a globally useful transformation require one end-to-end learning/credit path across the entire computation graph?

Conventional backpropagation answers this operationally by propagating one global objective through the full differentiable path. DiffusionBlocks and prior block-wise methods reopen a more general question:

> Can global learning be decomposed into local learning problems when each local objective is constructed so that local solutions compose into the desired global behavior?

The key distinction is therefore not:

```text
end-to-end training
vs
block-wise training
```

It is:

```text
GLOBAL BEHAVIOR REQUIREMENT
        ↓
what learning dependencies are actually necessary?
        ↓
┌──────────────────────────────────┐
│ global gradient/credit path      │
│ locally derived compositional    │
│ staged/tentative local updates   │
│ recurrent/shared local learner   │
│ hybrid/global correction         │
└──────────────────────────────────┘
```

## Mechanism extracted from DiffusionBlocks

DiffusionBlocks assigns each depth block a segment of a denoising trajectory. Each block is trained directly toward the task target at a corresponding corruption/noise range. The blocks therefore do not merely receive arbitrary auxiliary losses: their local targets are derived from one intended global dynamical process.

Implementation-neutral abstraction:

```text
one desired global transformation
        ↓
derive a sequence/field of intermediate objectives
        ↓
assign objective regions to local learners
        ↓
train local learners independently or semi-independently
        ↓
compose them at execution time
        ↓
measure global behavior
```

## Why this matters beyond VRAM

### 1. Active learning state can follow local dependency scope

If a local learner does not require the rest of the model for forward/backward credit, parameters, gradients, optimizer state and activations outside that learner need not all be active in the same training step.

This changes the memory requirement from something closer to total model depth toward the maximum simultaneously trained dependency scope.

### 2. Communication topology changes

If two learning regions are truly independent during optimization, they need not exchange gradients/activations merely because their inference-time computations compose sequentially.

This separates:

```text
inference dependency
!=
training dependency
```

That is an important clean-sheet distinction.

### 3. Credit scope becomes a design variable

Atlas PS-015 already says delayed/global outcomes should assign credit only across causally/eligibly plausible transitions rather than the full history by default.

DiffusionBlocks provides a different neural-training analogue: useful local credit can sometimes be **constructed directly** rather than obtained by backpropagating one downstream scalar through every preceding stage.

### 4. Decomposition granularity is resource priced

Too little decomposition leaves memory/communication savings unrealized.

Too much decomposition gives each local learner insufficient transformation capacity or creates objectives whose independent solutions no longer compose well.

Therefore the design variable is not `number_of_blocks = maximum`.

It is approximately:

```text
net value(block granularity)
=
resource savings
+ parallelism value
+ specialization/curriculum value
- local-capacity loss
- composition error
- target-construction cost
- interface/conditioning overhead
```

## Anti-assumptions

Atlas must not infer any of the following from current DiffusionBlocks evidence:

- Transformers are diffusion models in the sense that all future AI should use diffusion objectives.
- End-to-end backpropagation is obsolete.
- A `B`-block model always uses exactly `1/B` real GPU memory.
- More blocks are better.
- Inter-block independence eliminates all distributed-training communication.
- Generative metric parity on small/intermediate models implies frontier-LLM capability parity.
- Local objectives are generally easy to derive.
- Inference-time model/KV memory is automatically reduced by the training decomposition.

## Competing hypotheses

### H-LO1 — global gradient dependency is necessary

For sufficiently complex learned transformations, local objectives lose information that only end-to-end credit can provide. Decomposition gains disappear or global quality collapses with scale.

### H-LO2 — local compositional objectives are sufficient in some structured regimes

When a global process admits useful intermediate target semantics, local learners can match end-to-end quality with lower active memory/communication.

### H-LO3 — hybrid credit is the general case

Most systems benefit from local learning for routine structure plus sparse/global correction for cross-block interactions that local objectives miss.

### H-LO4 — the objective field should itself be adaptive

Fixed manually designed local targets may not scale; a higher-level system may need to learn where to split computation and what intermediate training targets preserve global behavior.

## Relation to existing Atlas selections

### PS-009 — conditional sharing with isolation fallback

Training dependencies should be shared only where shared structure/credit earns its interference and resource cost. Local training is one extreme point on this continuum.

### PS-010 — joint adaptive resource substitution

Block size changes memory, communication, parallelism, wall time and quality simultaneously. The correct choice is a joint resource decision.

### PS-015 — causal/eligibility-scoped credit

The new evidence strengthens the broader claim that credit need not spread globally by default. But DiffusionBlocks does not by itself establish a new general credit principle because its local objectives are manually derived from a particular mathematical process.

### PS-020 — evidence-scaled repair scope

Learning/update scope and repair scope may share a deeper rule: propagate change only as widely as the inferred cause/objective coupling requires.

### PS-021 — regularity-scaled structural encoding

A repeated residual/dynamical structure makes it possible to specify one common local-role rule across depth.

### PS-023 — value/sensitivity-scaled fidelity

Block capacity/granularity is another fidelity axis: local stages need enough expressive depth to preserve the transformation that matters.

## Candidate deeper law

Across control, credit, repair, topology and now training, evidence increasingly points toward:

> **Dependency scope should be the smallest scope that still preserves the semantics required by the global objective.**

This is not promoted as a new principle yet. E25 must distinguish whether the rule survives actual learning/resource trade-offs.

## Open questions

1. What makes a global objective decomposable into independently learnable local objectives?
2. Does decomposability depend on architecture, task, target representation, optimization trajectory, or all of them?
3. Is there a minimum absolute block capacity rather than a fixed block-count ratio?
4. Can a system learn the objective decomposition itself?
5. When does sparse end-to-end/global correction outperform complete independence?
6. Does block independence reduce communication enough to change optimal hardware topology?
7. How does local training interact with shared/recurrent weights?
8. Can local learning improve continual/self-improvement safety by limiting update blast radius, or does it hide cross-block regressions?
9. Can JEPA-like predictive targets or other machine-native representations provide better local objective fields than denoising?
10. Does selection-aware evidence (PS-027) matter when deciding which blocks/updates receive expensive global evaluation?
