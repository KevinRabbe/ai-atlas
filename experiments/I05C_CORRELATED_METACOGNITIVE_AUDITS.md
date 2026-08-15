# I05C — Correlated / Adversarial Metacognitive Audit Evidence

**Status:** implemented. I05C closes the queued correlated-audit / partially-unresolved feedback stress. No new provisional principle is added.

## Question

I05/I05B showed that the organism can learn changing tool/verifier quality and can buy audit evidence when its own metacognitive estimates are uncertain.

I05C attacks a stronger assumption:

> what if the audit evidence used to learn verifier quality is itself correlated, stale, partially unavailable or misleading?

The test deliberately mirrors I17's external-execution evidence problem so the Atlas can determine whether one general evidence law survives across domains.

## Environment

Two approved-candidate/verifier families swap quality halfway through a 6,000-task lifetime.

Correctness probability among approved candidates:

```text
before shift: family 0 = 0.93, family 1 = 0.58
after shift:  family 0 = 0.60, family 1 = 0.94
```

The learner maintains a decayed correctness estimate for each family and accepts durable writes only when estimated expected utility is positive.

### Correlated audit lineage

Three apparent audit records are copies of one source lineage.

Its label error is:

- `0.10` normally;
- `0.32` during the first 500 post-shift tasks, representing stale/adversarially misleading audit state.

### Independent audit

An independent audit path has error `0.03`, costs `0.08`, and is unavailable on `22%` of attempted resolutions.

Unavailable independent outcomes are therefore genuinely unresolved from the learner's point of view.

## Policies

1. **none** — no metacognitive feedback;
2. **correlated majority** — treat the copied lineage as the audit result;
3. **majority + independent** — buy an independent audit but still let three correlated copies dominate raw vote count;
4. **uniform independent** — always request the independent audit; skip update when unavailable;
5. **selective independent** — request independent audit when source state is stale, task value is high or the current estimate is near the durable-write boundary; otherwise use lineage A;
6. **missing as success** — when the independent outcome is unavailable, incorrectly update the verifier estimate as though the candidate was correct.

## 30-seed result

| policy | utility/task | estimate error | audit queries/task | unresolved/task | false durable writes/task |
|---|---:|---:|---:|---:|---:|
| none | ~0 | ~0.173 | 0 | 0 | 0 |
| correlated majority | ~0.215 | ~0.079 | 0 | 0 | ~0.0061 |
| majority + independent | ~0.181 | ~0.078 | 1.000 | 0 | ~0.0067 |
| uniform independent | ~0.932 | **~0.048** | 1.000 | ~0.220 | ~0.0294 |
| **selective independent** | ~0.953 | ~0.050 | **~0.666** | ~0.147 | ~0.0297 |
| missing as success | ~1.010 | ~0.065 | 1.000 | 0 | **~0.0338** |

The `none` policy remains too pessimistic to make durable writes because its initial estimate never receives evidence that moves it above the consequence-adjusted decision boundary.

## Important non-result

`missing as success` has the highest mean utility in this particular synthetic default despite being worse calibrated and producing more false durable writes.

That is retained deliberately.

The experiment does **not** establish:

> unresolved outcomes should always be preserved because doing so maximizes immediate reward.

It establishes:

> **missing resolution is not positive evidence. Treating it as success changes the epistemic state in a direction not supported by observation, increasing calibration error and false durable promotion. Whether that extra throughput is worth the added risk is a separate consequence/value decision.**

This is exactly why the Atlas keeps belief, action value and commitment authority separate.

## Correlated majority failure

The raw majority policy and the `majority + independent` policy are almost equally poorly calibrated.

Buying one independent audit does not help if the aggregation rule says:

```text
three copied votes from lineage A
        >
one genuinely independent observation
```

The count is not the evidence.

Failure lineage/provenance determines how much new information was added.

## Cross-domain synthesis

I05C and I17 now reproduce the same boundary in two different domains:

```text
external effect recovery
    correlated receipts != independent evidence

metacognitive verifier learning
    correlated audit records != independent evidence
```

This strengthens existing selections rather than creating a new one:

- **PS-013:** assurance value follows relevant failure-mode independence;
- **PS-014:** independent evidence is allocated by consequence/uncertainty/cost;
- **PS-004/006:** unresolved state may remain unresolved rather than being forced into certainty;
- **PS-025:** external execution evidence needs effect-specific provenance and independence, not raw receipt count.

## Architecture implication

Evidence records in the mature runtime likely need more than source text/value. To support the already-selected rules, they need enough metadata or learned relation state to answer questions like:

- which records descend from the same failure lineage?
- is this source stale relative to the claim/action?
- did this audit resolve the outcome or merely fail to observe it?
- how independent is a proposed reconciliation path from the failure being checked?

This still does not imply one fixed provenance database schema. The next implementation step should add a minimal typed evidence-lineage abstraction to the common runtime and test whether PS-013/014 can use it across both metacognitive audit and external-effect recovery.
