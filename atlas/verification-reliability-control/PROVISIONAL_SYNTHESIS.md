# Verification, Reliability & Control — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

## P-V01 — Verification produces scoped evidence, not universal truth

Every checker establishes particular properties under particular assumptions. Trust should track what was actually verified rather than promoting a passing score into a global correctness claim.

**Confidence:** very high.

## P-V02 — Verification strength should scale with consequence and optimization pressure

Low-risk reversible outputs can tolerate weaker evidence than persistent, privileged or irreversible actions. Likewise, an evaluator exposed to stronger search/optimization pressure requires stronger robustness/independence because proxy exploitation becomes more likely.

**Confidence:** high.

## P-V03 — Outcome and process verification solve different problems

Outcome checks are cheap and representation-agnostic when results are objectively testable. Process checks improve localization and long-horizon credit when intermediate properties can be checked. Neither dominates universally.

**Confidence:** high.

## P-V04 — Formal guarantees are powerful but specification-relative

Mechanically checked proofs/tests can provide unusually strong evidence for explicit formal properties. They do not establish that the formal specification captured all relevant human intent or real-world assumptions.

**Confidence:** very high.

## P-V05 — Evaluator independence matters because agreement is not evidence when errors are correlated

Multiple copies of the same blind spot can create high-confidence consensus. Valuable redundancy comes from different evidence sources, algorithms, hidden tests, formal checks or adversarial roles.

**Confidence:** high.

## P-V06 — Confidence should control behavior, not decorate outputs

Calibration becomes operationally useful when uncertainty changes action: verify, acquire evidence, reduce scope, require authorization or abstain. Thresholds should depend on consequence and regime rather than one global confidence cutoff.

**Confidence:** very high.

## P-V07 — Optimizing an imperfect evaluator changes its effective reliability

Goodhart/reward-model overoptimization shows that a proxy adequate for ranking ordinary samples can fail under targeted optimization. Search pressure and evaluator trust must therefore be coupled.

**Confidence:** high.

## P-V08 — Capability and authority should be separated

A component can be highly capable while its ability to read, write, execute or mutate persistent state remains restricted by an external runtime. Least privilege and staged authorization reduce dependence on model obedience.

**Confidence:** high.

## P-V09 — Instructions, observations and retrieved content need explicit authority/provenance

Tool outputs, web pages, documents and memories may contain imperative text but are not thereby trusted instructions. Persistent authority metadata should survive context/memory transformations.

**Confidence:** high.

## P-V10 — Interpretability is a diagnostic sensor, not a proof system

Internal feature/circuit analysis can expose useful predictive evidence and hypotheses, but current methods are incomplete and intervention on interpretable features can have unintended effects. Interpretability should feed monitoring/escalation rather than serve as sole authorization.

**Confidence:** high.

## P-V11 — Defense in depth should combine heterogeneous barriers

Robust systems should use different controls—permissions, preconditions, sandboxing, independent verification, effect checks, monitoring, audit and rollback—so one failure mode does not defeat every layer.

**Confidence:** high.

## P-V12 — Persistent/self-modifying changes should be transactional

Changes with large scope or durability should be staged, regression-tested, activated atomically, monitored and rollback-capable. The candidate change should not control the only evaluator, rollback path or audit record used to approve itself.

**Confidence:** high as a systems principle; exact gating policy open.

## P-V13 — Regression suites must remain partly outside the optimization loop

Repeated self-improvement can overfit fixed public tests. Hidden, rotating, adversarial or independently maintained checks are needed to estimate capability/safety beyond the optimized suite.

**Confidence:** medium-high.

## P-V14 — Reliability is a property of state transitions, not only answers

A correct textual answer does not imply safe memory writes, tool side effects, world-state changes or self-modifications. Verification should target the transition actually being authorized.

**Confidence:** very high.

---

## Emerging assurance controller

A clean-sheet system can treat trust as another allocation problem:

`candidate transition + uncertainty + consequence + reversibility + privilege + evaluator quality + optimization pressure`

-> choose

`accept / verify more / use independent checker / sandbox / reduce scope / acquire evidence / require authorization / reject / rollback`.

This creates a fourth recurring Atlas allocation dimension:

- **compute allocation** — what operation runs;
- **change allocation** — what state changes and for how long;
- **information allocation** — what evidence/state is retained or abstracted;
- **assurance allocation** — how much independent evidence/control a transition needs before it may propagate.

The cross-domain hypothesis is therefore becoming:

> intelligence may require adaptive allocation of information, computation, interaction, durable change and assurance according to expected future utility under uncertainty and consequence.

Still a hypothesis, not the final architecture or definition.

## Strong anti-conclusions

This pass does **not** justify:

- “an LLM judge makes an output verified”;
- “more judges always increase confidence”;
- “process supervision is always superior to outcome checks”;
- “formal verification solves alignment”;
- “confidence scores are trustworthy without calibration”;
- “interpretability proves intent/safety”;
- “safety can live only in model weights”;
- “sandboxing alone makes an untrusted agent safe”;
- “passing the regression suite proves a self-change is safe.”

## Most valuable experiments

1. Increase search pressure against evaluators with controlled blind spots and measure when proxy/gold performance diverges.
2. Compare outcome, structured-process and formal verification at equal total verification cost across tasks with different checkability.
3. Measure single-model consensus versus genuinely independent checker ensembles under correlated failure distributions.
4. Learn consequence-sensitive abstain/verify/escalate policies and compare with fixed confidence thresholds.
5. Give the same capable agent different external permission/transaction protocols and measure task utility versus harmful/irreversible side effects.
6. Run self-modification loops with public-only versus hidden/adversarial regression suites and measure overfitting/regression accumulation.
