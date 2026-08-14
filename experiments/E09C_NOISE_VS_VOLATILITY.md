# E09C — Sensor Noise vs True Environmental Volatility

**Status: implemented, tested and swept.**

## Purpose

E09/E09B support adaptive persistence timescales, but the original volatility estimator could confuse frequent observation flips with genuine world changes.

E09C tests the identifiability problem directly:

> does the world keep changing, or is the observation channel unreliable?

With one observation channel these causes can produce similar local evidence. A second independent sensor can supply discriminating information, but reading it continuously has a cost.

## Policies

- `single_sensor_adaptive` — estimates volatility from one channel;
- `always_corroborate` — reads two independent sensors every step and only treats agreement as usable evidence;
- `adaptive_corroboration` — samples the second sensor every tenth step while disagreement is low, estimates sensor ambiguity, and switches to full corroboration only when disagreement crosses a threshold.

The current mechanism is deliberately simple and hand-designed. The experiment tests whether selective independent evidence can separate noise from change economically.

## Validation

**4/4 E09C tests pass locally**:

- adaptive corroboration reduces false durable updates in a stable noisy world;
- it beats single-channel net utility in that regime;
- it keeps secondary sensing sparse in clean volatile and clean stable regimes;
- always-on corroboration pays unnecessary cost when the primary channel is already reliable.

## 30-seed sweep

Each cell reports `accuracy / false durable updates / average true-switch delay / secondary read rate / net utility`.

| regime | single sensor | always corroborate | adaptive corroboration |
|---|---|---|---|
| stable + noisy (`p_switch=.001`, reliability=.78) | 0.901 / 198.5 / 1.78 / 0.000 / 0.901 | **0.993 / 0.33 / 7.20 / 1.000 / 0.987** | **0.988 / 9.53 / 6.93 / 0.939 / 0.983** |
| volatile + clean (`.08`, `.96`) | **0.909 / 8.77 / 1.10 / 0.000 / 0.909** | 0.902 / 0.20 / 1.22 / 1.000 / 0.896 | **0.908 / 7.57 / 1.11 / 0.106 / 0.908** |
| stable + clean (`.001`, `.98`) | **0.997 / 0.00 / 3.30 / 0.000 / 0.997** | 0.997 / 0.00 / 3.36 / 1.000 / 0.991 | **0.997 / 0.00 / 3.30 / 0.100 / 0.996** |

## Interpretation

The experiment strengthens PS-002 but also exposes its boundary condition:

> persistence timescale cannot always be inferred from one stream of apparent state changes, because observation noise and true volatility can be observationally confounded.

Independent evidence can resolve that ambiguity, but PS-007 applies to the evidence channel itself. Corroboration should be purchased when disagreement/uncertainty makes it valuable, not made permanently mandatory.

The result therefore couples three existing principles:

- PS-002 — stage/consolidate according to estimated stability;
- PS-006 — keep alternative explanations (`world changed` vs `sensor unreliable`) alive when consequence warrants it;
- PS-007 — acquire independent evidence when its expected value exceeds cost.

## Remaining limits

- sensor errors are conditionally independent;
- only two binary sensors;
- thresholds are hand-written;
- the secondary sensor's price is fixed;
- no adversarial or correlated sensor failure.

A later integrated organism should learn when to request corroboration and should explicitly represent correlated failure rather than assuming another sensor is independent truth.
