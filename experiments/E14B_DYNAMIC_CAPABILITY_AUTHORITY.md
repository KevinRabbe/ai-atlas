# E14B — Dynamic Capability Authority / Revocation

**Status:** implemented, tested and swept. Second structurally different family for DL-014.

## Question

Can a hard capability boundary remain correct when authority changes during the lifetime, or does it become a stale permission cache?

E14 established the difference between categorical authority and contextual risk. E14B attacks the categorical mechanism itself by adding grants and revocations.

## Environment

Twenty-four principals/resources carry exact boolean authority plus an exact monotonically increasing authority version. Authority flips stochastically during an 8,000-task lifetime.

Contextual action risk remains separate and is handled by the same noisy behavioral policy across the hybrid variants.

## Policies

- `behavior_only` — no categorical boundary;
- `static_hybrid` — behavior + a hard boundary frozen from the initial authority snapshot;
- `live_hybrid` — behavior + exact authority lookup every task;
- `versioned_hybrid` — behavior + cached exact authority refreshed only when the transition's exact authority version differs from the cached version.

The version field is treated as exact typed side state, not as a learned latent confidence value.

## 30-seed results

| policy | net utility/task | invariant violations/run | contextual harms/run | authority reads |
|---|---:|---:|---:|---:|
| behavior only | -17.6326 | 2648.77 | 121.43 | none |
| static hybrid | -11.0752 | 1679.57 | **90.73** | initial snapshot only |
| live hybrid | 0.4399 | **0** | 121.43 | **1.0/task** |
| **versioned hybrid** | **0.4573** | **0** | 121.43 | **0.0114 refreshes/task** |

The static hard boundary is not a real invariant once authority changes: it continues permitting revoked actions and refusing some newly granted ones.

The always-live and versioned variants both hold categorical violations at zero. The versioned policy obtains the same useful/contextual behavior while paying the expensive authority refresh on only ~1.14% of tasks.

## Interpretation

A hard boundary is only as good as the authority state it enforces.

The stronger clean-sheet requirement is therefore not merely:

`put a hard gate before privileged effects`.

It is:

`privileged transition -> exact/current authority identity+version -> narrow enforcement -> contextual risk decision inside permitted envelope`.

This connects directly to PS-001: some identity/version/authority semantics have consequences that make approximate latent encoding inappropriate as the sole enforcement channel.

## DL-014 promotion implication

E14 and E14B now support a principle across two distinct failure families:

1. adversarial error in behavioral/contextual estimation;
2. stale categorical authority under grant/revocation dynamics.

A provisional principle is justified:

> **Categorical capability authority should be enforced independently from the behavior that proposes the effect and remain current/revocable through explicit identity/version semantics. Contextual risk remains adaptive inside the authorized capability envelope.**

This does not select a specific sandbox, OS permission, capability-token scheme, process boundary or hardware mechanism.

## Falsifiers / future stress

- delayed or missing version propagation allows revoked authority to remain usable;
- the authority source itself is compromised or equivocates;
- authority changes are so frequent that versioned refresh costs exceed live validation;
- delegated authority has partial/scope semantics that a boolean boundary cannot express;
- boundary failures create availability/deadlock costs larger than the invariant protection;
- a proof-carrying/cryptographic or alternative mechanism achieves the same independence/currentness with better lifetime utility.

## Current conclusion

The Atlas should retain **independent, narrow, current/revocable capability authority** as a provisional functional constraint while leaving the enforcement implementation open.
