# I28C — Cyclic / Mutually Adaptive Evidence

**Status:** implemented PS-026 refinement. No new provisional principle.

## Question

I28A/B assume derivation can be represented as a directed acyclic relation.

Real evaluators may repeatedly revise from one another:

```text
A <-> B
```

A static source graph therefore contains a cycle.

I28C asks whether that requires a fundamentally cyclic evidence calculus, or whether stable version/generation identity can unroll the interaction into a temporal DAG.

## Environment

Two mutually adapting sources A/B plus an independent comparator D.

Initial versions:

```text
A0    B0
```

Each adaptation round is sequential:

```text
B(t-1) -> A(t) -> B(t)
```

A/B source identities therefore form a repeated cycle across rounds, but versioned observations form an acyclic temporal graph.

Each new version:

- copies its predecessor/peer with probability `0.65`;
- independently self-checks otherwise;
- self-check error is `0.04`.

Initial A0/B0 error is `0.22`; D error is `0.18`.

Two adaptation rounds are used by default.

## Innovation-root provenance

Every initial or independent self-check creates a new innovation root.

A copied version inherits its parent's root.

So final A2/B2 may:

- share one innovation root and therefore not be independent;
- retain different innovation roots despite the static source-level A<->B cycle.

Approximate final same-root rate is ~65% in this family.

## Policies

### `final_independent`

Treats final A2/B2/D as independent evidence.

### `static_cycle_collapse`

Treats A and B as one permanent failure group because their source identities participate in a cycle.

### `history_independent`

Uses every A/B version plus D as independent evidence.

This has maximal record count and intentionally tests false precision from revision history.

### `versioned_root_groups`

Uses innovation-root provenance on the final A2/B2 values:

- same root -> one effective group;
- different roots -> separate groups.

### `learned_temporal`

Uses the full versioned temporal DAG and learns:

```text
P(A_t correct | B_(t-1) correct)
P(B_t correct | A_t correct)
```

from passively resolved outcomes.

### `oracle`

Uses exact hidden copy/self-check probabilities on the temporal graph.

## Approximate 30-seed result

12,000 tasks/seed:

| policy | error rate | Brier | same-root error | distinct-root error |
|---|---:|---:|---:|---:|
| final outputs independent | ~0.040 | ~0.061 | ~0.039 | ~0.043 |
| static cycle collapse | ~0.035 | ~0.032 | ~0.030 | ~0.045 |
| all history independent | ~0.029 | ~0.043 | ~0.030 | ~0.028 |
| versioned root groups | ~0.033 | ~0.032 | ~0.030 | ~0.037 |
| **learned temporal DAG** | **~0.030** | **~0.024** | **~0.026** | **~0.037** |
| oracle temporal DAG | ~0.026 | ~0.022 | ~0.024 | ~0.029 |

## What the metrics reveal

### Final independence

Overcounts A2/B2 whenever they share one innovation root.

### Static cycle collapse

Avoids that overcount but throws away real diversity on the ~35% of cases where A2/B2 have distinct innovation roots.

### History independence

Achieves good raw classification because it sees many values, but its Brier score is much worse than the learned temporal model. The revisions are not independent samples, so treating them as such creates false precision.

### Versioned root grouping

Captures dynamic current independence better than static source identity, but still compresses away transition evidence in the intermediate versions.

### Temporal unrolling

Retains the transition structure and produces much better calibrated evidence, approaching the generative oracle without requiring a fundamentally cyclic probabilistic object.

## Architecture implication

A source-level cycle does not necessarily require cyclic **state semantics**.

When dependency is temporally ordered, version/generation identity can transform:

```text
A <-> B
```

into:

```text
A0   B0
 |    |
 |    +--> A1 --> B1
 |              |
 +--------------+--> A2 --> B2
```

with every dependency pointing from an earlier authoritative version to a later one.

This is consistent with earlier Atlas requirements for explicit version identity in publication/recovery.

## Important limit

I28C does **not** prove every feedback loop can be unrolled cheaply.

The temporal history may become long, expensive or partially unavailable. A genuinely simultaneous algebraic constraint, recurrent hidden state or mutually co-trained model may not admit the same simple treatment.

The result only establishes:

> **Do not collapse a source-level cycle into one permanent evidence group before checking whether versioned temporal provenance removes the cycle.**

## PS-026 refinement

Evidence derivation relations can be version-sensitive.

Static source identity is insufficient to determine current independence when sources repeatedly adapt from one another.

The decision-relevant object may be:

```text
(source identity, version/generation, derivation parent, innovation root)
```

rather than source identity alone.

## Next discriminator

I28D should reduce and delay truth/resolution feedback.

I28A–C show that behavioral dependence/derivation learning can work when enough claims eventually resolve. The remaining question is whether it still pays when:

- only a small fraction of claims obtain ground truth;
- outcome feedback is delayed;
- derivation structure may change before enough outcomes arrive.

That is where explicit provenance or active interventions may become cheaper than behavioral learning.
