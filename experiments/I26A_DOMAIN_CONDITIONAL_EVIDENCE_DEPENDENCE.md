# I26A — Domain-Conditional Evidence Dependence

**Status:** implemented PS-026 refinement. No new provisional principle.

## Question

PS-026 says evidence independence can be unknown, learned and causally qualified.

I26A attacks another hidden simplification:

> **Is source dependence one global relation, or can the same source pair be dependent in one claim domain and independent in another?**

## Environment

Six stable visible source identities participate in two claim domains:

- `external`;
- `metacognitive`.

The hidden failure ancestry is different in each domain.

```text
external:
  (s0,s1) (s2,s3) (s4,s5)

metacognitive:
  (s0,s2) (s1,s4) (s3,s5)
```

Source names therefore remain constant while the relevant failure relation depends on claim scope.

Each task obtains a panel of three source outputs. Shared lineage failures create correlated errors; source-specific noise remains present. A subset of claims later receives sufficiently independent resolution and updates the dependence model.

## Policies

### `global`

Learns one source-pair dependence graph across both domains.

### `domain`

Uses the same `EvidenceDependenceModel`, but queries/learns the relation in the current claim-domain context.

### `domain_probe`

Adds a value-priced domain-scoped dependency/provenance probe when uncertainty about the majority pair's relation could change whether an independent claim audit is worth buying.

### `oracle`

Uses the true domain-specific relation as an information ceiling.

## Approximate 10-seed result

12,000 tasks/seed:

| policy | utility/task | weighted harm | independent audits/task | domain probes/task |
|---|---:|---:|---:|---:|
| one global relation graph | ~4.146 | ~0.253 | ~0.547 | 0 |
| **domain-scoped dependence** | **~4.224** | **~0.225** | **~0.387** | 0 |
| domain + active probe | ~4.225 | **~0.219** | ~0.395 | ~0.040 |
| oracle domain relation | ~4.226 | ~0.219 | ~0.398 | 0 |

Approximate source-pair relation accuracy:

| policy/model | external | metacognitive |
|---|---:|---:|
| global | ~0.80 | ~0.80 |
| **domain-scoped** | **~0.98** | **~0.98** |
| domain + probe | **~0.99** | **~0.99** |

## Why the global graph fails

Across the full history, each source participates in different hidden ancestry depending on claim family.

A global pair model therefore averages incompatible relations:

```text
same source IDs
    +
different domain-specific upstream paths
    ↓
one global relation
    ↓
false dependence + false independence
```

The resulting uncertainty causes unnecessary independent audits and lower utility.

## Reusable-model change

`EvidenceDependenceModel` now supports:

- global residual dependence across contexts;
- context-specific dependence scores;
- context-specific relation estimates/components;
- global or context-scoped explicit probes.

This matters because `context` can play two different roles:

1. **confounder conditioning** — I25 conditions on task difficulty to estimate a broadly shared ancestry relation;
2. **relation scope** — I26A asks for the ancestry/dependence relation that is actually relevant inside one claim domain.

Those are not the same operation.

## PS-026 refinement

The current principle becomes more precise:

> Evidence dependence is **typed/scoped relational state**. Independence may vary by claim family, environment, tool mode or other context; a globally averaged relation should not be assumed valid outside the scope that generated it.

This is a refinement of PS-026, not a new PS number.

## Remaining falsifier

I26A still represents dependence as symmetric shared ancestry.

A copied/derived relation can be directional:

```text
A -> B
```

B can inherit A's errors while A does not inherit errors originating only in B.

That is the next discriminator.
