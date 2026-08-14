# Resource Scaling and Allocation

## Required function

Allocate finite data, parameters/capacity, training compute, inference compute, memory, bandwidth, energy and interaction to maximize useful lifetime performance.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-RS-01 | Language-model loss exhibited empirical power-law-like scaling with model size, data and compute over the ranges measured in early scaling studies. | O | E3 | F-S036 |
| F-RS-02 | Re-estimating the compute-optimal model/data allocation changed the recommended balance substantially; training a smaller model on far more data outperformed a much larger undertrained model at similar training compute. | O | E4 | F-S037 |
| F-RS-03 | Under data constraints, repeated use of the same data can continue to help but eventually yields diminishing value; optimal allocation changes when fresh data is unavailable. | O | E3 | F-S038 |
| F-RS-04 | These results demonstrate regime-dependent resource surfaces rather than a universal law saying that one scalar such as parameter count determines capability. | I | E4 | F-S036, F-S037, F-S038 |

## Scaling laws are measurements, not constitutions

Empirical power laws are valuable because they let us forecast within studied regimes and expose bottlenecks. Their fitted exponents and compute-optimal prescriptions depend on data distribution, architecture, objective, optimization, tokenizer/representation, evaluation metric and hardware/system efficiency.

The change from early model-heavy scaling prescriptions to Chinchilla-style co-scaling is itself an important methodological lesson: **the optimum moves when the resource accounting or experimental regime changes**.

## Resource dimensions to track separately

- training FLOPs / operations;
- inference/test-time compute;
- parameter/capacity memory;
- activation/working memory;
- persistent external memory;
- memory bandwidth and communication;
- fresh data versus repeated/synthetic data;
- environmental interactions;
- wall-clock latency;
- energy and hardware utilization;
- human/evaluator feedback.

Two systems with equal FLOPs can have radically different cost because one is bandwidth-bound, sequential, poorly parallelized or interaction-limited.

## Lifetime compute matters

Training cost is amortized across use. A more expensive training process can be rational if it makes frequent inference much cheaper; conversely, a rarely used specialist may be better solved with inference-time search than by pretraining a large dedicated model. The relevant quantity for a persistent AI is likely a **lifetime resource budget**, not training loss alone.

## Clean-sheet restatement

Architecture should ultimately be treated as a resource allocator: **which regularities are worth compiling into persistent structure, which knowledge is worth storing externally, and which computation should be performed on demand?** This is a research question, not yet a design decision.

## Open questions

- What are scaling surfaces for systems containing retrieval, tools, search, memory and subagents rather than one model?
- How should data movement be priced relative to arithmetic on future hardware?
- When does inference-time compute substitute for training compute, and when are they complements?
- What is the marginal value of fresh interaction compared with additional static data?
- How should reliability/verification compute scale with action consequence?

## Discriminating experiments

Evaluate architectures on equal **lifetime cost**: training + inference + memory + communication + interaction + verifier cost over an explicit workload distribution. Vary reuse frequency and environment volatility to identify where the optimal allocation changes.

## Failure modes

Parameter-count worship; FLOP-only accounting; extrapolating empirical exponents outside their regime; ignoring data quality/repetition; optimizing benchmark accuracy while hiding inference or memory traffic; comparing systems with unequal lifetime workloads.
