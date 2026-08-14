# Design Ledger

No architectural choice is accepted without a traceable reason. This ledger records **version-specific experimental conclusions**, not permanent truths and not a component diagram.

## Status

**Phase 10 has produced fifteen provisional principle-level selections. No whole Phase-9 architecture family is selected.**

The detailed measurements live in the experiment notes; this ledger keeps the current decision, evidence trail and falsifier compact enough to remain auditable.

| Decision | Question | Current status | Evidence | Falsifier / next discriminator |
|---|---|---|---|---|
| DL-001 | control organization | **provisional — coupling-scoped coordination** | E01/E01B + E22/E22B + I01 | fixed universal-central or fully local control wins under equal quality/latency/communication across changing hidden coupling |
| DL-002 | cognitive integration | **provisional — conditional sharing with isolation fallback** | E02/E02B/E02C + I02 online quality learning | all-shared or all-isolated computation consistently dominates adaptive sharing under equal stored capacity, active compute and communication |
| DL-003 | history/current-state representation | **provisional — derived current belief linked to retained evidence** | E03/E03B + I01 durable evidence linkage | archive/link maintenance costs more lifetime utility than revision/provenance value across changing environments |
| DL-004 | internal representation | **provisional — typed hybrid boundary state** | E04/E04B + integrated exact identity/provenance | one homogeneous representation matches utility, bandwidth, exact semantics, protocol evolution and failure detection without recreating typed channels implicitly |
| DL-005 | inference budget | **provisional — value-of-computation stopping** | E05/E05B + integrated operation proposals | adaptive control overhead/miscalibration makes fixed compute better across changing task difficulty, value and resource prices |
| DL-006 | belief ambiguity | **provisional — consequence-sensitive hypothesis plurality** | E06 + E23B + I01 | single-belief state matches lifetime utility under ambiguity/consequence shifts after equal state/coordination cost |
| DL-007 | information acquisition | **provisional — value-driven active evidence acquisition** | E07 + E23B + I01 | passive/fixed acquisition matches adaptive lifetime utility under changing informativeness, option value, cost and risk |
| DL-008 | predictive-state breadth | **provisional — adaptive hot-state breadth with recoverable optionality** | E08 + E08B | one fixed breadth consistently dominates after estimator/control overhead, or future-relevance estimation costs more than optionality saves |
| DL-009 | learning persistence | **provisional — staged adaptive persistence with change-source uncertainty** | E09/E09B/E09C + I01/I02 durable discovery | correlated/adversarial observation failures or expensive corroboration erase lifetime benefit, or fixed timescale dominates after full evidence-acquisition cost |
| DL-010 | credit architecture | **provisional — causal/eligibility-scoped delayed credit** | E10 serial sparse reward + E10B speculative branching | full-history/global propagation matches learning, attribution accuracy, delayed state and communication across increasing causal sparsity/trajectory depth |
| DL-011 | memory retrieval policy | **provisional — retrieve for expected applicability/downstream value; similarity is a proxy** | E11 two families + I01 | similarity-only retrieval matches lifetime utility under staleness/causal conflicts and equal retrieval cost, or applicability checks cost more than avoided errors |
| DL-012 | verification granularity | unresolved; first integrated family shows outcome/process checks cover different failure classes | I03/E12 | second structurally different family must reproduce conditional granularity benefit before promotion |
| DL-013 | evaluator redundancy | **provisional — assurance value depends on failure-mode independence, not evaluator count** | Phase-5/Goodhart evidence + E23 exploit + I02 + I03/E13 pressure sweep | correlated evaluator ensembles match genuinely independent evidence under increasing optimizer/search pressure and equal cost |
| DL-014 | capability constraints | external hard boundary retained for consequential effects; implementation open | security/control evidence | E14 behavior-only vs external boundaries vs hybrid |
| DL-015 | self-improvement lineage | unresolved | self-improvement/evolution evidence | E15 greedy incumbent vs bounded archive/population |
| DL-016 | repair scope | unresolved | mutation attribution + lifetime economics | E16 local patch vs isolated durable update vs structural change |
| DL-017 | mature structure | unresolved | biological development + architecture search | E17 fixed vs direct structural mutation vs generative development |
| DL-018 | execution timing | unresolved | systems locality/event evidence | E18 synchronous vs asynchronous/event-driven execution |
| DL-019 | fidelity allocation | unresolved | precision + representation evidence | E19 uniform vs adaptive fidelity/precision |
| DL-020 | self-change test exposure | principle favors independent hidden/rotating evidence; mechanism open | verification/self-improvement evidence | E20 visible vs mixed-hidden vs rotating-adversarial regression suites |
| DL-021 | assurance allocator | **provisional — consequence/uncertainty/resource-sensitive assurance allocation** | I02 learned durable-claim assurance + I03/E21 mixed final/process assurance and price sweep | one implicit self-check rule or uniform-heavy verification dominates across changing consequence, verifier uncertainty and assurance prices after equal accounting |
| DL-022 | cross-resource metacontrol | **provisional — joint adaptive resource substitution under shared scarcity** | E22/E22B + I01/I02 | independent resource policies match lifetime utility after equal coordination cost, or joint allocator overhead exceeds substitution/anti-contention benefit |
| DL-023 | epistemic frontier policy | **provisional — verified frontier expansion** | E23/E23B + I01/I02 durable frontier knowledge | independent staging adds no reliability, or beyond-teacher results require hidden answer leakage rather than search/new evidence |

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
Share learned computation when reusable structure creates transfer benefit after active-compute/communication cost. Preserve private paths when task structure diverges or shared updates create interference. E02C and I02 both reproduce this frontier under different workloads.

