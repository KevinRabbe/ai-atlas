# Phase 10 Experimental Status

**Checkpoint: Tier-1 and first Tier-2 epistemic/action block complete to promotion depth; ten provisional design principles selected on 2026-08-14.**

## Implemented experimental families

Core/promotion work now includes:

- E01/E01B — coordination topology and shared-resource contention;
- E02/E02B/E02C — integration, compositional transfer/interference and compute-matched conditional sharing;
- E03/E03B — current state, evidence history and source revision;
- E04/E04B — representation/interface fidelity and machine-native/exact hybrid state;
- E05/E05B — adaptive compute and value-of-search stopping;
- E06 — consequence-sensitive hypothesis plurality;
- E07 — active value-of-information acquisition;
- E09/E09B — staged/adaptive persistence;
- E22/E22B — cross-resource substitution, shared capacity and quality drift;
- E23/E23B — constructive and empirical beyond-teacher discovery mechanics.

## Validation

The latest additions E02C and E22B each add **4 passing local semantic tests**. Together with the earlier Phase-10 validation groups, the current reconstruction history contains **62 newly added passing unit tests**.

All experimental runtime code remains Python 3.11+ stdlib-only.

## Latest system-level findings

### E02C — compute-matched conditional sharing

The routed candidate and specialist baseline both contain **45 learned parameters**. The routed system activates either a 15-parameter shared path or a 10-parameter task-private path per example, never both. Specialists activate 15 task-specific parameters.

The specialist baseline uses 75 train operations/example and 30 test operations/example. The routed candidate remains below both budgets.

20-seed accuracy means:

| training examples | sharedness | specialists | routed shared/private |
|---:|---:|---:|---:|
| 240 | 0.98 | 0.867 | **0.896** |
| 240 | 0.75 | **0.864** | 0.852 |
| 240 | 0.15 | **0.863** | 0.786 |
| 480 | 0.98 | 0.913 | **0.930** |
| 480 | 0.75 | **0.925** | 0.882 |
| 480 | 0.15 | **0.920** | 0.834 |
| 1,200 | 0.98 | 0.962 | **0.973** |
| 1,200 | 0.75 | **0.974** | 0.909 |
| 1,200 | 0.15 | **0.966** | 0.869 |

The transfer/interference result therefore survives parameter and active-compute matching. The current router is intentionally imperfect and still overuses sharing in low-relatedness regimes.

### E22B — shared capacity + resource-quality drift

Twelve tasks compete each round for 3 memory, 3 compute, 2 observation and 2 verification slots. All policies know current prices, but resource competence changes twice.

30-seed means (`actual utility / reference regret / unserved rate`):

| policy | regime 0 | regime 1 | regime 2 | post-shift regret |
|---|---|---|---|---:|
| frozen independent | 0.731 / 0.218 / 0.326 | 0.455 / 0.379 / 0.292 | 0.428 / 0.395 / 0.296 | 0.387 |
| adaptive independent | 0.684 / 0.265 / 0.383 | 0.416 / 0.419 / 0.582 | 0.303 / 0.518 / 0.699 | 0.468 |
| frozen joint | 0.952 / 0.000 / 0.264 | 0.624 / 0.207 / 0.239 | 0.622 / 0.204 / 0.209 | 0.206 |
| **adaptive joint** | **0.903 / 0.042 / 0.294** | **0.781 / 0.052 / 0.407** | **0.704 / 0.121 / 0.474** | **0.086** |

A useful failure appears: adaptive-but-capacity-blind local policies can become *worse* after learning that a resource improved, because many tasks independently rush toward the same scarce slots. Learning local value and coordinating shared scarcity are distinct functions.

## Current provisional selections

1. **PS-001 — typed hybrid boundary state**;
2. **PS-002 — staged adaptive persistence**;
3. **PS-003 — coupling-scoped coordination**;
4. **PS-004 — derived current belief with evidence linkage**;
5. **PS-005 — value-of-computation stopping**;
6. **PS-006 — consequence-sensitive hypothesis plurality**;
7. **PS-007 — value-driven active evidence acquisition**;
8. **PS-008 — verified epistemic frontier expansion**;
9. **PS-009 — conditional sharing with isolation fallback**;
10. **PS-010 — joint adaptive resource substitution under shared scarcity**.

No Phase-9 architecture family is selected. These are implementation-neutral constraints that multiple families can satisfy.

## Highest-value unresolved questions

- **DL-008 predictive-state breadth:** broad reconstructive state versus decision-sufficient compressed state versus source-recoverable hybrid;
- **DL-011 retrieval objective:** similarity versus temporal/causal/downstream decision value;
- **E09B noise versus volatility:** distinguish sensor unreliability from genuine environmental change;
- later verification/control and self-improvement experiments remain intentionally unresolved.

## Next targets

1. E08 predictive-state breadth with objective switches;
2. E11 retrieval by downstream decision value;
3. E09B noise-versus-volatility disentanglement;
4. then assemble a next-generation organism constrained by PS-001 through PS-010 and measure interaction regressions rather than assuming individually useful principles compose cleanly.

## Guardrail

The measuring instrument must remain simpler than the hypothesis it measures. Every selection remains reversible, and novel output is never promoted to knowledge merely because the generator or its visible evaluator prefers it.
