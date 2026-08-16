# I29 — Selection-Aware Self-Change Auditing

**Status:** implemented model-free discriminator; 8 semantic tests.

**Promotion role:** second structurally different family for the acquisition-selection effect first exposed by I28D.

## Question

If the organism chooses which self-change outcomes receive expensive independent audit, can it later treat the audited outcomes as though they were an unbiased description of evaluator quality?

I29 deliberately separates:

- the hidden quality of a proposed self-change;
- a cheap evaluator's visible `flagged / safe-looking` output;
- the audit policy that decides which outcomes become known;
- the statistical quantity learned from those audits;
- the later promotion decision that consumes that estimate.

Audits happen **after** the current promotion decision, so they improve future calibration rather than rescuing the current candidate.

## Environment

- 10% of proposed self-changes are harmful;
- the cheap evaluator detects 80% of harmful changes;
- it falsely flags 15% of safe changes;
- promoting a safe change yields +1;
- harmful promotion costs `8 × consequence`;
- consequence varies across 1×, 2×, 4× and 8×.

The true evaluator population error is therefore about 15.5%, but this scalar is not enough to make consequence-sensitive promotion decisions. The actual conditional risks are approximately:

```text
P(harmful | evaluator says safe)    ≈ 2.55%
P(harmful | evaluator flags change) ≈ 37.21%
```

## Policies

- `visible_only` — trust the cheap evaluator's binary output;
- `flagged_selected_scalar` — audit mostly flagged changes and treat their observed evaluator error as a global error rate;
- `random_coverage_scalar` — estimate that global error from a representative random audit sample;
- `flagged_only_conditional` — learn `P(harm | flagged)` but receive no coverage of the safe-looking path;
- `selection_aware_conditional` — heavily audit flagged changes while maintaining a small safe-path coverage sample and learn the two conditional risks separately;
- `oracle_conditional` — knows the true conditional risks, not each candidate's hidden truth.

World and audit RNGs are separate so all policies see the same hidden candidate stream for a given seed.

## 30-seed means

| policy | net utility/candidate | harmful promotions | safe promotions | audits | final global error estimate | safe-path harm estimate | flagged-path harm estimate |
|---|---:|---:|---:|---:|---:|---:|---:|
| visible only | ~0.161 | ~0.0201 | ~0.764 | 0 | 0.150 prior | 0.080 prior | 0.300 prior |
| flagged-selected scalar | ~-0.026 | ~0.0001 | ~0.001 | ~0.130 | **~0.637** | 0.080 | ~0.364 |
| random-coverage scalar | ~-0.008 | ~0.0217 | ~0.252 | ~0.040 | **~0.152** | ~0.027 | ~0.348 |
| flagged-only conditional | ~0.123 | ~0.0051 | ~0.190 | ~0.130 | ~0.637 | **0.080 stale prior** | ~0.364 |
| **selection-aware conditional** | **~0.214** | **~0.0105** | **~0.394** | ~0.161 | selected/global value not meaningful | **~0.027** | **~0.371** |
| oracle conditional | ~0.292 | ~0.0151 | ~0.573 | 0 | — | ~0.0255 | ~0.3721 |

## Result 1 — selected audits do not estimate population evaluator error

Among flagged candidates, a large fraction are actually safe false positives. Auditing that stratum heavily and treating its error fraction as the evaluator's population error drives the estimate toward ~64%, despite the actual population error being ~15.5%.

The resulting policy nearly stops self-improvement entirely.

A small random coverage audit estimates the global population error correctly. This isolates the **selection-bias effect** independently of the later question of whether a single scalar is sufficient.

## Result 2 — correct population calibration can still be the wrong estimand

`random_coverage_scalar` recovers the global error rate, but the promotion problem needs different risks after different evaluator outputs. One scalar cannot distinguish false-negative risk on apparently safe changes from false-positive risk on flagged changes.

Thus:

```text
representative evidence
    !=
necessarily sufficient evidence
```

The estimator must target the uncertainty actually used by the downstream decision.

## Result 3 — selective conditional learning needs coverage of every consequential stratum

`flagged_only_conditional` learns the flagged path but cannot update the safe-looking path, leaving `P(harm | safe)` at its 8% prior instead of the true ~2.55%.

The selection-aware policy preserves heavy audit effort on the suspicious path while maintaining only a 4% audit probability on safe-looking candidates. This is enough to move the safe estimate to ~2.7% and the flagged estimate to ~37.1%.

That improves utility over the unaudited visible policy while roughly halving harmful promotions.

## Result 4 — coverage is a resource, not a ritual

The default audit cost is 0.20. At that price selection-aware calibration pays.

As audit price rises, its advantage disappears. Around cost 1.0 in the current family, the unaudited visible policy again has higher net utility.

So the result is not `always random-audit some percentage`. It is:

> preserve enough knowledge of the acquisition/selection process to know what the observed sample can support, and buy corrective coverage only while its downstream value exceeds its cost.

## Cross-family synthesis with I28D

I28D learned an A/B dependence relation from selectively resolved source outcomes. Querying truth mainly on `A != B` biased the joint-error sample and worsened relation learning.

I29 learns self-change evaluator calibration from selectively audited candidate outcomes. Auditing mainly `flagged` candidates makes that selected stratum look like the full evaluator population and corrupts calibration.

The hidden variables, tasks and downstream decisions are different. The shared mechanism is:

```text
policy chooses what becomes observable
        ↓
observed sample distribution changes
        ↓
learner ignores selection mechanism
        ↓
learned belief answers a different question
        ↓
downstream decision is systematically miscalibrated
```

This is sufficient evidence for a narrow implementation-neutral promotion: acquired evidence carries **selection semantics** when the acquisition rule changes what is observable.
