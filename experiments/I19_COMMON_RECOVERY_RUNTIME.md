# I19 — Common Crash-Aware Organism Recovery Runtime

**Status:** implemented composition checkpoint. No new provisional principle is added.

## Goal

I14–I18 originally tested recovery semantics in separate model families. I19 moves those semantics behind the same reusable runtime used for topology, resource ownership, authority and event work.

The integration is intentionally small:

- `PublicationProtocol` stamps publication provenance at the same modeled authoritative commit as topology/lease state;
- `RecoveryRecord` can use publication provenance even when numeric target version is unknown;
- `OrganismRecoveryCoordinator` derives resource/topology recovery records from prepared publications and observes current authoritative runtime state;
- external effects use PS-025's separate external-execution evidence + current-authority decision path.

## Publication provenance is authoritative state

`ResourceLease` now optionally carries `publication_ref`.

`TypedScopeRuntime` carries `topology_publication_ref` for the current topology epoch.

`PublicationProtocol.publish(...)` stamps those values while it changes the lease/epoch rather than updating a side registry afterward.

This matters because:

```text
publish authority
    |
CRASH
    |
write provenance later
```

would recreate I14's ambiguity.

The model-level coherence boundary is now:

```text
new authoritative state
+ publication provenance
```

as one semantic publication.

## Unknown target numeric version

Resource leases use a runtime-wide version allocator. An unrelated resource can advance that allocator after a handoff is prepared while the prepared resource's own base fence remains unchanged.

I19 tests:

1. prepare `primary: holder 0`;
2. transfer an unrelated resource, advancing the global lease sequence;
3. publish `primary -> holder 1`;
4. recover using `target_version=None` plus publication provenance.

Recovery marks the handoff complete even though the final lease version was not predictable at preparation time.

## Common recovery decisions

The coordinator now produces the same typed outcomes for real runtime state:

```text
resource/topology publication
    already authoritative -> mark_complete
    same expected base + current checks -> retry_publish
    advanced through another publication -> discard/superseded
    conflict/inconsistent -> halt

external effect
    effect-specific applied evidence -> mark_complete
    exact absent + current authority -> retry
    exact absent + revoked -> blocked
    receiver-recognized identity + authority -> retry_same_identity
    non-identifiable ambiguous state -> unresolved / risk-priced retry-abstain
```

## Composition tests

Nine integration cases cover:

- prepared resource retry from unchanged base;
- already-published resource completion after later revocation;
- superseding resource change;
- unrelated global lease versions before publication;
- prepared topology recovery;
- published topology provenance;
- already-applied external effect after revocation;
- absent external effect after revocation;
- non-identifiable external effect remaining unresolved.

Separate provenance-runtime tests verify resource/topology publication tags and crash recognition with unknown target version.

## Architecture consequence

The current runtime no longer needs experiment-specific hidden facts to answer basic recovery questions.

The same semantic spine now covers:

```text
prepare
validate
publish
crash
restart
classify authoritative state
reacquire current validation if retry is needed
complete / retry / discard / block / remain unresolved
```

This still does not select a persistence engine. The runtime API says **what semantic records must survive**, not how bytes are durably stored.

## Remaining gap

I17 shows that external evidence can be correlated/stale. The recovery coordinator currently receives an already-interpreted `ExternalExecutionObservation`.

The next integration layer should therefore make evidence provenance/failure lineage part of the assurance input, so the coordinator itself can decide whether to:

- trust current external execution evidence;
- acquire independent reconciliation;
- retain unresolved execution state.

That should reuse PS-013/014 rather than create a special external-evidence controller.
