# I08 — Executable Typed-Scope Runtime

**Status:** implemented first executable candidate-architecture skeleton. No new provisional principle is added; I08 composes the existing state, authority, timing, provenance and topology laws behind real split/merge operations.

## Question

I07 showed that scope membership can be learned from noisy dependency evidence, but its scopes were only labels.

I08 asks the harder architecture question:

> can a changing topology move real system state without making identity, provenance, authority, resource ownership or in-flight work relative to a topology that may disappear?

This is the first Atlas experiment where a split/merge changes ownership/routing of typed runtime objects rather than just a group ID.

## Runtime state

The synthetic organism carries:

- exact node identities;
- evidence records with exact evidence IDs and source/provenance references;
- predictive records with source references used for later rematerialization;
- an authority registry with independent `allowed` state and monotonically versioned updates;
- exact resource leases with stable resource IDs and holder-node identities;
- delayed/in-flight events carrying node identity, creation topology epoch and captured scope;
- a learned coupling graph and current dynamic partition.

The topology is allowed to change. The exact identities above are not derived from the topology.

## Compared runtimes

### `static_typed`

Keeps the initial correct partition forever. All typed state remains exact, but the topology becomes stale after the hidden dependency structure changes.

### `scope_snapshot`

A deliberately cheaper scope-addressed migration ablation. Scope snapshots are copied/split when topology changes. Stable node identity is retained, but provenance/source pointers, cached authority and resource ownership are not represented strongly enough outside the scope snapshot.

This variant is not meant as a product design. It is the targeted falsifier for the claim that a dynamic topology can safely own semantics that should remain topology-independent.

### `typed_stale_route`

Keeps evidence, predictive source state, authority and resources typed/exact, but leaves in-flight events addressed to their captured scope. It isolates the asynchronous migration problem.

### `typed_epoch`

The candidate skeleton:

- exact semantic state stays node/resource/evidence addressed;
- topology changes increment an epoch;
- scope membership can change without changing identity;
- in-flight events from old epochs are forwarded by stable node identity to the current scope;
- external effects consult the current independent authority registry at execution time;
- provenance and predictive source references survive migration;
- resource leases remain unique because holder identity is outside the scope representation.

It pays the highest migration price of the adaptive variants.

## Default 30-seed result

Four cycles over the three recurrent I07 dependency partitions, 100 steps/partition:

| runtime | utility/step | migrations/run | event misroutes | authority violations | provenance failures | rematerialization failures | duplicate resource exposure/step |
|---|---:|---:|---:|---:|---:|---:|---:|
| static typed | 0.9957 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| scope snapshot | 0.7770 | ~27.0 | ~45.0 | ~4.53 | ~108.3 | ~97.0 | ~8.218 |
| typed stale-route | 1.0636 | ~27.0 | ~45.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| **typed epoch** | **1.0744** | ~27.0 | **0.0** | **0.0** | **0.0** | **0.0** | **0.000** |

The typed-epoch runtime forwards about `46.9` delayed events/run across a topology epoch instead of dropping/misrouting them.

It processes about `542` queued events/run versus ~`497` for the two stale-scope-route variants.

## What the result means

### 1. Dynamic topology can earn its cost without owning identity

`typed_epoch` beats `static_typed` because it keeps I07's topology benefit while preserving the exact semantics the static runtime already had.

The important architectural distinction is:

```text
stable semantic identity
        !=
current organizational scope
```

A scope may split, merge or disappear. Evidence IDs, resource IDs, node identities and authority records must not disappear with it.

### 2. In-flight work needs topology-version semantics

`typed_stale_route` is intentionally strong everywhere except event routing. It still misroutes about 45 events/run when their captured scope vanishes before execution.

The epoch-safe runtime instead treats an old route as routing evidence, not permanent addressing authority:

```text
old event
  carries stable target identity + old topology epoch
        ↓
current membership lookup / forwarding
        ↓
execute once in current scope
```

This extends PS-022 from synchronization timing into live reorganization.

### 3. Authority cannot become a scope snapshot

The scope-snapshot ablation caches authorization in topology-owned state. Revocation can therefore become stale between migrations and produce categorical authority violations.

The typed runtime never migrates permission as ordinary learned/organizational state. It resolves the current authority record at execution.

This directly exercises PS-017 during topology changes.

### 4. Provenance and rematerialization need stable references

Scope snapshots can be compact, but if a split/merge destroys source linkage then later verification, contradiction repair or predictive-state rematerialization can no longer recover what was discarded.

I08 therefore strengthens PS-004/012:

> organizational migration may move ownership/cache placement, but must not silently turn recoverable evidence into irrecoverable summaries.

### 5. Resource ownership must remain singular across a split

If a scope owns a resource only as an untyped scope-local snapshot, splitting that scope creates an ambiguous question: which descendant owns the resource?

The snapshot ablation duplicates it. The typed runtime avoids the ambiguity because the lease has an exact resource identity and stable holder identity independent of topology.

## Falsifier — safe migration is not free

The typed protocol intentionally pays more migration cost than the weaker variants.

With a short 20-step structural regime and safe migration cost raised to `0.20`, the static typed runtime is better in the matched local sweep (~`0.993` vs ~`0.985`).

So I08 does **not** imply continuous topology churn. It reproduces the same plasticity-timescale law from AF02/I07:

> migrate only when expected future topology benefit exceeds inference, state-transfer, forwarding and consistency cost.

## Candidate architecture boundary exposed by I08

The first executable skeleton can now be summarized as:

```text
stable exact semantic plane
  - identities
  - provenance/source refs
  - authority versions
  - resource leases
        |
        | referenced by
        v
revisable organizational plane
  - learned coupling graph
  - dynamic scopes
  - local organization mode
  - resource allocation
  - event routing/cache placement
        |
        v
versioned transition protocol
  split / merge / forward / execute
```

This is not a classical control-plane/data-plane commitment. Those are implementation names. The clean-sheet requirement is simply that **semantics whose validity must survive reorganization cannot be defined only by the organization being changed**.

## Validation

Six semantic tests cover:

1. zero typed-invariant violations under epoch-safe migration;
2. scope-snapshot failures across authority/provenance/rematerialization/resource ownership;
3. isolated stale-route event failure;
4. adaptive typed topology beating static topology when structure persists;
5. epoch forwarding beating stale scope routes;
6. static topology winning again when migration becomes too fast/expensive.

## Next — I09

I08 still gives the topology learner honest noisy coupling observations.

The next architecture stress should attack the coupling evidence itself:

- correlated false interactions;
- adversarial/spoofed edges;
- delayed evidence;
- asymmetric dependencies;
- overlapping/nested scopes;
- authority boundaries that limit which evidence can influence a scope merge.

The key question becomes:

> how much evidence and assurance should be required before topology is allowed to move real typed state?

That will connect PS-013/014/018/020 directly to architecture reconfiguration rather than only self-change and ordinary verification.
