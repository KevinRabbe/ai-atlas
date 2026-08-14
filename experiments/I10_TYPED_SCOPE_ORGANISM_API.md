# I10 — Persistent Typed-Scope Organism API

**Status:** implemented reusable architecture substrate plus integration scenario. No new provisional principle is added.

I10 is a deliberate change in experimental method: future architecture experiments should reuse one persistent runtime protocol rather than reimplementing identity, authority, topology, event and assurance semantics inside each synthetic policy.

## Why this exists

I04–I09 progressively derived the following boundaries:

- resource allocation can share machinery, but authority cannot be flattened into an ordinary value score;
- operation values can interact through complementarity/substitution;
- organizational mode, scope and membership can be adaptive;
- topology changes must not redefine exact semantic identity;
- in-flight work needs version/epoch semantics through reorganization;
- topology proposal evidence may require independent promotion evidence.

Before I10 those conclusions were implemented in separate experimental modules. That risks accidentally changing the architecture contract from experiment to experiment.

I10 therefore creates one common executable substrate: `TypedScopeRuntime`.

## Stable semantic API

The runtime exposes stable typed records for:

- `EvidenceRecord` — exact evidence ID, subject identity and source reference;
- `PredictiveRecord` — current predictive-state reference plus recoverable source reference;
- `AuthorityRecord` — current categorical permission plus monotonic version;
- `ResourceLease` — one exact resource identity, holder identity and lease version;
- `RuntimeEvent` — stable target identity, due step and topology epoch;
- `TransitionProposal` — typed proposed work/change with expected value, cost, uncertainty, consequence, reversibility and authority class;
- `AssuranceToken` — proposal-specific evidence with explicit independence/approval status;
- `TopologyChange` — staged old/new topology, moved subjects, consequence and promotion state.

These records are not scope-owned identities. Scope membership may change while the records remain valid.

## Runtime operations

### Evidence / predictive state

- `attach_evidence(...)`
- `register_predictive_state(...)`
- `rematerialize(...)`

### Authority / resources

- `set_authority(...)`
- `read_authority(...)`
- `lease_resource(...)`
- `transfer_resource(...)`

### Transition and resource allocation

- `propose_transition(...)`
- `allocate_bundle(...)`
- `execute_transition(...)`

The current experimental allocator is deliberately exact/small-set and can price explicit proposal interactions. This is an API semantic, not a commitment to brute-force allocation in a mature implementation.

### Assurance

- `request_assurance(...)`

A token is tied to one proposal and records whether its evidence is independent and approving. A high proposal value never upgrades the token's authority.

### Dynamic topology

- `stage_scope_change(...)`
- `commit_scope_change(...)`
- `rollback_scope_change(...)`

A sufficiently consequential/blast-radius structural change cannot commit without an independently approving assurance token for the exact topology-change proposal.

### Event continuity

- `enqueue_event(...)`
- `process_due_events(...)`

An event targets stable subject identity and carries the topology epoch at creation. If the topology changes before execution, the runtime marks/forwards it into the current epoch rather than treating its old scope as permanent addressing authority.

## Semantic tests

Eight API-level tests currently verify:

1. evidence/source, predictive rematerialization and resource leases survive a topology change;
2. one resource cannot be leased to two holders without an explicit versioned transfer;
3. arbitrarily high expected value cannot manufacture external capability authority;
4. durable knowledge promotion rejects non-independent self-assurance;
5. a sufficiently broad structural change requires independent assurance;
6. rollback leaves topology/epoch unchanged;
7. an old-epoch event forwards and processes exactly once;
8. bundle allocation can prefer a complementary pair over a stronger standalone proposal.

The local semantic suite passed 8/8 before connector publication.

## I10 integration scenario

`organism_runtime_scenario.py` drives multiple previously separate mechanisms through the API in one 900-step lifetime.

The scenario contains:

- three recurring hidden dependency regimes;
- learned pairwise coupling evidence;
- independently checked topology proposals;
- both accepted and rejected scope changes;
- authority revocation/restoration while external work is queued;
- delayed ordinary events;
- source-backed predictive-state rematerialization;
- competing runtime proposals with an explicit complementarity term;
- exact compute/verification resource leases.

No scenario code edits the runtime's topology, authority registry, evidence records, leases or event completion flags directly to bypass the API.

## 20-seed integration behavior

Mean behavior from the local validation sweep:

- topology epochs: ~`6.1`/lifetime;
- topology proposals: ~`8.55`;
- approved changes: ~`6.1`;
- independently rejected changes: ~`2.45`;
- old-epoch event forwards: ~`6.75`;
- queued external effects blocked by current revocation: ~`7.0`;
- queued events: ~`112.3`;
- processed events: ~`112.3`;
- predictive rematerializations: ~`35.7`;
- all semantic invariants true in every validated seed;
- exact resource leases remain singular.

The numerical task utility is intentionally not promoted as a new architecture result. I10's main purpose is **protocol integrity under composition**.

## Architectural consequence

The candidate system now has a reusable separation:

```text
semantic records
  stable IDs / provenance / authority / leases
          |
          v
transition proposals
          |
interaction-aware allocation
          |
assurance / authority boundary
          |
versioned execution + topology protocol
          |
observed outcome / later credit
```

Dynamic scopes become ordinary revisable state referenced by that protocol rather than containers that define the existence of everything inside them.

## Important non-commitments

I10 does **not** select:

- a database;
- an actor framework;
- an event-loop library;
- microservices;
- a control-plane/data-plane product architecture;
- an LLM or neural representation;
- a graph database;
- one global optimizer;
- A/B/C/D as a fixed architecture.

Those remain possible implementations only if later evidence earns them.

## Next stress

The first reusable-runtime stress should attack assumptions still baked into I10:

1. scopes are disjoint rather than overlapping/nested;
2. dependencies are mostly symmetric;
3. topology commit is atomic rather than partially failing;
4. one authority identity maps cleanly to one target subject;
5. migration does not yet move large bounded caches or partial credit traces;
6. assurance tokens are simple booleans rather than uncertain evidence objects.

The next experiment should begin with **overlapping/nested and asymmetric scopes** because those can reveal whether a single partition is already an accidental architecture assumption.
