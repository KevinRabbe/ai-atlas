# Design Ledger

No architectural choice is accepted without a traceable reason. This ledger records **version-specific experimental conclusions**, not permanent truths and not a component diagram.

## Status

**Phase 10 has produced ten provisional principle-level selections. No whole Phase-9 architecture family is selected.**

The detailed measurements live in the experiment notes; this ledger keeps the current decision, evidence trail and falsifier compact enough to remain auditable.

| Decision | Question | Current status | Evidence | Falsifier / next discriminator |
|---|---|---|---|---|
| DL-001 | control organization | **provisional — coupling-scoped coordination** | E01 dependency family + E01B shared scarcity + E22 resource-local/shared control | fixed universal-central or fully local control wins under equal quality/latency/communication across changing hidden coupling |
| DL-002 | cognitive integration | **provisional — conditional sharing with isolation fallback** | E02 transfer/interference + E02B compositional second family + E02C exact parameter/realized-compute matched routing | all-shared or all-isolated computation consistently dominates adaptive sharing under equal stored capacity, active compute and communication |
| DL-003 | history/current-state representation | **provisional — derived current belief linked to retained evidence** | E03 direct-address/compression + E03B source retractions/provenance | archive/link maintenance costs more lifetime utility than revision/provenance value across changing environments |
| DL-004 | internal representation | **provisional — typed hybrid boundary state** | E04 serialization/bandwidth + E04B search-state, exact side fields, corruption/version tests | one homogeneous representation matches utility, bandwidth, exact semantics, protocol evolution and failure detection without recreating typed channels implicitly |
| DL-005 | inference budget | **provisional — value-of-computation stopping** | E05 noisy evidence + E05B costly candidate evaluation | adaptive control overhead/miscalibration makes fixed compute better across changing task difficulty, value and resource prices |
| DL-006 | belief ambiguity | **provisional — consequence-sensitive hypothesis plurality** | E06 noisy four-world family + E23B same-intervention causal ablation | single-belief state matches lifetime utility under ambiguity/consequence shifts after equal state/coordination cost |
| DL-007 | information acquisition | **provisional — value-driven active evidence acquisition** | E07 probe-cost/complementarity + E23B causal intervention family | passive/fixed acquisition matches adaptive lifetime utility under changing informativeness, option value, cost and risk |
| DL-008 | predictive-state breadth | unresolved | world-model/objective-transfer synthesis | E08 objective-switch experiment |
| DL-009 | learning persistence | **provisional — staged adaptive persistence** | E09 noisy regime stream + E09B hidden-volatility adaptation | after independently varying sensor noise and true volatility, adaptive persistence loses lifetime utility to a fixed timescale |
| DL-010 | credit architecture | unresolved | foundations + biology + agent boundaries | E10 global vs factorized delayed credit |
| DL-011 | memory retrieval policy | unresolved | persistent-memory evidence suggests downstream value matters | E11 similarity vs temporal/causal/downstream-value retrieval |
| DL-012 | verification granularity | unresolved | Phase-5 verification evidence | E12 outcome vs transition/process checks under equal assurance budget |
| DL-013 | evaluator redundancy | principle favors independent failure modes; mechanism open | evaluator/Goodhart evidence + E23 evaluator exploit | E13 correlated-vs-independent evaluators under increasing search pressure |
| DL-014 | capability constraints | external hard boundary retained for consequential effects; implementation open | security/control evidence | E14 behavior-only vs external boundaries vs hybrid |
| DL-015 | self-improvement lineage | unresolved | self-improvement/evolution evidence | E15 greedy incumbent vs bounded archive/population |
| DL-016 | repair scope | unresolved | mutation attribution + lifetime economics | E16 local patch vs isolated durable update vs structural change |
| DL-017 | mature structure | unresolved | biological development + architecture search | E17 fixed vs direct structural mutation vs generative development |
| DL-018 | execution timing | unresolved | systems locality/event evidence | E18 synchronous vs asynchronous/event-driven execution |
| DL-019 | fidelity allocation | unresolved | precision + representation evidence | E19 uniform vs adaptive fidelity/precision |
| DL-020 | self-change test exposure | principle favors independent hidden/rotating evidence; mechanism open | verification/self-improvement evidence | E20 visible vs mixed-hidden vs rotating-adversarial regression suites |
| DL-021 | assurance allocator | unresolved | Phase-5 consequence-sensitive assurance synthesis | E21 implicit self-check vs explicit adaptive assurance vs uniform heavy checking |
| DL-022 | cross-resource metacontrol | **provisional — joint adaptive resource substitution under shared scarcity** | E22 price substitution + E22B shared capacity contention and resource-quality drift | independent resource policies match lifetime utility after equal coordination cost, or joint allocator overhead exceeds substitution/anti-contention benefit |
| DL-023 | epistemic frontier policy | **provisional — verified frontier expansion** | E23 constructive teacher-frontier search + E23B empirical causal discovery | independent staging adds no reliability, or beyond-teacher results require hidden answer leakage rather than search/new evidence |

