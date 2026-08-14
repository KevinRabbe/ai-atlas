# E02C — Compute-Matched Conditional Sharing

**Status: implemented, tested and swept.**

## Purpose

E02/E02B showed a transfer–interference frontier, but the most interesting partially shared E02B learner used more realized arithmetic than isolated specialists. E02C removes that confound.

## Candidate

`RoutedSharedPrivate` has exactly the same total learned parameter count as the specialist baseline: **45 parameters** in the default three-task, 15-feature setup.

Each example activates **one path only**:

- shared path: 15 parameters;
- task-private path: 10 parameters.

A tiny per-task online loss estimate routes training/inference toward the currently better path, with limited exploration during training. Shared and private paths are never summed on one example, so realized train/test arithmetic stays at or below the specialist baseline.

This is not proposed as the final routing algorithm. It is a discriminator for whether the value of conditional sharing survives equal stored capacity and realized compute accounting.

## Validation

**4/4 E02C tests pass locally**:

- exact parameter-count match;
- training compute no greater than specialists;
- test compute no greater than specialists;
- both shared and private routes remain reachable across task-relatedness regimes.

## 20-seed sweep

### 240 training examples

| sharedness | specialists accuracy | routed accuracy | routed train ops/example | routed test ops/example | shared route rate |
|---:|---:|---:|---:|---:|---:|
| 0.98 | 0.867 | **0.896** | 63.1 | 27.0 | 0.522 |
| 0.75 | **0.864** | 0.852 | 61.9 | 26.2 | 0.476 |
| 0.15 | **0.863** | 0.786 | 62.0 | 23.3 | 0.479 |

### 480 training examples

| sharedness | specialists accuracy | routed accuracy | routed train ops/example | routed test ops/example | shared route rate |
|---:|---:|---:|---:|---:|---:|
| 0.98 | 0.913 | **0.930** | 64.1 | 27.3 | 0.565 |
| 0.75 | **0.925** | 0.882 | 62.2 | 26.2 | 0.489 |
| 0.15 | **0.920** | 0.834 | 61.5 | 22.7 | 0.459 |

### 1,200 training examples

| sharedness | specialists accuracy | routed accuracy | routed train ops/example | routed test ops/example | shared route rate |
|---:|---:|---:|---:|---:|---:|
| 0.98 | 0.962 | **0.973** | 66.8 | 28.8 | 0.673 |
| 0.75 | **0.974** | 0.909 | 65.3 | 27.3 | 0.610 |
| 0.15 | **0.966** | 0.869 | 61.5 | 22.8 | 0.462 |

The specialist baseline uses **75 train operations/example** and **30 test operations/example** in every regime.

## Interpretation

The earlier result survives compute matching:

- highly reusable structure makes shared computation valuable even when active compute is not increased;
- divergent task structure makes isolation better;
- there is no evidence for a universal all-shared or all-isolated architecture.

The current router is imperfect: at low relatedness it still sends substantial training traffic through the shared path, which likely contributes to its accuracy gap. That is a useful failure, not a reason to hide the result.

## Design implication

The narrow principle supported across E02/E02B/E02C is:

> **sharing should be conditional on demonstrated reusable structure and should preserve an isolation path when transfer turns into interference.**

The remaining open problem is how a future system should estimate reusable structure and move the sharing boundary online without paying more metacontrol than it saves.
