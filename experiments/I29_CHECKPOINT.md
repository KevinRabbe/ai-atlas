# I29 / PS-027 Checkpoint

**Current Phase-10 validation count:** 514 added tests.

**Current provisional principle count:** 27 (`PS-001` through `PS-027`).

## Delta from the 500-test I28 checkpoint

- I29 selective self-change auditing: 8 tests;
- reusable `EvidenceAcquisitionRegistry`: 6 tests.

Total: `500 + 8 + 6 = 514`.

## New promotion

**PS-027 — selection-aware evidence semantics.**

When system policy affects which outcomes become observable, downstream learning must preserve/account for that acquisition process rather than treating the selected sample as automatically representative of a broader estimand.

Promotion evidence:

1. **I28D — sparse/delayed relation learning.** Disagreement-triggered truth acquisition biases the joint A/B relation learner even while obtaining more labels and detecting a hidden relation shift quickly.
2. **I29 — self-change evaluator calibration.** Flagged-only auditing makes a selected evaluator-error sample look like population error and leaves the unobserved safe-looking stratum uncalibrated.

The two families use different hidden variables, decisions and downstream objectives.

## I29 30-seed checkpoint

Approximate means:

| policy | net utility | harmful promotions | safe promotions | audits |
|---|---:|---:|---:|---:|
| visible only | ~0.161 | ~0.0201 | ~0.764 | 0 |
| flagged-selected scalar | ~-0.026 | ~0.0001 | ~0.001 | ~0.130 |
| random-coverage scalar | ~-0.008 | ~0.0217 | ~0.252 | ~0.040 |
| flagged-only conditional | ~0.123 | ~0.0051 | ~0.190 | ~0.130 |
| **selection-aware conditional** | **~0.214** | **~0.0105** | **~0.394** | ~0.161 |
| oracle conditional | ~0.292 | ~0.0151 | ~0.573 | 0 |

True conditional risks are approximately `P(harm|safe)=0.0255` and `P(harm|flagged)=0.3721`. The selection-aware learner converges near ~0.027 and ~0.371 respectively; flagged-only conditional auditing leaves the safe-path estimate at its stale 0.08 prior.

At sufficiently high audit price, the visible-only policy overtakes selection-aware auditing. The selected object is therefore evidence/acquisition semantics, not permanent coverage.

## Runtime delta

`EvidenceAcquisitionRegistry` records:

- evidence identity;
- acquisition identity;
- passive/randomized/targeted/interventional/unknown acquisition mode;
- optional known inclusion probability;
- optional selection scope.

It does not assign truth, independence or representativeness. It exists so those semantics are available to the estimator that actually needs them.

## Current evidence-plane decomposition

```text
source identity
    !=
source quality
    !=
common-mode dependence
    !=
directional derivation
    !=
versioned/path provenance
    !=
acquisition / selection process
    !=
claim aggregation
    !=
assurance authority
```

## Next integration target

Apply PS-027 to **frontier/discovery verification**. A discovery system naturally tests/promotes promising candidates selectively; the next stress should determine whether selective verification can make the generator/evaluator look better than it really is, hide whole failure classes, or distort the estimated value of future exploration.
