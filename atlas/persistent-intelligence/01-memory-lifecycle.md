# Memory Lifecycle and Governance

## Required function

Preserve useful information across time while controlling what is written, how it is revised, when it is consolidated, how it is retrieved, and when it should be forgotten.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-ML-01 | Learnable external read/write memory can add structured storage/manipulation capabilities beyond recurrent hidden state alone. | O | E4 | P-S003, P-S004 |
| P-ML-02 | Explicit non-parametric memory can improve knowledge-intensive generation and can be updated independently of model weights. | O | E4 | P-S005, P-S006 |
| P-ML-03 | Hierarchical memory/context management can extend useful history beyond the active model window. | O | E3 | P-S008 |
| P-ML-04 | Long-running agent memory requires write, revision, forgetting and retrieval policies; record-level correctness alone is insufficient when beliefs/world state change. | I | E3 | P-S010, P-S011, P-S012, P-S016 |
| P-ML-05 | Long-horizon memory benchmarks expose failures from stale state, poor task use and weak conflict handling even when simple recall is strong. | O | E3 | P-S010, P-S011, P-S012, P-S013, P-S014 |

## Memory is not append-only storage

A persistent agent accumulates observations whose truth status can differ:

- immutable event: “tool X returned Y at time t”;
- mutable state: “door is open”;
- user preference: “prefer compact answers,” which may change;
- hypothesis: “service failure was caused by rate limiting”;
- learned procedure: “this environment needs step A before B.”

Treating all of these as timeless facts produces contradiction accumulation and stale-action errors.

## Clean-sheet lifecycle

A persistent memory item should be considered a governed state object with at least:

`content + type + time/scope + provenance + confidence + dependencies + revision relation + usage history`

The lifecycle is approximately:

`observe -> candidate write -> validate/classify -> store -> retrieve/use -> revise/reconsolidate -> abstract or forget`

The storage engine is secondary to this semantics.

## Write control

Writing everything is not neutral. It creates:

- storage growth;
- retrieval competition;
- false-memory exposure;
- stale-state burden;
- consolidation cost;
- privacy/provenance burden.

Recent adaptive-memory work explicitly learns/selects what is worth retaining under finite budgets, reinforcing the Phase-2 “change allocation” view.

## Revision instead of overwrite

When new evidence conflicts with old state, three operations must remain distinct:

1. **invalidate/retire** an old belief;
2. **supersede** a time-varying state while preserving history;
3. **retain competing hypotheses** when evidence is insufficient.

Blind overwrite destroys provenance; blind accumulation leaves contradictory active truth.

## Forgetting

Forgetting can be functional when information is obsolete, low-value, redundant or harmful to retrieval. It should not mean silently deleting evidence required for audit or rollback. A useful system may separate archival history from active memory.

## Failure modes

Write-everything bloat; false durable memory; stale facts treated as current state; contradiction without temporal scope; provenance loss; deletion of audit evidence; semantic-similarity retrieval of irrelevant memories; memory poisoning; feedback loops where a mistaken memory generates evidence that reinforces itself.
