# Objective, Utility & Metareasoning — Focused Gap Closure

**Status:** focused evidence pass in progress.

This pass addresses a cross-domain dependency: allocation policies require some representation of value, constraints, uncertainty and cost. A system cannot rationally decide whether to compute, learn, explore, verify or self-modify without estimating what those operations are worth.

## Research decomposition

1. [`01-objective-uncertainty-and-preferences.md`](01-objective-uncertainty-and-preferences.md) — objectives as uncertain/inferred rather than perfectly specified scalars.
2. [`02-multiple-objectives-and-constraints.md`](02-multiple-objectives-and-constraints.md) — constraints, Pareto trade-offs and non-scalarized objectives.
3. [`03-value-of-computation-and-information.md`](03-value-of-computation-and-information.md) — metareasoning over the cost/benefit of another computation or observation.
4. [`04-meta-control-across-resources.md`](04-meta-control-across-resources.md) — applying value-of-computation logic to compute, memory, change and assurance.
5. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions.

## Evaluation axes

- true/hidden utility versus measured proxy;
- uncertainty about preferences/objectives;
- constraint violation probability/severity;
- Pareto/multi-objective trade-offs;
- cost of eliciting additional preference/evidence;
- calibration of expected value estimates;
- computation/observation cost;
- sensitivity to horizon and environment shift;
- Goodhart behavior under optimization pressure;
- consistency across resource-allocation decisions.

## Anti-assumption

Do not assume one fixed scalar reward fully specifies human intent, that an observed reward/preference is ground truth, or that additional computation is free. Objectives themselves can be uncertain evidence and metacognitive operations consume resources.
