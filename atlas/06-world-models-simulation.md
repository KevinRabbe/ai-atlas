# World Models & Simulation

## Required function

Predict consequences of actions, represent environment dynamics, support counterfactual reasoning and enable planning before expensive or irreversible interaction.

## Mechanism families to map

Explicit transition models; latent dynamics; predictive representation learning; model-based reinforcement learning; learned simulators; causal models; digital twins; search over imagined trajectories; uncertainty-aware rollout; multi-model ensembles.

## Early evidence anchors

AlphaZero demonstrates the strength of search when a reliable environment model/rules are available. MuZero learns only the aspects of dynamics needed for planning—reward, value and policy-relevant state—rather than reconstructing the full environment. DreamerV3 learns a world model and improves behavior through imagined trajectories across diverse domains. JEPA-style work explores prediction in representation space rather than reconstructing every observable detail.

## Clean-sheet questions

- What must a world model predict, and what information is irrelevant to decisions?
- Should prediction happen in observation space, latent state, symbolic structure, programs, or multiple levels?
- How should uncertainty grow through rollout depth?
- When should the system query reality instead of trusting simulation?
- Can multiple incompatible world-model hypotheses be maintained simultaneously?
- How are other agents, tools and the system itself represented inside the world model?
