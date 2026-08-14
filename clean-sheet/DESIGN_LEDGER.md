# Design Ledger

No architectural choice is accepted without a traceable reason. This ledger records **version-specific experimental conclusions**, not permanent truths and not a component diagram.

## Status

**Phase 10 has produced nineteen provisional principle-level selections. No whole Phase-9 architecture family is selected.**

The detailed measurements live in the experiment notes; this ledger keeps the current decision, evidence trail and falsifier compact enough to remain auditable.

| Decision | Question | Current status | Evidence | Falsifier / next discriminator |
|---|---|---|---|---|
| DL-001 | control organization | **provisional — coupling-scoped coordination** | E01/E01B + E22/E22B + I01/I04 | fixed universal-central or fully local control wins under equal quality/latency/communication across changing hidden coupling |
| DL-002 | cognitive integration | **provisional — conditional sharing with isolation fallback** | E02/E02B/E02C + I02 | all-shared or all-isolated computation consistently dominates adaptive sharing under equal stored capacity, active compute and communication |
| DL-003 | history/current-state representation | **provisional — derived current belief linked to retained evidence** | E03/E03B + I01 | archive/link maintenance costs more lifetime utility than revision/provenance value across changing environments |
| DL-004 | internal representation | **provisional — typed hybrid boundary state** | E04/E04B + I01/I04 | one homogeneous representation matches exact semantics, bandwidth, protocol evolution and failure detection without recreating typed channels implicitly |
| DL-005 | inference budget | **provisional — value-of-computation stopping** | E05/E05B + I01/I04 | adaptive overhead/miscalibration makes fixed compute better across changing task difficulty/value/resource prices |
| DL-006 | belief ambiguity | **provisional — consequence-sensitive hypothesis plurality** | E06 + E23B + I01 | single-belief state matches lifetime utility under ambiguity/consequence shifts after equal state/coordination cost |
| DL-007 | information acquisition | **provisional — value-driven active evidence acquisition** | E07 + E23B + I01 | passive/fixed acquisition matches adaptive lifetime utility under changing informativeness, option value, cost and risk |
| DL-008 | predictive-state breadth | **provisional — adaptive hot-state breadth with recoverable optionality** | E08 + E08B | one fixed breadth dominates after estimator/control overhead, or future-relevance estimation costs more than optionality saves |
| DL-009 | learning persistence | **provisional — staged adaptive persistence with change-source uncertainty** | E09/E09B/E09C + I01/I02 | correlated/adversarial evidence failures or expensive corroboration erase lifetime benefit, or fixed timescale dominates |
| DL-010 | credit architecture | **provisional — causal/eligibility-scoped delayed credit** | E10 serial sparse reward + E10B branching | full-history/global propagation matches learning, attribution, delayed state and communication across causal sparsity/trajectory depth |
| DL-011 | retrieval policy | **provisional — retrieve for expected applicability/downstream value; similarity is a proxy** | E11 two families + I01 | similarity-only retrieval matches lifetime utility under staleness/causal conflicts and equal retrieval cost |
| DL-012 | verification granularity | **provisional — failure-layer-targeted verification** | I03/E12 + E12B workflow family | one generic verification layer matches process/outcome/authority failure coverage at equal assurance cost across structurally different tasks |
| DL-013 | evaluator redundancy | **provisional — assurance value depends on failure-mode independence, not evaluator count** | Goodhart evidence + E23 + I02 + I03/E13 | correlated evaluator ensembles match genuinely independent evidence under increasing optimizer/search pressure and equal cost |
| DL-014 | capability constraints | **provisional — independent current/revocable categorical authority + adaptive contextual control** | E14 adversarial behavioral-cue family + E14B dynamic grants/revocations + I04 | live/learned alternatives match categorical integrity and contextual utility once authority propagation, delegation and boundary-maintenance costs are fully priced |
| DL-015 | self-improvement lineage | **provisional — resource-priced lineage diversity / variant optionality** | E15 recurring-objective family + E15B deceptive stepping-stone family | one reversible incumbent matches switching recovery and deceptive search after equal rollback/search cost, or archive maintenance dominates option value |
| DL-016 | repair scope | unresolved | mutation attribution + lifetime economics | E16 local reversible patch vs isolated durable update vs structural change |
| DL-017 | mature structure | unresolved | biological development + architecture search | E17 fixed vs direct structural mutation vs generative development |
| DL-018 | execution timing | unresolved | systems locality/event evidence | E18 synchronous vs asynchronous/event-driven execution |
| DL-019 | fidelity allocation | unresolved | precision + representation evidence | E19 uniform vs adaptive fidelity/precision |
| DL-020 | self-change test exposure | **provisional — rotating independent regression evidence across coverage and timescale** | E20 distribution/coverage shift + E20B long-horizon instability | rotating suites become predictable/stale enough for optimizer exploitation, or refresh/adversarial costs exceed prevented regressions |
| DL-021 | assurance allocator | **provisional — consequence/uncertainty/resource-sensitive assurance allocation** | I02 + I03/E21 + E12B | implicit self-check or uniform-heavy verification dominates across changing consequence, uncertainty and assurance prices |
| DL-022 | cross-resource metacontrol | **provisional — joint adaptive resource substitution under shared scarcity** | E22/E22B + I01/I02/I04 | independent resource policies match lifetime utility after equal coordination cost |
| DL-023 | epistemic frontier policy | **provisional — verified frontier expansion** | E23/E23B + I01/I02/I04 | independent staging adds no reliability, or beyond-teacher results require hidden answer leakage rather than search/new evidence |

