# E20 — Self-Change Regression Evidence Exposure

**Status:** implemented, tested and swept. Strong first-family evidence; DL-020 remains open pending a second structurally different family.

## Question

How should a self-improving system evaluate candidate changes when repeated optimizer exposure can turn a regression suite into an optimization target rather than independent evidence?

## Environment

The system repeatedly chooses among 30 candidate changes for 300 rounds. Candidates are selected using a fixed visible suite covering eight scenarios.

Each candidate contains:

- a general effect that may transfer;
- an explicit visible-suite boost created by selection pressure;
- a small tradeoff outside the visible suite;
- after round 150, a new side-effect channel affecting a previously unseen scenario family.

The active environment distribution shifts halfway through the lifetime from scenarios 0–19 to scenarios 20–39.

The visible optimizer does not directly observe true active-distribution performance.

## Regression policies

### `visible_only`

Accept the candidate when it improves the visible suite.

### `fixed_hidden`

Require visible improvement plus positive performance on one fixed eight-scenario hidden suite drawn from the original regime.

### `rotating_hidden`

Require visible improvement plus positive performance on a newly sampled hidden subset from the **current** active scenario distribution.

### `adversarial_rotating`

Evaluate the candidate on the current active scenarios where that candidate's effect is worst. This is intentionally expensive/conservative and approximates targeted regression hunting rather than ordinary random holdout evaluation.

## 30-seed results

| policy | pre-shift true score | post-shift true score | harmful accepted | good rejected | lifetime utility |
|---|---:|---:|---:|---:|---:|
| visible only | 0.9984 | **0.0341** | 98.73 | **0.0** | 0.6138 |
| fixed hidden | 0.9993 | **0.0778** | 85.93 | 13.3 | 0.6521 |
| **rotating hidden** | 0.9994 | **0.9972** | **3.3** | 14.9 | **0.9729** |
| adversarial rotating | 0.9996 | **0.9996** | **0.0** | 47.1 | 0.9706 |

All policies look strong before the environment shift. The failure only becomes visible after the candidate side effects move outside the coverage of the fixed suites.

## Interpretation

### Visible tests are not independent evidence

The optimizer selects candidates precisely because they look good on the visible suite. A high visible score therefore becomes less trustworthy as optimizer/search pressure rises.

### A fixed hidden suite can become functionally visible/stale

Even without directly revealing its contents, a fixed holdout only protects the slice of state space it covers. When the active distribution changes, "hidden" does not mean "representative."

### Rotation protects evidence coverage

Rotating hidden evidence tracks the current distribution and reduces harmful accepted changes by more than an order of magnitude relative to the fixed hidden suite while preserving useful changes.

### Maximum adversarial pressure has a cost

Adversarial rotation eliminates harmful accepted candidates in this synthetic family, but rejects roughly three times as many truly useful candidates as ordinary rotation. Stronger regression pressure is therefore not free.

## Clean-sheet inference

The evidence supports a stronger form of the existing self-change guardrail:

> **Regression evidence used to authorize self-change should remain sufficiently independent from the proposal/optimization path and refresh coverage as the system, environment and failure surface change.**

This does not imply that all tests must remain permanently secret. It distinguishes several roles:

- visible tests can provide fast learning/debug signals;
- independent hidden evidence can gate durable promotion;
- rotating coverage protects against stale blind spots;
- targeted/adversarial checks are valuable when their extra conservatism is justified by consequence.

## Relation to PS-013 / PS-014 / PS-016

- PS-013: independence is about failure modes, not evaluator count;
- PS-014: hidden/adversarial regression effort is a priced assurance resource;
- PS-016: the hidden suite still needs coverage of the actual failure layers that can invalidate the change.

E20 adds a new dimension: **test exposure and coverage drift over repeated optimization rounds**.

## Why DL-020 remains open

This is one synthetic self-change family. The next discriminator should be structurally different, for example:

- local code/config repairs with hidden interaction regressions;
- architecture/runtime changes where failures appear only after long-horizon state accumulation;
- self-modification of the evaluator or harness itself;
- candidate changes that trade performance, safety and resource efficiency rather than one scalar capability score.

## Current conclusion

Visible regression evidence is useful for optimization but insufficient as the sole promotion gate. Fixed hidden evidence is stronger but can become stale. Rotating/refreshing independent evidence is the current leading mechanism, with targeted adversarial checks allocated when their extra rejection cost is justified.
