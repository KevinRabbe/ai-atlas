# Discovery & Epistemic Growth — Focused Synthesis

**Status: implementation-neutral focused synthesis; not a selected architecture.**

The Atlas previously treated exploration as a way to improve decisions, acquire information, or search over system variants. This note adds a stronger requirement: an advanced system should be capable of **expanding its epistemic state beyond the human/bootstrap corpus**, while preserving a strict boundary between speculation and knowledge.

The central clean-sheet question is not:

> How can the system sound confident about things humans do not know?

It is:

> How can the system convert uncertainty into testable hypotheses, acquire discriminating evidence, reject failed ideas, and promote only sufficiently supported results into durable knowledge?

---

## 1. Human knowledge is a bootstrap prior, not an epistemic ceiling

Humanity provides an unusually valuable initial corpus:

- language and communication conventions;
- mathematics and formal methods;
- scientific theories and measurements;
- engineering practice;
- known failures and negative results;
- conceptual representations;
- tools and procedures;
- accumulated methods for checking claims.

This is a powerful starting state, but it cannot contain future empirical observations and it contains only a tiny explored subset of the consequences of existing formal knowledge.

Therefore a system optimized only to reproduce the human corpus eventually optimizes the wrong target for discovery.

Implementation-neutral lesson:

> **Supervision should provide epistemic scaffolding without becoming an epistemic ceiling.**

This does not mean established knowledge should be ignored. Departures from well-supported belief should require evidence proportional to the strength of the existing evidence and the consequence of error.

---

## 2. Teacher capability and student capability are different variables

Weak-to-strong evidence shows that the performance of a supervisor need not define a strict upper bound on a stronger learner in studied settings.

The important abstraction is not that a weak teacher magically creates stronger knowledge. The student may contribute:

- greater representational capacity;
- pretrained latent structure;
- different inductive bias;
- additional optimization;
- additional experience;
- search over hypotheses not explicitly demonstrated by the teacher.

Therefore the teacher can provide **directional/error information** without containing the final solution.

Clean-sheet implication:

> The system should be able to use imperfect supervision as one evidence source while retaining enough independent reasoning/evaluation capacity to disagree when stronger evidence supports disagreement.

---

## 3. Generator capability is not the system discovery ceiling

FunSearch and AlphaEvolve demonstrate a separate mechanism:

`candidate generator -> external evaluator -> retain/diversify -> mutate/recombine -> evaluate again`.

The generator need not produce the best candidate in one pass. The larger system can accumulate improvements through repeated objective evaluation.

This suggests a general distinction:

- **proposal quality** — how good individual hypotheses/candidates are;
- **search policy** — which candidates are explored next;
- **evaluation quality** — how reliably progress can be detected;
- **retention/diversity policy** — which partial solutions survive;
- **system discovery ceiling** — what the complete loop can eventually find under finite resources.

A weak proposal distribution paired with a strong evaluator/search procedure may exceed the generator's normal one-shot output. A powerful generator paired with an exploitable evaluator may instead optimize nonsense.

---

## 4. Novelty is not knowledge

The Atlas must explicitly distinguish epistemic states.

### Proposed state classes

1. **Inherited / previously supported knowledge**
   - accepted because of existing evidence/provenance;
   - still subject to revision.

2. **Hypothesis**
   - a candidate explanation, construction, model or prediction;
   - may be novel;
   - carries uncertainty and provenance;
   - must not be treated as established fact.

3. **Candidate discovery**
   - appears to improve or extend the current knowledge frontier;
   - has passed at least one relevant test/evaluator;
   - novelty and evaluator independence may still be unresolved.

4. **Verified discovery**
   - survives a domain-appropriate verification process sufficiently independent from the proposal process;
   - verification scope and assumptions remain explicit.

5. **Replicated / consolidated knowledge**
   - survives additional independent checks, reproduction, or evidence accumulation appropriate to the domain;
   - may be promoted into durable reusable knowledge.

6. **Rejected / unresolved hypothesis**
   - failed, contradicted, or insufficiently tested;
   - should remain recoverable when the negative result has future information value.

The transition rule is therefore not:

`novel output -> knowledge`.

It is closer to:

`novel proposal -> discriminating test -> evidence -> scoped verification -> replication/review -> consolidation`.

---

## 5. Two fundamentally different discovery regimes

### A. Deductive / constructive discovery

