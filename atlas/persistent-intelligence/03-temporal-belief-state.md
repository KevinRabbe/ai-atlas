# Temporal Belief State

## Required function

Maintain a compact, uncertainty-aware estimate of the current world when observations are partial, delayed, noisy or contradictory.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-TB-01 | State estimation can recursively combine prior state and new noisy observations while maintaining uncertainty; Kalman filtering gives the canonical linear-Gaussian example. | O | E5 | P-S001 |
| P-TB-02 | In partially observable decision problems, optimal action can depend on a belief over hidden state rather than the latest observation alone. | O | E5 | P-S002 |
| P-TB-03 | Latent recurrent world models can infer useful hidden state from observation/action histories and support planning under partial observability. | O | E4 | P-S019, P-S020 |
| P-TB-04 | Long-horizon embodied benchmarks expose failures from overwritten state, visibility changes and stale observations even when textual memory is available. | O | E2 | P-S014 |

## Archive is not current state

Suppose memory contains:

- 10:00 — door closed;
- 10:05 — robot opened door;
- 10:10 — camera view lost;
- 10:20 — another agent may have entered.

The correct present state is not a retrieved sentence. It is a belief conditioned on actions, elapsed time, visibility and possible exogenous changes.

Therefore persistent intelligence needs at least two separable objects:

1. **event history** — evidence of what was observed/done;
2. **belief state** — current best estimate, including uncertainty.

## Temporal semantics

Knowledge should be typed by temporal behavior:

- static/slow-changing facts;
- mutable state variables;
- events that happened once;
- periodic/routine patterns;
- hypotheses about latent causes;
- time-bounded commitments/preferences;
- actions with known/unknown delayed effects.

A fact without temporal scope can become a future hallucination even if it was once correct.

## Prediction-update loop

A general persistent state estimator has the form:

`belief_t --action/time/model--> predicted belief_{t+1} --observation--> corrected belief_{t+1}`.

The update need not be Bayesian in implementation, but it should expose equivalent questions:

- what changed because of our action?
- what may have changed independently?
- how informative is the new observation?
- what uncertainty remains?

## Object permanence and identity

Persistent systems also need correspondence across observations: whether two observations refer to the same entity, process, file, person, tool session or environment object. Identity errors corrupt every later memory operation.

## Clean-sheet restatement

Persistent intelligence needs an uncertainty-aware **state estimator**, not merely a long transcript. The estimator should integrate actions and observations, preserve unresolved alternatives, and know when its state is stale enough to require new observation.

## Failure modes

Last-observation-as-truth; stale state; identity merge/split errors; hidden state collapsed to one confident hypothesis; action effects not propagated; time ignored in retrieval; uncertainty forgotten during summarization; current belief overwritten without preserving evidence history.
