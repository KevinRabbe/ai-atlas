# I23 — Integrated Crash / Topology / Evidence / Transient-State Recovery Lifecycle

**Status:** implemented whole-runtime composition checkpoint. No new provisional principle is added.

## Goal

Earlier recovery experiments deliberately isolated failure classes. I23 puts their surviving semantics into one lifecycle.

Each episode contains all of the following:

- a topology publication that may already have committed before the crash;
- a local completion marker that cannot be trusted after restart;
- source-backed hot state created in the old topology epoch;
- delayed causal-credit eligibility created before structural change;
- an old-epoch external event still queued;
- capability authority that can be revoked while the process is down;
- an external effect whose visible receipts may be stale and are three copies of one lineage;
- an independent reconciliation path that is useful but imperfect/costly.

The purpose is not to add another mechanism. It is to see whether the mechanisms already selected remain coherent when they collide.

## Policies

### Typed recovery

Uses the common architecture:

- publication provenance + base fencing for topology recovery;
- current authority for new external work;
- topology-epoch forwarding for queued events;
- `TransientStateRegistry` currentness/causal-identity checks;
- source rematerialization for invalid hot state;
- exact transition identity for delayed credit;
- `EvidenceLineageRegistry + EvidenceAssuranceDecision` for external execution evidence;
- PS-025 to separate historical effect evidence from retry authority.

### Opaque snapshot restore

Represents the tempting alternative `restore everything the process remembered`:

- assumes the topology transition is still merely prepared;
- reuses hot state without source/epoch validity;
- restores credit by old position;
- routes old queued work with old scope/permission view;
- trusts the three correlated receipt copies as the execution conclusion.

Authoritative typed runtime state still prevents some actual corruption, so the benchmark counts the failed/unsafe restoration attempts rather than granting the opaque policy magical write access around the boundary.

### Discard transient

Uses safe typed publication/evidence/event recovery but throws away hot cache and delayed-credit state. This is the safety-without-optionality baseline.

## Approximate 30-seed composition result

2,000 episodes/seed:

| policy | utility/episode | stale hot use | false credit | unauthorized old-event execution | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

Typed recovery also forwards essentially every queued old-epoch event through the current topology and processes it exactly once. Runtime semantic invariants remain true in the typed path.

External execution remains probabilistic because the independent reconciliation source is intentionally imperfect. That is correct: composition should not turn uncertain evidence into certainty.

Typical external error rates in the same sweep are roughly:

- typed lineage-aware recovery: ~0.3% duplicate + ~3.3% omitted;
- opaque correlated-receipt recovery: ~4.8% duplicate + ~5.4% omitted.

The exact rates belong to this synthetic evidence model, not to a real service.

## Why `discard transient` matters

Typed recovery beating opaque restoration would be easy to dismiss as `just discard more state`.

The discard baseline tests that directly.

It avoids stale-cache and false-credit failures but loses the value of:

- rematerializable hot state;
- surviving causal-credit traces.

Typed recovery retains that option value by asking **what kind of transient state survived semantically**, not merely whether bytes survived.

## Architecture result

The combined lifecycle now follows one coherent sequence:

```text
crash / restart
      |
      v
read authoritative publication provenance
      |
classify prepared / already-published / superseded
      |
reacquire current validation for any retry
      |
recover topology/resource authority
      |
forward old-epoch events by stable identity
      |
re-read current capability authority
      |
recover evidence structure by lineage/staleness/resolution
      |
acquire independent evidence only when worth it
      |
recover transient state by typed validity:
  cache -> currentness + source rematerialization
  credit -> exact causal identity + optional history replay
      |
resume
```

This is much stronger than process-snapshot recovery because the recovery operation understands semantic types.

## What I23 does not prove

The current lifecycle still simplifies:

- actual durable byte-level storage and torn writes;
- concurrent multi-node recovery;
- independent evidence acquisition latency;
- large bounded caches and eviction interaction;
- partially replayable learning trajectories;
- learned uncertainty over evidence-lineage identity itself;
- nested/overlapping ownership.

Those remain later discriminators if they affect architecture.

## Current implication

At this checkpoint, the Atlas has an executable argument against one broad class of architecture:

> **opaque whole-process state is not a sufficient semantic recovery boundary for an adaptive intelligent system whose topology, authority, evidence quality and causal structure can change.**

The alternative is not `persist everything in more detail`. It is typed recovery with stable sources/provenance and value-priced rematerialization/replay.
