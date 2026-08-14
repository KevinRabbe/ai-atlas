# I05B — Imperfect Metacognitive Feedback

**Status:** implemented and tested. Composition checkpoint; **not a new provisional principle**.

## Question

I05 allowed operation/verifier quality to become learned state, but its synthetic research outcomes eventually supplied a clean delayed truth label. I05B removes that convenience.

Can the system still learn which evaluators deserve resources when feedback about evaluator correctness is:

- delayed;
- available only for some decisions;
- noisy when it arrives;
- itself worth purchasing selectively?

Categorical capability authority remains exact and external. I05B concerns uncertainty about **epistemic/tool quality**, not permission.

## Environment

Two research families swap quality at task 3000:

- before the shift, family 0 has reliable candidates/evaluators while family 1 has a high visible/secondary false-approval rate;
- after the shift, the roles reverse.

A visible approval creates a candidate for secondary verification. The metacognitive controller estimates:

- probability a visibly approved candidate is actually correct;
- secondary approval probability when the candidate is correct;
- secondary false-approval probability when it is wrong.

These estimates determine whether secondary verification has positive expected value.

## Feedback modes

1. `exact`
   - every visible approval receives a correct audit after a fixed delay;
2. `passive`
   - only ~28% receive audit evidence, delayed 8–35 tasks, with 14% label noise;
3. `active`
   - passive evidence remains available, but the controller may buy a faster 3%-noise audit when estimator uncertainty × task value × false-knowledge consequence exceeds a threshold;
4. `none`
   - no post-decision truth/audit feedback; priors never learn which family became unsafe.

The active audit itself costs utility.

## 30-seed result

| feedback | net utility/task | false durable writes/run | correct durable writes/run | verifications/task | active audits/task |
|---|---:|---:|---:|---:|---:|
| exact delayed | **1.7782** | 61.87 | **2592.3** | 0.4587 | 0.0000 |
| passive noisy/censored | 1.5711 | 47.10 | 2243.4 | 0.3954 | 0.0000 |
| **active selective audit** | **1.7595** | **46.80** | 2542.9 | 0.4460 | **0.3759** |
| no feedback | 1.2939 | **493.37** | 3734.7 | 0.7893 | 0.0000 |

No-feedback appears productive because it verifies far more candidates, but much of that apparent productivity is false durable knowledge.

## Hidden-quality-swap recovery

Mean utility/task:

| feedback | pre-shift | first 500 post-shift | late post-shift |
|---|---:|---:|---:|
| exact | 1.8213 | 1.2092 | 1.8403 |
| passive | 1.8018 | **-0.0769** | 1.6238 |
| **active** | 1.8010 | **1.0557** | **1.8504** |
| none | 1.0931 | 1.4518 | 1.5033 |

Sparse noisy feedback eventually adapts but reacts too slowly to the hidden swap. Selective high-quality audit recovers much of the exact-feedback behavior despite paying for audit evidence.

## Audit allocation

The active policy buys audit evidence on ~37.6% of all tasks. Its audit demand falls as estimates become better constrained:

- pre-shift active-audit rate: ~`0.4609`;
- first 500 post-shift: ~`0.4038`;
- late post-shift: ~`0.2683`.

The exact shape is policy-specific, but the clean-sheet implication is broader: **learning about the reliability of one's own tools/evaluators is itself an information-acquisition problem with value, cost and uncertainty.**

## Architecture implication

I05/I05B suggest a recursive form of the common allocator:

`estimate value of operation`

`estimate uncertainty in that value estimate`

`optionally buy evidence about the estimator/tool`

`revise metacognitive state`

`then allocate the underlying operation`

This does not require infinite regress. Assurance/audit can terminate at typed external evidence channels whose authority/failure assumptions are themselves explicit and periodically challenged.

## Relation to selected principles

- **PS-007:** metacognitive audit is active evidence acquisition;
- **PS-013:** audit is useful only if its failure mode is sufficiently independent;
- **PS-014:** assurance/audit effort scales with consequence, uncertainty and price;
- **PS-018:** evaluator/self-change evidence must refresh as the failure surface changes;
- **PS-010:** audit competes with other resource-consuming operations;
- **PS-017:** learned quality never substitutes for categorical authority.

No new principle is required yet; I05B demonstrates that existing allocation/assurance laws recurse onto metacognitive state.

## Limitations / next falsifiers

- audit noise is independent rather than correlated/adversarial;
- the system knows the audit channel's approximate noise class;
- feedback eventually arrives within a bounded horizon;
- only two evaluator families are learned;
- active-audit threshold is hand designed;
- audit evidence does not itself change because the evaluator adapts strategically.

A harder I05C would learn whether an audit source is independent/reliable from partially overlapping evidence without receiving its noise parameters.
