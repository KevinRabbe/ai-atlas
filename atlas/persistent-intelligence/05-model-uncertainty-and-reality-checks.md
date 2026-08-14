# Model Uncertainty and Reality Checks

## Required function

Represent when predicted futures are unreliable, propagate that uncertainty through simulation, and decide when real observation is worth more than further internal prediction.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-MU-01 | Learned dynamics can be highly sample-efficient but model error limits performance; probabilistic ensembles improve model-based control by representing uncertainty. | O | E4 | P-S021 |
| P-MU-02 | Long-horizon prediction is vulnerable to accumulated model error and multimodal futures; latent world-model work explicitly uses stochastic state to represent uncertainty. | O/I | E4 | P-S019, P-S020 |
| P-MU-03 | Recent agent-world-model work reports that low-confidence foresight can hurt downstream planning and benefits from selective filtering/revision. | O | E2 | P-S023 |
| P-MU-04 | Under partial observability, uncertainty is a property of the current hidden state estimate as well as future dynamics. | O | E5 | P-S001, P-S002 |

## Two uncertainty sources

A useful distinction is:

- **aleatoric/irreducible uncertainty** — the environment has multiple possible outcomes;
- **epistemic/model uncertainty** — the system lacks knowledge/data about what will happen.

They imply different actions. More internal compute may characterize irreducible uncertainty but cannot remove it; new observation/interaction can reduce epistemic uncertainty.

## Rollout uncertainty

A predicted trajectory should not be represented only as:

`state_0 -> state_1 -> state_2 -> state_3`.

It should carry uncertainty/dependencies so the controller can detect when an apparently precise deep rollout is mostly unsupported extrapolation.

One approximate decision rule is:

`trust simulation while expected decision value of model prediction > value of real observation/query + cost`.

## Reality checks

Possible grounding actions include:

- inspect the environment again;
- query a sensor/tool/API;
- execute a reversible probe action;
- retrieve a recent independent observation;
- ask another agent/user;
- run a higher-fidelity simulator;
- maintain multiple hypotheses instead of forcing one prediction.

This turns perception into an active information-acquisition policy.

## Model mismatch as a learning signal

The sequence:

`prediction -> action/observation -> prediction error`

should update more than task loss. It can reveal:

- stale world state;
- missing variables;
- regime change;
- bad causal assumption;
- local simulator failure;
- need to reduce confidence or increase observation frequency.

Persistent intelligence should preserve these mismatch events because they are unusually informative about model boundaries.

## Clean-sheet restatement

A world model should produce not only candidate futures but also enough uncertainty/model-validity information for a controller to choose between **imagination and reality**.

## Failure modes

Confident extrapolation beyond training/experience; uncertainty collapsed during rollout; treating ensemble disagreement as perfect epistemic uncertainty; repeated simulation where observation would be cheaper; unsafe exploratory probes; stale model trusted after regime change; using the same faulty model as both generator and verifier.
