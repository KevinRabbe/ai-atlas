# Clean-Sheet Functional Specification

**Phase 8 — implementation-independent capability contracts.**

This document defines what the system must be able to do, not how many components it contains or which computational substrate implements each function. Several contracts may be satisfied by one mechanism; one contract may require multiple cooperating mechanisms.

## Contract notation

Each function is described by:

- **Purpose** — why the function exists.
- **Consumes** — state/evidence it may read.
- **Produces** — state transition or evidence it may create.
- **Must preserve** — invariants that cannot be silently lost.
- **Must expose** — information needed by downstream control/verification.
- **Failure signal** — how the larger system can know the function may have failed.

---

# A. Perception, state and representation

## F01 — Observation interpretation and entity binding

**Purpose:** Convert raw observations into state that preserves task-relevant distinctions and identifies which observations refer to the same persistent entities/processes.

**Consumes:** raw observations; modality/source metadata; prior entity hypotheses; current belief state.

**Produces:** interpreted features/events; entity references; uncertainty; source/time metadata.

**Must preserve:** exact identifiers where exactness matters; source provenance; ambiguity rather than forcing identity when evidence is weak.

**Must expose:** confidence in entity binding; information lost by abstraction when known; unresolved alternatives.

**Failure signal:** incompatible observations mapped to one entity; one entity split incorrectly; downstream prediction/action repeatedly contradicts bindings.

## F02 — Current-state estimation

**Purpose:** Maintain the best current estimate of hidden/mutable environment state.

**Consumes:** prior belief; elapsed time; own actions; new observations; predictive state model.

**Produces:** revised belief distribution/set; uncertainty; stale-state indicators.

**Must preserve:** distinction between evidence and inferred current state; unresolved hypotheses when materially different.

**Must expose:** what changed, why belief changed, remaining uncertainty, age of supporting evidence.

**Failure signal:** repeated prediction mismatch; new observation incompatible with high-confidence state; state depends on superseded evidence.

## F03 — Working-state management

**Purpose:** Keep currently useful information cheap to access while larger evidence/history remains outside the hot path.

**Consumes:** goal; belief; candidate memories/evidence; intermediate computation.

**Produces:** bounded active working set; eviction/promote decisions; references to external state.

**Must preserve:** dependencies/provenance needed to reconstruct important conclusions; unresolved uncertainty relevant to decisions.

**Must expose:** why items were selected/evicted; active resource occupancy.

**Failure signal:** repeated retrieval of just-evicted information; important dependency missing; active-state growth dominates compute.

## F04 — Representation transformation and abstraction

**Purpose:** Change information form/granularity so future computation becomes cheaper while retaining required distinctions.

**Consumes:** observations, evidence, belief, working state, procedures.

**Produces:** compressed/structured/latent/discrete representations plus references to source state where needed.

**Must preserve:** required exact fields; uncertainty; authority/provenance; information needed by expected downstream tasks.

**Must expose:** representation schema/version; known lossy dimensions; compatibility requirements.

**Failure signal:** transformed state cannot support known task that source state could; protocol mismatch; lost uncertainty/provenance.

---

# B. Persistent information and knowledge

## F05 — Evidence persistence and memory governance

**Purpose:** Decide what should survive beyond the current task and manage its lifecycle.

**Consumes:** candidate events/results; confidence; future-use estimate; storage budget; policy/authority constraints.

**Produces:** persisted evidence/knowledge; revision/supersession links; archive/forget decisions.

**Must preserve:** provenance; temporal scope; authority; confidence; distinction between event history and current belief.

**Must expose:** write reason; dependencies; revision history; active/archive status.

**Failure signal:** contradiction accumulation; stale state repeatedly retrieved; memory growth without downstream value; unsupported durable belief.

## F06 — Experience abstraction and reusable knowledge formation

**Purpose:** Derive reusable facts, procedures, heuristics or failure knowledge from multiple episodes.

**Consumes:** episodes; outcomes; verification results; applicability conditions.

**Produces:** generalized reusable state plus evidence links and scope conditions.

**Must preserve:** exceptions that materially affect safe application; source evidence sufficient for later revision.

**Must expose:** supporting episode count/diversity; confidence; applicability boundary.

**Failure signal:** generalized rule fails outside training episodes; exceptions erased; unsupported confidence rises through self-reference.

## F07 — Knowledge/experience access

**Purpose:** Make the information most useful to the current decision available at acceptable cost.

