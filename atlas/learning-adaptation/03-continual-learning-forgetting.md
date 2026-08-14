# Continual Learning, Interference and Forgetting

## Required function

Acquire new competence over time without unacceptable loss or distortion of older competence under finite memory and compute.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| L-CL-01 | Sequential gradient learning can catastrophically impair older tasks. | O | E5 | L-S012 |
| L-CL-02 | Protecting parameters estimated to matter for older tasks can reduce forgetting in studied settings. | O | E3 | L-S012 |
| L-CL-03 | Replay can reduce forgetting, but its benefit depends on sample choice, task relation and signal/noise structure; more replay is not monotonically better in general. | O | E3 | L-S013, L-S014 |
| L-CL-04 | Even full replay can fail to eliminate forgetting in analyzed regimes when later-task noise/interference dominates earlier signal. | O | E2 | L-S014 |

## Central insight

Forgetting is not merely “old data disappeared.” It can arise because **new updates alter a shared representation in directions incompatible with old functions**.

This means continual learning has at least three distinct levers:

1. preserve/replay information about old experience;
2. constrain which shared state may change;
3. allocate new knowledge to separate or expandable state when interference is predicted to be high.

## Replay is not magic

The common story “replay approximates joint training, therefore more replay is safer” has counterexamples. Theory and experiments show harmful/non-monotonic replay when replay samples and task subspaces interact badly. This becomes a registered Atlas contradiction rather than an implementation footnote.

## Clean-sheet restatement

Before changing a shared substrate, estimate:

- expected benefit to new competence;
- overlap with old features/skills;
- uncertainty about the update;
- reversibility;
- availability of old-task validation;
- whether isolated storage is cheaper than interference repair.

A system capable of growing/isolating state may avoid forcing every new fact or skill through the same shared parameters.

## Metrics required

Average accuracy is insufficient. Track forward transfer, backward transfer, worst-case retained capability, calibration drift, representation change, memory/compute growth and recovery cost.

## Failure modes

Catastrophic forgetting; stability-plasticity deadlock; replay-induced interference; overprotection preventing useful transfer; unbounded memory growth; task-boundary assumptions; preserving obsolete behavior in a changed environment.