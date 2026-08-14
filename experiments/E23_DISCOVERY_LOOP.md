# E23 — Weak-Teacher / Independent-Evaluator Discovery Loop

**Status: specified, not yet implemented.**

## Question

Can a system produce **verified candidates beyond the demonstrated capability/knowledge of its supervisor** without confusing novelty with truth, and which parts of the discovery loop are necessary?

This experiment operationalizes `synthesis/DISCOVERY_AND_EPISTEMIC_GROWTH.md` and F26.

## Why this is different from ordinary supervised learning

The teacher is deliberately **not** given the best available solution. Better solutions exist in the environment/search space but are absent from demonstrations.

The experiment therefore distinguishes:

- imitation of the teacher frontier;
- search beyond the teacher frontier;
- evaluation of beyond-teacher candidates;
- promotion of verified discoveries into reusable knowledge.

## First synthetic task family

Construct deterministic optimization/program-discovery tasks with:

- a finite but large candidate space;
- exact hidden ground-truth scoring;
- teacher demonstrations restricted to suboptimal solution families;
- local optima/deceptive heuristic gradients;
- recombinable useful partial structures;
- some candidate features not represented in the teacher demonstrations;
- deterministic novelty checks against the teacher corpus.

The first task family should remain model-free if possible so the experiment measures the discovery loop rather than pretrained language knowledge.

## Variants

### V1 — teacher imitation

Learn/select only from teacher-demonstrated candidates.

Purpose: establishes the supervisor frontier.

### V2 — unguided generator/search

Generate candidates beyond the teacher demonstrations without a reliable evaluator loop.

Purpose: measures novelty without verification discipline.

### V3 — generator + evaluator + greedy incumbent

Generate variants, evaluate them with the visible evaluator, and retain only the current best.

Purpose: tests whether objective feedback alone exceeds the teacher and exposes local-optimum/premature-convergence failure.

### V4 — generator + evaluator + diverse archive

Retain multiple high-value/diverse candidate lineages.

Purpose: tests stepping-stone preservation and exploration breadth.

### V5 — epistemic lifecycle

Add explicit states:

`hypothesis -> candidate discovery -> visible verification -> hidden independent verification -> consolidated knowledge`.

Also retain rejected hypotheses/negative results with conditions.

Purpose: tests whether discovery governance reduces false promotion and repeated dead-end search.

## Evaluator structure

Use at least two evaluator layers:

1. **visible evaluator** — available to the search policy;
2. **hidden independent evaluator** — not queryable during search and used to detect evaluator exploitation/overfitting.

Later variants should inject controlled evaluator defects so increased search pressure can exploit the visible evaluator.

## Primary metrics

- best hidden-ground-truth score;
- fraction of runs exceeding the teacher frontier;
- time/evaluations to first beyond-teacher verified result;
- number of genuinely novel candidates relative to demonstrations;
- rediscovery rate;
- visible-vs-hidden evaluator gap;
- false-discovery/promoted-error rate;
- candidate diversity;
- repeated failed-hypothesis rate;
- total proposal/evaluation operations;
- retained state/archive size;
- lifetime utility after resource/evaluator shifts.

## Critical tests

### A. Teacher ceiling test

Does any variant reliably exceed the best teacher-demonstrated candidate?

### B. Evaluator necessity

Does unguided novelty produce many candidates but low verified improvement?

### C. Search pressure / Goodhart test

As proposal count grows, does visible evaluator score diverge from hidden ground truth when the evaluator is imperfect?

### D. Diversity ablation

Does greedy incumbent retention lose stepping stones that the diverse archive preserves?

### E. Epistemic-state ablation

Allow visible-evaluator winners to become durable knowledge immediately. Measure false promotion and downstream contamination versus staged hidden verification.

### F. Negative-result memory ablation

Remove retained failed hypotheses. Measure repeated wasted search on previously falsified regions.

### G. Resource-price shift

Change proposal/evaluator/archive costs mid-run and test whether discovery effort adapts rather than consuming a fixed research budget.

## Second task family requirement

Before any design-ledger promotion, repeat the discovery mechanism on a structurally different domain, for example:

- symbolic theorem/construction search with exact checker;
- algorithm synthesis on hidden test distributions;
- causal toy science where the system must select experiments to distinguish hidden world models.

The third option should connect E23 to E06/E07 because empirical discovery requires maintaining competing hypotheses and actively acquiring evidence.

## What success would mean

Success would support the principle that:

> weak/bootstrap knowledge can guide a system without defining its epistemic ceiling when the system can search beyond demonstrations and obtain sufficiently independent evidence about candidate improvements.

It would **not** mean the synthetic system created new human knowledge.

## What would count as real frontier discovery later

A real discovery claim requires an externally checkable result whose answer was not already known to the relevant human field, with enough provenance and independent verification to rule out benchmark leakage/rediscovery as far as practical.

## Connections to current provisional selections

- **PS-001:** hypotheses/results need typed exact provenance/identity plus potentially compact learned search state.
- **PS-002:** candidate discoveries remain tentative before durable consolidation.
- **PS-003:** evaluator/search coordination should occur at the scope of shared candidate/evaluator resources.
- **PS-004:** consolidated belief remains linked to source proof/experiment evidence.
- **PS-005:** discovery/search/experiment effort should stop when expected marginal information/value gain falls below cost.

## Source trail

See:

- `synthesis/DISCOVERY_AND_EPISTEMIC_GROWTH.md`
- `sources/DISCOVERY_EPISTEMIC_GROWTH.md`
