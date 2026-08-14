# E08B — Adaptive Predictive-State Breadth

**Status: second E08 family implemented and swept; supports promotion of the breadth-allocation principle.**

## Question

Should the amount of environment state kept continuously hot be fixed, or should the system adapt state breadth to the expected future relevance of currently inactive distinctions?

E08A used static objective-switch regimes and separated hot-state rent, cold/source retention and rematerialization cost. E08B removes the fixed-policy assumption: the hidden objective-switch rate changes over time and the controller must infer whether keeping the alternate objective state hot is worth its ongoing cost.

## Environment

Two goal families each require an exact three-bit state. Only one goal is active at a time.

The stream has three hidden regimes by default:

1. low goal-switch probability (`0.01`);
2. high goal-switch probability (`0.45`);
3. low goal-switch probability (`0.02`).

The controller is **not told** those probabilities.

Keeping both goal states hot pays continuous active-state rent. Keeping only the current goal hot is cheaper, but every goal change requires reacquiring the newly relevant state.

## Policies

- **always broad** — keep both goal states hot;
- **always narrow** — keep only the current goal state hot and reacquire after every switch;
- **adaptive breadth** — estimate recent switch frequency online and expand/contract hot state around the measured break-even between extra hot-state rent and expected reacquisition cost. Hysteresis prevents rapid thrashing near the boundary.

All policies answer correctly; the discriminator is lifetime state/reacquisition cost.

## Local validation

`4/4` E08B semantic tests pass:

- narrow state wins when the goal never changes;
- broad state wins under very frequent changes;
- the adaptive controller broadens in the hidden high-switch segment and narrows again afterward;
- over the mixed regime, the adaptive policy stays at least as good as the best fixed endpoint within the test tolerance.

## 30-seed sweep

Default three-segment stream, 4,800 steps/run:

| policy | mean net utility | mean cost/step | broad fraction | reacquisitions |
|---|---:|---:|---:|---:|
| always broad | 0.988000 | 0.012000 | 1.000 | 0.0 |
| always narrow | 0.979654 | 0.020346 | 0.000 | 765.1 |
| adaptive breadth | **0.990918** | **0.009082** | 0.353 | 51.4 |

Adaptive broad fraction by hidden segment:

- low-switch segment 1: `~0.0006`;
- high-switch segment: `~0.9903`;
- low-switch segment 2: `~0.0678`.

The controller therefore changes state breadth in the correct direction without receiving the hidden regime label.

## Interpretation

Together E08A and E08B reject both fixed extremes:

- keeping only current-decision state is cheapest when future objectives are stable;
- broad hot state is worthwhile when discarded distinctions become relevant frequently enough;
- recoverable/cold state is valuable between those extremes;
- the breadth choice itself can be adapted from observed objective dynamics and resource prices.

The implementation-neutral principle is:

> **Keep information hot in proportion to its expected future decision value relative to retention and rematerialization cost; preserve recoverability for distinctions whose future relevance is plausible but not worth permanent hot-state rent.**

This does not prescribe a cache hierarchy, recurrent state, database, attention window or specific learned representation.

## Falsifier

Weaken the principle if a single fixed breadth consistently dominates adaptive breadth under changing objective frequencies after pricing estimator/control overhead, or if reliable future-relevance estimation costs more than the state optionality it saves.
