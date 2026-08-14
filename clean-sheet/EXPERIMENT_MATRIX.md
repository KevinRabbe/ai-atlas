# Phase 9 Discriminating Experiment Matrix

The purpose of Phase 10 is **not** to build a miniature production AI. It is to build the smallest instrumented organism that can falsify architectural choices.

All experiments should report task quality **and** the Phase-8 resource/assurance metrics.

## Common controls

Unless the experiment explicitly varies them, hold constant:

- underlying task distribution;
- total available training experience;
- total active compute budget;
- persistent-state budget;
- interaction/tool budget;
- verification/assurance budget;
- hardware/platform;
- external evidence source;
- objective/constraint information;
- evaluation hidden set.

Random seeds/initialization should be replicated enough to separate architecture effect from optimization variance.

---

## E01 — Central/hierarchical versus distributed operation allocation

**Question:** Does global/hierarchical metacontrol produce better resource allocation than local event-driven policies after communication/latency overhead?

**Compare:** Candidate A vs Candidate B; optionally C as implicit-control reference.

**Task family:** mixed task stream where some items are trivial, some require retrieval, some require verification, some require additional observation and some require multi-step search.

**Manipulate:** dependency density and resource prices.

**Measure:** utility, operation count, wall-clock, communication bytes, missed escalations, unnecessary escalations, tail failures, metacontrol overhead.

**Falsifies A if:** distributed/local allocation matches or exceeds utility with lower cost across both sparse and moderately coupled tasks.

**Falsifies B if:** increasing interdependence causes rapidly rising communication/incoherence and A retains efficiency.

---

## E02 — Integrated versus heterogeneous cognitive computation

**Question:** Is shared integrated representation more resource-efficient than explicit specialized processes?

**Compare:** Candidate C vs Candidate A/B using matched total learned capacity and compute.

**Task family:** mixture of pattern generalization, exact state manipulation, structured planning, memory use and prediction.

**Measure:** quality, transfer, learning speed, internal/external communication, memory movement, update interference, diagnosis accuracy after injected failures.

**Falsifies C if:** heterogeneous systems deliver materially better capability/resource and lower interference across diverse tasks.

**Falsifies heterogeneous prior if:** C matches capability while substantially lowering communication/latency and does not suffer serious interference.

---

## E03 — Direct-address evidence versus compressed current state

**Question:** How much information should stay directly addressable versus compressed into evolving active state?

**Configurations:**

1. mostly direct-address history;
2. mostly bounded/compressed state;
3. hybrid compressed state + selective source retrieval.

**Task family:** long sequences with entity updates, exact earlier details, distractors, hidden exogenous changes and later objective switches.

**Measure:** exact recall, current-state accuracy, retrieval rate, active-state size, persistent-state size, latency, false stale-state actions, transfer after objective change.

**Key discriminator:** identify crossover point where source access cost exceeds compression errors/interference.

---

## E04 — Internal representation format

**Question:** What representation should intermediate reasoning/communication use?

**Compare:** human-readable discrete state, opaque continuous state, structured/executable state, hybrid.

**Task family:** backtracking, compositional constraints, exact interfaces, cross-process communication and tasks requiring human audit.

**Control:** equal information/bandwidth or equal realized compute in separate sub-experiments.

**Measure:** task utility, bytes/steps, latency, error correction, protocol stability, cross-version compatibility, verifier usefulness, audit faithfulness.

**Important:** do not reward human-readable formats merely for being easier to inspect; auditability is one explicit metric among several.

---

## E05 — Fixed versus adaptive computation budget

**Question:** Can a learned/engineered marginal-value policy reliably spend more compute only where useful?

**Compare:** fixed operation budget, difficulty heuristic, learned value-of-computation policy.

**Task family:** controlled difficulty spectrum with known ground truth and variable verifier/tool availability.

**Shift test:** change compute/latency costs after training.

**Measure:** quality-cost frontier, calibration of marginal-value prediction, underthinking rate, wasted compute, OOD allocation behavior.

**Falsifies adaptive-control hypothesis if:** meta-control overhead/misprediction eliminates gains outside its training resource regime.

---

## E06 — Single belief versus multiple hypotheses

**Question:** When does keeping multiple plausible current states outperform committing to one?

