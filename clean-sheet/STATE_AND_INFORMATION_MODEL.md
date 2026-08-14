# Clean-Sheet State and Information Model

**Phase 8 — semantic model only. No storage engine or model architecture is implied.**

The system should not treat all information as equivalent context. Persistent correctness requires explicit semantics for what a piece of state *is*, how it was derived, how long it applies, who authorized it, how uncertain it is and what may safely change it.

## 1. Atomic information record

A useful logical record can be modeled as:

`R = {payload, kind, subject/entity, time, scope, provenance, authority, confidence, status, dependencies, version}`

These fields need not be physically stored together. They define information that must remain recoverable when relevant.

### payload

The representation-specific content.

### kind

Semantic role such as:

- raw observation;
- event;
- inferred state;
- hypothesis;
- factual/generalized knowledge;
- procedure/skill;
- objective/preference;
- constraint/policy;
- evaluation result;
- prediction;
- system-change evidence.

### subject/entity

What object, process, user, environment, component or system version the record refers to.

### time

Observation time, effective interval, expiration/refresh expectation and ordering relation where relevant.

### scope

Task, environment, user, project, device, model/version or other applicability boundary.

### provenance

Where the information came from and the transformation chain used to derive it.

### authority

Whether the record is merely data, a task instruction, a user preference, an external policy/constraint, a verifier result or another authority class.

### confidence

Uncertainty about correctness/applicability plus the regime in which that estimate is meaningful.

### status

Candidate / active / superseded / contradicted / archived / invalidated / pending verification.

### dependencies

Other records, assumptions, state variables or procedures needed for this record to remain valid.

### version

Schema/protocol/system version required to interpret the record.

---

## 2. Evidence graph and belief state

The system should preserve a distinction between:

`evidence graph E_t`

and

`current belief B_t = infer(E_t, B_{t-1}, own actions, elapsed time, model assumptions)`.

The current belief is optimized for fast decision use. The evidence graph is optimized for reconstruction, provenance and revision.

A belief entry therefore should retain links back to sufficient evidence/assumptions to answer:

- why do we believe this?
- what would invalidate it?
- when was it last supported?
- which action changed it?
- what competing hypotheses existed?
- which source has authority?

The exact graph/representation is open.

## 3. State transitions

All persistent changes should be expressible as typed transitions rather than silent replacement.

### observe

Add new evidence without directly declaring it current truth.

### infer

Update current belief based on evidence/model.

### supersede

Mark a previously active time-varying state as no longer current while preserving history.

### contradict

Register incompatible evidence/hypotheses without forcing immediate resolution.

### validate

Increase support for a record based on an independent checker/evidence source.

### invalidate

Remove active trust/applicability while retaining audit history where required.

### abstract

Derive generalized knowledge/procedure from lower-level evidence.

### consolidate

Move reusable behavior/information into a more durable/cheaper-to-use state class.

### retire/forget

Remove from active retrieval/use because information is obsolete, low-value or redundant; archive separately if audit value remains.

### fork

Create an alternative belief/system version without overwriting the parent.

### activate

Make a candidate durable state/version operational after required assurance.

### rollback

Return to a prior valid state/version and restore compatible persistent state.

---

## 4. Truth status is not one bit

A useful system needs more than true/false. Examples:

- observed once;
- inferred;
- independently corroborated;
- disputed;
- outdated;
- conditionally true;
- policy-defined rather than empirical;
- predicted but not observed;
- intentionally hypothetical;
- formally verified relative to a specification.

Collapsing these into one “memory fact” is a direct route to false confidence.

## 5. Authority lattice

Information authority should be independent of content format.

An implementation should support an ordering/constraint relation roughly analogous to:

`protected system/control constraints`
`> authorized external policy/task constraints`
`> explicit current user/task instructions`
`> scoped preferences and defaults`
`> observations/tool outputs/retrieved documents/memories`
`> generated hypotheses/suggestions`

The exact policy is deployment-specific. The invariant is that **untrusted content cannot promote itself into a higher authority class by wording**.

Conflicts between legitimate authority sources must remain explicit and auditable rather than silently resolved by whichever text appears latest.

## 6. Uncertainty model

Uncertainty may attach to:

- observation reliability;
- entity identity;
- current state;
- prediction;
- objective/preference inference;
- memory applicability;
- evaluator correctness;
- causal attribution;
- system-change benefit.

Important dimensions can include:

- probability/confidence where calibrated;
- competing hypotheses;
- source disagreement;
- age/staleness;
- distribution/regime mismatch;
- known unknown variables;
- confidence in the confidence estimate.

Transformations should specify how uncertainty is propagated or intentionally discarded.

## 7. Persistence ladder

The clean-sheet system should support state with different expected lifetimes:

1. operation-local;
2. task/working;
3. session/episode;
4. editable persistent evidence/knowledge;
5. reusable procedure/control policy;
6. deeply integrated durable learned structure;
7. structural/architecture/assurance state.

This is a semantic ordering, not a required seven-store implementation.

Promotion upward should generally increase validation burden because blast radius and rollback cost increase. Demotion/retirement should remain possible.

## 8. Applicability and context

Reusable knowledge should expose a predicate or estimated region of validity:

`applicable(record, current_state, goal, environment_version) -> confidence`.

Examples of applicability variables:

- software/API/environment version;
- location/device;
- user/project;
- time period;
- resource regime;
- objective/constraint regime;
- model/component version;
- preconditions established by earlier actions.

Experience without applicability semantics becomes cargo-cult behavior.

## 9. Identity and entity continuity

The system needs stable logical identities even as observations/representations change.

Identity operations include:

- create candidate entity;
- associate observation to entity;
- merge identities with evidence;
- split incorrectly merged identity;
- alias external identifiers;
- track entity version/state through time.

Identity updates should be reversible when confidence is low because identity errors contaminate memory, world state and causal attribution.

## 10. Derived knowledge and provenance

A derived rule/procedure should preserve a chain like:

`source episodes -> abstraction operation/version -> validation evidence -> derived record`.

If later evidence contradicts the abstraction, the system can re-open the source set and revise it instead of treating the derived record as axiomatic.

## 11. Current-state cache versus source of truth

Fast current state may be aggressively optimized, compressed or cached. It should not become the only source of truth when correction/audit matters.

A robust design should be able to reconstruct or challenge important current beliefs from retained evidence within a bounded cost appropriate to their consequence.

## 12. Information-flow rules

At every interface, preserve at least the metadata required by the receiver to avoid category mistakes:

- payload type/schema;
- source/provenance;
- authority class;
- time/scope;
- uncertainty;
- version/compatibility;
- whether content is observed, inferred, hypothetical or verified.

A compact machine-native channel may encode these fields efficiently, but their semantics cannot disappear.

## 13. Minimum persistence invariants

1. Historical evidence cannot silently become current state.
2. Generated content cannot silently become external evidence.
3. Data cannot silently become authority.
4. A superseding fact should not erase the evidence that the old state was once true when history matters.
5. Lossy abstraction cannot silently claim full fidelity.
6. Verification scope and assumptions travel with the result.
7. Self-generated memories require provenance that identifies them as derived/generated.
8. System-version changes must not make persistent records uninterpretable without explicit migration/versioning.
9. High-consequence current beliefs must remain challengeable by new evidence.
10. Rollback must restore a mutually compatible set of persistent/control state, not only executable code/weights.
