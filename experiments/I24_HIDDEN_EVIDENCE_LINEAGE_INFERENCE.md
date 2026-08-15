# I24 — Hidden Evidence-Lineage Inference

**Status:** implemented discriminator. No new provisional principle is promoted yet.

## Question

I05C, I17, I20 and I21 assumed that the organism already knew which visible sources shared a failure lineage.

That is often unrealistic.

Two APIs can depend on the same upstream database. Multiple evaluators can inherit the same training/data failure. Many visible documents can copy one original claim. Source identities therefore do not imply evidence independence.

I24 asks:

> **Can the organism infer shared failure ancestry from observed error history, notice when those relationships change, and buy an explicit dependency/provenance probe only when the uncertainty matters to a consequential decision?**

## Environment

Six stable visible sources are driven by three hidden upstream failure processes.

Within a hidden lineage, sources share a common error event plus smaller source-specific noise. The learner never receives the hidden lineage IDs through ordinary observation.

At the midpoint, the upstream dependencies change while all six visible source identities stay constant:

```text
regime 0:  (0,0) (1,1) (2,2)
regime 1:  (0,5) (1,2) (3,4)
```

Claims alternate between the two consequence structures already used by the shared assurance experiments:

- external execution claims;
- metacognitive/verifier-quality claims.

A subset of claims later receives sufficiently independent passive resolution. Those resolved outcomes let the learner observe which visible sources failed together.

A separate independent claim audit is available at a price and can still be imperfect/unavailable.

An optional explicit **lineage/dependency probe** reveals whether the two majority sources currently share an upstream failure lineage for a bounded lifetime. It is not free.

## Learner

`HiddenLineageEstimator` maintains exponentially decayed:

- per-source error rate;
- pairwise co-error rate;
- excess co-error covariance.

A pair is provisionally treated as sharing failure ancestry when excess co-error exceeds a threshold.

This is deliberately a small model-free mechanism. It is testing the semantic need for learned dependence, not selecting a mature clustering algorithm.

The active-probe policy asks a narrower question than `am I uncertain?`:

> **Would resolving whether this majority pair is dependent change the audit decision, and is the expected consequence reduction worth the probe cost?**

## Policies

### `record_count`

Treats every visible source as independent. Three records therefore look like three independent votes.

### `all_correlated`

Treats the whole panel as one failure lineage. Safe against copied confidence, but often buys unnecessary independent audits.

### `learned`

Infers pairwise hidden dependence from resolved co-failure history and prices claim assurance using the inferred effective lineage structure.

### `learned_probe`

Uses the same learned model but can buy a bounded explicit dependency probe when dependence uncertainty could flip the claim-audit decision.

### `oracle`

Receives the hidden current lineage map. This is the information ceiling, not a deployable policy.

## Approximate 30-seed result

12,000 tasks/seed, upstream lineage shift at task 6,000:

| policy | utility/task | weighted harm | independent audits/task | lineage probes/task |
|---|---:|---:|---:|---:|
| record count / assume independent | ~4.157 | ~0.296 | ~0.277 | 0 |
| assume all correlated | ~4.002 | ~0.331 | ~0.865 | 0 |
| **learned lineage** | **~4.196** | **~0.232** | ~0.437 | 0 |
| learned + active probe | ~4.194 | **~0.221** | ~0.423 | ~0.238 |
| oracle lineage | ~4.213 | ~0.216 | ~0.408 | 0 |

The learned policy therefore lands between the two bad extremes:

- naive independence underestimates harm when the apparent majority is duplicated failure ancestry;
- universal correlation throws away real independent evidence and over-buys audits.

## Hidden-dependence recovery after the upstream shift

For the passive learned estimator:

- pre-shift pair-relation accuracy: ~`0.980`;
- first 800 post-shift tasks: ~`0.664`;
- later post-shift: ~`0.925`.

The upstream graph changes while source identities do not, so the old dependence model becomes temporarily wrong.

With value-priced explicit pair probes:

- early post-shift pair accuracy rises to ~`0.796`;
- late post-shift reaches ~`0.989`;
- weighted claim harm falls from ~`0.232` to ~`0.221`.

At the default probe price this lower harm roughly pays for itself but does not materially beat passive learned inference on mean utility. That is useful: the result does **not** justify mandatory provenance probing.

As probe price increases, the policy buys sharply fewer probes.

## Architecture consequence

The previous evidence substrate assumed:

```text
source -> known lineage
```

I24 replaces that assumption with:

```text
stable source identity
        |
        +--> observed outcomes / co-failures
        |
        +--> optional provenance/dependency probes
        v
revisable dependence model
        |
        v
estimated effective independent evidence
        |
        v
assurance allocation
```

This creates a new uncertainty type:

> **evidence-dependence uncertainty** — uncertainty about whether apparently distinct observations actually provide distinct failure modes.

It is separate from:

- uncertainty that a claim is true;
- uncertainty that a source is individually reliable;
- uncertainty that another audit will resolve the claim.

## Why no PS-026 yet

I24 is one synthetic family with one simple co-error estimator.

The result strongly supports PS-013/014 and removes the assumption that failure-mode independence is always known, but promotion should wait for a structurally different second family—for example:

- hidden shared training-data ancestry among evaluators;
- shared upstream provenance in a document/API graph;
- dependence inferred from interventions rather than outcome co-failure.

A second family should also test confounders where sources fail together because the **task itself is difficult**, not because they share ancestry.

That confounder is now the highest-value falsifier.

## Current implication

Evidence independence is not necessarily metadata supplied by the environment.

It can itself be a learned, stale, uncertain and actively testable model.

The architecture therefore should not equate:

```text
number of records
number of named sources
number of independent failure modes
```

Those are three different quantities.
