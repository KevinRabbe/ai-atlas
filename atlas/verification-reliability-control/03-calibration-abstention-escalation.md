# Calibration, Abstention and Escalation

## Required function

Estimate when the system is likely to be wrong or outside its evidence base and convert that uncertainty into safer behavior: abstain, verify, acquire information, downgrade privilege or escalate.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-CA-01 | Modern neural classifiers can be substantially miscalibrated; post-hoc temperature scaling improved calibration in studied settings. | O | E4 | V-S008 |
| V-CA-02 | Selective classification can trade coverage for lower risk by rejecting uncertain predictions. | O | E4 | V-S009 |
| V-CA-03 | Low-confidence multimodal systems can use additional evidence acquisition to recover answers rather than only abstaining permanently. | O | E2 | V-S010 |
| V-CA-04 | Calibration quality can change under architecture, training and distribution shift; confidence is not intrinsically a probability of correctness. | I | E4 | V-S008, Foundations uncertainty evidence |

## Confidence is useful only behaviorally

A confidence variable matters when it predicts failure and changes what the system does. Required external tests include:

- calibration curves/proper scoring;
- selective risk at different coverage;
- performance after distribution shift;
- whether high uncertainty triggers useful verification or observation;
- whether high confidence is actually sufficient for the action's consequence level.

## Abstention is one operation

The controller can respond to uncertainty with:

`answer / answer with caveat / verify / retrieve / query sensor/tool / ask user / run alternative model / simulate / reduce action scope / require authorization / abstain`.

Permanent abstention wastes capability when uncertainty can be cheaply reduced. Acting anyway is unsafe when evidence acquisition is cheap and consequences are high.

## Risk-sensitive thresholds

A single global confidence threshold is structurally weak. Evidence requirements should depend on:

- reversibility;
- action privilege;
- expected harm/cost;
- novelty/distribution shift;
- availability of independent verification;
- time pressure;
- whether the action mutates durable state.

This connects directly to Phase-2 durability thresholds and Phase-4 reality checks.

## Calibration is local to a regime

A system calibrated on ordinary queries may not remain calibrated on adversarial prompts, rare tool failures, long recursive trajectories or new domains. Trust estimates therefore need scope/provenance just like memories.

## Failure modes

Confidently wrong OOD behavior; uncertainty estimate trained on the same flawed target; global threshold ignoring consequence; excessive abstention; false certainty after consensus among correlated agents; confidence discarded during memory/summarization; escalation loops; uncertainty used as a cosmetic disclaimer rather than an action signal.
