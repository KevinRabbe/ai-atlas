# Foundations

## Required function

Identify the mathematical, statistical, computational and information-theoretic constraints that any intelligent learning system must obey.

## Status

**First evidence pass completed; not saturated.**

Detailed notes now live under [`atlas/foundations/`](foundations/INDEX.md). The first pass covers induction/generalization, information/compression, computation/complexity, optimization/search, uncertainty/decision, causality/control, credit assignment, representation, and resource scaling. A provisional implementation-neutral synthesis is in [`foundations/PROVISIONAL_SYNTHESIS.md`](foundations/PROVISIONAL_SYNTHESIS.md).

## Areas to map

Probability and Bayesian inference; information theory; compression and minimum description length; optimization; statistical learning theory; causality; control theory; dynamical systems; search; computability and complexity; decision theory; representation learning; credit assignment; exploration; generalization; compositionality.

Biology and cognitive science belong here only when they yield testable computational hypotheses. Biological plausibility is not itself an optimization target.

## Core questions

- What is intelligence optimizing, if anything can be stated generally?
- Which aspects of prediction, compression and control are equivalent or merely correlated?
- What resources fundamentally bound performance: data, compute, memory, communication, energy, interaction, or feedback quality?
- What makes a representation useful for transfer and recombination?
- Which forms of uncertainty must be represented explicitly?
- What determines whether additional computation should occur now versus knowledge being amortized into a learned policy?
- Where must inductive bias live, and how can it adapt when the environment changes?
- How should a system value information before deciding whether to search, ask, experiment, simulate or act?

## First-pass findings

The first pass supports several strong constraints without selecting an architecture:

1. **Inductive bias is unavoidable.** Superiority is distribution-relative; the useful question is where assumptions live and how they adapt.
2. **Expressivity is not learnability.** Representing a solution says little about whether finite compute/data can discover or use it well.
3. **Compression requires relevance.** More compression is not a universal intelligence objective; retained information must be judged against fidelity/utility and future tasks.
4. **Optimization selects solutions.** Search/optimizer dynamics can act as implicit regularization and therefore belong in the learning semantics.
5. **Intelligence is resource bounded.** Universal formal ideals can be uncomputable or impractical; compute/memory/data allocation is part of the problem.
6. **Uncertainty must affect decisions.** Confidence should be externally testable and tied to the value of more information or computation.
7. **Prediction is not intervention.** Acting well may require causal/action-conditioned knowledge beyond passive predictive accuracy.
8. **Differentiability is not a universal credit requirement.** Multiple credit estimators exist with different feedback and variance properties.
9. **Scaling is multidimensional.** Parameters, data, training compute, inference compute, memory, bandwidth and interaction form a joint resource surface.
10. **Representation quality is relational.** A representation is useful insofar as it preserves relevant state/uncertainty and makes future computation cheaper.

These are provisional synthesis statements. Detailed evidence and caveats are recorded in the subnotes rather than promoted directly into design choices.

## Anti-assumptions

Do not assume next-token prediction, gradient descent, differentiable computation, dense tensors, human language, Transformer attention, a single monolithic model, or von-Neumann hardware are necessary. Treat each as a successful mechanism to be evaluated against alternatives.

Likewise, do not promote universal approximation, universal induction, compression, Bayesian inference or asymptotic optimality into architecture requirements merely because they have elegant formal properties. Practicality and finite-resource behavior must be established separately.
