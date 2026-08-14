# I05 — Learned Transition Metacognition

**Status:** implemented and tested. Composition checkpoint; **not a new provisional principle**.

## Question

Can the I04 shared typed transition/resource kernel retain its value when several quantities that were previously supplied cleanly become **revisable learned state**?

I05 removes oracle access for the deployed/learned variants to:

- operation success/reliability;
- marginal value of buying extra work/coordination;
- family-specific coupling benefit;
- visible-evaluator correctness after approval;
- secondary-verifier true/false approval rates.

The environment keeps categorical capability authority exact and external. That boundary is intentionally **not** learned from behavioral success.

## Environment

A 600-batch lifetime contains `think`, `observe`, `coupled`, `external`, and `research` tasks. At batch 300, hidden operation economics change:

- which task family benefits from extra computation/coordination reverses;
- contextual external-action reliability changes;
- visible-evaluator false-approval patterns swap between research families;
- secondary-verifier failure rates also change.

The learned policy sees task type/family, value/consequence, explicit categorical authority, prior outcomes, verifier decisions, and delayed post-decision audit outcomes. It does **not** see the hidden reliabilities or regime label.

All policies use the same four shared transition slots per batch and one verification sub-capacity.

## Variants

1. `oracle_typed_upper_bound` — reads the hidden reliability/evaluator parameters; upper bound only.
2. `learned_conditional_typed` — online decayed family-conditional estimates with mild exploration.
3. `learned_global_typed` — learns, but pools task families into one estimate.
4. `frozen_conditional_typed` — learns before the shift and then freezes its estimates.

All four preserve the same exact typed authority boundary.

## 30-seed result

| variant | net utility/task | pre-shift | first 60 post-shift | last 100 post-shift | false durable writes/run |
|---|---:|---:|---:|---:|---:|
| oracle typed upper bound | **0.7597** | 0.7394 | 0.7683 | **0.7902** | 2.87 |
| **learned conditional typed** | **0.6818** | **0.7052** | 0.5170 | **0.7400** | **2.93** |
| learned global typed | 0.6257 | 0.6395 | 0.5963 | 0.6222 | 3.27 |
| frozen conditional typed | 0.5859 | **0.7052** | 0.4535 | 0.4851 | 3.47 |

The regime change causes a real transient failure in the learned controller rather than being hidden by oracle metadata. The conditional learner then recovers from ~`0.517` immediately after the shift to ~`0.740` in the final 100 batches. Frozen estimates do not recover.

## Learned coupling reversal

The `coupled` task family changes which sub-family benefits from coordinated/extra work.

Mean work-allocation rate per total task:

| phase | family 0 | family 1 |
|---|---:|---:|
| before shift | 0.0034 | **0.0432** |
| after shift | **0.0353** | 0.0134 |

The oracle rates are approximately `0.0002 / 0.0439` before and `0.0517 / 0.0004` after. The learned controller therefore discovers the direction change from outcomes rather than receiving the coupling label.

Global pooling cannot express this conditional reversal cleanly and stays near equal allocation across families.

## Authority result

All typed variants record **zero categorical authority violations**. Unauthorized external-effect proposals are blocked independently of the learned utility/reliability estimate.

This is important: I05 learns **whether authorized work is likely to help**, but does not learn whether it is authorized in the first place.

## Interpretation

I05 strengthens the I04 compression hypothesis:

`typed transition proposal -> learned marginal-value/resource estimate -> shared allocator -> independent authority/failure-layer gate -> execute -> outcome -> revise estimator`

Several apparent controllers can share a learned allocation substrate, but their metadata should be treated as uncertain/revisable rather than hard-coded constants.

The result also reproduces PS-009 inside the kernel: family-conditional estimates outperform one globally shared estimate because transfer changes into interference when the hidden economics differ by family.

## Limitation / next falsifier

The synthetic research environment provides an exact **delayed audit outcome after the decision**, allowing verifier-quality estimates to be learned cleanly. This is not equivalent to realistic scientific/self-change settings where feedback may be delayed, censored, noisy, or never fully resolved.

Next I05-level discriminator:

- partial/noisy delayed outcomes;
- nonstationary feedback delay;
- estimator uncertainty affecting its own evidence-acquisition decision;
- learned coupling across more than two families;
- explicit cost of maintaining conditional metacognitive state.

No new architecture principle is promoted from I05 alone.