Existing axioms, rules, observations or formal objects already imply a result, but humanity has not found the implication or construction.

Examples include:

- new mathematical proofs;
- counterexamples;
- improved bounds;
- better algorithms;
- new executable constructions.

The information is logically/computationally latent in the existing problem specification, but it is **epistemically new** to humanity.

This regime often permits unusually strong evaluators:

- formal proof checking;
- exact computation;
- executable tests;
- counterexample verification;
- deterministic scoring.

That makes aggressive search comparatively safe when evaluator scope is clear.

### B. Empirical discovery

The missing information is not available in the current corpus and cannot be obtained by internal reasoning alone.

Examples include unknown properties of:

- physical materials;
- biological systems;
- unexplored environments;
- interventions;
- measurements under new experimental conditions.

Here the system must interact with an external source of truth:

`hypothesis -> experiment/intervention -> observation -> update`.

No amount of internal computation can substitute for genuinely missing observations when multiple worlds remain observationally compatible with the existing evidence.

Clean-sheet implication:

> A complete discovery system requires both computation/search and a policy for acquiring new evidence from reality when internal uncertainty cannot be resolved deductively.

---

## 6. Discovery is a value-of-information / value-of-computation problem

A hypothesis does not need high probability to deserve investigation.

The relevant quantity is closer to:

`expected information/utility gain from resolving hypothesis - experiment/search/assurance cost`.

A low-probability hypothesis can deserve attention when:

- consequence/value if true is large;
- a cheap decisive test exists;
- it explains an important anomaly;
- it opens a large new hypothesis region;
- current theories are weak or contradictory.

This extends PS-005 beyond inference-time reasoning:

> **Experience and experiment selection should also be resource-rational.**

The system should choose among:

- think/search more;
- retrieve existing evidence;
- simulate;
- prove/check formally;
- ask an external expert/system;
- gather another observation;
- perform an intervention;
- build a tool or experiment;
- stop because expected information gain is too low.

---

## 7. Discovery must preserve epistemic disagreement

Prematurely collapsing to one explanation destroys discovery potential.

Useful discovery systems may need to retain multiple hypotheses with:

- supporting evidence;
- contradicting evidence;
- assumptions;
- predicted observations;
- discriminating experiments;
- estimated value of resolution.

This directly connects to unresolved DL-006 (single belief versus multiple hypotheses) and DL-007 (active information acquisition).

The discovery loop therefore gives Tier-2 experiments greater architectural importance: they are not only state-management features; they are prerequisites for autonomous epistemic growth.

---

## 8. Verification quality determines how far search can leave the known distribution

When evaluation is strong and objective, exploration can be aggressive.

When evaluation is weak, correlated, subjective or exploitable, search pressure can produce convincing false discoveries.

Therefore discovery power should co-scale with:

- verifier independence;
- hidden/holdout checks;
- replication;
- source provenance;
- adversarial counterexample search;
- uncertainty about the evaluator itself.

This directly reuses the Phase-5 principle that a verifier provides scoped evidence, not truth.

A discovery system must never infer:

`passed evaluator -> globally true`.

It should record:

`passed property X under assumptions Y using evaluator Z at time T`.

---

## 9. Failed discovery attempts are knowledge too

Negative results can remove uncertainty even when no positive discovery is produced.

Useful retained failure information includes:

- hypothesis tested;
- conditions tested;
- evaluator/experiment used;
- observed failure;
- likely reason;
- whether the failure generalizes;
- what would justify revisiting it.

Without this, an autonomous research system can repeatedly rediscover the same dead ends.

Therefore the value of discovery work is not only `new positive result`.

A more general objective is:

> **uncertainty removed per unit lifetime resource and risk cost.**

---

## 10. Human-readable explanation is downstream of discovery

The internal representation that produces a discovery need not match existing human conceptual vocabulary.

A system may benefit from inventing representations that make regularities computationally simple even if humans initially find them unintuitive.

However, a claim intended to enter shared human knowledge eventually needs a translation layer that exposes enough of:

- the claim;
- evidence;
- assumptions;
- reproducible procedure;
- uncertainty;
- counterexamples/failure limits;

for independent checking.

Thus:

`machine-native discovery representation != human-facing scientific explanation`.

They are separate interfaces with separate fidelity requirements.

---

# Focused synthesis principles

## DEG-P01 — Human knowledge is bootstrap, not ceiling

