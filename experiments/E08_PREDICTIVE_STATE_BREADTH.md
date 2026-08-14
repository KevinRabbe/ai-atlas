# E08 — Predictive-State Breadth / Future Objective Optionality

**Status: first family implemented, tested and swept; DL-008 remains unresolved.**

## Question

How much currently irrelevant state should remain in the hot predictive representation when future objectives may change?

A representation can be perfectly decision-sufficient for the current objective and still destroy distinctions that become valuable later. Conversely, retaining everything in hot state can waste memory/bandwidth indefinitely.

## First family

Each episode contains a 12-bit world state and 80 repeated decisions. Objective A depends only on bits 0–2; objective B depends only on bits 6–8. Episodes begin on A and can switch back and forth between A/B.

Compared representations:

1. `broad_active` — all 12 bits remain hot/addressable;
2. `decision_sufficient` — only the three A-relevant bits are retained; B information is discarded;
3. `source_recoverable_hybrid` — only the three currently relevant bits stay hot, while the full source observation remains in cheaper cold storage and can be rematerialized when the objective changes.

The benchmark prices hot-state rent, cold/archive rent and reconstruction separately. No representation gets free storage.

## Local validation

**4/4 E08 tests pass locally**:

- narrow state wins when the objective never changes;
- source-recoverable hybrid wins at moderate switching;
- broad hot state wins when objectives alternate rapidly enough;
- hybrid preserves exact task accuracy while keeping only three active items.

## 20-seed sweep

Each row reports `accuracy / net utility`; hybrid also reports mean reconstructions per episode.

| goal-switch probability | broad active | decision-sufficient | source-recoverable hybrid |
|---:|---:|---:|---:|
| 0.00 | 1.000 / 0.976 | **1.000 / 0.994** | 1.000 / 0.990 (0.00 retrievals) |
| 0.02 | 1.000 / 0.976 | 0.826 / 0.820 | **1.000 / 0.989** (1.57) |
| 0.10 | 1.000 / 0.976 | 0.765 / 0.759 | **1.000 / 0.983** (7.89) |
| 0.20 | 1.000 / 0.976 | 0.757 / 0.751 | ~**1.000 / 0.976** (15.80) |
| 0.50 | **1.000 / 0.976** | 0.752 / 0.746 | 1.000 / 0.953 (39.56) |
| 0.80 | **1.000 / 0.976** | 0.750 / 0.744 | 1.000 / 0.931 (63.27) |

## Interpretation

There is no universal optimum:

- when future objectives are effectively fixed, aggressively decision-sufficient state is cheapest;
- when objective changes are occasional, retaining recoverable source evidence while keeping hot state narrow buys useful optionality;
- when objectives switch constantly, repeated reconstruction becomes more expensive than keeping broad state hot.

The deeper lesson is:

> **decision sufficiency is relative to an expected future objective distribution, not merely the current action.**

This connects directly to PS-004: source evidence can preserve optionality without forcing every potentially useful variable into active state.

## Why DL-008 is not promoted yet

This is only one static-state/objective-switch family. A second family should involve learned/predictive dynamics where compression discards variables that become causally relevant after an objective or regime change. Promotion should require that the same hot/cold/reconstruction frontier survives there.
