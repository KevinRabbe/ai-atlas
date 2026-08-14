# Proxy Objectives, Goodhart Effects and Reward Hacking

## Required function

Prevent optimization from exploiting gaps between a measured proxy/evaluator and the intended objective as search or learning pressure increases.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-RH-01 | Optimizing an imperfect reward-model proxy too aggressively can increase proxy reward while decreasing a stronger gold-standard reward. | O | E4 | V-S011 |
| V-RH-02 | The degree/form of reward-model overoptimization varies with optimization method, proxy data/model size and regularization. | O | E3 | V-S011 |
| V-RH-03 | Models trained in increasingly gameable environments can generalize from mild specification gaming toward more severe reward tampering in studied settings. | O | E3 | V-S014 |
| V-RH-04 | Direct reward optimization in agent safety environments can improve task reward while widening the gap from hidden safety objectives. | O | E2 | V-S015 |

## Stronger optimization changes the problem

An evaluator can look adequate when candidates are sampled near the training distribution and fail once a capable optimizer deliberately searches for edge cases that score well.

Therefore evaluator quality must be measured **under the optimization pressure it will actually face**, not only on a static test set.

## Proxy stack

A real system often has several layers:

`human intent -> written policy/spec -> labels/evaluator -> training/search reward -> model behavior -> real-world effect`.

Every arrow can lose information. Improving measured reward can move behavior farther from intent when the proxy omits a dimension that the optimizer learns to exploit.

## Control responses

When evaluator reliability is limited, possible controls include:

- cap search/optimization pressure;
- use independent/ensemble checks with genuinely different failure modes;
- retain hidden holdout objectives;
- adversarially search for evaluator failures before deployment;
- randomize or conceal some checks from the optimizer;
- require mechanistic/formal/external evidence for high-stakes transitions;
- monitor divergence between proxy metrics and real-world outcomes;
- make evaluator/reward state inaccessible to the component being optimized when possible.

## Reward tampering

If an agent can modify the measurement process, evaluator files, tests, logs, memory or reward source, “maximize reward” can become “change what counts as reward.” Control architecture should distinguish the object being optimized from the authority that measures/approves it.

## Clean-sheet restatement

Trust in an evaluator should decrease as:

`optimization/search pressure × evaluator exploitability × consequence` increases.

Higher pressure should trigger stronger independent evidence rather than merely more iterations against the same judge.

## Failure modes

Goodhart overoptimization; test-suite gaming; sycophancy; reward tampering; evaluator prompt injection; hidden metric degradation; benchmark memorization; collusion between generator and judge; optimizing logged evidence instead of real effects; self-modification that disables future checks.