---

# Provisional selections

## PS-001 — Typed hybrid boundary state
Exact identity, control and provenance semantics remain exact. Tolerant numerical/learned state may use compact approximate representations. Version/integrity remain explicit; human-readable views need not occupy the hot path.

## PS-002 — Staged adaptive persistence
New evidence normally enters reversible/tentative state before globally durable mutation. Consolidation timescale responds to confidence/stability; when change and sensor failure are confounded, sufficiently independent corroboration may be worth buying.

## PS-003 — Coupling-scoped coordination
Keep decisions local while dependencies/scarcity are local. Expand coordination only to the scope where choices become coupled.

## PS-004 — Derived current belief with evidence linkage
Maintain cheap current belief while retaining source linkage whenever correction, contradiction handling, provenance or audit has meaningful expected value.

## PS-005 — Value-of-computation stopping
Continue optional inference only while estimated marginal downstream value exceeds compute, latency, risk and opportunity cost.

## PS-006 — Consequence-sensitive hypothesis plurality
Preserve multiple plausible states while ambiguity × consequence justifies their cost; prune as evidence resolves ambiguity or stakes fall.

## PS-007 — Value-driven active evidence acquisition
Acquire observations/interventions when expected downstream or epistemic value exceeds interaction cost/risk, including multi-step option value.

## PS-008 — Verified epistemic frontier expansion
Bootstrap knowledge is a starting prior/method library, not a permanent epistemic ceiling. Novel candidates remain tentative until sufficiently independent domain-appropriate evidence supports promotion.

## PS-009 — Conditional sharing with isolation fallback
Share learned computation while reusable structure creates transfer benefit; preserve private paths where interference outweighs transfer.

## PS-010 — Joint adaptive resource substitution under shared scarcity
When compute, memory, observation, verification or other operations substitute and share capacity, allocation accounts jointly for value, price/quality and contention.

## PS-011 — Retrieval by expected applicability / downstream value
Persistent evidence is ultimately selected for expected usefulness to the current decision/belief/action. Similarity is a candidate signal when it predicts applicability well.

## PS-012 — Adaptive predictive-state breadth / recoverable optionality
Keep information hot in proportion to expected future decision value versus active/rematerialization cost; preserve recoverability for distinctions with meaningful option value.

## PS-013 — Failure-mode-independent assurance
Additional evaluators are valuable only to the extent that they add evidence with sufficiently different relevant failure modes.

## PS-014 — Consequence/uncertainty/resource-sensitive assurance allocation
Verification effort scales with expected harm reduction, uncertainty, optimizer pressure and assurance cost. Heavy checking can win when cheap; selective checking when costly/scarce.

## PS-015 — Causal/eligibility-scoped delayed credit
Delayed outcomes should update transitions that remain plausible contributors, not automatically the entire retained history.

## PS-016 — Failure-layer-targeted verification
Verification targets the layer that can still invalidate the transition/result. Process, final outcome, provenance and authority evidence are not assumed substitutable.

## PS-017 — Independent current/revocable capability authority
Categorical authority for consequential capabilities is enforced independently from the same fallible behavior that proposes the effect. Authority remains current/revocable through explicit identity/version semantics; contextual risk remains adaptively evaluated inside the authorized envelope.

E14 separates categorical permission from contextual danger: the hybrid achieves zero categorical violations while behavior-only degrades under a spoofing shift and hard-only misses contextual harm. E14B then changes grants/revocations during the lifetime: a static boundary suffers ~1679.6 stale-authority violations/run, while live and versioned boundaries stay at zero. The versioned design refreshes on only ~1.14% of tasks and slightly beats always-live lookup utility.

