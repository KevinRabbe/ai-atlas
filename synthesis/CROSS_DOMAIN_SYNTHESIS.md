# Cross-Domain Synthesis — First Pass

**Status: implementation-neutral synthesis, not architecture.**

This document collapses recurring findings from Foundations, Architecture/Systems, Biology, Learning, Inference-Time Intelligence, Persistent Intelligence, Verification/Control and Self-Improvement.

## 1. The recurring object is a state transition under constraints

Across domains, an intelligent system repeatedly faces a general problem:

`current state + evidence + goal/utility + uncertainty + available operations + resource/authority constraints -> choose next transition`.

Different fields expose different transition classes:

- inference chooses a computation/tool/search/action;
- memory chooses a write/revision/retrieval/forget operation;
- learning chooses which substrate changes and how durably;
- world modeling predicts transitions before acting;
- verification decides whether a candidate transition has enough evidence to propagate;
- systems scheduling chooses physical execution and precision;
- self-improvement chooses transitions between system variants.

This does **not** imply one universal algorithm solves every class. It is a shared abstraction for comparing them.

## 2. Five allocation problems recur

### A. Compute allocation

What should be computed, searched, simulated, retrieved, delegated or executed—and when should computation stop?

Evidence: variable test-time compute, search, tools, recursion, adaptive computation, conditional routing and systems cost all show that fixed uniform computation is structurally wasteful.

### B. Information allocation

What information remains active, directly addressable, compressed into state, archived, abstracted, retrieved or forgotten?

Evidence: rate/relevance trade-offs, direct-address vs recurrent-state trade-offs, memory lifecycle, RLM-style external context and persistent belief-state requirements.

### C. Change allocation

What should adapt, at what scope, and for how long?

Evidence: runtime state, external memory, skills/adapters, shared weights, harness policy and architecture all have different update speeds, integration benefits and interference/rollback costs.

### D. Assurance allocation

How much independent evidence, restriction, verification and authorization should a transition require?

Evidence: calibration/selective prediction, formal/process/outcome verification, Goodhart effects, capability control, regression gates and rollback. Required assurance rises with uncertainty, consequence, scope, persistence, privilege, irreversibility and optimization pressure.

### E. Exploration / design allocation

How much resource should be spent exploiting the current best solution versus exploring alternatives, collecting information or searching over future system variants?

Evidence: exploration-exploitation theory, branching/search, active perception, populations/archives, architecture/algorithm discovery and self-improvement.

## 3. Uncertainty is not a metadata field; it controls allocation

Across Foundations, world models, inference and verification, useful uncertainty changes behavior.

It can trigger:

- more computation;
- branching or alternative hypotheses;
- retrieval;
- active observation/probing;
- tool use;
- reduced action scope;
- independent verification;
- abstention/escalation;
- delayed consolidation;
- preservation of multiple system variants.

Confidence that never changes decisions has limited operational value.

## 4. Persistence and reversibility form a major axis

Changes range from ephemeral to deeply durable:

`activation/working state -> session state -> memory -> procedure/skill -> harness/policy -> adapter/weights -> architecture/control structure`.

Increasing durability usually increases reuse/integration but also raises interference, provenance and rollback cost. The Atlas does not establish a universal ordering, but repeatedly supports treating persistence as a first-class variable.

## 5. Direct access and compressed state are dual strategies

Many domains contain the same trade-off:

- keep detailed items addressable and pay growing storage/access cost;
- compress history into a bounded state and pay information-loss/interference risk.

This appears in sequence models, context management, memory, world state and even self-improvement archives. Hybrid systems can occupy intermediate points, but no universal optimum is established.

## 6. Representation should serve future computation

No evidence supports human readability, maximum compression, reconstruction fidelity, disentanglement or one shared latent space as universal representation objectives.

A representation is valuable when it:

- preserves decision-relevant distinctions and uncertainty;
- makes likely future operations cheap;
- supports transfer when objectives change;
- exposes needed interfaces to other modules/tools;
- retains enough provenance/recoverability when compression is lossy.

This is one of the strongest reasons to avoid assuming human language as the machine's internal reasoning/communication substrate.

