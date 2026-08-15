# I15 — External Side Effects Across Crash Ambiguity

**Status:** implemented. I15 tests the boundary where local publication/recovery semantics stop being sufficient because the authoritative fact lives outside the organism.

## Question

I14 can recover an internal consequential transition when restart can read the authoritative version/identity that the candidate intended to replace or produce.

That does not solve this sequence:

```text
send consequential effect
        |
external world applies it
        |
process crashes before learning that fact
        |
restart
```

The local runtime can now have perfect version fences and still not know whether retrying will perform the effect once or twice.

I15 asks:

> what external evidence is required to recover safely, and what happens when the environment cannot identify the effect exactly?

## Family A — externally identifiable effect

This family models a ledger/service that can recognize a stable effect identity.

Policies:

- **blind retry** — send again whenever local completion is missing;
- **stable external identity** — retry the same externally recognized effect identity, allowing the receiver to deduplicate;
- **exact reconciliation** — ask the external system whether that exact effect identity was applied, then retry only when absent;
- **abstain** — never retry ambiguous effects.

### Default 30-seed result

20,000 trials/seed; duplicate penalty `4`, missed-effect penalty `1`, identity cost `0.025`, query cost `0.06`.

| policy | utility | duplicate effect | missed effect |
|---|---:|---:|---:|
| blind retry | ~-1.161 | ~0.540 | 0 |
| **stable external identity** | **~0.9825** | **0** | **0** |
| exact reconciliation | ~0.9580 | **0** | **0** |
| abstain | ~0.8398 | 0 | ~0.160 |

A local completion marker behaves like blind retry when the crash occurs after remote application but before that marker survives.

Both externally recognized identity and exact external reconciliation remove the modeled ambiguity; their relative value is then mostly the price of carrying/querying that evidence.

## Cost/consequence falsifier

With a deliberately larger identity cost `0.10` and reconciliation cost `0.15`, blind retry becomes rational when duplicate harm is tiny:

| duplicate penalty | blind retry | stable identity | reconcile |
|---:|---:|---:|---:|
| 0.01 | **~0.995** | ~0.930 | ~0.895 |
| 0.10 | **~0.946** | ~0.930 | ~0.895 |
| 0.50 | ~0.730 | **~0.930** | ~0.895 |
| 4.00 | ~-1.161 | **~0.930** | ~0.895 |

Therefore the Atlas does not select universal deduplication/reconciliation overhead. It prices the ambiguity against consequence.

## Family B — physical/non-identifiable effect

This family deliberately removes the convenient interface assumption.

The environment does **not** understand a stable local effect identity. After a crash, the organism can only query a noisy aggregate sensor that is correlated with whether the effect happened.

Default sensor:

- true-positive probability `0.88`;
- false-positive probability `0.18`;
- query cost `0.04`.

### Default consequence regime

Duplicate penalty `4`, omission penalty `1`:

| policy | utility | duplicate | missed | sensor queries |
|---|---:|---:|---:|---:|
| blind retry | ~-0.921 | ~0.480 | 0 | 0 |
| abstain | **~0.780** | 0 | ~0.220 | 0 |
| sensor reconcile | ~0.701 | ~0.058 | ~0.039 | ~0.700 |
| risk-sensitive | ~0.752 | **0** | ~0.220 | ~0.700 |

The noisy sensor cannot recreate exact effect history. It can only change the posterior probability that this effect occurred.

When duplicate harm dominates, the consequence-sensitive policy refuses to retry after ambiguous recovery and accepts omissions instead.

### Omission-dominated regime

Duplicate penalty `1`, omission penalty `4`:

| policy | utility | duplicate | missed |
|---|---:|---:|---:|
| blind retry | ~0.520 | ~0.480 | 0 |
| abstain | ~0.120 | 0 | ~0.220 |
| sensor reconcile | **~0.757** | ~0.058 | ~0.039 |
| risk-sensitive | **~0.757** | ~0.058 | ~0.039 |

Now retrying after sufficiently negative sensor evidence becomes rational because omission is more costly than accidental duplication.

## Core result

The two families separate three concepts that are easy to conflate:

```text
local intent identity
        !=
external effect identity
        !=
external evidence that the effect occurred
```

A stable local UUID cannot make an external environment deduplicate an action unless that environment participates in the identity semantics.

Likewise, observing a world state that is *consistent* with an effect is not the same as having evidence that uniquely attributes that state to this effect.

## Architecture implication

The current evidence supports this narrow rule:

> **After crash/retry ambiguity, local intent or past approval cannot establish that an external effect occurred. Consequential automatic recovery requires sufficiently effect-specific external evidence—such as externally recognized stable identity or exact reconciliation—or the state must remain epistemically unresolved and retry/abstention must be chosen from explicit consequence.**

This complements PS-024 rather than replacing it:

```text
internal consequential publication
    -> version/target fence can establish authority

external consequential effect
    -> local fence protects intent
    -> external evidence establishes execution
```

## What is not selected

I15 does not select:

- an HTTP idempotency key;
- a particular payment/request protocol;
- an outbox;
- a distributed transaction;
- a remote receipt database;
- a specific sensor/reconciliation technology.

Those are candidate implementations of the required semantics.

## Next discriminator

The next test should combine **current capability authority with external-effect recovery**:

- effect may have been applied before crash;
- capability is revoked while the process is down;
- restart must be allowed to mark an already-applied effect complete without treating revocation as evidence that it never happened;
- restart must not issue a new retry after revocation;
- external evidence itself may be stale, delayed or adversarially inconsistent.

This will test whether `execution evidence` and `permission to execute again` remain correctly separated under recovery pressure.