**Consumes:** goal; belief; active state; persistent evidence/knowledge; expected action/computation value.

**Produces:** selected evidence/knowledge with relevance/confidence metadata.

**Must preserve:** temporal validity; source; distinction between current and historical state.

**Must expose:** selection rationale/score factors; retrieval uncertainty; alternatives when ambiguity matters.

**Failure signal:** semantically close but operationally wrong retrieval; repeated retrieval misses later discovered as decisive; obsolete evidence overrides live observation.

---

# C. Prediction, uncertainty and information acquisition

## F08 — Predictive state transition modeling

**Purpose:** Estimate plausible consequences of candidate actions/time evolution before committing.

**Consumes:** current belief; candidate action; context; learned/known dynamics.

**Produces:** predicted future state/outcomes; uncertainty; model-validity indicators.

**Must preserve:** action conditioning; uncertainty growth; relevant alternative futures.

**Must expose:** prediction horizon; assumptions; model confidence; variables omitted/abstracted when known.

**Failure signal:** systematic observation mismatch; excessive confidence under extrapolation; predictions fail after regime change.

## F09 — Active information acquisition

**Purpose:** Obtain new evidence when reducing uncertainty is worth the cost/risk.

**Consumes:** decision uncertainty; available sensors/queries/probes; consequence; information cost.

**Produces:** new observation/evidence or explicit decision not to query.

**Must preserve:** authority/privacy limits; distinction between observation and intervention.

**Must expose:** expected value of acquisition; cost/risk; evidence source.

**Failure signal:** repeated expensive queries with no decision impact; irreversible probe used when safer evidence existed; action proceeds despite cheap decisive information.

## F10 — Uncertainty/confidence management

**Purpose:** Track uncertainty about state, predictions, memories, objectives, evaluators and candidate actions.

**Consumes:** local confidence signals; disagreement; prediction errors; distribution/regime indicators.

**Produces:** calibrated or behaviorally meaningful uncertainty attached to state/operations.

**Must preserve:** scope/regime; separation of uncertainty sources where operationally relevant.

**Must expose:** enough signal for escalation, verification and stopping decisions.

**Failure signal:** confidence unrelated to error; uncertainty disappears across summaries/interfaces; correlated agreement produces unjustified certainty.

---

# D. Inference, search and coordination

## F11 — Operation selection and stopping

**Purpose:** Choose the next internal/external operation and terminate when additional work is not worth its cost.

**Consumes:** goal/objectives; current state; uncertainty; available operations; budgets; reliability/cost models.

**Produces:** selected operation, resource budget and stopping decision.

**Must preserve:** hard constraints; authority limits; opportunity cost.

**Must expose:** operation identity; allocated budget; reason/expected value estimate sufficient for audit at appropriate granularity.

**Failure signal:** runaway computation; premature stop despite high-value available evidence; repeated low-value operation loops.

## F12 — Alternative generation and search

**Purpose:** Explore multiple hypotheses/solutions when one path is unreliable.

**Consumes:** problem state; current candidates; mutation/branch operations; evaluation signals; search budget.

**Produces:** candidate set/population/tree/graph or equivalent; retained partial results; pruning decisions.

**Must preserve:** useful diversity; candidate provenance; uncertainty about pruning.

**Must expose:** search budget, candidate lineage and selection evidence.

**Failure signal:** all branches near-identical; search cost grows without quality gain; correct region pruned systematically; evaluator exploitation.

## F13 — Delegation and coordination

**Purpose:** Divide work among computational processes when specialization, isolation or parallelism exceeds coordination cost.

**Consumes:** decomposable task state; available capabilities; communication/latency budget.

**Produces:** subproblem assignments; scoped state/messages; aggregated results.

**Must preserve:** task dependencies; authority boundaries; provenance; uncertainty from each result.

**Must expose:** worker/process identity/version; information exchanged; aggregation confidence.

**Failure signal:** duplicate work; dependency conflict; communication dominates; correlated errors mistaken for independent evidence.

## F14 — Internal/external communication

**Purpose:** Transfer useful state between machine processes or between machine and human/external systems.

**Consumes:** source state; receiver contract; bandwidth/fidelity/authority requirements.

**Produces:** typed/versioned message plus metadata.

**Must preserve:** required semantics, uncertainty, provenance and authority separately from payload format.

**Must expose:** sender/receiver version; schema; compression/fidelity; trust class.

**Failure signal:** protocol drift; decode/meaning mismatch; authority changes during translation; bandwidth dominates useful work.

