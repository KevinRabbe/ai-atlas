# Learning & Adaptation — Evidence Map

**Status:** first evidence pass in progress.

This area studies learning as **change allocation**: which information source produces a learning signal, what internal/external substrate should change, how quickly it should change, and when tentative adaptations should become durable.

## Research decomposition

1. [`01-learning-signals-objectives.md`](01-learning-signals-objectives.md) — labels, self-supervision, demonstrations, preferences, rewards and verifiable feedback.
2. [`02-adaptation-substrates.md`](02-adaptation-substrates.md) — context/fast state, external memory, parameter-efficient state, full weights, skills/routing and architecture.
3. [`03-continual-learning-forgetting.md`](03-continual-learning-forgetting.md) — interference, replay, regularization and nonstationarity.
4. [`04-meta-learning-fast-adaptation.md`](04-meta-learning-fast-adaptation.md) — learning to adapt and in-context/online adaptation.
5. [`05-distillation-consolidation.md`](05-distillation-consolidation.md) — converting expensive or transient computation into cheaper durable competence.
6. [`06-data-curriculum-selfplay.md`](06-data-curriculum-selfplay.md) — data order, self-generated experience, imitation and active data acquisition.
7. [`07-reinforcement-preference-feedback.md`](07-reinforcement-preference-feedback.md) — behavior learning from consequences/preferences/evaluators.
8. [`08-learning-timescales-migration.md`](08-learning-timescales-migration.md) — when information should migrate among substrates.
9. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions only.

## Shared evaluation axes

Every learning mechanism should report:

- information source and supervision density;
- which substrate changes;
- adaptation latency;
- sample and compute efficiency;
- retention of old capability;
- transfer/generalization;
- reversibility and provenance;
- susceptibility to reward/proxy exploitation;
- interaction/data collection cost;
- stability under distribution shift;
- cost of consolidating or undoing the change.

## Core separation

`feedback source != optimization rule != storage substrate != timescale`

For example, a reward signal could update temporary search policy, episodic memory, a local adapter, a routing policy, or durable weights. Treating these choices as one indivisible “training method” hides the design space.