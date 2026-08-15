# I16 — External Execution Evidence vs Current Capability Authority

**Status:** implemented composition discriminator. I16 builds on I15's external-effect crash boundary.

## Question

After restart there are two different questions:

1. **Did this external effect already happen?**
2. **Is the organism currently allowed to perform a new attempt?**

These are not substitutes.

A revocation after an effect happened does not rewrite history. Conversely, evidence that an earlier effect did not happen does not grant permission to retry it now.

## Environment

A consequential effect is in one of three hidden states at restart:

- absent/unknown;
- applied but local completion is unknown;
- already fully completed.

An effect-specific external receipt can reveal whether the effect was already applied. Independently, current capability authority is revoked with probability `0.35`.

The policies differ only in how they combine these two facts.

## Policies

- **authority only** — uses current permission as a proxy for execution history and retries when allowed;
- **evidence only** — uses exact execution evidence, but retries an absent effect without re-checking current permission;
- **revocation erases history** — re-checks authority but treats revocation as though the historical effect never happened;
- **separated** — external evidence determines historical completion; current authority gates only a fresh/retry effect.

## 30-seed result

20,000 trials/seed:

| policy | utility | duplicate effect | unauthorized retry | history error |
|---|---:|---:|---:|---:|
| authority only | ~-0.560 | ~0.324 | 0 | ~0.176 |
| evidence only | ~0.379 | 0 | ~0.098 | 0 |
| revocation erases history | ~0.705 | 0 | 0 | ~0.176 |
| **separated** | **~0.969** | **0** | **0** | **0** |

## Core distinction

The surviving semantics are:

```text
external execution evidence
        |
        +--> already happened -> record/complete historical fact
        |
        +--> absent/unknown -> possible NEW attempt
                                |
                                v
                        CURRENT authority gate
```

Not:

```text
authorized now -> therefore it did not already happen
```

and not:

```text
old intent/evidence says absent -> therefore retry is authorized now
```

## Architecture implication

This strengthens I15 and PS-017/024:

> **Execution status and execution authority are independently grounded. Effect-specific external evidence determines whether an external transition already occurred; any new attempt is a new consequential transition and must satisfy current authority.**

If I15's physical/non-identifiable case cannot determine exact execution status, that status remains unresolved rather than being forced to `applied` or `absent` by the permission system.

## Why this matters for recovery

A capability revocation while the process is down can produce the following valid recovery:

```text
external receipt: effect already applied
current authority: revoked
        |
        v
mark historical effect complete
DO NOT retry
```

The inverse can also happen:

```text
external evidence: effect absent
current authority: revoked
        |
        v
record absent/unresolved
DO NOT retry
```

Permission controls future action; it does not edit observed history.

## Next hardening target

External execution evidence can itself be delayed, stale, correlated or contradictory.

A later discriminator should test multiple external evidence sources with different failure modes and determine when the system should:

- accept an effect-specific receipt;
- acquire independent reconciliation;
- preserve an unresolved execution state;
- escalate assurance because duplicate/omission consequence is high.
