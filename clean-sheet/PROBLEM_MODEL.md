# Clean-Sheet Problem Model

**Phase 8: implementation vocabulary deliberately removed.**

## 1. System problem

The system exists in an environment it cannot observe perfectly. It receives observations, has objectives/constraints that may themselves be uncertain, maintains internal state, can perform internal computations and external actions, and has finite physical resources.

At any point it must choose among possible state transitions.

Abstractly:

`S_t = {belief, evidence, working state, learned structure, objectives, uncertainty, authority, resources, lineage}`

Given available operations `O_t`, choose a transition `o ∈ O_t` whose expected future value justifies its cost and risk.

The system must operate even when:

- observations are incomplete/noisy;
- objectives are ambiguous/conflicting/changing;
- the environment changes independently;
- computations/evaluators can be wrong;
- useful information exceeds active-state capacity;
- some actions are irreversible or high-consequence;
- resource prices/availability change;
- the system itself changes over time.

## 2. State classes

These are semantic classes, not required physical stores.

### 2.1 Momentary computational state

Intermediate values used during one operation and safely discardable afterward unless promoted.

Properties: very fast; reversible; limited lifetime.

### 2.2 Working state

Information actively relevant to the current task/decision.

Properties: small enough for cheap repeated access; replaceable; linked to source evidence where needed.

### 2.3 Evidence history

Time-scoped observations, actions, outcomes and source records.

Properties: provenance; append/history semantics; audit/reconstruction value; not automatically current truth.

### 2.4 Current belief state

Best current estimate of relevant environment/internal variables.

Properties: uncertainty; temporal validity; update from action + observation; multiple hypotheses where necessary.

### 2.5 Reusable knowledge/procedure state

Generalized facts, rules, procedures and skills derived from repeated/validated evidence.

Properties: applicability conditions; confidence; source links; cheaper reuse than re-derivation.

### 2.6 Durable learned computational state

Slow-changing integrated structure that shapes future representation, prediction, operation selection and learning.

Properties: high reuse/integration; expensive validation/rollback; potential broad interference.

### 2.7 Objective/constraint state

Current representation of goals, preferences, hard limits, risk tolerance and uncertainty about them.

Properties: authority/provenance; conflict handling; time/scope; not assumed to be one scalar.

### 2.8 Authority/control state

Defines which components/operations may cause which effects and which evidence is required.

Properties: independently enforceable where high consequence; protected provenance; explicit scope/duration.

### 2.9 Lineage/recovery state

Version history, accepted changes, parent-child relationships, test evidence and rollback points.

Properties: tamper-resistant relative to candidate change; supports comparison/recovery.

## 3. Operation classes

The clean-sheet system may need operations with semantics equivalent to:

- transform/encode information;
- update current belief;
- retrieve evidence/knowledge;
- compress/abstract;
- expand/refine working state;
- generate alternative hypotheses/solutions;
- compare/select alternatives;
- predict future consequences;
- acquire new information;
- execute an external action;
- delegate/coordinate computation;
- verify a property;
- update a mutable substrate;
- consolidate repeated computation into reusable state;
- forget/retire obsolete active state;
- fork a system variant;
- test a variant;
- activate or rollback a durable change;
- communicate with humans/external systems;
- stop.

The final architecture may combine many of these semantics inside fewer primitives.

## 4. Transition value

A transition cannot be evaluated only by immediate task score.

Relevant terms include:

- expected objective/preference improvement;
- objective uncertainty;
- state/model uncertainty;
- information gained;
- future reuse/amortization;
- compute/memory/bandwidth/energy/time cost;
- communication/synchronization cost;
- risk and severity of failure;
- reversibility;
- privilege/authority required;
- effect on future learning data;
- maintenance/complexity cost;
- opportunity cost.

These terms need not be collapsed permanently into one scalar; some may remain hard constraints or Pareto dimensions.

## 5. Central design question

The clean-sheet design problem is:

> What is the smallest set of learnable and deterministic mechanisms that can implement these state-transition semantics, adapt their allocation policies from experience, remain physically efficient, and preserve enough independent assurance to detect and recover from their own errors?

Nothing in this statement requires a specific neural architecture, language representation, memory implementation, number of components or hardware family.
