# I21 — Evidence-Lineage Planning Inside the Common Recovery Runtime

**Status:** implemented composition checkpoint. No new provisional principle is added.

## Goal

I19 integrated internal crash recovery and external-effect recovery into one `OrganismRecoveryCoordinator`, but external execution evidence still arrived already interpreted as `applied`, `absent` or `unknown`.

I17/I05C/I20 show that this interpretation itself is consequential because records can be:

- copied from one failure lineage;
- stale;
- non-resolving;
- independently contradictory;
- expensive to reconcile.

I21 removes that privileged interpretation step from evidence planning.

## Shared runtime layers

The common organism now separates:

```text
runtime evidence records
        |
        v
EvidenceLineageRegistry
  source lineage
  current/stale
  resolves claim?
  conflict across resolving lineages
        |
        + learned source-quality estimates
        + consequence / asymmetric harm
        + independent evidence cost
        v
EvidenceAssuranceDecision
  use_current
  acquire_independent
  unresolved
        |
        v
OrganismRecoveryCoordinator
  historical execution decision
  + current authority for any new attempt
```

None of these layers gets to manufacture the semantics owned by another layer.

## Recovery-coordinator integration

`OrganismRecoveryCoordinator.plan_external_execution_evidence(...)` now:

1. queries `EvidenceLineageRegistry` for the external-effect claim;
2. receives lineage/resolution/staleness/conflict structure;
3. combines it with learned current/independent error estimates, consequence, duplicate/omission harm and reconciliation cost;
4. calls the same `EvidenceAssuranceDecision` used by I20;
5. returns one of:
   - use current evidence;
   - acquire another independent failure lineage;
   - preserve unresolved execution state.

Only after execution evidence is resolved enough does PS-025's external-effect recovery path answer whether to mark history complete or consider a new retry. Current capability authority continues to gate the new attempt separately.

## Semantic integration tests

Six cases pin the new boundary:

- three copied records from one good lineage can still be used when another check is not worth its cost;
- stale lineage evidence triggers independent reconciliation when valuable;
- contradiction across independent lineages can trigger another independent source;
- the same contradiction can remain unresolved when another source is too expensive;
- a non-resolving observation such as timeout/absence-of-result is not upgraded into execution confirmation;
- evidence planning requires an explicit lineage registry instead of silently assuming record independence.

## Architecture consequence

The crash-aware organism no longer needs separate hard-coded policies for:

```text
external receipts
verifier audits
```

The shared abstraction is now:

```text
typed evidence provenance
        +
learned source quality
        +
consequence / cost
        ->
assurance allocation
```

This is direct executable support for PS-013 and PS-014 across two domains, with PS-025 consuming the result for external execution.

## What remains intentionally separate

The runtime still does **not** collapse:

- evidence provenance into reliability;
- reliability into truth;
- truth/history into current permission;
- independent evidence count into record count;
- unresolved evidence into a default positive or negative label.

Those separations are all experimentally motivated.

## Next hardening target

The next high-value state-migration problem is no longer basic publication/recovery. It is **transient cognitive state across structural recovery**:

- bounded hot caches/predictive state;
- delayed causal-credit eligibility traces;
- tentative hypotheses/work-in-progress;
- events that reference old scopes or state versions.

The test should determine which transient state must survive a crash/topology handoff, which can be safely rematerialized from source evidence, and which should deliberately be discarded because restoring it is more dangerous/expensive than recomputation.

That will connect PS-012, PS-015, PS-022 and PS-024 inside the same recovery lifecycle.
