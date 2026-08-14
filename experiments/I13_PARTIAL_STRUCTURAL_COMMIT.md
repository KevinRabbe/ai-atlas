# I13 — Partial Structural Commit and Failure-Isolated Reconfiguration

**Status:** implemented first structural-failure family. No new provisional principle is promoted yet because this is one migration family; the next discriminator should reproduce the boundary in a different durable state-change problem.

## Question

I10 exposes `stage -> commit -> rollback` as a clean API, but that abstraction can hide a dangerous implementation assumption:

> what if the implementation fails after only part of the new topology has become live?

A correct target topology is not sufficient if the transition path can temporarily create mixed routing versions, ambiguous resource placement or duplicated/lost work.

I13 injects failure at a random intermediate migration operation.

## Compared mechanisms

### `naive_in_place`

Move live subjects one by one and mutate the active routing structure immediately.

It has the smallest success-path overhead, but a failure can leave part of the system on the new structure and part on the old structure until detection/recovery.

### `stop_world_replace`

Block live work, construct/copy the replacement, then atomically replace the old structure only after the copy succeeds.

Failure leaves the old live structure intact, but all arrivals during preparation incur blocking/latency cost.

### `staged_transaction`

Prepare the new state without publishing it. On failure, discard/rollback staged work. On success, validate and publish behind a short version fence.

This retains a small commit pause but avoids exposing partial live state.

### `dual_version_handoff`

Keep the old live version while building the new one. On success, maintain both for a short handoff interval and route/forward work by version before retiring the old one.

It pays extra temporary state/forwarding cost but avoids a stop-the-world commit pause.

## Default 30-seed result

500 migrations, 12 moved subjects, 20% partial-failure probability, event rate 8:

| mechanism | net utility/migration | corrupt migration rate | lost events/migration | duplicate events/migration | downtime/migration |
|---|---:|---:|---:|---:|---:|
| naive in-place | 2.860 | ~0.202 | ~3.96 | ~0.51 | 0.000 |
| stop-world replace | 3.241 | **0.000** | **0.000** | **0.000** | ~1.299 |
| **staged transaction** | **3.310** | **0.000** | **0.000** | **0.000** | ~0.402 |
| dual-version handoff | 3.291 | **0.000** | **0.000** | **0.000** | **0.000** |

Naive in-place mutation also creates ambiguous resource-placement exposure during failed partial migrations; the isolated mechanisms remain zero in this abstraction.

## Failure-path result

The key result is not that a transaction API is fashionable. It is that **preparation and publication are different failure domains**.

Naive live mutation interleaves them:

```text
prepare subject 1 -> immediately visible
prepare subject 2 -> immediately visible
...
FAIL
```

so failure can expose a state that is neither the old valid organization nor the new valid organization.

The isolated variants instead maintain an externally valid state while the candidate structure is incomplete.

## Crossovers — no universal migration mechanism

### Essentially no failure + very low traffic

At failure probability `0` and event rate `0.2`:

- naive in-place: ~`4.788`;
- stop-world: ~`4.779`;
- staged transaction: ~`4.760`;
- dual version: ~`4.733`.

If partial failure is genuinely negligible and the change is cheap/recoverable, isolation overhead can exceed its value.

### High failure + low traffic

At failure probability `0.50`, event rate `0.2`:

- stop-world: ~`1.20`;
- dual version: ~`1.15`;
- staged transaction: ~`1.12`;
- naive: ~`0.85`.

Blocking is relatively cheap when almost no work arrives, so the simpler isolated copy/replace strategy is competitive/best.

### High failure + very high live traffic

At failure probability `0.50`, event rate `80`:

- **dual version: ~`0.98`**;
- staged transaction: ~`0.84`;
- stop-world: ~`0.21`;
- naive live mutation: strongly negative (~`-6.9`).

When the system must stay live, carrying two versions temporarily can be cheaper than blocking work.

## Architecture inference

I13 does **not** support one permanent transaction mechanism.

It supports a narrower clean-sheet rule:

> **a consequential multi-step structural transition needs a failure-isolation mechanism whenever partial visibility can create more expected harm than isolation/staging costs. The mechanism may be blocking replacement, staged publish or dual-version handoff depending on failure risk and live-work pressure.**

This fits the existing Atlas pattern:

```text
low failure / cheap reversible change
        -> direct update may be enough

meaningful partial-failure risk
        -> isolate preparation from publication

low traffic
        -> blocking isolation can be cheap

high live traffic
        -> staged or dual-version handoff
```

## Relation to existing principles

I13 currently refines rather than extends the PS list:

- **PS-002** staged persistence: tentative/prepared state before durable publication;
- **PS-014** assurance allocation: stronger transition machinery only when expected harm earns it;
- **PS-017** current authority: live authority semantics should not be copied into a half-published topology;
- **PS-018** independent change evidence: validation belongs before promotion;
- **PS-020** blast radius: larger multi-step change increases the cost of partial exposure;
- **PS-022** versioned event execution: dual/staged handoff depends on explicit version semantics.

A second structurally different durable-change family is required before considering a new provisional rule about failure-isolated publication.

## Validation

Six tests cover:

1. partial failure corrupts naive live migration and loses/duplicates work;
2. stop-world, staged transaction and dual-version mechanisms expose zero partial live corruption in the model;
3. staged transaction beats naive at the default failure/load regime;
4. no-failure/low-traffic conditions can make direct mutation cheapest;
5. high-failure/low-traffic conditions can justify stop-world isolation;
6. high-failure/high-traffic conditions can justify dual-version handoff.

## Next discriminator — I13B

Use a structurally different durable transition: **resource/service ownership handoff with current authority and queued requests**.

Unlike topology labels, a resource has exactly one legal owner at a time. Partial handoff can create either:

- two active owners;
- zero active owners;
- stale authority at the new owner;
- duplicated or lost queued work.

If the same preparation/publication boundary survives that family, it can be considered for principle-level promotion.
