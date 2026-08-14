# Implementation-Neutral Required Functions

**Status: Phase-7 synthesis candidate set, not a component diagram.**

A required function is a capability/problem the eventual system must address. Several functions may be implemented by one mechanism; one function may require several cooperating mechanisms. The list deliberately avoids contemporary implementation names.

## F01 — Observation encoding and entity binding

Convert heterogeneous observations into representations that preserve relevant distinctions, uncertainty, identity and temporal/spatial correspondence.

Required properties: multimodal support where needed; modality-specific precision; cross-modal binding; provenance; entity continuity.

## F02 — Current-state estimation

Infer what is likely true now from partial/noisy observations, prior state, elapsed time and the system's own actions.

Required properties: uncertainty; multiple hypotheses when needed; stale-state detection; action-conditioned updates.

## F03 — Working-state management

Maintain the small subset of information/computation state required for the current task without forcing the entire available history into every operation.

Required properties: selection, replacement, compactness, fast access, recoverability/provenance.

## F04 — Persistent evidence and memory governance

Store useful experience/knowledge across time and control write, revision, consolidation, retrieval, archival and forgetting.

Required properties: temporal scope; provenance; confidence; contradiction/supersession semantics; applicability conditions.

## F05 — Knowledge/experience access

Retrieve or reconstruct the information most useful to the current decision rather than merely the most similar stored item.

Required properties: task/causal/temporal relevance; cost sensitivity; retrieval uncertainty; failure detection.

## F06 — Representation transformation and abstraction

Construct representations that preserve future-useful distinctions while making likely downstream computation cheaper.

Required properties: task relevance; uncertainty preservation; compositionality; controllable information loss; transfer under changing objectives.

## F07 — Predictive/world-state modeling

Predict action-conditioned future states/outcomes and support counterfactual evaluation before expensive interaction.

Required properties: decision relevance; uncertainty propagation; model-validity estimation; multiple timescales; mismatch learning.

## F08 — Active information acquisition

Choose observations, queries, probes or interactions that reduce decision-relevant uncertainty when their expected value exceeds cost/risk.

Required properties: value-of-information reasoning; reversible probing where possible; sensor/tool selection.

## F09 — Operation selection / inference control

Choose what computation should happen next.

Candidate operation classes: direct solve, internal refinement, retrieve, simulate, branch, execute, use specialist tool, delegate, verify, ask, store, stop.

Required properties: marginal-value estimation; budget awareness; latency/risk sensitivity; stopping.

## F10 — Search and alternative management

Explore multiple hypotheses/solutions when one trajectory is insufficient and preserve useful partial results or diversity.

Required properties: branch allocation; pruning; backtracking/retention; diversity; evaluator integration; termination.

## F11 — External action and tool execution

Translate decisions into environment-changing operations through bounded interfaces.

Required properties: schema/state awareness; preconditions; error recovery; effect observation; authority limits; reversibility where possible.

## F12 — Delegation and coordination

Partition work among specialized/parallel processes when decomposition benefit exceeds communication/aggregation cost.

Required properties: scope isolation; information interfaces; synchronization; diversity/independence estimation; aggregation.

## F13 — Uncertainty and confidence management

Maintain behaviorally meaningful uncertainty about state, predictions, memories, outputs and evaluators.

Required properties: calibration; scope/regime metadata; consequence-sensitive thresholds; escalation/evidence acquisition.

## F14 — Verification and evaluation

Generate scoped evidence about correctness, utility, safety or invariants of candidate outputs/state transitions.

Required properties: property-specific checks; evaluator reliability/independence; process/outcome/formal checks as appropriate; exploitability estimation.

## F15 — Authority and capability control

Determine what operations a component is permitted to perform independently of what it is capable of proposing.

Required properties: least privilege; instruction/data provenance; sandboxing; authorization; effect limits; audit.

## F16 — Learning signal extraction and credit assignment

Convert observations, outcomes, demonstrations, preferences, verifiers and prediction errors into information about what should change and where responsibility lies.

Required properties: delayed/long-horizon credit; local/global signals; nondifferentiable boundaries; evaluator uncertainty.

## F17 — Change/substrate routing

Choose which mutable substrate should absorb new information or improvement and at what persistence timescale.

Possible persistence classes: temporary state, memory, procedure/skill, runtime policy, parameter delta/shared parameters, structural design.

Required properties: confidence; expected reuse; interference; provenance; rollback; consolidation criteria.

## F18 — Continual stability and functional forgetting

Learn under nonstationarity without unacceptable interference while also retiring obsolete beliefs/behaviors when appropriate.

Required properties: transfer/retention measurement; stability control; selective replay/refresh; deliberate forgetting; regime-change detection.

## F19 — Consolidation / amortization

Compile repeated expensive successful computation or experience into cheaper reusable forms when lifetime savings exceed learning/validation cost.

Required properties: reuse estimation; information-loss checks; source provenance; rollback; revalidation after environment change.

## F20 — Physical resource scheduling

Map abstract operations/state to hardware execution under memory, bandwidth, communication, latency, precision, energy and parallelism constraints.

Required properties: locality; placement; precision allocation; batching/asynchrony; realized-cost measurement.

## F21 — Monitoring and anomaly detection

Observe internal/external signals that indicate failure, drift, attack or unexpected behavior.

Required properties: multiple layers; calibration; adversarial robustness; diagnostic provenance; escalation rather than unsupported direct intervention.

## F22 — Transactional persistence and recovery

Make durable/irreversible changes only after sufficient evidence and preserve ability to inspect, version, rollback or recover.

Required properties: staging; atomic activation; immutable/independent audit evidence; recovery points; compatibility/migration checks.

## F23 — Self-improvement attribution and variant search

Diagnose which system layer limits performance, generate candidate mutations/variants, preserve useful alternative lineages and select improvements using lifetime utility.

Required properties: causal attribution; diverse candidate search; hidden regressions; protected evaluators; lineage; meta-mutation controls.

## F24 — Objective/utility representation

Represent what outcomes matter sufficiently to guide decisions, learning, search, resource allocation and trade-offs without silently collapsing all objectives into a single exploitable proxy.

Required properties: multiple objectives/constraints; uncertainty/ambiguity; provenance of authority; explicit trade-offs; resistance to proxy substitution.

## F25 — Human/external communication interface

Translate between human conventions and internal machine representations without requiring internal computation to use human language.

Required properties: faithful intent extraction; uncertainty/clarification; inspectable summaries; machine-native internal bandwidth; authority separation between messages and external data.

---

## Important note

This is **not** a proposal for 25 modules.

The clean-sheet problem is to discover the smallest set of mechanisms that jointly implement these functions with good capability, learning dynamics and physical efficiency. Combining functions can reduce overhead; separating functions can reduce interference and improve verification. Which boundaries are real is an experimental question.