**Task family:** partially observed environments with ambiguous entities/causes and reversible/irreversible actions.

**Manipulate:** observation ambiguity, cost of additional evidence, consequence of wrong commitment.

**Measure:** decision utility, state memory, evidence queries, catastrophic wrong commitments, resolution speed.

**Expected crossover:** single belief should dominate when ambiguity is low; multiple hypotheses should gain as uncertainty/consequence rise.

---

## E07 — Passive versus active information acquisition

**Question:** Does the controller learn when a query/probe is worth more than internal computation?

**Task family:** hidden-state problems where optional observations have known costs and varying informativeness.

**Compare:** passive-only, fixed query schedule, value-of-information policy.

**Measure:** decision quality, query cost, avoidable uncertainty, risky unnecessary probes, model-simulation compute saved.

---

## E08 — World-state representation breadth

**Question:** Should predictive state reconstruct broad environment information or retain only current-decision variables?

**Train:** both representations on Objective A.

**Then switch:** Objective B depends on variables irrelevant under A.

**Measure:** initial efficiency, A performance, B adaptation sample/compute cost, unrecoverable information loss, source-evidence retrieval dependence.

**Discriminator:** lifetime utility under changing goals rather than one-objective accuracy.

---

## E09 — One persistence timescale versus staged consolidation

**Question:** Should new experience become durable immediately or pass through reversible state first?

**Task stream:** alternating stable regularities, temporary noise, real regime changes and rare important exceptions.

**Compare:** immediate durable update; fast editable state + evidence threshold + consolidation; multiple learned timescales.

**Measure:** adaptation speed, false durable updates, forgetting, rollback, repeated inference/retrieval cost, retained rare capability.

---

## E10 — Global versus factorized credit assignment

**Question:** Can local temporary credit plus delayed outcome feedback scale without full end-to-end history/credit propagation?

**Task family:** compositional multi-stage tasks with delayed final outcome and nondifferentiable/external operations.

**Compare:** full global credit where technically possible; local/factorized credit; hybrid.

**Measure:** sample efficiency, memory required for trajectory retention, communication, error localization, final utility.

---

## E11 — Similarity retrieval versus decision-value retrieval

**Question:** Should persistent evidence access optimize representational similarity or downstream action value?

**Corpus:** same memories with obsolete, causally relevant, semantically similar and procedurally relevant distractors.

**Compare:** generic similarity score; temporal/causal rules; learned downstream-value policy; hybrid.

**Measure:** retrieval precision by category, task success, stale-state errors, training/maintenance cost.

---

## E12 — Outcome versus process/state-transition verification

**Question:** Which verification granularity yields the best reliability per cost?

**Task family:** tasks with controllably checkable intermediate states and final outcomes.

**Compare:** final-only, intermediate-only, adaptive hybrid.

**Measure:** final correctness, irreversible intermediate failures caught, verification cost, false reject rate, search speed, error localization.

---

## E13 — Evaluator independence under optimization pressure

**Question:** How quickly does correlated evaluator consensus fail as a generator searches against it?

**Setup:** create evaluators with deliberately shared versus independent blind spots.

**Sweep:** candidate/search pressure.

**Measure:** evaluator score, hidden ground-truth score, false acceptance, attack discovery rate, cost.

**Discriminator:** empirical assurance value of independent failure sources versus evaluator count.

---

## E14 — Learned behavior constraints versus external capability boundaries

**Question:** How much safety/reliability comes from behavioral policy versus externally enforced action scope?

**Compare:** behavior-only constraints, external bounds only, hybrid.

**Adversarial environment:** untrusted observations attempting to redirect privileged action.

**Measure:** successful task utility, unauthorized-effect rate, false blocks, escalation friction, recovery.

---

## E15 — Greedy versus population self-improvement

**Question:** Does preserving alternative system variants/stepping stones improve adaptation under later objective/resource changes?

**Setup:** sequence of improvement opportunities with deceptive local optima; later change objective or hardware cost.

**Compare:** keep only current best; small diverse archive; larger population.

**Measure:** peak/current utility, recovery/adaptation after shift, search/validation cost, diversity, hidden regression rate.

---

## E16 — Local patch versus broad structural mutation

