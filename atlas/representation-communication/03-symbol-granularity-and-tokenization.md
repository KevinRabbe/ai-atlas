# Symbol Granularity, Tokenization and Adaptive Units

## Required function

Partition raw information into computational units whose granularity matches local information complexity without introducing unnecessary vocabulary assumptions or compute.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| R-SG-01 | Fixed subword vocabulary/tokenization is not required for scalable language modeling; byte-level BLT matches token-based performance at studied scale. | O | E3 | R-S006 |
| R-SG-02 | BLT dynamically groups bytes into patches according to local entropy, allocating more model computation where the next-byte distribution is less predictable. | O | E3 | R-S006 |
| R-SG-03 | Learned discrete communication and byte/continuous approaches together demonstrate that useful computational units can be task-learned, raw-data-derived or adaptive rather than hand-fixed linguistic tokens. | I | E3 | R-S004, R-S006 |

## Tokenization is an interface optimization

A token vocabulary provides:

- shorter sequence length than raw characters/bytes;
- stable discrete IDs;
- human-language regularities embedded in segmentation;
- efficient lookup/embedding operations.

But it also introduces:

- language/domain-specific segmentation assumptions;
- fixed granularity even where information complexity differs;
- brittle handling of rare strings, code, numbers or novel scripts;
- vocabulary storage and boundaries unrelated to machine reasoning needs.

## Adaptive granularity

The broader clean-sheet idea is not specifically “use bytes.” It is:

> computational granularity can depend on information content and downstream needs.

Possible regimes:

- coarse chunks for highly predictable/redundant regions;
- fine units around novelty, uncertainty or exact identifiers;
- event-based representations when nothing changes;
- hierarchical units where local detail is summarized into larger structures.

This connects directly to adaptive compute and information allocation.

## Internal versus external units

Human-facing input/output may retain textual characters/tokens while internal state uses different units. Conversely, tool/software interfaces may need exact byte/symbol preservation even if semantic reasoning uses compressed state.

The system therefore may require **lossless boundary representations** plus task-adaptive internal abstraction.

## Clean-sheet restatement

Choose representation granularity as part of resource allocation:

`local uncertainty + exactness requirement + future-use likelihood + interface constraints -> unit size/fidelity/compute`.

## Failure modes

Vocabulary lock-in; byte-level sequences waste compute on predictable regions; adaptive segmentation destroys stable identity; chunk boundary loses dependencies; compression of exact code/IDs; representation granularity changes incompatibly after model update; human-language segmentation accidentally becomes internal ontology.