---

# Provisional selections

## PS-001 — Typed hybrid boundary state

Exact identity, control and provenance semantics remain exact. Tolerant numerical/learned state may use compact approximate representations. Version and integrity semantics remain explicit. Human-readable views are generated when audit/communication requires them rather than being mandatory on the internal hot path.

## PS-002 — Staged adaptive persistence

New evidence normally enters reversible/tentative state before globally durable mutation. Consolidation lifetime/threshold should respond to estimated confidence and environmental stability. The estimator and storage implementation remain experimental.

## PS-003 — Coupling-scoped coordination

Keep decisions local while dependencies and scarcity are local. Expand coordination only to the resource/domain/global scope where choices become coupled. This selects a **scope rule**, not a fixed centralized or distributed topology.

## PS-004 — Derived current belief with evidence linkage

Maintain current belief cheaply for repeated reasoning/action, while retaining links to source evidence whenever later correction, contradiction handling, provenance or audit has meaningful expected value. Evidence retention itself remains a resource/value decision.

## PS-005 — Value-of-computation stopping

Continue optional inference work only while its estimated marginal downstream value exceeds computation, latency, risk and opportunity cost. A maximum budget is a ceiling/guardrail, not a target to consume.

## PS-006 — Consequence-sensitive hypothesis plurality

Do not force one current world state when materially different states remain plausible and wrong commitment is costly. Preserve alternatives while their expected decision/discovery value exceeds their state/coordination cost; collapse or prune as evidence resolves ambiguity or stakes fall.

## PS-007 — Value-driven active evidence acquisition

Observation and experiment are resource-consuming operations. Acquire evidence when expected downstream or epistemic value exceeds interaction cost/risk. Include multi-step option value when observations are complementary, and stop when remaining information is not worth its price.

## PS-008 — Verified epistemic frontier expansion

Human/bootstrap knowledge is a starting prior and method library, not a permanent epistemic ceiling. Search and experimentation may leave demonstrated answers, but novelty remains tentative. Candidate discoveries become durable knowledge only through domain-appropriate evidence sufficiently independent from the proposal/optimization path, with verifier scope and provenance retained. Rejected and unresolved hypotheses remain distinct epistemic states.

## PS-009 — Conditional sharing with isolation fallback

Share learned computation when evidence shows reusable structure creates transfer benefit after active-compute and communication costs. Preserve isolated/private paths when task structure diverges or shared updates create interference.

E02C removes the main prior confound: with the same **45 learned parameters**, its routed shared/private learner activates only one path per example and uses less arithmetic than the specialist baseline. At sharedness 0.98 it beats specialists across 240/480/1,200-example regimes; at 0.75 and 0.15 specialists remain better. The selected object is the **conditional sharing rule**, not the current EMA router or a fixed modularity level.

## PS-010 — Joint adaptive resource substitution under shared scarcity

When operations/resources substitute for one another and share limited capacity, allocation must account jointly for current value, price/quality and capacity coupling. Local policies remain appropriate only while their choices do not materially contend for the same scarce resource.

E22B isolates this from E22's price-shift result. Across 30 seeds, post-drift reference regret is approximately:

- adaptive joint: **0.086**;
- frozen joint: **0.206**;
- frozen independent: **0.387**;
- adaptive independent: **0.468**.

The surprising failure is informative: fresher local quality estimates can **increase** system regret when many individually rational tasks rush toward the same newly attractive resource. The selected object is joint substitution under coupling, not the current greedy allocator.

---

## Current architecture implications

The ten selections constrain an eventual system without choosing its named architecture:

- local computation remains attractive, but coordination appears where coupling appears;
- shared learned structure is conditional, with isolation retained as an interference boundary;
- current belief is fast but revisable from evidence;
- ambiguous high-consequence worlds may require several live hypotheses;
- information, inference compute and cross-resource substitutions are all explicitly allocatable;
- knowledge changes pass through reversible stages;
- discovery may exceed the bootstrap teacher, but only evidence promotes novelty into knowledge.

## Architecture-family status

| Candidate | Status | What it still tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | how far integration can go before interference/authority/provenance boundaries dominate |
| D — Developmental Variant System | retain | structural adaptation, indirect organization and variant populations |

No family is selected because PS-001 through PS-010 can be implemented by multiple families.

## Selection rule

A design decision moves to a provisional selection only after:

1. the relevant experiment runs under matched resource/assurance budgets;
2. the claimed benefit survives a structurally different task family;
3. a targeted failure/ablation test attacks the claimed mechanism;
4. resource costs and regressions are reported;
5. the falsifier is updated from observed evidence.

“Current systems do it this way” remains evidence of feasibility, not evidence of optimality.
