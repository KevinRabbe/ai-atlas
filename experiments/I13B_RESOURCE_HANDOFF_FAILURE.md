# I13B — Partial Failure During Singular Resource / Service Ownership Handoff

**Status:** implemented second structural-failure family. Together with I13 this supports promotion of a new implementation-neutral transition principle.

## Why this is structurally different from I13

I13 changes topology for many subjects. A failed partial migration can expose a mixed old/new organization.

I13B instead changes **one exact ownership authority**:

> one resource/service may have exactly one legal writer/owner at a time.

The challenge is not partition consistency. It is whether a multi-step handoff can temporarily produce:

- two active owners;
- zero active owners;
- duplicate writes;
- lost requests.

## Naive ordering problem

There are two obvious live-mutation orders.

### Make before break

```text
prepare new owner
activate new owner
revoke old owner
```

If failure lands between activation and revocation, there are two live writers.

### Break before make

```text
prepare new owner
revoke old owner
activate new owner
```

If failure lands between revocation and activation, there is no live owner.

Neither ordering removes the partial-publication problem.

## Failure-isolated alternatives

### Stop-world transfer

Block requests, prepare/transfer state, then replace ownership. Failure leaves the old owner intact but incurs request latency.

### Staged lease fence

Prepare new state while the old lease remains authoritative. If preparation fails, discard it. If preparation succeeds, publish one versioned lease change behind a short fence.

### Dual-read / single-write handoff

Allow the new instance to become useful for reads while the old instance remains the sole writer. Publish the singular write lease only after preparation succeeds, then retire the old version.

This pays temporary duplicate read-state/forwarding cost but never permits two write owners.

## Default 30-seed result

500 handoffs, 20% failure probability, request rate 10, write fraction 30%:

| mechanism | utility/handoff | ownership violation rate | duplicate writes/handoff | lost requests/handoff | downtime/handoff |
|---|---:|---:|---:|---:|---:|
| make-before-break | 0.5621 | ~0.065 | ~0.780 | 0.000 | 0.000 |
| break-before-make | 0.3846 | ~0.064 | 0.000 | ~5.142 | 0.000 |
| stop-world transfer | 0.6841 | **0.000** | **0.000** | **0.000** | ~1.080 |
| staged lease fence | 0.7704 | **0.000** | **0.000** | **0.000** | ~0.120 |
| **dual-read / single-write** | **0.7743** | **0.000** | **0.000** | **0.000** | **0.000** |

## Crossovers

### Zero failure + negligible traffic

At failure probability `0`, request rate `0.2`, direct live handoff is cheapest:

- make/break direct: ~`0.0120`;
- stop-world: ~`0.0056`;
- staged fence: ~`-0.0043`;
- dual version: ~`-0.0101`.

Isolation is not free and should not be ritualized when partial failure truly has negligible expected cost.

### High failure + negligible traffic

At failure probability `0.50`, request rate `0.2`, stop-world isolation is best (~`0.0062`) because almost no useful work is being blocked.

### High failure + high live traffic

At failure probability `0.50`, request rate `80`:

- make-before-break: ~`1.48`, with ~`16.4` duplicate writes/handoff;
- break-before-make: ~`-1.99`, with ~`104.8` lost requests/handoff;
- stop-world: ~`5.67`;
- staged lease fence: ~`6.33`;
- **dual-read/single-write: ~`6.37`**.

When live traffic is expensive to stop, temporary dual-version state becomes worth carrying while the **write authority remains singular**.

## Cross-family synthesis with I13

Two different durable changes now produce the same abstract boundary.

### I13 topology migration

Partial live publication creates mixed routing/topology state. Isolated preparation avoids exposing the incoherent intermediate state.

### I13B singular ownership handoff

Partial live publication creates either duplicate writers or no writer. Isolated preparation plus a publication fence preserves the ownership invariant.

The shared mechanism is:

```text
candidate change
      ↓
prepare while still non-authoritative
      ↓
validate / acquire required evidence
      ↓
small publication boundary
      ↓
new authoritative version
      ↓
retire / garbage-collect old state
```

The publication mechanism can differ according to workload:

- direct mutation when failure exposure is negligible;
- stop-world replacement when blocking is cheap;
- staged/version-fenced publication under ordinary live load;
- dual-version handoff when continuity is especially valuable.

## Provisional promotion — PS-024

I13 + I13B support:

> **PS-024 — failure-isolated consequential transition publication:** prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish authority/ownership/topology only across a coherence boundary after required validation. Choose direct, blocking, staged or dual-version publication according to partial-failure risk, blast radius, live-work pressure and isolation cost.

The selected object is **failure isolation between preparation and publication**, not database transactions, locks, consensus protocols, blue/green deployment or any named implementation.

## Falsifier

PS-024 should be weakened/rejected if a later family shows that:

- partial live visibility can be made harmless more cheaply without recreating isolation/version semantics;
- staged/dual mechanisms create more systemic risk than the corruption they prevent;
- the system cannot determine transition boundaries reliably enough for isolation to help;
- fine-grained reversible operations dominate coherent publication across realistic large state changes.

## Validation

Six tests cover:

1. make-before-break duplicate ownership/write failure;
2. break-before-make zero-owner/lost-request failure;
3. failure-isolated mechanisms preserve singular ownership;
4. default failure/load favors isolated publication;
5. zero-failure/low-traffic can make direct handoff cheapest;
6. high live traffic can justify dual-read/single-write handoff.

## Next

Promote PS-024 in the design ledger and modify the reusable runtime so topology/resource transitions can represent **prepared version → publication fence → retired version** explicitly rather than relying on atomic Python method semantics.

Then test simultaneous authority revocation during an in-progress staged/dual handoff: the new version must not inherit stale permission merely because preparation began before revocation.
