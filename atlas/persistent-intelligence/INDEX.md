# Persistent Intelligence — Coupled Map

**Status:** first evidence pass in progress.

Persistent intelligence is the problem of maintaining a useful, revisable model of experience and world state across time. It couples memory, state estimation, knowledge management, world models, multimodal grounding and action because a stored fact is useful only if the system knows when it is still true, how it was learned, what it predicts, and when it should affect behavior.

## Research decomposition

1. [`01-memory-lifecycle.md`](01-memory-lifecycle.md) — writing, revision, consolidation, retrieval and forgetting.
2. [`02-memory-use-and-abstraction.md`](02-memory-use-and-abstraction.md) — episodic/semantic/procedural memory and when recall becomes useful experience.
3. [`03-temporal-belief-state.md`](03-temporal-belief-state.md) — hidden state, partial observability, confidence and change over time.
4. [`04-world-models-and-simulation.md`](04-world-models-and-simulation.md) — predictive state, imagination and planning.
5. [`05-model-uncertainty-and-reality-checks.md`](05-model-uncertainty-and-reality-checks.md) — uncertainty accumulation, model error and when to query reality.
6. [`06-multimodal-grounding-and-action.md`](06-multimodal-grounding-and-action.md) — cross-modal state, embodiment and action representations.
7. [`07-long-horizon-stateful-agents.md`](07-long-horizon-stateful-agents.md) — persistent memory used in real decisions across sessions.
8. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions only.

## Shared evaluation axes

Every persistent-state mechanism should be measured by:

- write precision and false-memory rate;
- revision/conflict handling;
- retrieval usefulness rather than similarity alone;
- temporal/state correctness after changes;
- provenance and confidence preservation;
- memory growth and consolidation efficiency;
- downstream action/task improvement;
- robustness to partial observability and stale observations;
- world-model rollout accuracy and uncertainty calibration;
- ability to detect model mismatch and query reality;
- multimodal grounding and cross-modal transfer;
- cost of storage, retrieval, simulation and state updates;
- rollback/auditability of persistent changes.

## Anti-assumption

Do not equate memory with a vector database, knowledge with model weights, state with a text transcript, or a world model with photorealistic video generation. The required functions are persistence, revision, state estimation, prediction and useful future action; representation is open.
