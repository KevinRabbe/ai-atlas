# Verification, Reliability & Control — Coupled Map

**Status:** first evidence pass in progress.

This area studies how an intelligent system decides which outputs, intermediate states, memories, predictions, actions and self-modifications are trustworthy enough to propagate. Verification quality, uncertainty, permissions and containment are coupled: a weak evaluator should not authorize the same search pressure or irreversible action as a mechanically checked result.

## Research decomposition

1. [`01-verification-and-evaluators.md`](01-verification-and-evaluators.md) — candidate checking, evaluator quality and independence.
2. [`02-process-outcome-formal-checking.md`](02-process-outcome-formal-checking.md) — outcome/process supervision and mechanically checked specifications.
3. [`03-calibration-abstention-escalation.md`](03-calibration-abstention-escalation.md) — uncertainty, selective prediction and evidence acquisition.
4. [`04-proxy-objectives-reward-hacking.md`](04-proxy-objectives-reward-hacking.md) — Goodhart effects, specification gaming and evaluator exploitation.
5. [`05-interpretability-monitoring.md`](05-interpretability-monitoring.md) — internal diagnostics, feature monitoring and their limits.
6. [`06-agent-security-capability-control.md`](06-agent-security-capability-control.md) — untrusted inputs, tool permissions, sandboxing and control protocols.
7. [`07-regression-defense-in-depth.md`](07-regression-defense-in-depth.md) — staged gates, rollback, adversarial tests and persistent-change containment.
8. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions only.

## Shared evaluation axes

Every verification/control mechanism should report:

- false acceptance and false rejection rates;
- calibration and coverage/risk trade-offs;
- robustness under adversarial optimization;
- evaluator independence/correlation with generator errors;
- specification coverage and omitted-objective risk;
- verification cost and latency;
- privilege/action scope authorized by the signal;
- reversibility and rollback cost;
- attack surface from untrusted data/tools/memory;
- transfer under distribution shift;
- hidden/holdout regression performance;
- auditability and provenance of decisions.

## Anti-assumption

Do not equate verification with an LLM judge, safety with a refusal policy, interpretability with proof, or formal verification with correctness relative to unstated human intent. Trust must be tied to what the checking mechanism actually establishes.
