# Safety, Control & Reliability

## Required function

Keep system behavior within intended constraints under uncertainty, distribution shift, tool use, long horizons, self-improvement and increasing capability.

## Mechanism families to map

Preference/constitutional training; uncertainty calibration; capability and permission boundaries; sandboxing; reversible actions; human approval gates; monitoring; anomaly detection; interpretability; provenance; policy enforcement; adversarial robustness; scalable oversight; corrigibility; shutdown/rollback; audit logs; containment.

## Early evidence anchors

RLHF and constitutional/RLAIF approaches demonstrate that learned behavior can be steered by human or AI-generated preference signals, but neither makes the underlying optimization problem disappear. Calibration work shows models can expose useful confidence information in some settings while generalization of calibration remains imperfect. Agentic systems add a separate control surface: permissions, execution environments and irreversible side effects can often be constrained outside model weights.

## Clean-sheet questions

- Which safety invariants must live outside self-modifiable components?
- What actions must remain reversible or require external authorization?
- How should uncertainty alter permission to act?
- How can self-improvement be rolled back atomically?
- How do we detect evaluator manipulation or deceptive optimization?
- Which internal representations need observability for reliable control without requiring every thought to be human-readable?
