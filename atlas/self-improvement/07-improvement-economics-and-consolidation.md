# Improvement Economics and Consolidation

## Required function

Decide whether a discovered improvement is worth creating, validating and making durable given its expected future reuse, resource savings, maintenance burden and regression risk.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-IE-01 | Harness self-improvement can sometimes raise task performance while reducing inference cost, so improvement value need not equal benchmark accuracy alone. | O | E2 | SI-S003 |
| SI-IE-02 | Distillation from Phase 2 can convert expensive competence into cheaper reusable execution, but can lose rare behavior/uncertainty. | O | E4 | prior Learning evidence |
| SI-IE-03 | AlphaTensor shows search can optimize actual hardware runtime rather than only abstract operation count, reinforcing lifetime realized cost as an objective. | O | E5 | SI-S010 |
| SI-IE-04 | Population/archive methods incur ongoing evaluation/storage cost in exchange for preserving alternative future paths. | I | E4 | SI-S005, SI-S006 |

## Improvement has an acquisition cost

A candidate improvement consumes:

- diagnosis compute;
- proposal/search compute;
- sandbox/testing resources;
- human/external review where needed;
- migration cost;
- additional runtime complexity;
- future maintenance/regression cost.

The correct comparison is not “new version scores higher” but:

`expected lifetime utility(new) - lifetime cost(new) - transition/risk cost` versus retaining the existing system.

## Consolidation ladder

Successful behavior may migrate through increasingly durable substrates:

`one-off trace -> memory -> reusable procedure/tool -> harness policy -> adapter/weight update -> architectural change`.

Promotion should depend on reuse, generality, confidence and recurring cost. Demotion/retirement should also be possible when the environment changes.

## Patch debt

Cheap local improvements can accumulate complexity. A system needs signals for when many runtime patches indicate a deeper substrate problem. Candidate trigger:

`maintenance/context/routing cost of patches > expected cost/risk of broader consolidation`.

This is analogous to software refactoring but spans learned and procedural state.

## Stopping self-improvement

Improvement itself is an inference/search process and should obey marginal-value stopping:

`continue improving if expected future gain from another mutation/search round > compute + validation + delay + risk cost`.

An autonomous system should be allowed to conclude that the current version is good enough for the current distribution.

## Portfolio allocation

Improvement resources can be split across:

- exploiting the best incumbent;
- repairing known weaknesses;
- exploring alternative lineages;
- improving evaluators/tests;
- reducing system cost;
- improving data quality;
- researching structural alternatives.

The optimal allocation changes as uncertainty and bottlenecks change.

## Clean-sheet restatement

Self-improvement is not an infinite imperative. It is **investment under uncertainty**: spend resources on changes whose expected lifetime benefit exceeds their acquisition, assurance, maintenance and regression cost.

## Failure modes

Benchmark gain with worse lifetime cost; endless self-tuning; patch debt; premature consolidation; frequent architecture churn; archive/storage explosion; improvement compute starves actual tasks; optimizing short-term gains that degrade future learning traces; refusing beneficial broad change because local fixes are easier to validate.
