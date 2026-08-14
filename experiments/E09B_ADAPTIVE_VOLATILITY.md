# E09B — Adaptive Consolidation Under Hidden Volatility

**Status:** promotion-quality E09 follow-up; preliminary multi-seed evidence only.

## Question

Can a system adjust how much evidence it requires before changing durable state when environmental volatility changes, without being told the hidden volatility regime?

## Environment

The stream alternates four hidden regimes:

1. 1,800 steps with switch probability 0.0005;
2. 700 steps with switch probability 0.10;
3. 1,800 steps with switch probability 0.001;
4. 700 steps with switch probability 0.07.

Observation reliability is 0.94 throughout. Policies observe only the noisy binary observations, not segment IDs, switch probabilities or true state.

## Adaptive policy

`adaptive_volatility_threshold` estimates recent state volatility from transitions between short **confirmed observation runs**. This avoids treating every one-step noisy flip as a regime change. A sliding event-rate estimate controls the evidence threshold:

- low estimated volatility → high consolidation threshold;
- high estimated volatility → low threshold.

This is still a hand-designed adaptation rule. The experiment tests whether adapting the *timescale* is useful before attempting to learn the rule itself.

## 30-seed means

| policy | accuracy | durable updates | false durable updates | avg switch delay |
|---|---:|---:|---:|---:|
| fixed threshold 1.8 | 0.9674 | 136.2 | 18.1 | 1.00 |
| fixed threshold 2.4 | 0.9561 | 92.0 | 2.53 | 1.75 |
| fixed threshold 3.4 | 0.9421 | 75.2 | 0.73 | 2.41 |
| fixed threshold 4.4 | 0.9286 | 64.6 | 0.53 | 2.99 |
| adaptive volatility threshold | **0.9678** | 105.7 | **4.23** | **1.24** |

The adaptive policy reaches roughly the aggressive fixed policy's accuracy while producing about 76% fewer false durable updates. Relative to the conservative 3.4 threshold, it adapts about twice as fast while retaining much higher accuracy.

## Learned threshold behavior

Average adaptive thresholds by hidden segment:

| segment | hidden switch probability | mean threshold |
|---:|---:|---:|
| 0 | 0.0005 | 3.92 |
| 1 | 0.10 | 1.97 |
| 2 | 0.001 | 3.84 |
| 3 | 0.07 | 2.13 |

The policy never reads the hidden probability. The separation arises from its observation-history proxy.

## Interpretation

This provides direct experimental support for the Phase-2/biology hypothesis that **persistence timescale should respond to environmental stability rather than be one global constant**.

It does not yet prove a particular consolidation algorithm. The volatility proxy, threshold mapping and environment structure are hand-designed. The next discriminator is whether a learned/meta-adapted policy can discover the trade-off and remain calibrated when observation noise changes independently of true volatility.

## Design-ledger implication

DL-009 should remain unresolved at the mechanism level, but confidence in **multiple/adaptive persistence timescales** can be increased. The falsifier now shifts from “does staging ever help?” toward “does adaptive timescale control generalize when volatility and observation reliability vary independently?”