Human knowledge is an initial prior, method library and evidence base. A discovery-capable system must be allowed to form and test hypotheses outside the demonstrated human solution distribution.

**Type:** inference/design requirement
**Confidence:** medium-high

## DEG-P02 — Supervision can guide without containing the final answer

Weak supervisors can provide useful learning signal while stronger learners generalize beyond supervisor performance in studied settings.

**Type:** observation/inference
**Confidence:** medium

## DEG-P03 — Search + reliable evaluation can exceed one-shot generator capability

System discovery capability can exceed normal generator output when candidate search is coupled to sufficiently reliable external evaluation and diversity/retention.

**Type:** observation/inference
**Confidence:** high in verifiable domains

## DEG-P04 — Novelty and truth must remain separate state dimensions

A novel proposal is not knowledge. Promotion requires evidence appropriate to the domain and explicit verifier scope.

**Type:** design requirement grounded in verification failures
**Confidence:** high

## DEG-P05 — Discovery requires epistemic state transitions

Hypothesis, candidate discovery, verified result and consolidated knowledge should be distinguishable states with different authority and persistence semantics.

**Type:** design requirement
**Confidence:** medium-high

## DEG-P06 — Deductive and empirical discovery require different evidence channels

Internal search can produce new deductive/constructive knowledge; empirical unknowns require new external observations/interventions when current evidence is insufficient to identify the answer.

**Type:** inference from causality/computation foundations
**Confidence:** high

## DEG-P07 — Discovery effort should be allocated by expected information/value gain

The system should decide whether to search, simulate, prove, observe, experiment or stop according to expected uncertainty reduction/future utility relative to cost and risk.

**Type:** hypothesis extending value-of-computation/value-of-information results
**Confidence:** medium

---

# New implementation-neutral required function

This synthesis adds **F26 — Epistemic frontier expansion / discovery** to `REQUIRED_FUNCTIONS.md`.

It does **not** require a dedicated discovery module. Existing reasoning, memory, experimentation, verification and learning mechanisms may jointly implement it.

---

# Candidate Phase-10 experiment — E23

## E23 — Weak-teacher / independent-evaluator discovery loop

**Question:** Can a system reliably produce verified candidates beyond the demonstrated capability/knowledge of its supervisor, and which parts of the loop are necessary?

### Compare

1. teacher imitation only;
2. generator/search without independent evaluator;
3. generator + evaluator + greedy retention;
4. generator + evaluator + diverse hypothesis archive;
5. full epistemic lifecycle with hypothesis status, independent hidden checks and consolidation.

### Synthetic first task family

Use a search space where:

- the teacher demonstrates only suboptimal constructions/rules;
- a hidden exact evaluator can identify better solutions;
- better solutions are absent from demonstrations;
- local optima and deceptive heuristic regions exist;
- ground-truth novelty relative to the teacher corpus is measurable.

### Measure

- verified improvement beyond teacher frontier;
- novelty relative to demonstrations;
- rediscovery rate;
- false-discovery rate under hidden evaluator checks;
- evaluator exploitation;
- diversity retained;
- compute/evaluation cost;
- time to first verified beyond-teacher result;
- retention of negative results;
- performance after evaluator/resource regime changes.

### Critical ablations

- remove independent hidden checking;
- remove diversity/archive;
- allow hypotheses to enter durable knowledge immediately;
- weaken evaluator quality;
- increase search pressure;
- remove explicit negative-result memory.

### Promotion rule

Success on E23 would establish only that the **mechanics of epistemic growth** work in a controlled world. It would not by itself demonstrate new human knowledge. Promotion to real discovery claims requires externally verified results on domains where the answer was not previously known.

---

# Falsifiers / boundary conditions

This synthesis should be weakened if:

- systems trained on existing answers cannot reliably exceed teacher frontiers without hidden additional answer information;
- generator/evaluator loops fail to outperform one-shot generation after matched resource accounting;
- novelty tracking cannot distinguish rediscovery from genuine frontier expansion at usable cost;
- evaluator exploitation grows faster than assurance can scale;
- retaining explicit hypothesis/evidence state adds no value over immediate belief mutation;
- empirical discovery cannot select informative experiments better than fixed/random policies under matched interaction budgets.

---

# Source trail

See `sources/DISCOVERY_EPISTEMIC_GROWTH.md` for the primary-source registry.
