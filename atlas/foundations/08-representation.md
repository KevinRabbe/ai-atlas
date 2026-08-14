# Representation

## Required function

Encode aspects of the world, task and internal computation so that useful predictions, recombinations and decisions become easier under finite resources.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-RP-01 | Simple feed-forward neural families can be universal function approximators under mathematical conditions, establishing broad representational capacity without establishing efficient learning. | O | E5 | F-S011 |
| F-RP-02 | Unsupervised data alone does not uniquely identify semantically disentangled latent factors without inductive assumptions. | O | E4 | F-S010 |
| F-RP-03 | An information-bottleneck objective formalizes representation relevance relative to a target variable, but generic hidden-state compression is not a universal explanation of deep generalization. | O | E4 | F-S004, F-S005, F-S006 |
| F-RP-04 | The optimizer and data distribution can change which representation is selected from the same expressive family. | I | E4 | F-S023, F-S024 |

## Representation quality is relational

A representation is not useful merely because it is compact, disentangled, human-readable, high-dimensional, sparse, continuous or symbolic. Its value depends on what computations must be performed from it and at what cost.

A useful representation may make some transformations cheap while making others harder. Therefore Atlas comparisons should measure **downstream computational consequences**, not only intrinsic representation metrics.

## Desirable properties are task-dependent

Possible properties include:

- predictive sufficiency;
- invariance to irrelevant variation;
- sensitivity to intervention-relevant variation;
- compositional/recombinable structure;
- uncertainty preservation;
- temporal persistence;
- easy updating;
- low communication/storage cost;
- easy decoding into actions or external interfaces;
- transfer across task families.

These objectives can conflict. For example, aggressively invariant representations can discard details needed by a future task. Human interpretability may increase interface value while increasing machine-machine communication cost.

## Human semantics are not guaranteed coordinates

Disentanglement impossibility results are an important warning: semantic factorization cannot simply be expected to emerge uniquely from unlabeled observations. If we want particular factors, some form of bias, interaction, supervision or objective must privilege them.

This applies directly to the later question of machine-internal language. We should not assume the best internal representation is human text, nor assume an opaque latent code is better merely because it is compact.

## Clean-sheet restatement

The system needs representations that **make future useful computation cheap while retaining the information and uncertainty required for expected future tasks**. Representation choice is therefore part of compute allocation and inductive bias.

## Open questions

- Can representation utility be optimized over a distribution of future tasks rather than a fixed target?
- When should the system maintain multiple representations of the same state at different abstraction levels?
- Can a learned intermediate representation be both machine-efficient and externally auditable?
- How should representations encode causal/action affordances rather than only observational similarity?
- How can representations expand when previously discarded variables become relevant?

## Discriminating experiments

Train equal-compute systems with representations optimized for reconstruction, predictive sufficiency, explicit task loss, causal intervention prediction and communication cost. Evaluate transfer to held-out task families and measure the compute needed by downstream solvers.

## Failure modes

Intrinsic-metric optimization disconnected from downstream utility; premature invariance; forced human semantics; opaque latent codes that break interoperability; representational collapse; inability to revise abstractions after distribution shift.
