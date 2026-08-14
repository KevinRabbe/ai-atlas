# E11 — Similarity Retrieval vs Applicability / Downstream Decision Value

**Status: two synthetic families implemented, tested and swept.**

## Question

Should persistent evidence be retrieved because it *looks like* the current query, or because its premises make it useful for the current decision?

E11 deliberately gives similarity a regime where it is the right cheap answer. The purpose is not to discredit semantic retrieval; it is to find when semantic similarity stops being a sufficient proxy for applicability.

## Family A — stale procedures after regime change

Each query belongs to a topic/family and a current regime. The corpus contains:

- an exact-topic old memory from regime 0;
- a less surface-similar memory from the same family that matches the current regime;
- an irrelevant family distractor.

Policies pay explicit field-check cost. `similarity` is cheapest; `temporal_applicability` checks regime/family; `decision_value` checks additional outcome/verification fields.

20-seed means (`accuracy / net utility`):

| shifted fraction | similarity | temporal applicability | decision value |
|---:|---:|---:|---:|
| 0.0 | **1.000 / 0.994** | 1.000 / 0.982 | 1.000 / 0.970 |
| 0.1 | 0.902 / 0.896 | **1.000 / 0.982** | 1.000 / 0.970 |
| 0.5 | 0.495 / 0.489 | **1.000 / 0.982** | 1.000 / 0.970 |
| 0.9 | 0.099 / 0.093 | **1.000 / 0.982** | 1.000 / 0.970 |
| 1.0 | 0.000 / -0.006 | **1.000 / 0.982** | 1.000 / 0.970 |

When the corpus is stable, similarity is correctly preferred because deeper checks add cost without changing the answer. Once applicability changes, exact semantic identity becomes actively misleading.

## Family B — surface similarity versus causal/action relevance

The current task has a mechanism that determines the correct action. The corpus contains:

- one or more exact-topic surface lures;
- a different-topic memory with the same mechanism and verified successful action;
- a same-mechanism memory whose action failed.

A conflict probability controls how often the exact-topic memory comes from the wrong mechanism.

20-seed means (`accuracy / net utility`):

| surface/causal conflict | similarity | causal-only | decision value | hybrid |
|---:|---:|---:|---:|---:|
| 0.0 | **1.000 / 0.990** | 1.000 / 0.980 | 1.000 / 0.960 | 1.000 / 0.960 |
| 0.1 | 0.897 / 0.887 | 0.949 / 0.929 | **1.000 / 0.960** | **1.000 / 0.960** |
| 0.4 | 0.596 / 0.586 | 0.800 / 0.780 | **1.000 / 0.960** | **1.000 / 0.960** |
| 0.8 | 0.201 / 0.191 | 0.601 / 0.581 | **1.000 / 0.960** | **1.000 / 0.960** |
| 1.0 | 0.000 / -0.010 | 0.500 / 0.480 | **1.000 / 0.960** | **1.000 / 0.960** |

Causal matching alone is not enough in this family because some causally applicable experiences are failures. Outcome/verification semantics are needed to distinguish "same mechanism" from "useful precedent."

## Validation

**4/4 E11 tests pass locally.** They pin both sides of the crossover: cheap similarity wins when applicability is stable, and applicability/decision-value retrieval wins when staleness or causal conflict breaks the semantic proxy.

## Interpretation

Two families support the principle:

> **retrieval should target expected downstream applicability/value; semantic similarity is one potentially cheap signal for that target, not the target itself.**

This does not imply every retrieval should run an expensive causal model. PS-005 applies here too: deeper applicability checking should be purchased only when its expected reduction in stale/irrelevant retrieval errors exceeds its cost.

## Remaining open mechanism questions

- how to learn applicability rather than receive synthetic fields;
- how retrieval uncertainty composes with PS-006 hypothesis plurality;
- multi-memory aggregation instead of top-1 retrieval;
- adversarial/poisoned memory;
- archive indexes that approximate decision value cheaply;
- learning when semantic similarity is sufficiently reliable that deeper checking is wasteful.
