# I03 — Assurance Composition: Granularity, Independence and Allocation

**Status: implemented; 6/6 replicated semantic tests pass; 30-seed sweeps complete.**

## Why combine E12, E13 and E21?

I02 made verifier reliability a learned and fallible quantity. The next question is not merely whether verification helps, but **which property should be checked, by which evidence source, and when the check is worth its cost**.

I03 therefore uses one candidate environment to attack three design decisions:

- **E12 — verification granularity:** final outcome versus intermediate/process state;
- **E13 — evaluator independence:** repeated correlated judges versus genuinely different failure modes;
- **E21 — assurance allocation:** confidence-triggered self-checking versus explicit consequence-sensitive allocation versus uniform heavy verification.

## Candidate environment

Each selected candidate has two distinct correctness dimensions:

1. **final correctness** — whether the final answer/result is correct;
2. **process validity** — whether the intermediate transition/process is valid and safe.

A candidate can therefore have the right final answer while using an invalid process, or a valid process that ends in a wrong result.

The proposal/search loop also has a **shared evaluator exploit**. Wrong candidates can carry a feature that raises the visible proposal/evaluator score. As more candidates are searched, the optimizer becomes increasingly likely to find and select that exploit.

Verifier channels:

- primary final-outcome evaluator;
- second evaluator with the **same exploit blind spot**;
- more expensive independent outcome evaluator with a different failure mode;
- process/state-transition verifier.

All channels are fallible.

---

# E12 — verification granularity

## Policies

- outcome-only;
- process-only;
- uniform outcome + process;
- adaptive granularity, which buys each check only when estimated risk × consequence exceeds check cost.

## 30-seed result

| policy | net utility/task | false accept | final-failure accept | process-failure accept | verification cost/task |
|---|---:|---:|---:|---:|---:|
| outcome only | -0.979 | 0.293 | 0.205 | 0.113 | 0.080 |
| process only | -0.229 | 0.232 | 0.227 | 0.006 | 0.320 |
| uniform both | -0.005 | 0.181 | 0.176 | 0.006 | 0.400 |
| **adaptive granularity** | **0.013** | 0.205 | 0.183 | 0.029 | **0.329** |

## Interpretation

Outcome and process verification are not substitutes:

- outcome checking strongly reduces wrong-final-result acceptance but largely misses invalid processes;
- process checking nearly removes invalid-process acceptance but does little about adversarially selected wrong final results;
- checking both catches more of both classes;
- adaptive granularity trades some residual risk for lower assurance cost and produces the best net utility in this first family.

**DL-012 remains unresolved.** One structurally different task family is still required before promoting a granularity rule. The current evidence supports only the narrower conclusion that `verification` is not one homogeneous operation.

---

# E13 — evaluator independence under optimization pressure

The search policy chooses the highest visible-scoring candidate from 1, 4 or 16 proposals. The shared exploit raises visible score and fools both correlated outcome evaluators, but not the independent evaluator.

## 30-seed means

### Search pressure = 1

| policy | net utility | false accept | exploit accept |
|---|---:|---:|---:|
| single primary | 0.355 | 0.140 | 0.0349 |
| correlated double | 0.270 | 0.124 | 0.0345 |
| independent double | 0.256 | 0.0899 | **0.00145** |

At low pressure the independent check is safer but its extra cost is not always worth it.

### Search pressure = 4

| policy | net utility | false accept | exploit accept |
|---|---:|---:|---:|
| single primary | -0.254 | 0.235 | 0.133 |
| correlated double | -0.441 | 0.231 | 0.132 |
| **independent double** | **0.302** | **0.104** | **0.00514** |

### Search pressure = 16

| policy | net utility | false accept | exploit accept |
|---|---:|---:|---:|
| single primary | -2.925 | 0.499 | 0.434 |
| correlated double | -3.084 | 0.494 | 0.430 |
| **independent double** | **-0.086** | **0.081** | **0.0176** |

