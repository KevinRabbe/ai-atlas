# Self-Improvement — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

## P-SI01 — Self-improvement is mutation routing, not one update rule

Weaknesses can live in context policy, memory, tools, harness, data, weights, architecture or evaluators. Improvement requires selecting the causal layer rather than defaulting to whichever substrate is easiest to mutate.

**Confidence:** high.

## P-SI02 — Mutation scope should be evidence-driven

Cheap reversible local changes are attractive probes, while broader mutations can yield better transfer when the bottleneck is structural. Scope should escalate when controlled evidence shows narrower interventions are insufficient.

**Confidence:** medium-high.

## P-SI03 — Runtime/harness policy is a genuine learning substrate

Automated harness optimization can materially improve fixed-model performance and cost. Runtime self-improvement should be measured independently from weight learning rather than treated as prompt engineering noise.

**Confidence:** high.

## P-SI04 — Model and harness co-evolve through data

The runtime determines which experiences/traces are generated, retained and later trained on. Weight learning changes how the runtime behaves. Long-term optimization must therefore account for the coupled feedback loop.

**Confidence:** high conceptually; quantitative dynamics open.

## P-SI05 — Improvement search benefits from preserving alternative lineages

Population/archive methods reduce premature convergence and retain stepping stones or variants optimized for different objectives. One greedy incumbent is not established as the best self-improvement strategy.

**Confidence:** medium-high.

## P-SI06 — Self-improvement can search over computation itself

Neural architecture search, AlphaTensor/AlphaEvolve and self-modifying agents show that useful search spaces can include architectures, executable algorithms and the procedure that creates future variants—not only parameter values.

**Confidence:** high that this is possible; general/open-ended scalability remains open.

## P-SI07 — Structural/meta-mutations require stronger assurance than local patches

Changing architecture, evaluators, update rules or mutation operators changes future behavior/search distributions and can undermine prior tests. Assurance should scale with the meta-level and blast radius of the change.

**Confidence:** high as a systems inference.

## P-SI08 — Acceptance authority must remain sufficiently independent from the candidate mutation

A candidate should not be able to earn acceptance solely by modifying its own evaluator, hidden tests, permissions, audit history or rollback mechanism. Changes to those components require a separate/higher-level migration path.

**Confidence:** very high.

## P-SI09 — Self-improvement should preserve lineage and rollback

Versioned variants, evidence and parent-child relationships make improvements auditable, comparable and reversible. Archive/population approaches also preserve information about rejected alternatives.

**Confidence:** high.

## P-SI10 — Improvement value is lifetime utility, not immediate benchmark gain

A mutation's worth includes future reuse, inference savings, training-data effects, maintenance complexity, assurance cost and regressions. Some improvements should be rejected even when a target score rises.

**Confidence:** high conceptually; operational utility model open.

## P-SI11 — Successful computation can migrate to more durable/cheaper substrates

Repeated verified inference, procedures and harness workarounds are candidates for consolidation into skills, adapters, weights or structural changes when expected reuse justifies it.

**Confidence:** medium-high.

## P-SI12 — Self-improvement itself needs a stopping policy

Another mutation/search round is worthwhile only when expected future gain exceeds proposal, evaluation, delay and risk cost. Infinite self-modification is not an intelligence requirement.

**Confidence:** high.

## P-SI13 — Evaluator improvement is uniquely dangerous

Improving the evaluator can be necessary, but it changes the ruler used to judge every later change. Evaluator/reward mutations need independent holdouts, cross-version comparisons and protected acceptance paths.

**Confidence:** high.

---

## Emerging self-improvement loop

An implementation-neutral loop is:

`observe failure/opportunity -> localize cause -> choose mutation surface -> generate diverse candidate variants -> sandbox/evaluate -> independent regressions/assurance -> compare lifetime utility -> accept/archive/reject -> monitor -> consolidate or rollback`.

Crucially, the loop itself is also a possible mutation target. When that happens, the acceptance mechanism must remain outside the candidate's uncontrolled scope.

## Cross-domain connection

Self-improvement turns the four earlier allocation problems into a meta-allocation problem:

- allocate **compute** to proposed changes;
- allocate **information** to diagnosis and retained evidence;
- allocate **change** to the correct substrate/lifetime;
- allocate **assurance** according to mutation scope/consequence;
- allocate **exploration** across competing system lineages.

This suggests another provisional formulation:

> a self-improving intelligent system must allocate not only resources and state, but also the search over its own future implementations.

Still not a final architecture.

## Strong anti-conclusions

This pass does **not** justify:

- “recursive self-rewriting automatically leads to better intelligence”;
- “all improvements should modify weights”;
- “harness improvements make model training unnecessary”;
- “the best current variant should replace every alternative”;
- “a candidate can safely update its own evaluator and tests together”;
- “benchmark improvement establishes net system improvement”;
- “more self-improvement iterations are always desirable”;
- “open-ended search should be unconstrained.”

## Most valuable experiments

1. Inject failures attributable to different layers and test whether a learned mutation router selects the causal substrate better than fixed heuristics.
2. Compare greedy single-lineage versus archive/population self-improvement under changing objectives and hidden regressions.
3. Repair identical weaknesses through harness, skill, adapter and full-weight changes under equal lifetime resource budgets.
4. Co-optimize harness and weights while measuring future trace quality, not only current task score.
5. Allow mutation of the mutation operator while keeping acceptance/control independent; measure improvement versus regression/Goodhart risk.
6. Compare immediate benchmark selection with lifetime-utility selection including inference cost, maintenance, transfer and safety regressions.
