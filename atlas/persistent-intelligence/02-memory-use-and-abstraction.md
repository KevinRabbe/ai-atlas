# Memory Use, Abstraction and Experience

## Required function

Turn stored experience into information that improves future decisions rather than merely reproducing old text.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-MU-01 | Retrieval-augmented models can use explicit external knowledge to improve knowledge-intensive prediction while using substantially less parametric capacity. | O | E4 | P-S005, P-S006 |
| P-MU-02 | Episodic records plus retrieval/reflection can change long-horizon agent behavior; ablations in Generative Agents found memory/reflection/planning components materially affected behavioral evaluations. | O | E3 | P-S007 |
| P-MU-03 | Current agent-memory methods that perform well on recall/long-context tests can still fail when memory must guide later actions in interdependent tasks. | O | E3 | P-S010, P-S011, P-S013 |
| P-MU-04 | No single memory form dominates across knowledge-oriented and execution-oriented settings; procedural/experience memory becomes more useful when stored experience matches task structure. | O | E3 | P-S012 |
| P-MU-05 | Similarity-only retrieval can lose causal/objective structure important for agentic trajectories. | O/I | E2 | P-S015 |

## Distinct memory products

A persistent system should distinguish at least:

- **episodic** — specific events/trajectories with time and provenance;
- **semantic** — generalized facts/relations abstracted across evidence;
- **procedural** — reusable workflows, policies and skills;
- **state** — best current estimate of mutable environment variables;
- **failure memory** — conditions, attempted actions and observed failure modes;
- **source/archive** — raw evidence retained for audit/reconstruction.

These are functional categories, not required storage formats.

## Retrieval objective

Semantic similarity is only one signal. Useful retrieval may depend on:

`goal relevance + causal relation + temporal validity + reliability + expected decision impact + recency + novelty + cost`.

A memory can be semantically similar but actively misleading if it describes an obsolete state or a failed procedure.

## Reflection / abstraction

Repeated episodes can be transformed into higher-level knowledge:

`episodes -> patterns -> hypothesis/rule -> validation -> semantic/procedural memory`.

This is closely related to Phase-2 consolidation: repeated costly lookup should be converted only when abstraction preserves the conditions under which the rule is valid.

## Experience is not raw trajectory storage

An experienced system should be able to answer questions such as:

- what usually works here?
- what changed since last time?
- what failed and under which preconditions?
- which parts of the old procedure remain valid?
- how confident is this lesson and from how many independent episodes?

The trajectory itself is evidence; the reusable lesson is a derived object that must retain links back to evidence.

## Failure modes

Similarity without usefulness; over-generalization from one episode; procedural memory applied outside its domain; reflection hallucination; loss of edge cases during abstraction; duplicated memories competing for retrieval; derived rule losing source provenance; retrieving an old success after environment conditions changed.