The correlated second evaluator adds cost without removing the shared failure mode. At high optimization pressure it is almost as exploitable as the single evaluator.

This reproduces the E23 lesson in a different mechanism: **search power finds evaluator blind spots, and assurance value comes from failure-mode independence rather than judge count.**

Together with E23 and I02, this is sufficient to promote the evaluator-independence principle in the design ledger.

---

# E21 — assurance allocation

## Policies

### Implicit self-check

The candidate's own visible confidence/score determines whether an extra independent check is requested.

This is deliberately vulnerable to Goodhart: exploit candidates receive *higher* visible confidence, so the system becomes less likely to check exactly the candidates that most need checking.

### Explicit adaptive assurance

A separate policy estimates expected harm from:

- final-result failure as search pressure increases;
- invalid process as process consequence increases;
- current verification cost;
- shared assurance capacity.

Independent outcome and process checks are allocated to the highest expected harm reduction.

### Uniform heavy assurance

Every candidate receives primary, independent outcome and process checks.

## Default 30-seed result

| policy | net utility/task | false accept | exploit accept | verification cost/task |
|---|---:|---:|---:|---:|
| implicit self-check | -0.982 | 0.288 | 0.200 | 0.119 |
| explicit adaptive | 0.543 | 0.149 | 0.0858 | **0.336** |
| **uniform heavy** | **0.635** | **0.0117** | **0.0071** | 0.850 |

At the default assurance price, full verification is still worth its cost. This is an important negative result: an adaptive allocator should not be preferred merely because it is adaptive.

## Assurance-price sweep

Scale both independent/process verification prices while leaving task consequences fixed:

| check-price scale | implicit self-check | explicit adaptive | uniform heavy |
|---:|---:|---:|---:|
| 0.5× | -0.954 | 0.676 | **1.027** |
| 1.0× | -0.961 | 0.548 | **0.642** |
| 1.5× | -0.963 | **0.420** | 0.257 |
| 2.0× | -0.969 | **0.294** | -0.128 |
| 3.0× | -0.980 | **0.066** | -0.898 |

The correct conclusion is therefore conditional:

> **Assurance should be allocated according to expected harm reduction relative to verification cost and uncertainty. Uniform heavy checking is appropriate when assurance is cheap relative to error consequence; selective checking becomes preferable as assurance itself becomes scarce/expensive.**

I02 provides the structurally different second family: durable frontier claims with learned family-specific verifier risk. There adaptive verification matched the false-write rate of uniform double checking while using fewer secondary checks and slightly improving lifetime utility.

Together I02 + I03 support promotion of the consequence-sensitive assurance-allocation principle.

---

# New synthesis from composition

I03 sharpens the architecture in three ways.

## 1. Verification targets typed state transitions

A verifier should answer a scoped question such as:

- `is the final result correct?`
- `was this intermediate transition valid?`
- `is this durable mutation supported?`
- `is this action authorized?`

There is no generic scalar `verified` bit that substitutes for these scopes.

## 2. Independence is relational

Two evaluators are not independent because they are different model instances or produce different prose. Independence means their relevant **failure modes are sufficiently uncorrelated for the property being checked**.

## 3. Optimizer pressure changes assurance economics

As proposal/search pressure rises, the chance that the optimizer finds a verifier exploit rises. Therefore the value of independent evidence should increase with optimization pressure even when the task itself has not changed.

This creates a direct bridge between PS-005 value-of-computation, PS-008 verified discovery and the assurance layer.

---

# What remains open

- DL-012 verification granularity needs a structurally different second family;
- independence estimation itself is still hand-specified rather than learned from latent failure patterns;
- explicit assurance risk estimates are engineered rather than learned online;
- authorization/capability boundaries (E14) are not tested here;
- self-improvement regression assurance (E20) remains open.

The next integrated assurance generation should learn verifier covariance/failure clusters from outcomes and test hidden/rotating evidence under repeated self-improvement pressure.