---

# E. Action and environment interaction

## F15 — External action execution

**Purpose:** Cause controlled changes in the environment.

**Consumes:** authorized action proposal; preconditions; current belief; permissions; execution interface.

**Produces:** environment transition request/result; observed effects; errors.

**Must preserve:** scope limits; auditability; reversibility where promised.

**Must expose:** exact requested/actual effect; authority used; side effects known/observed.

**Failure signal:** unexpected side effect; precondition invalid; action result inconsistent with model; privilege exceeds task scope.

## F16 — Capability/authority enforcement

**Purpose:** Decide what effects each component/task is allowed to cause independently of its cognitive capability.

**Consumes:** task authority; component identity; requested operation; resource/side-effect scope; assurance evidence.

**Produces:** permit/deny/reduce-scope/escalate decision.

**Must preserve:** least privilege; authority provenance; duration/scope.

**Must expose:** enforced capability set and reason for exceptional escalation.

**Failure signal:** untrusted data changes authority; privilege persists after scope expires; component bypasses enforcement path.

---

# F. Verification, monitoring and assurance

## F17 — Property verification/evaluation

**Purpose:** Generate scoped evidence that a candidate state transition satisfies specific required properties.

**Consumes:** candidate; property/specification; checker/evaluator; assumptions.

**Produces:** pass/fail/score/uncertainty plus property scope and evidence provenance.

**Must preserve:** distinction between checked and unchecked properties.

**Must expose:** checker identity/version; assumptions; reliability/coverage where known.

**Failure signal:** proxy/gold divergence; checker disagreement; evaluator distribution shift; test gaming.

## F18 — Monitoring/anomaly detection

**Purpose:** Detect unexpected internal/external behavior during and after operation.

**Consumes:** runtime signals, state changes, resource patterns, prediction errors, security events.

**Produces:** anomaly evidence; escalation/block/review triggers.

**Must preserve:** monitor independence where required; evidence history.

**Must expose:** what signal triggered concern and confidence/coverage.

**Failure signal:** known incidents occur without trigger; high false-positive rate causes bypass; monitor can be trivially optimized around.

## F19 — Assurance allocation

**Purpose:** Choose how much independent checking, restriction, sandboxing or authorization a proposed transition deserves.

**Consumes:** uncertainty; consequence; privilege; persistence; reversibility; evaluator quality; optimization pressure.

**Produces:** assurance plan/gate strength.

**Must preserve:** minimum hard constraints; independence requirement for high-risk transitions.

**Must expose:** assurance basis and residual risk.

**Failure signal:** low-evidence irreversible transition accepted; trivial actions blocked by excessive assurance cost; repeated correlated checks treated as independent.

---

# G. Learning and persistent change

## F20 — Learning signal extraction and credit assignment

**Purpose:** Convert observations/outcomes/feedback into evidence about what should change and which state/process caused the outcome.

**Consumes:** trajectory/events; outcome; verification; prediction error; prior hypotheses about causality.

**Produces:** update/credit signals with causal confidence and target candidates.

**Must preserve:** evaluator uncertainty; temporal/source dependencies; distinction between correlation and causal evidence.

**Must expose:** target layer(s); confidence; delayed dependencies.

**Failure signal:** same failure persists after repeated updates; unrelated capability degrades; credit targets easy-to-change rather than causal state.

## F21 — Change/substrate routing

**Purpose:** Choose where new information/improvement should be stored and how persistent it should be.

**Consumes:** update evidence; expected reuse; confidence; volatility; interference risk; rollback/provenance needs.

**Produces:** chosen mutable state class, update scope and lifetime.

**Must preserve:** reversible path for uncertain changes when possible; applicability/provenance.

**Must expose:** why this substrate/lifetime was selected.

**Failure signal:** transient noise becomes durable; repeated stable behavior remains needlessly expensive; patch/adapter/skill proliferation.

## F22 — Continual stability, consolidation and forgetting

**Purpose:** Integrate useful new knowledge while preserving still-valid competence and retiring obsolete state.

**Consumes:** old/new competence evidence; memory/state; environment-change signals; resource budgets.

**Produces:** consolidated, retained, isolated, revised or retired state.

**Must preserve:** validation of important prior capability; audit history when needed.

**Must expose:** what was lost/retired and why; consolidation evidence.

**Failure signal:** catastrophic interference; obsolete behavior preserved; replay/retention cost grows without value; rare critical competence silently disappears.

