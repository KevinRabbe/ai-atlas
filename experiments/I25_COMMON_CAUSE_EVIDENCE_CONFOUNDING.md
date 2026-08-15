# I25 — Common-Cause Confounding in Learned Evidence Dependence

**Status:** implemented second-family discriminator. Together with I24 this supports a narrow new provisional principle.

## Question

I24 showed that hidden shared failure ancestry can be learned from repeated co-failure.

But raw co-failure is not enough to establish shared ancestry.

Independent evaluators can fail together because the **task itself is difficult**. That common cause can make unrelated sources look dependent.

I25 asks:

> **Can the organism distinguish hidden shared failure ancestry from broad common-cause task difficulty, and can it use controlled dependency evidence when observational correlation remains ambiguous?**

## Structurally different family

Eight stable evaluators are driven by four hidden shared-failure lineages.

The environment also has a global latent task-difficulty variable:

- easy tasks: low source-specific error;
- hard tasks: much higher source-specific error across **all** evaluators.

This creates broad co-failure among unrelated evaluators even though their hidden ancestry is independent.

The organism receives only a noisy observable difficulty proxy, not the latent hard/easy variable itself.

At the midpoint the hidden upstream lineage relationships change while evaluator identities remain constant.

This family therefore contains **two causes of co-failure**:

```text
shared ancestry --------> correlated evaluator error

hard task --------------> broad evaluator error
```

A dependence learner that sees only `A and B were wrong together` can confuse those causes.

## Policies

### `raw_cofailure`

Uses one unconditional co-error covariance model across all tasks.

### `difficulty_conditioned`

Maintains separate error/co-error statistics by noisy observed difficulty context and infers shared ancestry from residual co-error after conditioning on that common cause.

### `conditioned_probe`

Adds a value-priced controlled dependency/provenance probe when uncertainty about a majority pair's dependence could change the downstream audit decision.

The probe abstracts a matched diagnostic intervention, explicit upstream provenance trace or another mechanism that provides evidence about dependence under controlled conditions. No particular implementation is selected.

### `oracle`

Uses the true hidden lineage map as an information ceiling.

## Approximate 10-seed result

10,000 tasks/seed, hidden lineage shift at task 5,000:

| policy | utility/task | weighted harm | independent audits/task | dependency probes/task |
|---|---:|---:|---:|---:|
| raw co-failure | ~4.116 | ~0.296 | ~0.433 | 0 |
| **difficulty-conditioned** | **~4.149** | ~0.294 | **~0.337** | 0 |
| conditioned + active probe | ~4.145 | **~0.277** | ~0.335 | ~0.217 |
| oracle lineage | ~4.165 | ~0.281 | ~0.337 | 0 |

The conditioned passive policy improves utility mainly by avoiding false dependence and therefore unnecessary audits.

The active controlled probe further reduces harm, but at the default probe price its extra information does not fully pay back in mean utility. Again, the result does not support mandatory probing.

## Hidden-lineage identification

Approximate pair-relation accuracy:

| policy/model | pre-shift | early post-shift | late post-shift |
|---|---:|---:|---:|
| raw co-failure | ~0.926 | ~0.696 | ~0.834 |
| difficulty-conditioned | ~0.919 | ~0.728 | ~0.876 |
| conditioned + probe | **~0.989** | **~0.944** | **~0.997** |

The passive conditioned estimator is not perfect because the difficulty proxy is noisy and source relationships also change.

The controlled probe is most valuable exactly where observational dependence is causally ambiguous.

## What this falsifies

I25 falsifies the stronger interpretation of I24:

> `persistent co-failure => shared evidence lineage`

That inference is unsafe.

Co-failure must be interpreted relative to plausible common causes.

The evidence question is therefore closer to:

```text
Did A and B fail together
BECAUSE they share a failure mechanism,
OR because the same difficult circumstance affected both?
```

## PS-026 promotion basis

I24 and I25 are now two distinct families:

1. **hidden shared upstream ancestry** with changing source dependencies;
2. **shared ancestry plus global task-difficulty confounding**, where raw correlation can create false dependence.

Both favor a revisable dependence model and value-priced explicit dependence evidence over either source-count confidence or a fixed universal correlation assumption.

This is enough for a narrow principle-level selection, but not for a specific clustering, causal-discovery or provenance-graph implementation.

## Remaining falsifiers

- adversarial sources that intentionally mimic independent failure patterns;
- dependence that is directional rather than symmetric;
- latent common causes not represented by any useful observable context;
- sparse feedback where pairwise dependence cannot be learned cheaply;
- large source populations where pairwise modeling itself becomes too expensive;
- dependence that varies by claim domain rather than globally by source pair.

Those should shape the next generation of the common evidence substrate.
