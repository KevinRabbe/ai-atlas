# Clean-Sheet System Invariants

**Phase 8 — requirements candidate architectures must satisfy or explicitly challenge with evidence.**

These invariants are derived from cross-domain evidence/failure modes. They are not implementation prescriptions. A future experiment may weaken or replace one, but it must do so explicitly rather than violate it accidentally.

## I01 — Evidence/belief separation

Historical observations, generated hypotheses and current inferred state must remain distinguishable.

**Reason:** a once-correct observation can become false current state; generated content can self-reinforce if treated as evidence.

## I02 — Authority/data separation

Information content cannot elevate its own authority. Instructions, policy, preferences, observations and untrusted external data require independent authority semantics.

**Reason:** prevents confused-deputy/prompt-injection style failures and memory-based authority escalation.

## I03 — Provenance preservation for consequential state

Consequential beliefs, objectives, verification results and durable changes must retain enough provenance to reconstruct why they were accepted.

**Reason:** correction, audit and self-improvement attribution require source lineage.

## I04 — Temporal applicability

Mutable facts/procedures/preferences must expose when/scope in which they apply rather than being treated as timeless truth.

**Reason:** long-horizon failure often comes from correct old information applied after premises change.

## I05 — Uncertainty is operational

When uncertainty materially affects expected outcome, it must be preserved through relevant transformations and influence operation/assurance decisions.

**Reason:** confidence without behavioral consequences is not useful control information.

## I06 — No silent certainty amplification

Compression, summarization, consensus or repeated self-generated evidence may not silently convert weak/correlated evidence into stronger confidence.

**Reason:** correlated agreement and lossy summaries can create false certainty.

## I07 — Capability/authority separation

A component's ability to compute/propose an action does not authorize it to cause that effect.

**Reason:** external capability control reduces reliance on learned obedience and enables use of powerful partially trusted components.

## I08 — Least sufficient privilege

External effects should use the minimum authority/resources needed for the current operation and duration unless explicitly escalated.

**Reason:** reduces blast radius of error or adversarial input.

## I09 — Verification is scoped

A passing check certifies only the property, assumptions and regime actually tested.

**Reason:** tests/proofs/judges do not imply global correctness.

## I10 — Assurance scales with transition consequence

Required independent evidence/control should rise with scope, persistence, privilege, irreversibility, uncertainty and optimization pressure.

**Reason:** low-risk reversible cognition and architecture/control mutation should not share one acceptance threshold.

## I11 — Independent acceptance for self-change

A candidate durable self-change cannot earn acceptance solely by changing the evaluator, tests, authority or recovery mechanism used to judge it.

**Reason:** otherwise improvement can redefine success.

## I12 — Durable change is versioned

Persistent changes to reusable knowledge, policy, learned structure or system organization must have identifiable lineage/version and compatibility semantics.

**Reason:** enables rollback, comparison and protocol/memory migration.

## I13 — Recovery state survives candidate failure

For changes where rollback is required, the recovery path must remain available if the candidate crashes, behaves incorrectly or corrupts its own active state.

**Reason:** a rollback mechanism controlled only by the candidate is not a recovery mechanism.

## I14 — Current belief remains challengeable

New evidence can revise even high-confidence current state; high confidence may raise evidence thresholds but cannot make beliefs logically immune to contradiction.

**Reason:** environments and objectives change; world models can be wrong.

## I15 — Lossy transformations disclose loss

When information is compressed/abstracted such that exact reconstruction is unavailable, downstream processes must not assume full fidelity.

**Reason:** prevents summaries/latent abstractions from being treated as source evidence.

## I16 — Representation conversion preserves control metadata

Provenance, authority, time/scope and required uncertainty must survive transitions among machine-native, structured and human-facing representations.

**Reason:** trust semantics are orthogonal to representation format.

## I17 — Exact state remains exact where required

Identifiers, cryptographic/security material, formal symbols, tool arguments or other exact fields must not pass through lossy representation without explicit validation.

