# E24 — Predictive Representation Objective: Latent Target vs Reconstruction vs Task-Sufficient State

**Status:** implemented and tested in two model-free synthetic families. **JEPA is not selected. No new provisional principle is promoted from E24 alone.**

## Decision under test

Does prediction in a learned target representation preserve useful world structure more efficiently than raw reconstruction or narrow task-specific prediction **across changing future objectives and interventions**?

This is not a benchmark of I-JEPA/V-JEPA implementations. It tests the implementation-neutral mechanism extracted from them:

> predict useful hidden/future structure in representation space rather than necessarily reproducing every raw observation detail.

The implementation deliberately uses simple empirical mutual-information feature scoring and binary predictors instead of a neural model so the first discriminator tests the **objective/representation trade-off**, not transformer/encoder details.

## No hidden decomposition labels

The learner sees observed feature streams and task/intervention feedback. It is not told which dimensions are stable, nuisance, rare, causal or future-relevant.

Predictive latent masks are chosen from empirical current-feature -> next-same-feature mutual information. Task-sufficient masks are chosen from empirical current-feature -> current-task-target association. Recoverable-source variants retain raw transition evidence outside hot state and may re-score it after the objective changes.

## Policies

1. `raw_reconstruction`
   - retain all observed features in hot state;
2. `task_sufficient`
   - retain a four-feature mask optimized for the initial target;
3. `coarse_latent_target`
   - retain the four most empirically predictive features;
4. `dense_latent_target`
   - retain the ten most empirically predictive features;
5. `latent_recoverable_source`
   - retain the four-feature coarse hot latent plus cold raw/source transitions, then materialize only the newly relevant feature after objective/intervention feedback identifies it.

Hot-state and cold-source widths are priced separately.

---

# Family A — objective shift / future optionality

24 observed binary dimensions contain:

- four strongly temporally predictable factors;
- four moderately predictable factors;
- a lower-frequency factor at feature 8 that is less predictive than the top eight but later becomes the target;
- another weaker predictive factor;
- high-dimensional unpredictable nuisance.

The initial objective predicts next-state feature 0. The future objective predicts next-state feature 8.

## 30-seed result

| policy | initial balanced acc. | future balanced acc. | initial net | future net | lifetime net | future hot width |
|---|---:|---:|---:|---:|---:|---:|
| raw reconstruction | 0.9601 | **0.8504** | 0.8881 | 0.7784 | 0.8332 | 24 |
| task sufficient | 0.9601 | 0.6280 | **0.9481** | 0.6160 | 0.7820 | 4 |
| **coarse latent** | 0.9601 | **0.5000** | **0.9481** | 0.4880 | 0.7180 | **4** |
| dense latent | 0.9601 | **0.8504** | 0.9301 | 0.8204 | 0.8752 | 10 |
| **latent + recoverable source** | 0.9601 | **0.8504** | 0.9361 | **0.8234** | **0.8797** | **5** |

## Interpretation

The coarse predictive latent is excellent for the original objective and cheaper than raw reconstruction, but its top-four predictive mask discards the lower-ranked factor that the later objective needs. Its future balanced accuracy therefore collapses to chance.

Dense predictive state retains that factor and transfers while remaining much smaller than raw reconstruction. The source-backed hybrid starts with the compact latent, retains raw transition evidence cold, and rematerializes only the new factor after the objective changes. In this synthetic cost model it achieves the best lifetime net.

This is direct evidence for the PS-012 claim that **decision/prediction sufficiency is relative to future objective distribution and recoverability**, not a permanent property of a latent.

---

# Family B — passive prediction vs intervention consequence

16 observed dimensions are generated in episodes with a hidden mechanism. Most strongly predictive features are sufficient for the passive prediction objective. Feature 8 is a noisy observable cue of the hidden mechanism; it is less dominant in passive predictive ranking but becomes decisive when the system must predict which intervention consequence will occur.

The representation mask is learned from the passive stream before intervention labels are used.

## 30-seed result

| policy | passive balanced acc. | intervention balanced acc. | passive net | intervention net | lifetime net | intervention hot width |
|---|---:|---:|---:|---:|---:|---:|
| raw reconstruction | 0.9498 | **0.8989** | 0.9018 | 0.8509 | 0.8763 | 16 |
| task sufficient | 0.9498 | 0.5884 | **0.9378** | 0.5764 | 0.7571 | 4 |
| **coarse latent** | 0.9498 | **0.4899** | **0.9378** | 0.4779 | 0.7078 | **4** |
| dense latent | 0.9498 | **0.8989** | 0.9198 | 0.8689 | 0.8943 | 10 |
| **latent + recoverable source** | 0.9498 | **0.8989** | 0.9298 | **0.8759** | **0.9028** | **5** |

## Interpretation

All representations appear equally strong on the passive objective. That fact does **not** establish intervention sufficiency.

The coarse predictive latent omits the lower-ranked mechanism cue and falls to chance when intervention consequence becomes the task. Dense/raw representations retain it. The source-backed hybrid can re-score retained raw evidence after intervention feedback and materialize the cue without keeping all features hot permanently.

The result attacks a particularly important failure mode:

`good passive prediction != good intervention/counterfactual state`

A representation can accurately model observational regularity while discarding variables needed to predict what happens **when the system acts**.

---

# What E24 says about JEPA

E24 does **not** support either extreme claim:

- `JEPA/latent prediction is the answer` — not supported;
- `reconstruction is necessary for world models` — also not supported.

The synthetic evidence instead supports a frontier:

`coarse predictive target -> highest efficiency while future/action-relevant distinctions stay inside the target`

`denser predictive target -> more hot cost, more transfer/optionality`

`raw reconstruction -> maximum retained information, highest hot-state cost`

`compact predictive state + recoverable evidence -> aggressive hot compression with an escape path when future relevance changes`

This is consistent with the Atlas treatment of V-JEPA 2.1: richer/dense predictive supervision can be useful when fine spatial/temporal distinctions matter, rather than assuming abstraction means permanently discarding detail.

## Relation to current principles

- **PS-001:** exact authority/provenance semantics remain outside approximate predictive latents;
- **PS-005:** extra prediction/reconstruction work must earn downstream value;
- **PS-007:** intervention evidence is a priced operation, not implied by passive prediction;
- **PS-009:** shared predictive factors only help where structure is reusable;
- **PS-010:** hot state, cold source storage and rematerialization substitute under resource pressure;
- **PS-012:** predictive breadth is allocated by future relevance/recoverability;
- **PS-023:** fidelity/granularity should increase when discarded detail can alter consequential decisions;
- **PS-013/014/016:** a world model's own prediction is not independent verification of itself.

## Why no new principle is promoted

The strongest E24 conclusion is already largely expressible as the combination of PS-012 and PS-023. Creating a separate "JEPA principle" would preserve an implementation name instead of the underlying function.

The new evidence instead refines those principles:

> **Predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone. Target breadth and recoverable evidence are part of the predictive objective.**

## Important limitations / next falsifiers

This first implementation is intentionally model-free and therefore does not answer:

- whether neural JEPA-style objectives learn the same feature ranking;
- optimization/collapse dynamics;
- representation geometry and transfer;
- decoder/reconstruction training cost;
- high-dimensional continuous/video structure;
- action-conditioned latent dynamics trained from scarce intervention data;
- hardware/batching differences between dense reconstruction and latent prediction;
- whether source rematerialization is still attractive when archive storage/privacy costs are high.

A later neural E24C should compare actual learned objectives at matched capacity/compute only if that distinction remains architecture-relevant after composition.
