# Design Ledger

No architectural choice is accepted without a traceable reason. This ledger records **version-specific experimental conclusions**, not permanent truths and not a component diagram.

## Status

**Phase 10 has produced twelve provisional principle-level selections. No whole Phase-9 architecture family is selected.**

The detailed measurements live in the experiment notes; this ledger keeps the current decision, evidence trail and falsifier compact enough to remain auditable.

| Decision | Question | Current status | Evidence | Falsifier / next discriminator |
|---|---|---|---|---|
| DL-001 | control organization | **provisional — coupling-scoped coordination** | E01 dependency family + E01B shared scarcity + E22 resource-local/shared control + I01 mixed scarce operations | fixed universal-central or fully local control wins under equal quality/latency/communication across changing hidden coupling |
| DL-002 | cognitive integration | **provisional — conditional sharing with isolation fallback** | E02 transfer/interference + E02B compositional second family + E02C exact parameter/realized-compute matched routing | all-shared or all-isolated computation consistently dominates adaptive sharing under equal stored capacity, active compute and communication |
| DL-003 | history/current-state representation | **provisional — derived current belief linked to retained evidence** | E03 direct-address/compression + E03B source retractions/provenance + I01 evidence-linked durable knowledge | archive/link maintenance costs more lifetime utility than revision/provenance value across changing environments |
| DL-004 | internal representation | **provisional — typed hybrid boundary state** | E04 serialization/bandwidth + E04B search-state, exact side fields, corruption/version tests + I01 exact identity/provenance fields | one homogeneous representation matches utility, bandwidth, exact semantics, protocol evolution and failure detection without recreating typed channels implicitly |
| DL-005 | inference budget | **provisional — value-of-computation stopping** | E05 noisy evidence + E05B costly candidate evaluation + I01 optional operation proposals | adaptive control overhead/miscalibration makes fixed compute better across changing task difficulty, value and resource prices |
| DL-006 | belief ambiguity | **provisional — consequence-sensitive hypothesis plurality** | E06 noisy four-world family + E23B same-intervention causal ablation + I01 safe-action ablation | single-belief state matches lifetime utility under ambiguity/consequence shifts after equal state/coordination cost |
| DL-007 | information acquisition | **provisional — value-driven active evidence acquisition** | E07 probe-cost/complementarity + E23B causal intervention family + I01 scarce exact probes | passive/fixed acquisition matches adaptive lifetime utility under changing informativeness, option value, cost and risk |
| DL-008 | predictive-state breadth | **provisional — adaptive hot-state breadth with recoverable optionality** | E08 static objective-switch optionality + E08B online hidden switch-rate adaptation | a single fixed breadth consistently dominates after estimator/control overhead, or future-relevance estimation costs more than retained optionality saves |
| DL-009 | learning persistence | **provisional — staged adaptive persistence with evidence about change-source uncertainty** | E09 noisy regime stream + E09B hidden-volatility adaptation + E09C independent corroboration + I01 durable-discovery staging | correlated/adversarial observation failures or expensive corroboration erase lifetime benefit, or a simpler fixed-timescale policy dominates once evidence-acquisition cost is fully priced |
| DL-010 | credit architecture | unresolved | foundations + biology + agent boundaries | E10 global vs factorized delayed credit |
| DL-011 | memory retrieval policy | **provisional — retrieve for expected applicability/downstream value; similarity is a proxy signal** | E11 stale-procedure + surface-vs-causal families + I01 stale surface-memory conflict | similarity-only retrieval consistently matches lifetime utility under regime changes, causal conflicts and equal retrieval cost, or applicability checking costs exceed avoided errors |
| DL-012 | verification granularity | unresolved | Phase-5 verification evidence | E12 outcome vs transition/process checks under equal assurance budget |
| DL-013 | evaluator redundancy | principle favors independent failure modes; mechanism open | evaluator/Goodhart evidence + E23 evaluator exploit + I01 visible-vs-independent discovery verification | E13 correlated-vs-independent evaluators under increasing search pressure |
| DL-014 | capability constraints | external hard boundary retained for consequential effects; implementation open | security/control evidence | E14 behavior-only vs external boundaries vs hybrid |
| DL-015 | self-improvement lineage | unresolved | self-improvement/evolution evidence | E15 greedy incumbent vs bounded archive/population |
| DL-016 | repair scope | unresolved | mutation attribution + lifetime economics | E16 local patch vs isolated durable update vs structural change |
| DL-017 | mature structure | unresolved | biological development + architecture search | E17 fixed vs direct structural mutation vs generative development |
| DL-018 | execution timing | unresolved | systems locality/event evidence | E18 synchronous vs asynchronous/event-driven execution |
| DL-019 | fidelity allocation | unresolved | precision + representation evidence | E19 uniform vs adaptive fidelity/precision |
| DL-020 | self-change test exposure | principle favors independent hidden/rotating evidence; mechanism open | verification/self-improvement evidence | E20 visible vs mixed-hidden vs rotating-adversarial regression suites |
| DL-021 | assurance allocator | unresolved | Phase-5 consequence-sensitive assurance synthesis | E21 implicit self-check vs explicit adaptive assurance vs uniform heavy checking |
| DL-022 | cross-resource metacontrol | **provisional — joint adaptive resource substitution under shared scarcity** | E22 price substitution + E22B capacity contention/quality drift + I01 mixed retrieval/probe/verification allocation | independent resource policies match lifetime utility after equal coordination cost, or joint allocator overhead exceeds substitution/anti-contention benefit |
| DL-023 | epistemic frontier policy | **provisional — verified frontier expansion** | E23 constructive teacher-frontier search + E23B empirical causal discovery + I01 durable frontier knowledge | independent staging adds no reliability, or beyond-teacher results require hidden answer leakage rather than search/new evidence |

