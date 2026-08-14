# Foundations — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

These statements are implementation-neutral deductions from the current evidence map. They may be revised as Foundations research reaches saturation.

## P-F01 — Inductive bias cannot be eliminated; it can be relocated or adapted

Finite evidence does not determine a unique continuation. Practical learning succeeds by exploiting structure in its task/environment distribution. Bias can live in architecture, data, objectives, optimization, memory, retrieval, search, interaction or learned meta-policies.

**Confidence:** high.

**Design consequence later:** every claimed “general” component must expose what structure it assumes and how that assumption can change.

## P-F02 — Expressive capacity is not practical intelligence

Being able to represent a function does not imply that the function can be found with finite data/compute, generalized robustly, or executed efficiently.

**Confidence:** high.

## P-F03 — Training fit and nominal parameter count do not determine generalization

Interpolation can generalize or fail depending on data geometry, noise, solution selection and learning dynamics. We should track effective solution properties rather than rely on a simple underfit/overfit capacity story.

**Confidence:** high within studied regimes; mechanism-general formulation remains active research.

## P-F04 — Compression is meaningful only relative to preserved utility/fidelity

Information should not be discarded merely to make a representation smaller. Compression, invariance and simplicity are valuable when they preserve what future prediction/action needs under resource constraints. Generic hidden-state compression is not established as a universal cause of generalization.

**Confidence:** high for the rejection of unconditional compression; medium for the best general relevance objective.

## P-F05 — The optimization/search process is part of the inductive bias

When many candidate solutions satisfy an objective, the procedure used to search/select among them can systematically determine which one is obtained.

**Confidence:** high in important model classes; scope across heterogeneous systems requires more mapping.

## P-F06 — Intelligence is resource-bounded computation

Universal induction/control ideals are theoretically useful but can be uncomputable or prohibitively expensive. A practical system must decide what to compute, approximate, cache, learn, retrieve, delegate or abandon.

**Confidence:** high.

## P-F07 — Uncertainty should be behaviorally testable and decision-linked

Confidence is useful only insofar as it predicts error/risk and changes rational action. Proper scoring, calibration and value-of-information concepts give external tests that an uncertainty mechanism can be required to pass.

**Confidence:** high for the requirement; implementation open.

## P-F08 — Observation prediction, intervention prediction and control are different queries

A system that predicts passive data well need not know the effect of changing the process. Acting systems require action-conditioned/causal knowledge or sufficient interaction to learn it.

**Confidence:** high.

## P-F09 — Exploration is a resource-allocation decision

Information can have instrumental value because it improves future decisions. Exploration should therefore be selected when expected future value exceeds its cost/risk, not treated as a fixed behavior mode.

**Confidence:** high in formal sequential settings; general estimation remains open.

## P-F10 — Credit assignment is not synonymous with differentiability

Backpropagation is one efficient credit mechanism. Temporal bootstrapping, stochastic estimators and external evaluators show that useful credit can cross nondifferentiable boundaries with different variance/information trade-offs.

**Confidence:** high.

## P-F11 — Scaling is a multidimensional allocation surface

Model size is one resource dimension. Data, training compute, inference compute, memory, bandwidth, interaction and evaluation cost can substitute for or complement one another. Empirical scaling laws are regime-specific measurements.

**Confidence:** high for multidimensionality; exact joint laws unknown.

## P-F12 — Representation quality is downstream-computation dependent

Compactness, disentanglement, human readability or reconstruction quality are not universally sufficient objectives. A representation is useful when it preserves relevant state/uncertainty and makes future needed computations cheap.

**Confidence:** medium-high; how to measure future-task utility remains open.

---

## Emerging meta-principle

A recurring pattern across the foundations is **selection under constraints**:

- learning selects hypotheses;
- compression selects retained information;
- optimization selects solutions;
- attention/search selects computation;
- decision theory selects actions;
- exploration selects information to acquire;
- architecture selects where resources and inductive bias live.

This does **not** imply one universal selection algorithm. It suggests a useful cross-domain research question:

> Can intelligence be characterized as adaptive allocation of finite representational, computational and interaction resources toward regularities and actions with the highest expected future value?

That statement is currently a **hypothesis**, not a definition of intelligence and not an architecture decision.

## What would falsify/modify this synthesis?

- a practically useful learner demonstrating broad generalization without identifiable structural assumptions or acquired bias;
- a representation metric such as compression that causally predicts broad generalization independent of task relevance and solution selection;
- a resource regime where computation/memory/data allocation does not materially affect attainable performance;
- evidence that intervention-capable systems can reliably infer action effects from observational prediction alone without the assumptions required by causal identification.
