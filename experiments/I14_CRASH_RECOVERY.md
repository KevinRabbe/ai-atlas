# I14 — Crash/Restart Recovery Across Consequential Publication

**Status:** implemented. I14 extends PS-024 across process failure/restart; it does not add a new provisional principle.

## Question

I13 established that a consequential multi-step change should normally be prepared outside live authority and published behind a coherence/version fence when partial visibility can violate invariants.

I14 asks what must survive if the process crashes anywhere around that fence.

The clean-sheet question is deliberately not:

> should the runtime use a WAL, journal, transaction database or event log?

It is:

> what semantic information must survive so restart can determine whether a prepared transition is unpublished, already authoritative, superseded, conflicting, or no longer valid?

## Two independent ambiguities

A phase marker alone cannot answer either of these reliably:

1. **Did publication already occur before the crash?**
   A crash can happen after authoritative state changes but before a local `published` marker survives.
2. **Is a previously approved candidate still publishable?**
   Capability authority can be revoked or supporting evidence retracted after preparation/assurance.

Old assurance therefore cannot become permanent authority merely because it survived the crash.

## Families

I14 uses two structurally different consequential states:

1. **singular resource ownership** — a prepared handoff changes the exact authoritative holder/version;
2. **durable knowledge promotion** — a prepared claim changes the authoritative knowledge version and can become invalid if supporting evidence is retracted.

Each trial crashes in one of five states:

- prepared;
- assured but unpublished;
- published but the completion marker was not persisted;
- published and marked;
- superseded by a newer authoritative version.

## Policies

- **assurance replay** — replay anything that had old approval and lacks a published marker;
- **phase + current recheck** — re-check current authority/evidence but still trust the local phase marker to decide whether publication already happened;
- **version-fenced recovery** — compare current authoritative version + target identity to the expected base and intended target; retry only from the unchanged base and only after current validation/assurance;
- **atomic snapshot** — idealized upper-bound comparator, not an implementation selection.

## 30-seed result

10,000 crash trials/seed, resource revocation probability `0.08`, knowledge retraction probability `0.10`.

### Resource ownership recovery

| policy | correct recovery | duplicate publication | revoked publication | superseded overwrite |
|---|---:|---:|---:|---:|
| assurance replay | ~0.599 | ~0.220 | ~0.021 | ~0.160 |
| phase + current recheck | ~0.620 | ~0.220 | 0 | ~0.160 |
| **version-fenced** | **1.000** | **0** | **0** | **0** |
| atomic snapshot | **1.000** | **0** | **0** | **0** |

### Durable knowledge recovery

| policy | correct recovery | duplicate publication | retracted promotion | superseded overwrite |
|---|---:|---:|---:|---:|
| assurance replay | ~0.594 | ~0.220 | ~0.026 | ~0.160 |
| phase + current recheck | ~0.620 | ~0.220 | 0 | ~0.160 |
| **version-fenced** | **1.000** | **0** | **0** | **0** |
| atomic snapshot | **1.000** | **0** | **0** | **0** |

The exact percentages are properties of this synthetic crash distribution, not universal reliability estimates. The discriminator is the failure class.

## Why phase state fails

Suppose the durable state is currently:

```text
version 10 / owner A
```

A candidate intends:

```text
version 11 / owner B
```

Publication succeeds, so the authoritative state becomes version 11 / owner B, but the process crashes before its local status changes from `assured` to `published`.

On restart, a phase-only protocol sees:

```text
assured + not marked published
```

and publishes again.

Current validation does not fix this ambiguity. It can prevent a revoked/retracted candidate from publishing, but it cannot tell whether the same candidate already became authoritative.

## Minimum recovery semantics

The companion `RecoveryRecord` therefore stores implementation-neutral semantics rather than a storage mechanism:

```text
stable publication identity
kind
expected base authoritative version
intended target version
target identity / digest
references needed to reacquire current validation
```

It deliberately does **not** require a persisted `approved = true` bit.

Restart classifies current authority as:

```text
current == target version + target identity
    -> already published; mark recovery complete

current == expected base
    -> unpublished; retry only after CURRENT validation/assurance

current advanced elsewhere
    -> superseded; discard old intent

same target version but another identity
    -> conflict; halt/reconcile

current below expected base
    -> inconsistent; halt/reconcile
```

## Architecture implication

PS-024 survives crash/restart only if the publication fence has enough durable semantic identity to answer **what became authoritative**, not merely **what phase the local process remembers**.

The stronger formulation is:

> **Prepared intent and past approval are recoverable evidence, not authority. After restart, authoritative version/identity determines whether publication already occurred or was superseded; any retry re-resolves current validation and authority.**

This does not select a WAL, journal, database transaction, event sourcing, snapshot protocol or persistence engine. Those are candidate implementations of the required semantics.

## Remaining falsifier

I14 still assumes the consequential effect is represented inside an authoritative state whose version/identity can be read after restart.

That assumption fails for some **external side effects**. If an external system performed an irreversible effect and the local process crashed before recording the response, local version fencing may not reveal whether the world already acted.

The next discriminator should therefore test crash ambiguity across external effects and compare:

- blind retry;
- local-only marker recovery;
- stable external effect identity / idempotent replay;
- external reconciliation/query before retry;
- combinations priced by effect consequence and external query/idempotency cost.
