# World Models & Simulation

## Required function

Predict action-conditioned consequences, represent hidden environment dynamics and support counterfactual planning before expensive or irreversible interaction.

## Status

**First coupled persistent-intelligence evidence pass completed on 2026-08-14; not saturated.**

Detailed evidence lives under [`persistent-intelligence/`](persistent-intelligence/INDEX.md), especially the world-model, uncertainty and temporal-belief notes.

## First-pass findings

1. **World model does not mean renderer.** Useful models can predict compact latent/decision-relevant quantities instead of reconstructing all sensory detail.
2. **Prediction state is task-relative.** A representation sufficient for one objective may hide variables required by later goals.
3. **Partial observability requires belief state.** Current state is inferred from observation/action history, not taken directly from the latest observation.
4. **Uncertainty is part of the model output.** Rollout confidence should decay/change as model error and stochasticity accumulate.
5. **Imagination competes with reality.** Simulation, retrieval, observation, probing and tool use are alternative information/computation operations.
6. **Prediction error is valuable persistent evidence.** Mismatches can signal stale state, missing variables, causal error or regime change.
7. **Multiple time scales are plausible.** Physical control, workflows and long-lived semantic changes need not share one transition granularity.

## Mechanism families to map

Explicit transition models; latent dynamics; predictive representation learning; model-based reinforcement learning; learned simulators; causal models; digital twins; search over imagined trajectories; uncertainty-aware rollout; ensembles; multi-timescale dynamics; model revision from deployment experience.

## Clean-sheet questions

- What must be predicted for future decisions, and what can be safely ignored?
- How can a model preserve information whose future task relevance is unknown?
- Should prediction occur in observation space, latent state, structured state, programs, or several levels at once?
- How should uncertainty propagate through rollout depth?
- When should the controller stop simulating and query reality?
- Can multiple incompatible world-model hypotheses be maintained until evidence resolves them?
- How should the system represent other agents, tools and itself inside the world state?
- How should prediction-observation mismatches modify confidence, memory and learning priority?

## Anti-assumptions

Do not assume photorealistic generation is a better world model, that lower prediction loss guarantees better planning, or that more imagined rollouts improve decisions. The relevant metric is decision quality under model uncertainty and cost.