---

# Provisional selections

## PS-001 — Typed hybrid boundary state
Exact identity, control and provenance semantics remain exact. Tolerant numerical/learned state may use compact approximate representations. Version and integrity remain explicit; human-readable views need not occupy the hot path.

## PS-002 — Staged adaptive persistence
New evidence normally enters reversible/tentative state before globally durable mutation. Consolidation lifetime/threshold should respond to confidence and estimated environmental stability.

E09C adds a boundary condition: apparent volatility is not always identifiable from one observation stream. When `world changed` and `sensor failed` remain plausible alternatives, persistence control should be allowed to acquire sufficiently independent corroborating evidence. That corroboration is resource-priced and should be requested selectively rather than made permanently mandatory.

## PS-003 — Coupling-scoped coordination
Keep decisions local while dependencies/scarcity are local. Expand coordination only to the resource/domain/global scope where choices become coupled. This selects a scope rule, not a fixed topology.

## PS-004 — Derived current belief with evidence linkage
Maintain current belief cheaply for repeated reasoning/action while retaining source linkage whenever later correction, contradiction handling, provenance or audit has meaningful expected value.

## PS-005 — Value-of-computation stopping
Continue optional inference work only while estimated marginal downstream value exceeds compute, latency, risk and opportunity cost. Maximum budgets are ceilings, not targets.

## PS-006 — Consequence-sensitive hypothesis plurality
Preserve multiple plausible world states while ambiguity × consequence justifies their state/coordination cost; collapse/prune as evidence resolves ambiguity or stakes fall.

## PS-007 — Value-driven active evidence acquisition
Acquire observations/interventions when expected downstream or epistemic value exceeds interaction cost/risk, including multi-step option value when evidence channels are complementary.

## PS-008 — Verified epistemic frontier expansion
Human/bootstrap knowledge is a starting prior and method library, not a permanent epistemic ceiling. Novel candidates remain tentative until domain-appropriate evidence sufficiently independent from the proposal path supports promotion into durable knowledge.

