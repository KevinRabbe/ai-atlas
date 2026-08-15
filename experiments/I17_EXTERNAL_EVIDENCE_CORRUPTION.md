# I17 — Correlated / Stale External Execution Evidence

**Status:** implemented. I17 attacks the evidence plane introduced by PS-025. It strengthens PS-013/014/025 and does not add a new provisional principle.

## Question

PS-025 requires sufficiently effect-specific external evidence to recover exact execution when local state is ambiguous.

But `three receipts agree` is not necessarily three independent observations. They may all descend from one stale or corrupted source.

I17 asks:

> can confidence/majority aggregation recover external execution safely when evidence errors are correlated, and when is independent reconciliation worth its cost?

## Environment

Each trial has a true external execution state plus a consequence value in `{1, 2, 4, 8}`.

Visible lineage A produces **three receipts**, but they are exact copies of one latent source. That lineage is wrong with probability:

- `0.06` when fresh;
- `0.28` when stale.

An independent reconciliation source can be purchased separately:

- error probability `0.02`;
- default cost `0.10`.

The stale/fresh cue and consequence are observable. The true execution state is not.

## Policies

1. **trust primary** — use one lineage-A receipt;
2. **correlated majority** — count all three copied receipts as three votes;
3. **majority + independent** — buy one independent observation but still use raw vote count, allowing the three correlated copies to dominate it;
4. **uniform independent** — always buy and use the independent reconciliation;
5. **selective independent** — buy the independent source only when lineage A is stale or consequence is high;
6. **unresolved on conflict** — selectively query but retain unresolved execution state when the independent source contradicts lineage A.

## Default 30-seed result

30,000 trials/seed:

| policy | utility | duplicate | omitted | independent queries | weighted harm |
|---|---:|---:|---:|---:|---:|
| trust primary | ~3.562 | ~0.0853 | ~0.0524 | 0 | ~0.931 |
| correlated majority | ~3.562 | ~0.0853 | ~0.0524 | 0 | ~0.931 |
| majority + independent | ~3.468 | ~0.0852 | ~0.0521 | 1.000 | ~0.932 |
| **uniform independent** | **~4.266** | ~0.0123 | ~0.0076 | 1.000 | **~0.135** |
| selective independent | ~4.257 | ~0.0207 | ~0.0126 | ~0.675 | ~0.173 |
| unresolved on conflict | ~4.174 | ~0.0136 | ~0.0083 | ~0.675 | ~0.257 |

The raw three-way majority is exactly as informative as its one shared source. More importantly, **buying an independent observation but then treating every copied receipt as an independent vote wastes the independent evidence**: three correlated votes still outvote one genuinely independent source.

## Assurance-price crossover

20-seed utility means:

| independent check cost | trust primary | uniform independent | selective independent |
|---:|---:|---:|---:|
| 0.01 | ~3.562 | **~4.359** | ~4.323 |
| 0.10 | ~3.562 | **~4.269** | ~4.263 |
| 0.30 | ~3.562 | ~4.069 | **~4.128** |
| 0.70 | ~3.562 | ~3.669 | **~3.858** |
| 1.20 | **~3.562** | ~3.169 | ~3.520 |

This reproduces PS-014 at the external-execution layer:

- uniform independent checking is rational while assurance is cheap;
- selective checking wins as independent evidence becomes costly;
- sufficiently expensive assurance can make trusting the imperfect primary source rational in low-enough consequence regimes.

## Core result

```text
number of agreeing records
        !=
number of independent failure modes
```

Evidence value depends on provenance/failure independence, not count alone.

This is the same principle previously seen in verifier ensembles and topology assurance, now reproduced for **external execution recovery**.

## Architecture implication

PS-025 should not be interpreted as `obtain more receipts`.

The recovery layer needs enough provenance to distinguish:

```text
three records copied from lineage A
```

from:

```text
one observation from lineage A
+
one genuinely independent reconciliation path
```

Then PS-014 prices whether the independent path is worth invoking.

The surviving rule is:

> **Effect-specific evidence only improves recovery to the extent that its relevant failure mode is independent enough to add information. Correlated copies remain one epistemic source; independent reconciliation is allocated by consequence, staleness/conflict and cost.**

## Why unresolved state remains useful

The `unresolved on conflict` policy is not the utility winner under this default synthetic model because the independent source is very reliable and conflict resolution is priced modestly. It still demonstrates a required semantic option: contradictory execution evidence need not be collapsed immediately into `applied` or `absent`.

A later environment with weaker reconciliation or much higher duplicate/omission consequence may make unresolved retention optimal.

## Next integration

The next architecture step is to move the I14/I15 recovery semantics into the reusable organism lifecycle:

- persistent recovery record attached to a typed transition;
- internal publication classification from base/target version identity;
- external effect status from an effect-specific evidence record;
- current authority checked only for a new/retry attempt;
- evidence provenance/failure-lineage metadata available to assurance allocation;
- unresolved execution state permitted explicitly.

This should be done without selecting a storage engine or networking protocol.
