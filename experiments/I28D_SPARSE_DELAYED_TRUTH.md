# I28D — Sparse / Delayed Truth and Relation Evidence

**Status:** implemented model-free discriminator; 8 semantic tests.

**Selection status:** no new provisional principle. I28D refines PS-007/013/014/026 and exposes a new acquisition-selection failure that needs a second structurally different family before any promotion.

## Question

When source dependence/derivation must be learned from resolved outcomes, what happens when truth is sparse and delayed?

The benchmark separates three epistemic channels:

1. sparse delayed passive ground truth about past tasks;
2. actively purchased delayed task truth, used only for future relation learning;
3. direct provenance/dependency evidence that answers only whether B is currently derived from A.

Active truth therefore cannot solve the current task, and provenance cannot reveal current task truth.

## Environment

Visible source identities remain fixed. The hidden A/B structural relation changes once without announcement:

- first half: B is derived from A, usually copying A but sometimes performing an independent check;
- second half: B becomes an independent evaluator.

Independent sources C and D remain available throughout.

Passive truth resolves about 1.2% of tasks and arrives 80–240 steps late. Policy-dependent acquisition uses a separate RNG from world generation, so every policy sees the same hidden task stream for a given seed.

## Policies

- `conservative` — never declare A/B dependence known;
- `passive_behavioral` — learn the relation only from sparse delayed passive outcomes;
- `disagreement_targeted_truth` — buy delayed truth primarily when A and B disagree;
- `coverage_targeted_truth` — buy a small output-independent truth sample while relation uncertainty remains material;
- `provenance_probe` — buy a bounded direct relation/provenance observation; it does not reveal task truth;
- `oracle_relation` — hidden-relation upper bound.

## 30-seed matched sweep

| policy | error | Brier | net utility/task | relation accuracy | relation coverage | post-shift error | post-shift relation accuracy | active truth/task | provenance probes/task |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| conservative | ~0.0854 | ~0.0694 | ~2.4679 | — | 0 | ~0.0712 | — | 0 | 0 |
| passive behavioral | ~0.0830 | ~0.0692 | ~2.5032 | ~0.7324 | ~0.8884 | ~0.0712 | ~0.0000 | 0 | 0 |
| disagreement-targeted truth | ~0.1152 | ~0.0733 | ~2.0001 | ~0.5407 | ~0.9811 | ~0.0629 | ~0.9866 | ~0.0516 | 0 |
| **coverage-targeted truth** | **~0.0824** | **~0.0685** | **~2.5038** | **~0.8275** | ~0.9670 | ~0.0712 | ~0.0590 | ~0.0211 | 0 |
| **provenance probe** | **~0.0809** | **~0.0661** | **~2.5332** | **~0.9946** | ~0.9995 | **~0.0643** | **~0.9256** | 0 | **~0.00451** |
| oracle relation | ~0.0808 | ~0.0660 | ~2.5353 | 1.0000 | 1.0000 | ~0.0627 | 1.0000 | 0 | 0 |

Passive feedback rate is only ~0.0118/task.

## Result 1 — sparse delayed truth makes behavioral relation state stale

Sparse passive outcomes are enough to learn useful average structure, but not enough to follow a hidden relation shift quickly. In the first 600 tasks after B becomes independent, the passive behavioral learner's resolved relation is effectively always the old one.

So a high-confidence learned relation can be stale even when the source identities did not change.

## Result 2 — targeted truth acquisition can bias relation learning

The surprising failure is `disagreement_targeted_truth`.

It buys far more truth than passive learning and rapidly detects the post-shift relation. Yet lifetime decision error worsens to ~11.52% and overall relation accuracy falls to ~54.1%.

Why: the learner is estimating the joint A/B error process, but the acquisition policy selects examples conditional on `A != B`. The resolved training set is therefore not representative of the distribution whose dependence relation is being estimated.

This is not evidence that active learning is bad. It is evidence that:

> **information acquisition can alter the statistical meaning of the evidence used to learn epistemic relations.**

An acquisition policy must either preserve enough coverage, model its selection mechanism, or use an estimator valid under the induced sample distribution.

## Result 3 — output-independent coverage avoids the worst bias

`coverage_targeted_truth` purchases only ~2.11% active outcomes versus ~5.16% for disagreement-targeted truth, yet reaches ~82.75% relation accuracy and returns near the passive/better decision frontier.

It is not immediately good at detecting the hidden shift because it still learns behaviorally. Its value here is removing the severe selection bias while increasing resolution density.

## Result 4 — direct relation evidence can dominate when truth is scarce

A bounded provenance/dependency probe reaches ~99.46% relation accuracy with only ~0.45% probes/task and nearly matches the hidden-relation oracle.

This does **not** imply provenance should always be bought. Its value depends on price.

30-seed provenance-price sweep:

| provenance cost | net utility/task |
|---:|---:|
| 0.18 | ~2.5332 |
| 8 | ~2.4979 |
| 12 | ~2.4799 |
| 15 | ~2.4663 |
| 20 | ~2.4438 |

At sufficiently high provenance cost, coverage-targeted delayed truth (~2.5038 at its default price) is better.

## Architecture inference

I28D strengthens the current evidence substrate:

```text
claim truth evidence
    !=
source-quality evidence
    !=
dependence/derivation evidence
```

A resolved task can update all three only if the acquisition process makes that update statistically meaningful. Direct provenance can update relation state without supplying task truth; task truth can teach the relation only through an appropriate sampling/estimation path.

The current clean-sheet interpretation is therefore:

> **buy the evidence type that resolves the uncertainty actually controlling the decision, and treat the acquisition policy itself as part of the evidence-generating process.**

This is still a refinement, not PS-027. A second structurally different family should test whether selection-conditioned assurance/auditing produces the same bias in self-change or discovery.