## PS-009 — Conditional sharing with isolation fallback
Share learned computation when reusable structure creates transfer benefit after active-compute/communication cost. Preserve isolated/private paths when task structure diverges or shared updates create interference. E02C confirms the frontier at equal 45-parameter storage and lower realized compute than specialists.

## PS-010 — Joint adaptive resource substitution under shared scarcity
When compute, memory, observation, verification or other operations substitute for one another and share limited capacity, allocation must account jointly for current value, price/quality and scarcity coupling. E22B and I01 show that better local choices can worsen system utility if uncoordinated tasks consume the same scarce resource.

## PS-011 — Retrieval by expected applicability / downstream value
Persistent evidence should ultimately be selected for expected usefulness to the current decision, belief update or action—not semantic resemblance by itself. Similarity remains a valuable cheap candidate signal when it predicts applicability well.

E11 pins both sides: in a stable corpus, similarity is cheapest because deeper checks do not change the answer; under staleness or surface/causal conflict, temporal, causal, outcome and verification semantics become worth their additional retrieval cost.

## PS-012 — Adaptive predictive-state breadth / recoverable optionality
Keep information hot in proportion to its expected future decision value relative to active-state cost and rematerialization cost. Distinctions that are not currently worth hot-state rent should remain recoverable when their future relevance has material option value.

E08A establishes the static frontier: narrow state wins under fixed goals, source-recoverable state wins under occasional objective switches, and broad hot state wins when rematerialization becomes constant. E08B then hides and changes the switch rate; the online controller expands from ~0% broad state to ~99% in the high-switch segment and narrows again afterward, achieving ~0.9909 mean net utility versus 0.9880 for always-broad and ~0.9797 for always-narrow across 30 seeds.

The selected object is the **breadth-allocation rule**, not any particular cache, recurrent state, attention span or world-model representation.

---

## Composition checkpoint — I01

`I01_INTEGRATED_ORGANISM` is the first experiment where several selected principles coexist in one epistemic state-transition kernel rather than being tested separately.

Across 30 seeds its full variant reaches mean net utility/task **2.3589** versus 2.3418 without plurality, 2.0879 without active evidence acquisition, 1.9437 with similarity-only retrieval, 1.8541 with immediate visible-evaluator consolidation, and 2.2756 with first-come rather than joint scarce-resource allocation.

The largest interaction so far is between discovery governance and persistent memory: immediate consolidation averages ~54.6 false durable writes/run, which then contaminate later application decisions. The full staged/independent path records zero false durable writes in this exact-verifier environment.

I01 is **not a new design principle and not an architecture selection**. It is the start of composition testing: determine which principles remain separate boundaries, which collapse into one common mechanism, and which create interaction regressions when combined.

## Current architecture implications

The twelve selections constrain an eventual system without choosing its named architecture:

- coordination appears where coupling appears;
- shared computation is conditional, with isolation retained as an interference boundary;
- current belief remains fast and evidence-revisable;
- ambiguous high-consequence worlds may require several live hypotheses;
- state breadth expands/contracts with expected future relevance;
- retrieval targets applicability/value rather than resemblance alone;
- observation, corroboration, inference compute and cross-resource substitutions are explicitly allocatable;
- knowledge changes pass through reversible stages;
- discovery may exceed the bootstrap teacher, but only evidence promotes novelty into knowledge.

## Architecture-family status

| Candidate | Status | What it still tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | how far integration can go before interference/authority/provenance boundaries dominate |
| D — Developmental Variant System | retain | structural adaptation, indirect organization and variant populations |

No family is selected because PS-001 through PS-012 can be implemented by multiple families.

## Selection rule

A design decision moves to a provisional selection only after:

1. the relevant experiment runs under matched resource/assurance budgets;
2. the claimed benefit survives a structurally different task family;
3. a targeted failure/ablation test attacks the claimed mechanism;
4. resource costs and regressions are reported;
5. the falsifier is updated from observed evidence.

“Current systems do it this way” remains evidence of feasibility, not evidence of optimality.