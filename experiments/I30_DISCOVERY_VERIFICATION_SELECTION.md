# I30 — Selection-Aware Discovery Verification

**Status:** implemented model-free composition stress; 8 semantic tests.

**Selection status:** strengthens PS-007/008/014/027. No PS-028.

## Question

A discovery system naturally verifies promising candidates selectively. Can outcomes from that selected subset be generalized to the rest of the rejected hypothesis space?

I30 makes that error explicit.

## Environment

Candidates belong to two domains:

- `ordinary`: higher prior truth rate, value 2;
- `frontier`: lower prior truth rate, value 8.

A visible score is informative but imperfect. Candidates above 0.65 always receive independent verification before they can become discoveries. Rejected candidates may optionally receive an additional independent check costing 1.20.

True and false candidates have different score distributions, so the region just below the visible pass threshold is substantially richer in real discoveries than the deep-reject region.

## Policies

- `pass_only` — independently verify only visible passes;
- `near_threshold_global` — sample near-threshold rejects, estimate one rejected-candidate truth rate per domain, then generalize it to all rejects in that domain;
- `random_domain` — representative random reject coverage, still one scalar per domain;
- `selection_aware_bin` — maintain domain + score-stratum estimates and preserve random coverage;
- `oracle_score` — knows the generative posterior `P(true | domain, score)`.

World and acquisition RNGs are separate.

## 30-seed means

| policy | net utility/candidate | discoveries | recovered discoveries | missed discoveries | rejected verification rate |
|---|---:|---:|---:|---:|---:|
| pass only | ~0.377 | ~0.178 | 0 | ~0.128 | 0 |
| near-threshold global | ~0.421 | ~0.237 | ~0.059 | ~0.069 | ~0.266 |
| random-domain scalar | ~0.381 | ~0.200 | ~0.023 | ~0.105 | ~0.132 |
| **selection-aware score bins** | **~0.461** | **~0.214** | **~0.036** | **~0.092** | **~0.155** |
| oracle score | ~0.524 | ~0.242 | ~0.065 | ~0.063 | ~0.177 |

## Selection distortion

For ordinary rejected candidates, a representative rejected sample is only about 15% true in this family.

The near-threshold selected sample is about 48–49% true.

`near_threshold_global` therefore learns an ordinary rejected-candidate truth estimate around ~0.48 and generalizes it to deep rejects. At the default verification price, this triggers excessive rejected-candidate checks.

`random_domain` removes that bias and estimates the domain-wide reject rate around ~0.15, but one scalar still misses the fact that discovery probability changes sharply with visible score.

`selection_aware_bin` preserves both:

```text
selection coverage
    +
score/domain conditioning
```

and reaches a better verification/value frontier.

## Why this matters for epistemic frontier expansion

Independent verification prevents a false visible score from becoming knowledge, but verification policy also changes what the system learns about its own search frontier.

The two questions are different:

```text
Is this candidate verified enough to promote?

vs

What does the set of verified candidates tell us about
unverified regions of hypothesis space?
```

The first is assurance. The second is inference under a policy-selected observation process.

A system can be perfectly strict about individual promotion yet still learn a badly biased model of where future discoveries are likely to exist.

## Cost crossover

The selection-aware reject-verification policy wins at the default rejected-verification cost of 1.20.

When the cost is raised to 2.0, `pass_only` becomes better in the replicated semantic sweep. Thus PS-027 does not imply universal coverage of rejected hypotheses.

## Architecture consequence

Discovery/frontier state should preserve enough acquisition context to distinguish:

```text
verified because it looked promising
verified by representative coverage
verified because a specific uncertainty was targeted
not verified
```

The acquisition label does not change whether the verification itself is correct. It changes what that result can safely teach about other candidates.

I30 therefore strengthens the current rule:

> **verification authority and statistical generalization authority are distinct.**

A verified candidate may be authoritative about itself without making the selected verification set representative of the surrounding frontier.