## 7. Intelligence is system-level, not weight-level

Capability can change materially while weights remain fixed through:

- better interfaces;
- context/memory policy;
- tools;
- search;
- verification;
- harnesses;
- persistent state;
- routing/scheduling.

Conversely, some competence is most economical when amortized into learned parameters. Therefore “the model” is one adaptive computational substrate inside a larger system-level optimization problem.

## 8. Learning and inference form a loop

Inference performs expensive task-specific computation. Learning can compile repeated successful computation into cheaper reusable state/skills/weights. The learned system then changes what future inference trajectories are generated.

A general lifetime loop is:

`perform -> verify -> retain evidence -> identify reusable structure -> consolidate if worthwhile -> generate changed future behavior -> re-evaluate`.

The boundary between training and deployment is therefore operational, not fundamental.

## 9. World modeling links memory, causality and action

Persistent intelligence requires both:

- evidence/history of what happened;
- an uncertainty-aware belief about what is true now.

World models extend that belief forward under candidate actions. Prediction error then updates both belief and the model. This creates a closed loop between memory, prediction, action, observation and learning.

A world model need not reconstruct every observable detail; it must preserve what downstream decisions require while managing the risk that future objectives need previously discarded variables.

## 10. Verification changes what optimization is safe

When correctness can be checked mechanically, candidate generation/search can be aggressive because bad proposals are cheap to reject. When evaluators are subjective, learned or incomplete, stronger optimization pressure can exploit them.

Therefore search power and assurance quality should co-scale. More capable generators without stronger evaluators/control can worsen optimization toward the wrong target.

## 11. Capability and authority are orthogonal

A system component can be highly capable yet externally restricted in what state transitions it may cause. This supports using specialized or even partially untrusted components while permissions, sandboxing, transaction gates and independent checks remain separate.

This separation is central for tools, multi-agent systems and self-improvement.

## 12. Self-improvement is ordinary improvement plus a moving search space

Once the system can mutate harnesses, data policies, weights, architecture or mutation operators, improvement itself becomes a target of optimization.

The distinctive risks are:

- attribution to the wrong layer;
- evaluator/objective mutation;
- loss of rollback/lineage;
- premature convergence;
- meta-mutations changing future proposal distributions;
- assurance capacity lagging behind mutation scope.

Self-improvement therefore inherits every earlier requirement rather than replacing them.

## 13. Physical cost is part of intelligence engineering

Actual system performance depends on memory movement, communication, locality, precision, latency and energy—not only mathematical operation counts or parameter counts.

Any clean-sheet design that ignores realized physical cost risks optimizing an abstraction that is not deployable.

## 14. Inductive bias cannot disappear

Every learner/search/controller prefers some structures, operations and representations. The goal is not a bias-free system but one whose biases:

- match useful environment structure;
- are visible enough to test;
- can adapt when that structure changes;
- do not become accidental constraints inherited from current implementation convenience.

---

# Emerging meta-hypothesis

The evidence across domains is consistent with—but does not yet prove—the following characterization:

> **Practical intelligence is adaptive selection and allocation of information, computation, interaction, change and assurance under uncertainty, using learned structure to maximize expected future utility within physical/resource constraints.**

This should be treated as a falsifiable organizing hypothesis, not a definition imposed on the project.

## What would weaken this hypothesis?

- broad intelligence where adaptive allocation policies add no value over uniform fixed computation/state/update rules;
- evidence that uncertainty need not affect rational operation selection or authorization;
- systems where lifetime performance is independent of how information/change are distributed across substrates;
- a single homogeneous mechanism that dominates heterogeneous allocation across tasks/resources without hidden system costs;
- successful self-improvement without any meaningful distinction between generator, evaluator, persistence, authority or rollback.

## What the hypothesis does NOT specify

It does not tell us:

- the neural architecture;
- the internal representation language;
- whether there is one controller or distributed local controllers;
- whether allocation is explicit/symbolic or emerges implicitly;
- the number/type of memory stores;
- whether world models are neural, symbolic, programmatic or hybrid;
- which learning rule is used;
- how much should be centralized versus local;
- what hardware should implement it.

Those remain design dimensions for the clean-sheet phase.
