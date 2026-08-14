# E14 — Capability Boundaries: Behavioral vs Hard vs Hybrid

**Status:** implemented, tested and swept. Strong first-family evidence; concrete enforcement mechanism remains open.

## Question

When a system can propose consequential actions, should safety/authorization rely on behavioral judgment, external hard capability boundaries, or a hybrid?

I04 showed that a shared allocator score is not sufficient authority. E14 isolates that boundary.

## Environment

Tasks contain two distinct risk classes:

1. **categorical authority risk** — a privileged effect may be attempted without an exact authorization fact;
2. **contextual risk** — an otherwise permitted action can still be a bad decision because its current expected harm is too high.

The behavioral controller receives noisy contextual cues. Mid-lifetime, a distribution shift makes unauthorized privileged attempts more likely to spoof the behavioral cue toward apparent safety. The exact external authorization fact does not change.

## Policies

### `behavior_only`

A learned/noisy risk estimate decides whether the action proceeds. There is no external categorical authority gate.

### `narrow_hard_only`

An exact hard boundary blocks unauthorized privileged effects, but all categorically authorized actions proceed regardless of context-dependent risk.

### `broad_hard`

All privileged actions are blocked, including authorized useful ones. This intentionally tests the cost of over-broad hard constraints.

### `hybrid`

A narrow hard boundary enforces the categorical authority invariant, while behavioral control decides context-dependent risk among actions that remain authorized.

## 30-seed results

| policy | net utility/task | invariant violations/run | contextual harms/run | blocked rate | useful success rate |
|---|---:|---:|---:|---:|---:|
| behavior only | -2.2985 | 364.63 | **226.10** | 0.3100 | 0.5916 |
| narrow hard only | -1.7620 | **0.0** | 795.90 | **0.0781** | **0.7893** |
| broad hard | -1.3474 | **0.0** | 616.60 | 0.2798 | 0.6174 |
| **hybrid** | **0.3530** | **0.0** | **226.10** | 0.3708 | 0.5916 |

Behavior-only categorical violations rise after the adversarial cue shift:

- phase 0: ~157.1/run;
- phase 1: ~207.5/run.

The hybrid keeps the same categorical violation count—zero—because the exact authority fact is enforced outside the behavior estimate.

## Interpretation

Three different failure modes appear:

- **behavior-only:** contextual intelligence cannot guarantee a categorical invariant under error or distribution shift;
- **hard-only:** exact permission does not imply that executing the action is currently wise;
- **over-broad hard boundary:** safety can be bought by deleting useful capability rather than governing it precisely;
- **hybrid:** narrow invariant enforcement and adaptive contextual judgment solve different problems and therefore compose.

## Clean-sheet inference

The result supports the existing Phase-8/verification-control requirement that some consequential capabilities need authority boundaries not reducible to model confidence.

A narrow implementation-neutral form is:

> **Categorical capability invariants should be enforced by a mechanism whose authority does not depend on the same fallible behavioral estimate that proposes the action. Context-dependent risk should remain adaptively evaluable inside the permitted capability envelope.**

This does not select operating-system permissions, sandboxes, typed tokens, hardware enclaves, process isolation or any other implementation.

## Relation to I04

I04 suggests:

`shared marginal-value allocator -> typed authority/evidence boundary -> state transition`

E14 strengthens the second edge. The shared allocator can decide that a privileged transition would be valuable to attempt, but it cannot manufacture the categorical authority required to execute it.

## Why broad boundaries are not the principle

The `broad_hard` variant demonstrates that hard constraints can trivially lower some risks by refusing legitimate work. The desired boundary should be as narrow as the invariant permits, preserving useful authorized capability while remaining independent from the behavioral proposal path.

## Falsifiers / next discriminator

- a learned/behavioral controller demonstrates effectively zero categorical violations under adversarial distribution shift without silently recreating an external authority mechanism;
- external-boundary maintenance errors dominate the violations they prevent;
- exact capability boundaries create unacceptable deadlock/availability cost under changing authority;
- a softer proof/assurance mechanism can satisfy the same invariant with equal failure independence and better utility;
- dynamic delegation/revocation makes a static boundary invalid, requiring E14B-style changing authority tests.

## Current status

E14 supplies strong experimental support for a **hybrid boundary principle**, but the Atlas should retain the concrete capability-control mechanism as open until dynamic delegation/revocation and boundary-failure cases are tested.
