# Clean-Sheet Assurance and Change Protocol

**Phase 8 — transition semantics, not a particular security/product architecture.**

The system causes many kinds of state transition, from disposable intermediate computation to durable self-modification. The acceptance process should depend on the transition's blast radius rather than use one universal gate.

## 1. Transition descriptor

Before a consequential transition is authorized, represent:

`T = {operation, target, scope, persistence, privilege, reversibility, uncertainty, objective impact, dependencies, proposed evidence, resource cost}`.

### operation

What transformation/action is requested.

### target

Which environment/internal state may change.

### scope

How much of the system/environment is affected.

### persistence

How long effects survive and how broadly future computation reuses them.

### privilege

Authority/resources required.

### reversibility

Whether/how the transition can be undone and at what cost.

### uncertainty

Uncertainty about state, objective, predicted effects and evaluator reliability.

### objective impact

Which objectives/constraints could improve or degrade.

### dependencies

Preconditions and components/state whose compatibility matters.

### proposed evidence

Checks that will establish enough confidence to proceed.

### resource cost

Execution + assurance + recovery opportunity cost.

---

## 2. Assurance classes

These are semantic classes; exact thresholds remain deployment/research variables.

### A0 — Disposable internal computation

Characteristics: no durable/external effect; cheap to discard.

Typical requirements: resource bound; no privileged side effect.

### A1 — Reversible local state change

Characteristics: task/session state or easily reverted working state.

Typical requirements: basic validity/schema checks; provenance.

### A2 — Persistent editable information/procedure

Characteristics: future behavior can be influenced across sessions; state remains directly editable/revisable.

Typical requirements: provenance, consistency/applicability checks, versioning, ability to supersede/rollback.

### A3 — External or privileged action

Characteristics: changes environment/resources or accesses restricted capability.

Typical requirements: current-state/precondition check, least privilege, predicted side effects, appropriate independent verification/authorization, post-effect observation.

### A4 — Broad durable learned/runtime change

Characteristics: affects many future tasks, may cause interference or change generated traces.

Typical requirements: branch/version, target tests, hidden/independent regressions, cost comparison, migration plan, rollback, monitoring.

### A5 — Structural/control/meta-change

Characteristics: changes computation organization, learning/update policy, evaluator/control path, mutation process or recovery assumptions.

Typical requirements: strongest available independent acceptance path; adversarial/hidden evaluation; old/new parallel comparison where feasible; protected recovery lineage; staged activation; post-deployment monitoring; explicit authority to alter control semantics.

No class label is intrinsically safe; it only selects the expected assurance burden.

---

## 3. Generic transition protocol

### Step 1 — Describe

Specify target, expected benefit, affected objectives/constraints, scope, persistence and privileges.

Reject transitions that cannot identify their target/effect well enough for the consequence level.

### Step 2 — Check current state and preconditions

Verify that the world/system assumptions used to justify the change are still valid.

### Step 3 — Predict effects

Use available causal/predictive knowledge to estimate intended effects, side effects and uncertainties.

### Step 4 — Bound authority/resources

Grant only capabilities/resources needed for the candidate transition/test.

### Step 5 — Stage/fork when persistence warrants it

Create a candidate state/version without destroying the currently accepted version.

### Step 6 — Evaluate target benefit

Measure whether the change addresses the diagnosed problem.

### Step 7 — Evaluate broader regressions

Check properties outside the optimized target: existing competence, resource cost, calibration, memory/state integrity, authority behavior and other consequence-relevant dimensions.

### Step 8 — Use independent/hidden evidence as required

As optimization pressure and blast radius rise, increase evidence independence and reduce reliance on checks directly optimized by the candidate.

### Step 9 — Compare lifetime utility

Include deployment cost, maintenance, future trace/data effects, assurance burden and rollback risk—not only immediate score.

### Step 10 — Authorize or reject

Acceptance authority must be outside the candidate's uncontrolled mutation scope.

### Step 11 — Activate atomically or within explicit staged scope

Avoid ambiguous half-migrated states when possible.

### Step 12 — Verify actual effects

Observed post-transition state overrides predicted state; record mismatches.

### Step 13 — Monitor