## PS-010 — Joint adaptive resource substitution under shared scarcity
When compute, memory, observation, verification or other operations substitute and share limited capacity, allocation must account jointly for current value, price/quality and scarcity coupling. Better local choices can worsen system utility if uncoordinated processes stampede toward the same resource.

## PS-011 — Retrieval by expected applicability / downstream value
Persistent evidence should ultimately be selected for expected usefulness to the current decision, belief update or action—not semantic resemblance by itself. Similarity remains a valuable cheap candidate signal when it predicts applicability well.

## PS-012 — Adaptive predictive-state breadth / recoverable optionality
Keep information hot in proportion to expected future decision value relative to active-state and rematerialization cost. Distinctions not worth current hot-state rent should remain recoverable when their future relevance has material option value. E08B adapts breadth online across hidden objective-switch regimes.

## PS-013 — Failure-mode-independent assurance
Additional evaluators are valuable to the extent that they add evidence with sufficiently different relevant failure modes. Different instances, prompts or votes do not create meaningful redundancy if optimizer pressure can exploit the same blind spot.

I03/E13 makes this explicit: at search pressure 16, correlated double evaluation accepts the shared exploit at ~0.430/task versus ~0.0176 for independent double checking. This extends the E23 evaluator-exploit result into a different candidate/search environment.

The selected object is **failure-mode independence**, not evaluator count or model diversity by name.

## PS-014 — Consequence/uncertainty/resource-sensitive assurance allocation
Verification effort should scale with expected harm reduction, uncertainty about the relevant verifier/state transition, optimizer pressure and assurance cost.

Uniform heavy verification is rational when checking is cheap relative to error consequence. Selective assurance becomes preferable as checking becomes expensive/scarce. I02 provides a durable-knowledge family; I03/E21 provides a distinct final/process candidate family and verification-price crossover.

This is distinct from PS-005 only in scope: PS-005 prices optional computation generally; PS-014 requires that **assurance evidence retain its own independence, authority and failure semantics** rather than being treated as ordinary cognition.

## PS-015 — Causal/eligibility-scoped delayed credit
A delayed/global outcome need not propagate identical credit through the entire retained history. Credit should flow through transitions that remain causally or evidentially plausible contributors to that outcome, expanding to broader history only when responsibility is genuinely unresolved and worth the state/communication cost.

E10A shows local eligibility protecting correct stages under sparse serial final reward; E10B shows branch-scoped credit eliminating updates to causally inactive speculative computation. In E10B the eligibility variant retains ~1.12 delayed items versus 10 for global history and cuts false blame from ~1.38 to ~0.147/episode while raising tail success from ~0.533 to ~0.812.

The selected object is the **credit-scope rule**, not a specific biological trace, gradient estimator or RL algorithm.

---

# Composition checkpoints

## I01 — first integrated epistemic organism

Several selected principles coexist in one epistemic state-transition/resource loop. Across 30 seeds the full system reaches ~2.359 utility/task and beats each one-principle ablation. Immediate visible-evaluator consolidation produces ~54.6 false durable writes/run; staged independent verification prevents that contamination in the exact-verifier setting.

## I02 — learned metacognition and fallible assurance

Operation quality and verifier safety become revisable learned state. Conditional shared/private estimation reaches ~1.351 utility/task versus ~1.266 all-shared, ~1.332 all-private and ~1.339 frozen-initial. Adaptive assurance averages ~0.43 false durable writes/run versus ~12.1 primary-only, while using fewer secondary checks than uniform double verification.

## I03 — assurance composition

Outcome correctness, process validity and evidence independence are separated. Correlated evaluators remain exploitable under search pressure; explicit adaptive assurance beats confidence-triggered self-checking and crosses over with uniform-heavy verification as assurance prices rise. DL-012 granularity remains open after this first family.

These integrated checkpoints are **not additional principles and not architecture-family selections**. Their purpose is to discover interaction regressions and determine which apparent functions collapse into common mechanisms.

---

## Current architecture implications

The fifteen selections increasingly suggest a small number of recurring laws rather than fifteen permanent modules:

- **scope follows coupling:** coordination and credit expand only with actual dependency/responsibility;
- **state follows future value:** hot breadth, persistence and retrieval depend on expected future usefulness and recoverability;
- **work follows marginal value:** compute, observation and assurance are purchased when expected gain/harm reduction justifies cost;
- **sharing follows reusable structure:** learned state is shared where transfer exceeds interference;
- **epistemic authority follows evidence:** novelty, confidence and evaluator votes do not bypass provenance/independent verification;
- **durable change is staged:** persistent knowledge and system changes require stronger evidence than temporary reasoning state.

This convergence is now a primary target for the next integrated organism: test whether several PS rules can be implemented by one general typed state-transition/resource allocator without losing their distinct authority and failure semantics.

## Architecture-family status

| Candidate | Status | What it still tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | how far integration can go before interference/authority/provenance boundaries dominate |
| D — Developmental Variant System | retain | structural adaptation, indirect organization and variant populations |

No family is selected because PS-001 through PS-015 remain implementable by multiple families.

## Selection rule

A design decision moves to a provisional selection only after:

1. the relevant experiment runs under matched resource/assurance budgets;
2. the claimed benefit survives a structurally different task family;
3. a targeted failure/ablation test attacks the claimed mechanism;
4. resource costs and regressions are reported;
5. the falsifier is updated from observed evidence.

“Current systems do it this way” remains evidence of feasibility, not evidence of optimality.