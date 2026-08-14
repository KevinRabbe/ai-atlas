# Objective, Utility & Metareasoning — Provisional Synthesis

**Status: focused gap-closure synthesis, not architecture.**

## P-O01 — Objective signals are evidence, not automatically the objective

Rewards, preferences, demonstrations, instructions and metrics can be incomplete/noisy/context-specific observations about intended value.

**Confidence:** very high.

## P-O02 — Objective uncertainty should be represented explicitly when it can change decisions

If plausible interpretations of user/policy intent produce different actions, the system should preserve uncertainty and potentially seek clarification rather than silently committing to one reward model.

**Confidence:** high.

## P-O03 — Value can require structure beyond one fixed scalar

Constraints, risk limits, resource budgets, preferences and unknown trade-offs can make one fixed scalarization inadequate or undesirable. Pareto/constraint representations are legitimate decision objects.

**Confidence:** high.

## P-O04 — Scalarization is a decision operation, not necessarily a permanent ontology

A system can preserve multiple objectives/constraints and choose a context-specific trade-off only when action requires it, with provenance for how that trade-off was selected.

**Confidence:** medium-high.

## P-O05 — Metareasoning turns computation into an action with cost and expected value

Another reasoning step, verifier, retrieval, simulation or query is worthwhile only if expected downstream improvement exceeds its resource/risk/opportunity cost.

**Confidence:** high.

## P-O06 — Value of information is decision-relative

Information is valuable insofar as it can improve future decisions, calibration or reusable learning—not merely because it is surprising or reduces entropy.

**Confidence:** high.

## P-O07 — Resource classes can substitute for one another

Inference compute, external tools, observation, memory, learning, verification and self-improvement can sometimes solve the same bottleneck through different lifetime cost profiles.

**Confidence:** high as systems inference.

## P-O08 — Metacontrol itself must be resource-bounded

Exact calculation of the best next computation can be more expensive than the computation. Cheap learned/heuristic policies are required for common cases, with expensive meta-analysis reserved for high-value ambiguity.

**Confidence:** high.

## P-O09 — Allocation policies are themselves learnable objects

Evidence from metareasoning, adaptive compute, retrieval, active perception, consolidation and self-improvement supports learning when to think, ask, retrieve, verify, learn and stop.

**Confidence:** medium-high; generalization is unresolved.

## P-O10 — Central metacontrol is not yet established

The recurring need for allocation does not prove one global executive should make every decision. Distributed local policies, hierarchical control and implicit learned dynamics remain competing designs.

**Confidence:** high that the architecture is unresolved.

---

## Refined cross-domain hypothesis

The Atlas now has evidence for a more precise organizing statement:

> A practical intelligent system must continually choose among possible **state transitions and information/computation operations** under uncertain objectives, uncertain world state, finite resources and consequence-dependent assurance requirements.

A useful policy therefore needs estimates of:

`expected future utility + objective uncertainty + state uncertainty + operation reliability + lifetime reuse - resource cost - risk/irreversibility - opportunity cost`.

This equation is conceptual, not a proposed scalar reward. Several terms may remain constraints/distributions/Pareto dimensions rather than being numerically collapsed.

## Important implication

The earlier “allocation under uncertainty” hypothesis survives this gap closure, but with an important correction:

**the value function being optimized is itself uncertain, structured and partially learned.**

That prevents the synthesis from quietly assuming a perfectly known scalar objective.

## Strong anti-conclusions

This pass does **not** justify:

- “reward is enough” as a complete specification strategy;
- “the system should infer what users really mean and ignore explicit instructions”;
- “everything should be converted to one scalar utility”; 
- “hard constraints never need exceptions or contextual governance”;
- “a central metacognitive controller is required”;
- “value-of-computation can be calculated exactly in real systems”;
- “more resource-rational behavior is always safer if the objective is wrong.”

## Most valuable experiments

1. Compare fixed scalar objective, constrained objective and uncertainty-aware multi-objective representations under deliberate environment/priority shifts.
2. Give systems ambiguous preference evidence and measure whether calibrated clarification beats confident reward inference.
3. Train value-of-computation policies for reasoning/retrieval/verification and test out-of-distribution cost/difficulty regimes.
4. Compare one global allocation controller with hierarchical/distributed local policies at equal compute/communication budgets.
5. Jointly allocate between simulation, real observation, tool use and learning to test whether cross-resource metacontrol beats independent heuristics.
