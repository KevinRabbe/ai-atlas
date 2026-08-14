# Replay, Consolidation and Multiple Timescales

## Required function

Acquire information quickly while deciding later which information deserves durable integration and how it should be reorganized with older knowledge.

## Evidence

- **B-S013 — Frey & Morris (1997):** hippocampal LTP showed a distinction between early transient plasticity and later protein-synthesis-dependent persistence, with synaptic tagging proposed/tested as a mechanism for selective stabilization.
- **B-S014 — Skaggs & McNaughton (1996):** hippocampal firing sequences observed during spatial experience were reflected in subsequent sleep activity, including temporal order.
- Biological memory research more broadly supports multiple consolidation scales, but causal roles and mechanisms differ across memory systems and remain active research.

## Computational abstraction

Separate at least three states:

1. **candidate/working adaptation** — cheap and rapidly reversible;
2. **eligible memory** — marked as potentially important and available for replay/evaluation;
3. **consolidated knowledge** — expensive, durable integration after additional evidence.

Replay provides a mechanism for using idle/offline compute to re-evaluate or reorganize stored experience without requiring the original environment to be present.

## Clean-sheet relevance

This directly motivates experiments comparing immediate weight updates against delayed consolidation into weights, memory, skills or policies. It does **not** justify copying biological sleep cycles.

## Failure modes

Replay can amplify biased or erroneous experience; consolidation can fossilize mistakes; excessive replay can overfit remembered trajectories; delayed consolidation can miss rapidly changing environments.