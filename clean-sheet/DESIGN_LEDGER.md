# Design Ledger

No architectural choice is accepted without a traceable reason. This ledger records **version-specific experimental conclusions**, not permanent truths and not a component diagram.

## Status

**Phase 10 has produced sixteen provisional principle-level selections. No whole Phase-9 architecture family is selected.**

The detailed measurements live in the experiment notes; this ledger keeps the current decision, evidence trail and falsifier compact enough to remain auditable.

| Decision | Question | Current status | Evidence | Falsifier / next discriminator |
|---|---|---|---|---|
| DL-001 | control organization | **provisional — coupling-scoped coordination** | E01/E01B + E22/E22B + I01/I04 | fixed universal-central or fully local control wins under equal quality/latency/communication across changing hidden coupling |
| DL-002 | cognitive integration | **provisional — conditional sharing with isolation fallback** | E02/E02B/E02C + I02 | all-shared or all-isolated computation consistently dominates adaptive sharing under equal stored capacity, active compute and communication |
| DL-003 | history/current-state representation | **provisional — derived current belief linked to retained evidence** | E03/E03B + I01 | archive/link maintenance costs more lifetime utility than revision/provenance value across changing environments |
| DL-004 | internal representation | **provisional — typed hybrid boundary state** | E04/E04B + I01/I04 | one homogeneous representation matches utility, bandwidth, exact semantics, protocol evolution and failure detection without recreating typed channels implicitly |
| DL-005 | inference budget | **provisional — value-of-computation stopping** | E05/E05B + I01/I04 | adaptive control overhead/miscalibration makes fixed compute better across changing task difficulty, value and resource prices |
| DL-006 | belief ambiguity | **provisional — consequence-sensitive hypothesis plurality** | E06 + E23B + I01 | single-belief state matches lifetime utility under ambiguity/consequence shifts after equal state/coordination cost |
| DL-007 | information acquisition | **provisional — value-driven active evidence acquisition** | E07 + E23B + I01 | passive/fixed acquisition matches adaptive lifetime utility under changing informativeness, option value, cost and risk |
| DL-008 | predictive-state breadth | **provisional — adaptive hot-state breadth with recoverable optionality** | E08 + E08B | one fixed breadth consistently dominates after estimator/control overhead, or future-relevance estimation costs more than optionality saves |
| DL-009 | learning persistence | **provisional — staged adaptive persistence with change-source uncertainty** | E09/E09B/E09C + I01/I02 | correlated/adversarial observation failures or expensive corroboration erase lifetime benefit, or fixed timescale dominates after full evidence-acquisition cost |
| DL-010 | credit architecture | **provisional — causal/eligibility-scoped delayed credit** | E10 serial sparse reward + E10B branching | full-history/global propagation matches learning, attribution accuracy, delayed state and communication across increasing causal sparsity/trajectory depth |
| DL-011 | memory retrieval policy | **provisional — retrieve for expected applicability/downstream value; similarity is a proxy** | E11 two families + I01 | similarity-only retrieval matches lifetime utility under staleness/causal conflicts and equal retrieval cost, or applicability checks cost more than avoided errors |
| DL-012 | verification granularity | **provisional — failure-layer-targeted verification** | I03/E12 + E12B workflow family | one generic verification layer matches process/outcome/authority failure coverage at equal assurance cost across structurally different tasks |
| DL-013 | evaluator redundancy | **provisional — assurance value depends on failure-mode independence, not evaluator count** | Goodhart evidence + E23 + I02 + I03/E13 | correlated evaluator ensembles match genuinely independent evidence under increasing search pressure and equal cost |
| DL-014 | capability constraints | **strong first-family evidence for narrow hard invariant boundary + adaptive contextual control; mechanism open** | security/control evidence + I04 + E14 | dynamic delegation/revocation or boundary-maintenance failures erase hybrid benefit; E14B required before promotion |
| DL-015 | self-improvement lineage | unresolved | self-improvement/evolution evidence | E15 greedy incumbent vs bounded archive/population |
| DL-016 | repair scope | unresolved | mutation attribution + lifetime economics | E16 local patch vs isolated durable update vs structural change |
| DL-017 | mature structure | unresolved | biological development + architecture search | E17 fixed vs direct structural mutation vs generative development |
| DL-018 | execution timing | unresolved | systems locality/event evidence | E18 synchronous vs asynchronous/event-driven execution |
| DL-019 | fidelity allocation | unresolved | precision + representation evidence | E19 uniform vs adaptive fidelity/precision |
| DL-020 | self-change test exposure | principle favors independent hidden/rotating evidence; mechanism open | verification/self-improvement evidence | E20 visible vs mixed-hidden vs rotating-adversarial regression suites |
| DL-021 | assurance allocator | **provisional — consequence/uncertainty/resource-sensitive assurance allocation** | I02 + I03/E21 + E12B | implicit self-check or uniform-heavy verification dominates across changing consequence, uncertainty and assurance prices after equal accounting |
| DL-022 | cross-resource metacontrol | **provisional — joint adaptive resource substitution under shared scarcity** | E22/E22B + I01/I02/I04 | independent resource policies match lifetime utility after equal coordination cost, or joint allocator overhead exceeds substitution/anti-contention benefit |
| DL-023 | epistemic frontier policy | **provisional — verified frontier expansion** | E23/E23B + I01/I02/I04 | independent staging adds no reliability, or beyond-teacher results require hidden answer leakage rather than search/new evidence |

