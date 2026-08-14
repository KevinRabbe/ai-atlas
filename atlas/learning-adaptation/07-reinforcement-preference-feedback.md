# Reinforcement, Preferences and Evaluator Feedback

## Required function

Improve behavior when exact target actions/outputs are unavailable but outcomes, comparisons or evaluator signals reveal which behavior is better.

## Evidence

- **L-S004 — InstructGPT:** demonstrations plus a learned preference reward and policy optimization substantially changed human-preferred behavior; a 1.3B aligned model was preferred to a much larger base GPT-3 model on the evaluated prompt distribution.
- **L-S005 — DPO:** the same broad preference-learning problem can be reformulated without the full reward-model-plus-online-RL pipeline, showing that feedback information and optimization machinery are separable.
- **L-S006 — DeepSeek-R1:** large-scale reinforcement learning with verifiable/task-derived signals produced stronger reasoning behavior; the zero-SFT variant also exposed readability/language-mixing failures, showing objective pressure can improve one dimension while damaging others.
- **L-S016 — AlphaGo Zero:** repeated self-play plus exact game outcomes allowed learning beyond human demonstrations in a fully specified environment.

## Signal quality hierarchy

Feedback differs along several axes:

- correctness/ground-truth reliability;
- density/frequency;
- delay;
- susceptibility to exploitation;
- coverage of desired behavior dimensions;
- cost to obtain;
- variance/noise;
- whether the evaluator itself shifts as the learner improves.

A formally scalar reward can hide a high-dimensional requirement. Compressing multiple objectives into one number can create trade-offs or loopholes not intended by the designer.

## Verifiable feedback

When outcomes can be checked externally—tests, formal proofs, game result, simulator constraints, exact numerical answer—the evaluator can support aggressive search/RL because feedback is cheap and comparatively objective.

Where evaluation is subjective or model-generated, optimization pressure must be lower or paired with independent checks because evaluator exploitation becomes easier.

## Clean-sheet restatement

The learner needs an **evidence-weighted update policy**: stronger, more durable changes require stronger and more independent evidence.

Potential rule:

`update magnitude/persistence ∝ expected correctness × transfer value × evidence independence ÷ interference/risk`

This is a hypothesis, not an established formula.

## Failure modes

Reward hacking; specification gaming; preference-model bias; evaluator collusion; Goodhart effects; overoptimization; loss of diversity; sacrificing unmeasured qualities; unstable policy updates.