Track delayed regressions, drift, security anomalies and resource changes.

### Step 14 — Consolidate, retain alongside predecessor or rollback

Do not destroy alternatives/history until evidence justifies pruning.

---

## 4. Independent evidence

Evidence independence is about differing failure sources, not simply number of checks.

Potentially independent evidence can come from:

- deterministic invariants;
- formal property checking;
- independent environment observations;
- separately trained/implemented evaluators;
- hidden or rotated tests;
- adversarial candidate generation;
- old-version comparison;
- user/external authorization;
- effect-level measurements after execution.

A candidate and evaluator sharing training data, state, assumptions or incentives should be treated as partially correlated.

---

## 5. Trusted-root migration

A control/assurance component may eventually need improvement. The rule is not permanent immutability; it is **non-circular transition authority**.

For assurance-system change:

1. preserve the old accepted authority/recovery path;
2. construct candidate new assurance state in isolation;
3. validate new state against hidden/adversarial and historical cases;
4. verify that it correctly rejects deliberately unsafe candidates;
5. migrate authority only through a path the candidate cannot unilaterally redefine;
6. retain rollback to old assurance state until sufficient operational evidence accumulates.

If both old and new systems have known limitations, an external/higher-level authority or formally constrained migration process may be required.

---

## 6. Persistent memory changes

Memory is a state transition and can have broad future effects.

Candidate durable memory should distinguish:

- raw external observation;
- derived/inferred record;
- current-state update;
- generalized rule/procedure;
- authority-bearing preference/instruction.

Higher-authority or broadly generalized memories require stronger validation than ordinary episode archival.

Memory retrieved later inherits its original authority/provenance; persistence does not promote trust.

---

## 7. Objective changes

Changing the objective/constraint state is more sensitive than changing an ordinary belief.

Requirements include:

- source authority;
- scope/time;
- conflict detection with existing constraints;
- evidence that a preference truly changed rather than one noisy observation;
- no self-generated content silently becoming an objective;
- explicit exception process for changes to hard constraints.

---

## 8. Learning/consolidation changes

Before promoting repeated behavior into more durable integrated state, evaluate:

- reuse frequency;
- stability across contexts;
- confidence/source diversity;
- generalization beyond triggering cases;
- interference with existing capability;
- information/provenance loss;
- rollback/alternative availability;
- expected lifetime compute savings.

Durability should be earned by evidence and reuse, not simply by repetition.

---

## 9. Structural/meta changes

A structural change may alter:

- available operations;
- state representation;
- update/learning dynamics;
- communication protocols;
- physical scheduling;
- candidate-generation/mutation distribution;
- evaluator/control interfaces.

Therefore structural tests must include migration/compatibility and future-improvement behavior, not only current task performance.

A meta-change that improves current score while making future variants impossible to validate is not necessarily an improvement.

---

## 10. Rollback semantics

Rollback should restore a **compatible system state**, including as required:

- executable/learned computation version;
- persistent-state schema;
- memory/index interpretation;
- communication protocols;
- objective/control state;
- evaluator/test version;
- caches/derived state that cannot safely cross versions.

Rollback is not just loading old code/parameters.

---

## 11. Assurance budget policy

A conceptual assurance demand function is:

`AssuranceDemand(T) ↑ with consequence + scope + persistence + privilege + irreversibility + uncertainty + evaluator exposure/optimization pressure`.

This should not necessarily be one numeric formula. Some terms can impose minimum categorical requirements.

The system should also account for the **cost of false rejection** so assurance does not become a universal blocker.

---

## 12. Failure conditions requiring immediate containment

Candidate architecture should define responses when:

- authority metadata becomes inconsistent;
- audit/recovery state is unexpectedly modified;
- candidate attempts to access hidden evaluators/tests outside allowed interface;
- post-action effects contradict high-confidence prediction;
- resource consumption exceeds bound;
- evaluator disagreement exceeds allowed threshold;
- memory/objective state receives high-authority change from untrusted source;
- rollback verification fails;
- protocol/schema version mismatch could corrupt persistent state.

Containment may mean stop, reduce capability, revert, isolate state, request external review or acquire more evidence. Exact response is implementation/deployment-specific.
