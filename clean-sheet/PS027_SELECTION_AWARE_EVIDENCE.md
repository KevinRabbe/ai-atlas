# PS-027 — Selection-Aware Evidence Semantics

**Status:** provisional implementation-neutral selection.

**Promotion evidence:** I28D sparse/delayed relation learning + I29 selective self-change auditing.

## Selected principle

When the system's own acquisition, audit, experiment, verification or deployment policy affects **which outcomes become observable**, the resulting evidence must retain enough selection/acquisition semantics that downstream learning does not silently treat the observed sample as supporting a population, stratum, dependence relation, calibration target or causal claim it does not identify.

In compact form:

```text
observed evidence
    =
world/source process
    +
acquisition/selection process
```

The second term cannot be discarded when it changes the distribution of what is observed.

## What is selected

- evidence acquisition can alter evidence semantics, not only evidence quantity;
- targeted/selective observations are not automatically representative of unobserved cases;
- the acquisition process is part of provenance when it materially affects interpretation;
- corrective coverage, explicit selection modeling, controlled intervention, alternative evidence channels or explicit unresolved state are all valid candidate responses;
- corrective acquisition is itself resource-priced and should stop when its expected downstream value no longer exceeds cost.

## What is NOT selected

- random sampling as a universal requirement;
- a fixed exploration/coverage percentage;
- inverse-propensity weighting;
- importance sampling;
- a particular causal-inference estimator;
- a particular audit schedule;
- mandatory persistence of every acquisition decision.

Those are implementations/estimators to compare when their assumptions fit the active problem.

## I28D — relation learning under sparse/delayed truth

The A/B dependence relation changes while source identities remain fixed. Passive truth is sparse and delayed.

Querying truth mainly when `A != B` obtains far more resolved outcomes and detects the hidden shift quickly, but worsens lifetime relation learning because the estimator treats a disagreement-selected sample as though it represented the full joint A/B error process.

Output-independent coverage avoids the worst bias. Direct relation/provenance evidence is even cheaper at the default price because it targets the uncertainty directly, but loses when provenance evidence becomes sufficiently expensive.

## I29 — self-change evaluator calibration

A cheap evaluator flags risky self-changes. Auditing mostly flagged candidates and treating the audited evaluator-error fraction as a global population error drives the estimate toward ~64%, while the actual population error is ~15.5%.

A representative random audit estimates the global scalar correctly, but the downstream decision actually needs conditional risks:

```text
P(harm | safe-looking)
P(harm | flagged)
```

A conditional learner with heavy flagged auditing plus a small safe-path coverage sample learns both risks and outperforms the unaudited visible policy at the default audit price.

When audit cost becomes high enough, the extra coverage stops paying.

## Relation to existing principles

- **PS-007** decides whether additional evidence is worth acquiring. PS-027 says the acquisition decision can change the statistical meaning of the resulting evidence.
- **PS-013** values independent failure modes. PS-027 prevents selective observation from corrupting the learned estimate of those failure modes.
- **PS-014** prices assurance. PS-027 constrains how assurance outcomes may be generalized after selective checking.
- **PS-026** models evidence dependence/derivation as uncertain relational state. PS-027 says the dataset used to learn those relations must preserve the semantics of how it was selected.

## Minimal runtime consequence

`EvidenceAcquisitionRegistry` is the current model-free semantic substrate. It records acquisition identity/mode and optional selection probability/scope separately from evidence payload, truth, source lineage and authority.

It deliberately does not decide whether evidence is representative or prescribe a correction method.

## Falsifier / next discriminator

PS-027 should be weakened or removed if selection-blind learning matches selection-aware learning across structurally different adaptive-acquisition regimes after equal acquisition/modeling cost, or if preserving/modeling acquisition semantics systematically costs more lifetime value than the calibration/assurance errors it prevents.

Next useful stress: compose selection-aware evidence into discovery/frontier verification, where only promising hypotheses are normally tested and promotion pressure can strongly distort which failures become observable.