**Question:** When do accumulated local fixes become more expensive than changing a deeper shared mechanism?

**Setup:** inject a repeated family of related failures.

**Compare:** procedure/runtime patches; isolated durable adaptation; broad learned/structural change.

**Measure:** immediate repair, transfer to unseen related failures, patch complexity, inference overhead, regression, assurance cost, lifetime utility.

---

## E17 — Fixed structure versus developmental/generative organization

**Question:** Can compact rules that grow/reconfigure structure find better long-horizon organizations than directly fixed/mutated mature structures at equal search cost?

**Compare:** fixed topology with state/parameter learning; direct structural search; indirect/generative structural search.

**Task stream:** changing modular tasks/resource constraints.

**Measure:** final utility, search evaluations, adaptation after shift, structural complexity, interface churn, rollback/regression burden.

**Critical for Candidate D.**

---

## E18 — Synchronous versus event-driven execution

**Question:** Does event-triggered/local computation reduce physical cost without introducing coordination instability?

**Task family:** sparse-event and dense-interaction regimes.

**Measure:** active operations, latency, synchronization, data movement, stale-state race failures, energy where measurable.

**Compare primarily:** Candidate B versus synchronized variants of A/C.

---

## E19 — Uniform versus adaptive representation/precision granularity

**Question:** Can the system allocate fidelity/compute according to uncertainty/exactness without destabilizing long-lived state?

**Task family:** predictable bulk sequences with rare exact identifiers, arithmetic/formal fields and long-horizon state.

**Measure:** quality, exact-field errors, memory/bandwidth, accumulated state error, compute/energy.

---

## E20 — Transparent versus hidden regression evidence during self-improvement

**Question:** How quickly does repeated improvement overfit its acceptance suite?

**Compare:** all tests visible; mixed visible + hidden; rotating/adversarial holdout.

**Measure over many iterations:** public score, hidden score, regression accumulation, repair speed, search efficiency.

---

## E21 — Integrated versus explicit assurance allocation

**Question:** Can the cognitive substrate safely learn when verification is needed, or does an explicit external risk/assurance allocator add value?

**Compare:** implicit self-check/decision; explicit consequence-sensitive assurance policy; uniform high verification.

**Measure:** task utility, verification cost, catastrophic false acceptance, false reject, distribution-shift behavior.

---

## E22 — System-level resource substitution

**Question:** Can a meta-policy learn substitutions among memory, computation, observation, tools and learning?

**Setup:** same tasks under changing relative prices for compute, storage, observation and verification.

**Compare:** independently optimized fixed policies versus shared cross-resource controller.

**Measure:** lifetime utility/cost vector and adaptation speed after price changes.

**Critical discriminator:** whether the Atlas's allocation hypothesis provides practical gain beyond fixed heuristics.

---

# Experiment ordering for the smallest research organism

Do **not** implement all experiments at once.

Recommended order:

### Tier 1 — architectural core

1. E03 direct-address vs compressed state;
2. E05 adaptive compute;
3. E01 hierarchical vs distributed control;
4. E02 integrated vs heterogeneous computation;
5. E04 internal representation;
6. E09 persistence/consolidation.

These determine the core state/control organization.

### Tier 2 — persistent/action intelligence

7. E06 belief hypotheses;
8. E07 active information acquisition;
9. E08 predictive-state breadth;
10. E11 memory retrieval objective.

### Tier 3 — verification/control

11. E12 verification granularity;
12. E13 evaluator independence;
13. E14 capability boundaries;
14. E21 assurance allocation.

### Tier 4 — learning/self-improvement

15. E10 credit assignment;
16. E16 patch vs structural change;
17. E15 population self-improvement;
18. E20 hidden regressions;
19. E17 developmental structure.

### Tier 5 — physical co-design

20. E18 event-driven execution;
21. E19 adaptive fidelity;
22. E22 cross-resource substitution.

This ordering gives the research organism enough structure to test later mechanisms without baking them into the initial design.

# Minimum rule for conclusions

No architecture conclusion should be promoted from one synthetic benchmark. A design preference should survive:

- at least one in-distribution task family;
- one structurally different task family;
- one resource-regime change;
- a failure/ablation test targeted at the mechanism's claimed benefit.
