# I20 — Shared Evidence-Lineage Assurance Allocation

**Status:** implemented composition checkpoint. No new provisional principle is added.

## Question

I17 and I05C independently produced the same failure:

```text
three copied external receipts
        !=
three independent execution observations

three copied verifier audits
        !=
three independent metacognitive checks
```

The Atlas now has `EvidenceLineageRegistry` for source-lineage / staleness / resolution / conflict structure.

I20 asks the next composition question:

> can one assurance decision rule consume that evidence structure plus learned source-quality estimates and consequence/cost, and work across both external-execution and metacognitive claims?

If not, the apparent cross-domain law is only verbal similarity.

## Separation of responsibilities

The shared implementation deliberately keeps three jobs separate:

```text
EvidenceLineageRegistry
    -> how records are related
       lineage / staleness / resolves? / conflict

metacognitive quality state
    -> estimated error of current and independent sources

EvidenceAssuranceDecision
    -> use current evidence
       acquire a new independent lineage
       or remain unresolved
```

The registry does not assign truth/reliability. The assurance allocator does not infer provenance. Source-quality estimates are imperfect inputs, not hidden ground truth.

## Two claim families

### External execution

Binary claim: `effect was applied`.

- false `applied` can omit a needed effect;
- false `absent` can cause a duplicate retry.

### Metacognitive verifier quality

Binary claim: `approved verifier/candidate family is safe enough`.

- false positive can promote bad durable state;
- false negative can miss a useful improvement.

The loss asymmetries are intentionally different. The same allocator is used in both.

## Evidence

Each trial exposes three visible records, but all three descend from one primary failure lineage.

Actual primary error:

- fresh: `0.07`;
- stale: `0.24`.

The allocator only has imperfect estimates:

- fresh: `0.09`;
- stale: `0.20`.

Independent resolving evidence:

- actual error: `0.025`;
- estimated error: `0.04`;
- unavailable on `18%` of attempts;
- default acquisition cost: `0.18`.

Consequence varies over `{1,2,4,8}`.

## Policies

1. **record-count confidence** — three agreeing copies are treated as a strong majority;
2. **stale-only** — acquire independent evidence only when the primary lineage is stale;
3. **uniform independent** — always acquire independent evidence;
4. **lineage-value** — call the shared `EvidenceAssuranceDecision` using current lineage structure, learned quality estimate, consequence, asymmetric failure cost and check price.

When a requested independent path fails to resolve, the value-aware policy does not rewrite that absence into positive evidence; the claim remains unresolved for that decision.

## Default 30-seed result

30,000 mixed claim trials/seed:

| policy | utility/task | weighted harm/task | independent queries/task | unresolved/task |
|---|---:|---:|---:|---:|
| record-count confidence | ~3.062 | ~1.438 | 0 | 0 |
| stale-only | ~3.651 | ~0.798 | ~0.301 | ~0.0545 |
| uniform independent | ~3.585 | ~0.733 | 1.000 | ~0.1803 |
| **lineage-value** | **~3.782** | **~0.592** | **~0.695** | ~0.1256 |

Per-family harm for the shared policy:

| family | record-count confidence | lineage-value |
|---|---:|---:|
| external execution | ~1.248 | **~0.599** |
| metacognitive verifier claim | ~1.629 | **~0.585** |

So the same assurance rule improves both domains despite different error consequences.

## Evidence-price response

20-seed lineage-value means:

| independent cost | utility/task | query rate | weighted harm |
|---:|---:|---:|---:|
| 0.01 | ~3.879 | ~0.825 | ~0.613 |
| 0.10 | ~3.842 | ~0.695 | ~0.591 |
| 0.18 | ~3.787 | ~0.695 | ~0.591 |
| 0.40 | ~3.696 | ~0.564 | ~0.577 |
| 0.80 | ~3.539 | ~0.402 | ~0.650 |
| 1.50 | ~3.332 | ~0.282 | ~0.749 |
| 3.00 | ~3.156 | ~0.119 | ~0.994 |

The allocator therefore does not contain the rule `always verify independently`. It continuously sheds assurance work as its price rises, accepting more evidence risk when the alternative costs more.

## Why the weighted harm is not monotonic in check price

The minimum harm around moderate prices is not a contradiction.

At very cheap prices, the policy requests independent evidence even in cases where the independent path can be unavailable; those unresolved cases themselves carry a priced cost. At moderate prices, low-consequence cases can rationally use a reasonably good fresh primary lineage instead.

The relevant objective is lifetime expected value, not minimum raw query count or minimum classification error in isolation.

## Architecture result

I20 supports a shared evidence/assurance substrate:

```text
records
   |
   v
failure-lineage / staleness / resolution structure
   |
   + learned source-quality estimates
   + consequence / asymmetric harm
   + independent evidence cost
   |
   v
use current / acquire independent / unresolved
```

This is stronger than `count votes` and more general than hard-coding one recovery policy per domain.

## Relation to existing principles

No new PS is needed:

- **PS-004:** current belief remains linked to evidence/provenance;
- **PS-006:** ambiguity can remain explicit;
- **PS-007:** additional evidence is acquired by value;
- **PS-013:** evidence value follows relevant failure-mode independence;
- **PS-014:** assurance is consequence/uncertainty/resource-sensitive;
- **PS-025:** external execution recovery uses effect-specific evidence rather than local intent/count.

The new contribution is executable composition: the same assurance interface now applies to external and self-evaluative evidence.

## Next architecture step

The evidence-lineage registry should be attached to the common `OrganismRecoveryCoordinator` so raw external evidence is not pre-interpreted before recovery.

Then a recovery attempt can ask the shared assurance layer itself whether to:

- accept the current external execution conclusion;
- acquire another independent reconciliation lineage;
- preserve an unresolved execution state.

That will remove the last privileged interpretation step from the current crash-aware organism.