**Reason:** semantic similarity is not sufficient for exact interfaces.

## I18 — Physical resource bounds are enforceable

Compute, memory, bandwidth, interaction and assurance budgets must be bounded at runtime where runaway behavior would matter.

**Reason:** recursive/search/self-improving processes can otherwise consume unbounded resources.

## I19 — Stopping is always representable

Every open-ended computation/search/interaction/self-improvement loop must have a valid stop/yield/abort state that does not require success.

**Reason:** marginal value can become negative or resources can change.

## I20 — World-model prediction is not observation

Predicted/simulated state remains typed as hypothetical until grounded by evidence.

**Reason:** prevents imagined trajectories from contaminating memory/current belief as real events.

## I21 — Model mismatch is retained as evidence

When predicted and observed outcomes diverge materially, the mismatch must be available to update belief/model confidence or trigger diagnosis.

**Reason:** prediction error is evidence about model validity/regime change.

## I22 — Objective evidence retains source/authority

Preferences, instructions, demonstrations and reward/evaluation signals must not silently collapse into one unprovenanced objective state.

**Reason:** objectives can conflict and be uncertain; proxy optimization risk depends on their origin/scope.

## I23 — Hard constraints are not ordinary preferences

Where deployment defines non-negotiable constraints, ordinary utility improvements cannot silently trade them away.

**Reason:** scalarization can hide safety/policy requirements.

## I24 — Evaluator exposure is accounted for

If a generator/search process has repeated access to an evaluator's behavior or tests, the system must treat overfitting/exploitation risk as increasing.

**Reason:** evaluator reliability changes under optimization pressure.

## I25 — Independence is about failure correlation, not count

Additional evaluators/agents/checks only count as stronger evidence to the extent their failure sources differ.

**Reason:** duplicated blind spots create false-confidence consensus.

## I26 — Persistent memory can be superseded without erasing history

The system must support changing active truth while retaining prior evidence when audit/causal history matters.

**Reason:** append-only truth and destructive overwrite are both insufficient.

## I27 — Functional forgetting is explicit

Removal from active use must be distinguishable from proof that information was false; archival deletion and active retirement are separate operations where needed.

**Reason:** resource management should not corrupt epistemic history.

## I28 — Learned allocation cannot bypass hard resource/authority envelopes

Adaptive operation policies may optimize inside allowed space but cannot grant themselves new authority/budget simply because expected value appears high.

**Reason:** metacontrol itself can be wrong or exploited.

## I29 — Component/interface version compatibility is checked

Self-improving or heterogeneous components must not exchange opaque state under an assumed stable protocol when their representation/version has changed.

**Reason:** silent protocol drift can corrupt cognition without obvious errors.

## I30 — Human-facing explanations are not presumed faithful internal traces

Summaries/explanations may support audit and interaction but cannot be used as proof of the full computation unless independently validated.

**Reason:** machine-native state may contain information not represented in the explanation.

## I31 — Local improvement cannot silently redefine global utility

A component optimized on a local metric must remain subject to system-level constraints and hidden/independent outcome checks where consequence warrants it.

**Reason:** local optimum/proxy improvement can degrade broader behavior.

## I32 — System evaluation is longitudinal

Persistent/self-improving candidates must be tested over changing tasks/time, not only isolated stateless queries.

**Reason:** memory pollution, interference, drift and patch debt appear only over repeated interaction.

## I33 — Architecture claims require resource-matched comparisons

A mechanism cannot be declared superior from unmatched flagship-system benchmarks alone.

**Reason:** scale, data, hardware, context, tools and verification can dominate the architectural variable.

## I34 — No mechanism is included without a required function

Every architecture component/operation must map to one or more functional requirements and justify its complexity/resource cost.

**Reason:** prevents architecture soup/cargo culting.

## I35 — Every major mechanism has a falsification/ablation path

The research organism must be able to remove, replace or disable a mechanism and measure what capability/cost changes.

**Reason:** clean-sheet design requires mechanisms to earn their existence experimentally.
