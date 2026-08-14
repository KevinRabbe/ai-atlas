# Persistent Intelligence — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

## P-P01 — Persistent memory is governed evolving state, not passive storage

Long-lived memory needs write, revision, retrieval, consolidation and forgetting semantics. Correctness depends on how state evolves over time, not only whether individual stored records are accurate.

**Confidence:** high.

## P-P02 — Event history and current belief state should remain conceptually separate

A record of past observations is evidence; current state is an inference conditioned on later actions, elapsed time, hidden changes and uncertainty. Treating the latest retrieved event as current truth is unsafe under partial observability.

**Confidence:** very high.

## P-P03 — Memory value is downstream-use dependent

Similarity and recall accuracy are insufficient. A useful memory changes future decisions correctly. Retrieval should account for temporal validity, causal/task relevance, reliability and expected decision impact.

**Confidence:** high.

## P-P04 — Persistent experience should support abstraction without destroying provenance

Episodes can be consolidated into semantic rules, procedures and failure knowledge, but derived memories should retain links to supporting evidence and applicability conditions.

**Confidence:** medium-high.

## P-P05 — No single memory substrate/form is established as universal

Long context, retrieval, recurrent/test-time state, explicit episodic records, procedural memory and parametric knowledge have different access, update and cost profiles. Recent benchmarks show task-dependent wins and no universal memory method.

**Confidence:** high.

## P-P06 — A world model should predict what decisions require, not necessarily reconstruct everything

MuZero, latent dynamics methods and predictive representation learning show that useful planning models can operate over compact task-relevant state. Full sensory reconstruction is an optional capability, not the definition of a world model.

**Confidence:** high.

## P-P07 — Decision-sufficient state is task-relative

Compression that is sufficient for one objective may remove variables required by later goals. Persistent general systems need mechanisms to preserve/recover information whose future relevance is uncertain.

**Confidence:** medium-high.

## P-P08 — World-model uncertainty must constrain imagination

Model error compounds through rollouts. Internal simulation should compete with real observation, tools and interaction; uncertainty/model-validity should determine when imagined futures stop being trustworthy.

**Confidence:** high.

## P-P09 — Prediction errors are persistent learning events

Mismatch between predicted and observed consequences is evidence about stale state, missing variables, causal error or regime change. These events should influence world-model confidence and future information-acquisition policy.

**Confidence:** high conceptually; implementation open.

## P-P10 — Multimodal grounding benefits from shared correspondences without requiring one homogeneous representation

Shared latent concepts can bind modalities and support transfer, while modality-specific detail can remain local. Language is a powerful interface/supervision signal but is not established as the optimal hub for every internal modality/action channel.

**Confidence:** high for multimodal alignment; medium for optimal representation split.

## P-P11 — Action is also perception

In embodied/digital environments, actions can reveal hidden state. Persistent intelligence should value reversible probes, sensor queries, tool calls and viewpoint changes as information-acquisition operations when they reduce decision-relevant uncertainty.

**Confidence:** high as a control/information principle.

## P-P12 — Long-horizon memory must be evaluated through stateful action

Recall benchmarks alone overestimate persistent competence. Multi-session agent benchmarks expose a memory-to-action gap: systems may remember information but fail to apply it, update it or recognize when it is obsolete.

**Confidence:** high.

## P-P13 — Applicability conditions are part of experience

Reusable knowledge should include when it is valid. Experienced behavior includes declining to reuse an old rule after the environment, user or premise changes.

**Confidence:** medium-high.

---

## Emerging persistent-state loop

A clean-sheet persistent system can be described without choosing a storage/model implementation:

`observe -> identify entities/events -> update belief state -> write governed evidence -> predict/simulate -> act/query -> observe mismatch -> revise confidence/state -> abstract/consolidate/forget`.

The loop connects earlier Atlas themes:

- **compute allocation:** simulate, retrieve, observe, query, act or stop;
- **change allocation:** what memory/belief/model state changes and how durably;
- **information allocation:** what evidence remains active, archived, compressed or discarded.

The recurring cross-domain hypothesis is becoming more specific:

> intelligence may require adaptive allocation of information, computation, interaction and durable change according to expected future utility under uncertainty.

This is still a hypothesis, not the project's final definition.

## Strong anti-conclusions

This pass does **not** justify:

- “memory means vector search”;
- “remember everything”;
- “latest observation is current truth”;
- “world model means video generator”;
- “one latent state is sufficient for every future task”;
- “more imagined rollouts always improve planning”;
- “shared multimodal embedding should erase modality-specific representations”;
- “language should mediate all internal perception/action”;
- “high memory QA accuracy implies a good long-lived agent.”

## Most valuable experiments

1. Compare append-only retrieval memory against governed revision + temporal belief state in environments with deliberately changing facts and hidden state.
2. Hold memory budget constant and optimize retrieval for semantic similarity versus downstream action value.
3. Compare full-observation reconstruction world models with decision-sufficient latent models, then change the downstream objective to measure lost transfer information.
4. Calibrate world-model uncertainty and vary the cost of real observation to learn when the controller should simulate versus query reality.
5. Compare language-mediated multimodal reasoning with shared-latent/direct action channels under equal information and compute budgets.
6. Run multi-session tasks where correct behavior requires remembering old evidence, updating mutable state and refusing obsolete procedures.
