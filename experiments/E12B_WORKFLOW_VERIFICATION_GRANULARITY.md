# E12B — Workflow Verification Granularity

**Status:** implemented, tested and swept. This is the second structurally different family for DL-012.

## Question

Are outcome checks and process/transition checks interchangeable forms of assurance, or do they protect different failure layers that must remain explicitly targetable?

## Environment

Each task is a multi-step workflow with two independent failure channels:

1. an intermediate process/invariant violation;
2. a final-output/result corruption.

The process violation may be repaired before the final result, so a correct final output does **not** imply that the transition history was valid. Conversely, a perfectly valid process can still end with a corrupted final output.

Observable high/low risk cues are provided for each channel, but the actual failures remain hidden. Consequence varies across tasks. Checks are imperfect (0.96 sensitivity) and explicitly priced.

## Policies

- `process_only` — inspect the workflow/invariant layer only;
- `outcome_only` — inspect the final result only;
- `uniform_both` — inspect both layers every task;
- `adaptive_granularity` — buy each check only when estimated avoided harm exceeds its cost.

## 30-seed results

| policy | net utility/task | process harm rate | outcome harm rate | checks/task |
|---|---:|---:|---:|---:|
| process only | 1.6521 | **0.0050** | 0.1113 | 1.0000 |
| outcome only | 1.3030 | 0.1337 | **0.0042** | 1.0000 |
| uniform both | 1.8803 | **0.0053** | **0.0041** | 2.0000 |
| **adaptive granularity** | **1.9877** | 0.0226 | 0.0180 | **1.0684** |

## Interpretation

The result reproduces I03's first-family finding in a different causal structure:

- outcome evidence cannot certify an invalid process merely because the final state looks correct;
- process evidence cannot certify the final artifact merely because every intermediate transition was valid;
- checking both layers gives the lowest residual harm but can waste assurance when one layer is low-risk;
- adaptive granularity trades a small increase in residual harm for almost half the checking load and higher lifetime utility at the default assurance price.

The selected mechanism is therefore **not** `always check process`, `always check outcome`, or `always check both`.

## DL-012 promotion implication

I03 and E12B now support the same implementation-neutral rule across two structurally different families:

> Verification should target the failure layer(s) that can still invalidate the proposed transition or result. Outcome, process/transition, provenance, authority and other checks are not assumed substitutable merely because they all produce confidence.

The actual granularity remains allocatable under PS-014. When assurance is cheap relative to harm, checking multiple layers can be rational; when expensive, the system should concentrate checks on the dominant residual failure modes.

## Relation to I04

E12B fits naturally into the typed transition kernel:

`proposal -> identify relevant failure layers -> price assurance operations -> acquire layer-specific evidence -> authority decision -> transition`

This strengthens the I04 result that allocation may be common while assurance semantics stay typed.

## Falsifiers

- one generic checker matches layer-specific assurance across unrelated failure classes at equal cost;
- process/outcome distinction disappears once the benchmark removes synthetic cues and uses learned risk estimates;
- adaptive granularity overhead exceeds the checks it saves;
- one layer becomes a sufficient statistic for the other under realistic workflows;
- correlated checks create apparent coverage without independent evidence of the relevant failure mode.

## Current conclusion

DL-012 now meets the Atlas two-family promotion gate. The provisional principle should remain about **failure-layer-targeted verification**, not about any particular verifier implementation or fixed checklist.