---

# Provisional selections

## PS-001 — Typed hybrid boundary state
Exact identity, control and provenance semantics remain exact. Tolerant numerical/learned state may use compact approximate representations. Version/integrity remain explicit; human-readable views need not occupy the hot path.

## PS-002 — Staged adaptive persistence
New evidence normally enters reversible/tentative state before globally durable mutation. Consolidation lifetime/threshold should respond to confidence and estimated stability. When `world changed` and `sensor failed` remain plausible alternatives, persistence control may buy sufficiently independent corroboration rather than guessing from one channel.

## PS-003 — Coupling-scoped coordination
Keep decisions local while dependencies/scarcity are local. Expand coordination only to the scope where choices become coupled. This selects a scope rule, not a fixed topology.

## PS-004 — Derived current belief with evidence linkage
Maintain current belief cheaply for repeated reasoning/action while retaining source linkage whenever later correction, contradiction handling, provenance or audit has meaningful expected value.

## PS-005 — Value-of-computation stopping
Continue optional inference work only while estimated marginal downstream value exceeds compute, latency, risk and opportunity cost. Maximum budgets are ceilings, not targets.

## PS-006 — Consequence-sensitive hypothesis plurality
Preserve multiple plausible world states while ambiguity × consequence justifies their state/coordination cost; collapse/prune as evidence resolves ambiguity or stakes fall.

## PS-007 — Value-driven active evidence acquisition
Acquire observations/interventions when expected downstream or epistemic value exceeds interaction cost/risk, including multi-step option value when evidence channels are complementary.

## PS-008 — Verified epistemic frontier expansion
Human/bootstrap knowledge is a starting prior and method library, not a permanent epistemic ceiling. Novel candidates remain tentative until domain-appropriate evidence sufficiently independent from the proposal path supports durable promotion.

## PS-009 — Conditional sharing with isolation fallback
Share learned computation when reusable structure creates transfer benefit after active-compute/communication cost. Preserve private paths when task structure diverges or shared updates create interference.

## PS-010 — Joint adaptive resource substitution under shared scarcity
When compute, memory, observation, verification or other operations substitute and share limited capacity, allocation must account jointly for current value, price/quality and scarcity coupling.

## PS-011 — Retrieval by expected applicability / downstream value
Persistent evidence should ultimately be selected for expected usefulness to the current decision, belief update or action—not semantic resemblance by itself. Similarity remains a valuable cheap candidate signal when it predicts applicability well.

## PS-012 — Adaptive predictive-state breadth / recoverable optionality
Keep information hot in proportion to expected future decision value relative to active-state and rematerialization cost. Distinctions not worth current hot-state rent should remain recoverable when their future relevance has material option value.

## PS-013 — Failure-mode-independent assurance
Additional evaluators are valuable to the extent that they add evidence with sufficiently different relevant failure modes. Different instances, prompts or votes do not create meaningful redundancy if optimizer pressure can exploit the same blind spot.

## PS-014 — Consequence/uncertainty/resource-sensitive assurance allocation
Verification effort should scale with expected harm reduction, uncertainty about the relevant verifier/state transition, optimizer pressure and assurance cost. Uniform heavy verification is rational when cheap; selective assurance becomes preferable when checking is expensive or scarce.