The selected object is the **authority property**, not sandbox/OS/capability-token/hardware implementation.

## PS-018 — Rotating independent self-change regression evidence
Evidence that authorizes durable self-change remains sufficiently independent from the proposal/optimization path and refreshes coverage as the system, environment, failure surface and relevant timescale change. Targeted/adversarial regression pressure is allocated by consequence rather than universally maximized.

E20 shows a fixed hidden suite becoming stale after a state-space distribution shift: post-shift true capability falls to ~0.078 versus ~0.997 for rotating hidden evidence. E20B reproduces the failure with slow long-horizon instability: fixed-short hidden evidence falls to ~0.095 post-shift versus ~0.942 with rotating horizons. Adversarial rotation is safer in both synthetic families but rejects substantially more useful changes and costs more assurance.

The selected object is the **regression-evidence exposure/refresh rule**, not permanent secret tests.

## PS-019 — Resource-priced lineage diversity / variant optionality
Retain multiple self-improvement lineages only while estimated future reuse, uncertainty reduction or stepping-stone value exceeds storage/evaluation/coordination cost; collapse toward one incumbent when those option values disappear.

E15 family A pins both sides: under a stationary objective greedy net performance is ~0.9928 versus ~0.9880 for the archive because the archive cost is wasted. Under recurring A/B demand, the bounded archive reaches ~0.9804 net versus ~0.9562 greedy and improves first-10-round post-switch performance from ~0.799 to ~0.955 while retaining both specialists. E15B then uses a deceptive score landscape where every path from local score 10 to global score 15 temporarily gets worse: greedy stays at 10 on 30/30 seeds, while the bounded archive reaches 15 on 30/30 with the same candidate-evaluation budget.

The selected object is the **lineage-retention rule**, not evolutionary algorithms or a fixed population size.

---

# Composition checkpoints

## I01 — integrated epistemic organism
Memory conflict, ambiguity, active observation, discovery staging and shared scarcity coexist. Full composition beats each one-principle ablation; immediate visible-evaluator consolidation creates persistent contamination.

## I02 — learned metacognition and fallible assurance
Operation quality and verifier safety become revisable learned state. Conditional shared/private estimation survives drift; adaptive assurance approaches uniform-double reliability with lower verification spend.

## I03 — assurance composition
Outcome correctness, process validity and evidence independence are separated. Correlated evaluators remain exploitable under search pressure; assurance allocation crosses from uniform-heavy to adaptive as checking price rises.

## I04 — typed transition/resource kernel
One shared allocator ranks cognition/observation/verification work while authority semantics remain typed. Across 30 seeds typed shared reaches ~0.9758 utility/task versus ~0.7846 fixed typed silos and -0.3494 flat scalar; the flat kernel creates ~194 false durable writes and ~68 unsafe external effects/run. Allocation can unify; authority cannot be flattened into the score.

---

## Current architecture implications

The nineteen selections increasingly collapse into a smaller set of recurring laws:

- **scope follows coupling/responsibility**;
- **state follows future value/recoverability**;
- **work follows marginal value under shared scarcity**;
- **sharing follows reusable structure**;
- **authority follows evidence and current typed invariants, not confidence alone**;
- **verification follows residual failure layer**;
- **durability raises the evidence requirement**;
- **self-change preserves optionality only while its future value earns the carrying cost**;
- **self-change evidence itself must evolve as optimizer pressure and deployment coverage change**.

I04 remains the leading compression hypothesis:

`typed state/transition proposals -> shared value/resource allocator -> layer-specific assurance/authority gate -> execute -> observe -> scoped credit/update`

This is not yet a selected architecture. JEPA remains a candidate predictive-representation family only; E24 is specified to test it against reconstruction, task-sufficient prediction and recoverable-source alternatives.

## Architecture-family status

| Candidate | Status | What it still tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | how far integration can go before interference/authority/provenance boundaries dominate |
| D — Developmental Variant System | retain | structural adaptation, indirect organization and variant populations |

No family is selected because PS-001 through PS-019 remain implementable by multiple families.

## Selection rule

A design decision moves to a provisional selection only after:

1. matched resource/assurance budgets;
2. survival in a structurally different task family;
3. targeted mechanism ablation/falsifier;
4. explicit resource costs/regressions;
5. updated falsifier from observed evidence.

“Current systems do it this way” remains feasibility evidence, not optimality evidence.
