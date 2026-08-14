# E23 — Weak-Teacher / Independent-Evaluator Discovery Loop

**Status: first model-free implementation complete; preliminary synthetic evidence only.**

## Question

Can a system produce **verified candidates beyond the demonstrated capability/knowledge of its supervisor** without confusing novelty with truth, and which parts of the discovery loop are necessary?

This experiment operationalizes `synthesis/DISCOVERY_AND_EPISTEMIC_GROWTH.md` and F26.

## First implemented landscape

The current synthetic world contains five deceptive three-bit subproblems.

For each subproblem:

- the teacher demonstrates the all-zero construction;
- all-zero is a strict local optimum under one-bit mutation;
- crossing the low-scoring intermediate states reaches a better all-one construction;
- the teacher frontier has hidden score **10**;
- the global optimum has hidden score **15**.

Therefore a greedy system that only accepts immediately better mutations cannot exceed the teacher, while a system preserving diverse stepping stones can.

The experiment is deliberately model-free so it measures discovery-loop mechanics rather than pretrained language knowledge.

## Implemented variants

### V1 — `teacher_imitation`

Returns the best teacher-demonstrated construction. Establishes the supervisor frontier.

### V2 — `unguided_search`

Generates novel candidates without using evaluation to select what becomes the output.

### V3 — `greedy_visible`

Uses the visible evaluator and retains only immediate improvements.

### V4 — `diverse_archive`

Retains candidates across behavioral descriptors so temporarily worse stepping stones can survive long enough to reach better regions.

### V5 — `epistemic_lifecycle`

Uses the same exploratory archive, but a candidate only becomes consolidated knowledge after an independent hidden evaluator confirms that it really exceeds the currently consolidated frontier.

Rejected candidates are retained as negative-result memory.

### V6 — `epistemic_no_negative_memory`

Ablation of V5 that forgets rejected candidates and may pay to reverify the same false hypotheses.

## Evaluator structure

Two evaluator layers exist:

1. **visible evaluator** — available to the search policy;
2. **hidden evaluator** — used only for experiment ground truth and, in V5/V6, explicit independent verification before promotion.

A controlled visible-evaluator defect can be enabled. A particular candidate pattern then receives a large visible bonus that has no corresponding hidden-ground-truth value.

This makes evaluator exploitation measurable rather than rhetorical.

## Local validation

The implementation was tested locally with Python 3.11+ stdlib only.

**6/6 E23 unit tests pass.** They verify:

- the teacher is genuinely a local optimum rather than an artificially bad example;
- greedy one-step improvement remains at the teacher frontier;
- the diverse archive can cross the deceptive valley;
- a defective visible evaluator can produce a high-scoring false discovery;
- independent hidden verification blocks false promotion while still allowing real beyond-teacher improvement;
- negative-result memory prevents repeated verification of already rejected candidates.

## Preliminary 30-seed sweep

Each run uses 1,500 proposal operations.

### Exact visible evaluator

| variant | mean selected hidden score | beyond teacher |
|---|---:|---:|
| greedy visible | 10.000 | 0 / 30 |
| diverse archive | 12.167 | 30 / 30 |
| epistemic lifecycle | 12.167 | 30 / 30 |

This is a direct synthetic teacher-ceiling result: the supervisor demonstrates score 10, greedy search cannot leave it, while preserving diverse intermediate hypotheses finds verified constructions above that frontier on every tested seed.

### Defective visible evaluator

The defect bonus is +8 visible score for a pattern that is not actually valuable under hidden ground truth.

| variant | mean selected hidden score | beyond teacher | false discoveries |
|---|---:|---:|---:|
| greedy visible | 10.000 | 0 / 30 | 0 / 30 |
| diverse archive | 8.433 | 1 / 30 | 29 / 30 |
| epistemic lifecycle | 12.267 | 30 / 30 | 0 / 30 promoted |

The result demonstrates why **search power and verification quality must co-scale**. Diversity/search is useful under a correct evaluator, but under an exploitable evaluator the same search pressure reliably finds the evaluator defect.

### Negative-result memory

With the defective evaluator:

- lifecycle **with** rejected-hypothesis memory averages ~21.3 independent verification calls and 0 repeated failed verifications;
- the no-negative-memory ablation averages ~27.5 verification calls and ~6.23 duplicate failed verifications.

The selected hidden score is essentially unchanged, so the retained negative result saves assurance work rather than creating capability by itself.

## What this result supports

This first family supports the mechanism-level hypothesis that:

> bootstrap/teacher knowledge does not need to define the system's epistemic ceiling when the system can preserve alternatives, search beyond demonstrations and obtain sufficiently independent evidence about candidate improvements.

It also supports three narrower claims:

1. **Diversity/stepping stones matter** on deceptive landscapes where every local move away from the teacher appears worse.
2. **Evaluator optimization can turn discovery machinery into false-discovery machinery** when the evaluator is exploitable.
3. **Epistemic staging matters:** candidate discovery and consolidated knowledge should not be the same state transition.

## What this result does NOT show

It does **not** show that the organism created new human knowledge.

The hidden answer is deliberately known to the benchmark designer. This family tests the mechanics of crossing a teacher frontier and governing candidate discoveries.

A real discovery claim still requires an externally checkable result whose answer was not already known to the relevant human field.

## Primary metrics for later families

- best hidden-ground-truth score;
- fraction of runs exceeding the teacher frontier;
- time/evaluations to first beyond-teacher verified result;
- novelty relative to demonstrations;
- rediscovery rate;
- visible-vs-hidden evaluator gap;
- false-discovery/promoted-error rate;
- candidate diversity;
- repeated failed-hypothesis rate;
- total proposal/evaluation operations;
- retained state/archive size;
- lifetime utility after resource/evaluator shifts.

## Required second task family before any new provisional selection

Repeat the discovery mechanism on a structurally different domain, preferably one of:

- symbolic theorem/construction search with an exact checker;
- algorithm synthesis on hidden test distributions;
- causal toy science where the system must maintain competing world hypotheses and select experiments to distinguish them.

The third option is highest-value because it connects E23 to E06/E07 and begins testing **empirical** rather than purely constructive discovery.

## Connections to current provisional selections

- **PS-001:** hypotheses/results need typed exact provenance/identity plus potentially compact learned search state.
- **PS-002:** candidate discoveries remain tentative before durable consolidation.
- **PS-003:** evaluator/search coordination should occur at the scope of shared candidate/evaluator resources.
- **PS-004:** consolidated belief remains linked to source proof/experiment evidence.
- **PS-005:** discovery/search/experiment effort should stop when expected marginal information/value gain falls below cost.

## Next E23 work

1. add the causal toy-science second family after E06/E07 exist;
2. vary search pressure against multiple evaluator defect classes;
3. distinguish rediscovery from genuinely novel benchmark constructions;
4. add resource-price shifts and value-of-discovery stopping;
5. later replace synthetic hidden truth with externally checkable open research problems only after the discovery governance survives these controlled tests.

## Source trail

See:

- `synthesis/DISCOVERY_AND_EPISTEMIC_GROWTH.md`
- `sources/DISCOVERY_EPISTEMIC_GROWTH.md`
