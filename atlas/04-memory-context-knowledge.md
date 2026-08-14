# Memory, Context & Knowledge

## Required function

Preserve useful information across timescales, maintain its temporal/provenance semantics, and make the right information available to future computation and action without overwhelming the active substrate.

## Status

**First coupled persistent-intelligence evidence pass completed on 2026-08-14; not saturated.**

Detailed notes live under [`persistent-intelligence/`](persistent-intelligence/INDEX.md). Memory is studied together with temporal belief state, world models and action because persistent correctness depends on revision and downstream use, not storage alone.

## First-pass findings

1. **Memory is a lifecycle.** Write, revise, consolidate, retrieve and forget are separate decisions.
2. **Archive != current belief.** Past observations are evidence; mutable current state must be inferred from actions, time and later observations.
3. **Memory value is downstream-use dependent.** Similarity/recall alone do not establish usefulness.
4. **Experience needs abstraction.** Episodes can become semantic/procedural knowledge, but applicability conditions and provenance should survive consolidation.
5. **No memory form dominates.** Long context, retrieval, learned state, episodic records, procedures and parametric knowledge expose different trade-offs.
6. **Forgetting can be functional.** Obsolete or low-value information can damage retrieval, while audit history may still need archival retention.
7. **Recent benchmarks expose a memory-to-action gap.** Systems can remember old information yet fail to use it correctly in later stateful tasks.

## Distinctions to preserve

Parametric knowledge; active/working state; episodic memory; semantic memory; procedural/skill memory; external factual stores; current environment belief; event/archive history; caches; learned recurrent/test-time state; provenance; temporal scope; confidence; applicability conditions.

## Clean-sheet questions

- What deserves a write at all?
- What should be remembered verbatim versus compressed/generalized?
- How should contradictory and superseded state be represented?
- What retrieval objective best predicts downstream decision value?
- How is current belief reconstructed from partial/stale observations?
- When should repeated external knowledge migrate into weights or executable skills?
- When is forgetting correct, and what must remain in immutable audit history?
- Can memory policy itself learn from downstream success/failure without creating self-reinforcing false memory?

## Anti-assumptions

Do not assume memory means a vector database, a transcript, an ever-growing context or a human cognitive taxonomy. These are implementations/descriptions; the required function is governed persistence and future-useful state.
