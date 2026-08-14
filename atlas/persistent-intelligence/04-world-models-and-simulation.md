# World Models and Simulation

## Required function

Predict action-conditioned future state well enough to compare candidate actions, perform counterfactual reasoning, and learn from imagined experience before paying real interaction cost.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-WM-01 | Planning can use a learned latent dynamics model rather than a hand-specified simulator. | O | E5 | P-S018, P-S019, P-S020 |
| P-WM-02 | A world model need not reconstruct every observable detail; MuZero achieved strong planning by predicting reward/value/policy-relevant quantities. | O/I | E4 | P-S018 |
| P-WM-03 | Compact latent predictive models can support control directly from pixels and reduce required environment interaction. | O | E4 | P-S019, P-S020 |
| P-WM-04 | Self-supervised predictive representation learning over large-scale video can transfer into action-conditioned robotic planning with relatively little robot interaction. | O | E3 | P-S022 |
| P-WM-05 | Deployment-time world-model memory/revision can improve prediction and downstream planning without changing backbone weights in evaluated LLM-agent environments. | O | E2 | P-S023 |

## World model != renderer

A photorealistic generative model can be useful, but rendering all details is not the defining function. The clean-sheet requirement is:

`state + candidate action + time/context -> distribution over future decision-relevant states/outcomes`.

Different tasks may require different prediction levels:

- low-level continuous dynamics;
- object/state transitions;
- semantic consequences;
- tool/software state changes;
- social/other-agent responses;
- reward/cost/risk;
- procedural preconditions and failure modes.

## Decision-sufficient prediction

MuZero provides strong evidence that modelling only quantities needed for planning can outperform insisting on full environment reconstruction. PlaNet/Dreamer likewise show that latent prediction can be more useful than pixel-perfect future generation.

The difficult clean-sheet question is therefore:

> sufficient for which future decisions?

A compressed model can be excellent for today's objective and useless for a later one if it discarded the wrong latent variables.

## Multi-timescale simulation

A persistent system may need several simulators:

- milliseconds/seconds for physical/control dynamics;
- minutes/hours for workflows and resource state;
- days/months for user/environment changes;
- abstract event-level simulation for software, organizations or strategic decisions.

One uniform time step is not a known requirement.

## Counterfactuals

The system should distinguish:

- prediction under current policy;
- prediction after intervention/action;
- alternative hypothetical action;
- prediction conditioned on uncertain hidden state.

This links world models directly to the Foundations distinction between observation and intervention.

## Imagination as compute

Simulation is an inference-time operation and should compete against alternatives:

`simulate / retrieve past episode / query tool / act and observe / ask / use direct policy`.

If model uncertainty is high, more imagined rollouts can amplify error rather than add evidence.

## Failure modes

Model bias; omitted decision-relevant variable; reward-predictive but transfer-poor latent state; compounding rollout error; simulator exploitation; hallucinated affordances; incorrect other-agent model; failure to update after environment change; treating realistic-looking prediction as calibrated prediction.