## PS-015 — Causal/eligibility-scoped delayed credit
A delayed/global outcome need not propagate identical credit through the entire retained history. Credit should flow through transitions that remain causally or evidentially plausible contributors to that outcome, expanding only when responsibility is genuinely unresolved and worth the state/communication cost.

## PS-016 — Failure-layer-targeted verification
Verification should target the layer or failure mode that can still invalidate the proposed transition/result. Process validity, final outcome correctness, provenance, authority and other assurance evidence are not assumed substitutable merely because they can all increase confidence.

I03's candidate/search family and E12B's multi-step workflow family both show complementary process/outcome failures. In E12B, outcome-only checking leaves ~0.1337 process-harm rate while process-only leaves ~0.1113 outcome-harm rate. Uniform checking covers both but uses 2 checks/task; adaptive granularity reaches the best default utility (~1.9877) with ~1.068 checks/task by targeting the currently valuable layers.

The selected object is the **granularity/coverage rule**, not a fixed verifier stack.

---

# Composition checkpoints

## I01 — integrated epistemic organism

Memory conflict, ambiguity, active observation, discovery staging and shared scarcity coexist. The full system beats each one-principle ablation; immediate visible-evaluator consolidation creates persistent contamination.

## I02 — learned metacognition and fallible assurance

Operation quality and verifier safety become revisable learned state. Conditional shared/private estimation survives drift; adaptive assurance approaches uniform-double reliability with lower verification spend.

## I03 — assurance composition

Outcome correctness, process validity and evidence independence are separated. Correlated evaluators remain exploitable under search pressure; assurance allocation crosses from uniform-heavy to adaptive as checking price rises.

## I04 — typed transition/resource kernel

One shared allocator ranks cognition/observation/verification work under a shifting workload while authority semantics remain typed.

30-seed means:

| variant | net utility/task | false durable writes | unsafe external effects | authority violations |
|---|---:|---:|---:|---:|
| **typed shared** | **0.9758** | 5.13 | **5.03** | **0** |
| typed fixed silos | 0.7846 | **2.67** | 6.57 | **0** |
| flat scalar | -0.3494 | **194.13** | **68.43** | **1144.7** |

The shared allocator reallocates verification from ~0.100/task before the workload shift to ~0.155 afterward. I04 therefore supports **common allocation + typed authority**, not one-controller-per-function and not one scalar that grants execution permission.

These checkpoints are composition evidence, not additional architecture-family selections.

---

## Current architecture implications

The sixteen selections increasingly collapse into a smaller set of recurring laws:

- **scope follows coupling/responsibility** — control and credit widen only when dependencies do;
- **state follows future value** — breadth, persistence and retrieval depend on expected future use and recoverability;
- **work follows marginal value** — compute, sensing and assurance are allocatable rather than fixed budgets;
- **sharing follows reusable structure** — transfer is useful until interference outweighs it;
- **authority follows evidence and typed invariants** — confidence, novelty and local value do not manufacture epistemic or external authority;
- **verification follows residual failure layer** — the check must cover what can still invalidate the transition;
- **durability demands stronger evidence** — persistent changes have higher downstream consequence than temporary computation.

I04 suggests these rules may be implementable by a common transition/resource substrate with explicit typed authority/evidence boundaries. E14 strengthens the case that categorical capability invariants should not depend on the same fallible behavioral estimate that proposes the action, while also showing that over-broad hard boundaries can destroy useful capability.

JEPA remains a candidate predictive-representation family only; E24 is specified to test it against reconstruction, task-sufficient prediction and recoverable-source alternatives.

## Architecture-family status

| Candidate | Status | What it still tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | how far integration can go before interference/authority/provenance boundaries dominate |
| D — Developmental Variant System | retain | structural adaptation, indirect organization and variant populations |

No family is selected because PS-001 through PS-016 remain implementable by multiple families.

## Selection rule

A design decision moves to a provisional selection only after:

1. the relevant experiment runs under matched resource/assurance budgets;
2. the claimed benefit survives a structurally different task family;
3. a targeted failure/ablation test attacks the claimed mechanism;
4. resource costs and regressions are reported;
5. the falsifier is updated from observed evidence.

“Current systems do it this way” remains evidence of feasibility, not evidence of optimality.
