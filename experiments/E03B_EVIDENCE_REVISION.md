# E03B — Evidence Revision and Current-Belief Reconstruction

**Status:** second E03 family; preliminary 20-seed evidence.

## Question

Should a persistent system keep only a compressed current belief, replay raw evidence whenever it needs current state, or maintain a fast current-state cache that stays linked to source evidence so old evidence can later be retracted/corrected?

## Environment

A stream adds signed evidence for 20 entities. Later operations can retract an earlier evidence item by exact event ID. Queries ask either:

- current aggregate belief for an entity; or
- exact active provenance IDs supporting that entity.

Retraction probability is swept from 0 to 0.30. Policies are not given extra reconstruction information after a retraction.

## Variants

- `direct_evidence_replay` — stores the raw mutation log and reconstructs active evidence from the full log at every query.
- `compressed_current_only` — stores only per-entity aggregate current state. It is intentionally unable to reverse a source update after discarding which event contributed it.
- `evidence_linked_current` — stores a compact current aggregate plus source/event indexes so a retraction can update the derived state directly.

## 20-seed means

| retraction probability | policy | current accuracy | provenance accuracy | reads/query | writes/mutation |
|---:|---|---:|---:|---:|---:|
| 0.00 | raw replay | 1.000 | 1.000 | ~599.5 | 1.00 |
| 0.00 | compressed only | 1.000 | 0.000 | 1.0 | 1.00 |
| 0.00 | evidence-linked | 1.000 | 1.000 | 1.0 | 4.00 |
| 0.05 | compressed only | 0.882 | 0.000 | 1.0 | 0.95 |
| 0.05 | evidence-linked | **1.000** | **1.000** | ~1.1 | 3.95 |
| 0.15 | compressed only | 0.789 | 0.000 | 1.0 | 0.85 |
| 0.15 | evidence-linked | **1.000** | **1.000** | ~1.3 | 3.85 |
| 0.30 | compressed only | 0.684 | 0.000 | 1.0 | 0.71 |
| 0.30 | evidence-linked | **1.000** | **1.000** | ~1.7 | 3.71 |

Raw replay remains exact across the sweep but stays near ~600 reads/query because it reconstructs from the full mutation history.

## Interpretation

This second family makes the E03 trade-off sharper:

- **compressed current state is valuable** when source history will never matter again;
- **raw evidence is valuable** for correction/provenance but is an expensive working-state representation;
- **evidence-linked current state** pays write/index/storage overhead to make current decisions cheap while preserving revision and provenance semantics.

This directly supports the persistent-intelligence distinction between **event history** and **current belief**: they are separate computational objects, but current belief should remain reconstructible/revisable from evidence when the environment permits corrections.

## Design-ledger implication

Together with original E03, E03B supplies a second task family, a source-correction failure test and a retraction-rate resource/regime sweep. DL-003 can therefore move to a principle-level provisional selection: **fast derived current state + retained source evidence/provenance**, with the exact archive/index strategy remaining open.

## Falsifier

A compressed-only system should regain preference where future correction/provenance value is genuinely zero. A raw-replay system should regain preference if write/index/storage cost dominates query/revision cost. The selected principle is therefore conditional on persistent systems where revision, audit or conflicting evidence have nonzero future value.