---

# H. Physical resource realization

## F23 — Physical resource scheduling

**Purpose:** Realize abstract operations under finite compute, memory, bandwidth, communication, energy, precision and latency.

**Consumes:** operation graph/dependencies; state placement; hardware/resource availability; deadlines/budgets.

**Produces:** execution placement/order/precision/resource allocation and measured realized cost.

**Must preserve:** numerical/semantic fidelity requirements; authority isolation.

**Must expose:** wall-clock, memory movement, communication, energy/compute and bottleneck metrics as available.

**Failure signal:** theoretical savings increase realized cost; communication/synchronization dominates; precision error exceeds tolerance.

---

# I. Objective and metacontrol

## F24 — Objective/constraint interpretation

**Purpose:** Maintain structured, uncertain representation of goals, preferences, constraints and resource/risk trade-offs.

**Consumes:** authorized instructions/policies; preference evidence; demonstrations/corrections; environment consequences.

**Produces:** current objective/constraint state with uncertainty, authority and conflict semantics.

**Must preserve:** signal provenance; unresolved conflicts; hard/soft distinction where applicable.

**Must expose:** which objectives constrain a decision and where scalar/trade-off choices were introduced.

**Failure signal:** low-authority signal overrides stronger constraint; proxy score improves while intended effect worsens; objective drift without evidence.

## F25 — Cross-resource metacontrol

**Purpose:** Allocate compute, information acquisition, communication, learning, assurance and self-improvement according to expected lifetime value under uncertainty.

**Consumes:** current meta-state: objectives, uncertainty, operation capabilities/reliability, budgets, consequence, future-use estimates.

**Produces:** resource allocations and escalation between cheap local policies and expensive global deliberation where appropriate.

**Must preserve:** hard limits and authority; metacontrol cost must itself remain bounded.

**Must expose:** resource decisions at enough granularity to diagnose systematic allocation failure.

**Failure signal:** meta-control overhead exceeds savings; novel operations are starved; safety/assurance budget sacrificed to chase short-term score; recursive meta-analysis fails to terminate.

---

# J. Self-improvement and recovery

## F26 — System-variant diagnosis, search and selection

**Purpose:** Improve the system itself by localizing bottlenecks, generating alternative mutations and selecting variants by validated lifetime utility.

**Consumes:** failure/opportunity evidence; mutable-surface map; current lineage; mutation/search budget; independent evaluation.

**Produces:** candidate variants, test evidence, archive/selection decisions.

**Must preserve:** alternative lineages while uncertainty justifies them; protected acceptance authority; causal attribution evidence.

**Must expose:** exact mutation scope, parent, tests, costs, expected transfer and known regressions.

**Failure signal:** candidate wins by changing its evaluator; one lineage monopolizes search prematurely; broad mutation follows weak diagnosis.

## F27 — Transactional persistent change and recovery

**Purpose:** Make durable system changes without losing ability to inspect, compare, reject or roll back them.

**Consumes:** accepted candidate; assurance evidence; migration/compatibility checks; current recovery state.

**Produces:** staged/activated version, audit lineage, rollback point and post-activation monitoring plan.

**Must preserve:** acceptance evidence and recovery mechanism outside uncontrolled mutation scope.

**Must expose:** version relationship, activation scope/time and rollback target.

**Failure signal:** accepted state cannot revert; candidate controls only recovery path; state migration corrupts memory/authority; hidden regression appears after activation.

---

# Cross-contract invariants

Every implementation of these functions must respect the following cross-cutting rules:

1. **Evidence is not belief.** Observations/history remain distinguishable from current inferred state.
2. **Data is not authority.** Payload content cannot silently change permission or objective authority.
3. **Confidence is scoped.** Uncertainty cannot be promoted across transformations without preserving its regime/meaning.
4. **Persistence raises stakes.** More durable/broader mutations require stronger evidence or explicit exception authority.
5. **Capability is not permission.** Ability to propose/compute an action does not authorize its execution.
6. **Verification is property-scoped.** A successful check cannot silently certify untested properties.
7. **Lossy transformation is explicit.** Important abstraction/compression must make recoverability or known losses visible when relevant.
8. **Physical cost is real cost.** Abstract operation count cannot be the sole resource metric.
9. **Self-change cannot self-certify without independent evidence.** Mutation of acceptance/recovery paths requires a separate trusted transition.
10. **Stopping is valid.** The system may rationally choose not to compute, store, act, learn or self-improve further.
