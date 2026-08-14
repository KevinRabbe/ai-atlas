# Information, Compression and Relevance

## Required function

Represent, transmit and store information while preserving what matters for future prediction, decision or reconstruction under resource constraints.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-IC-01 | Entropy and mutual information quantify properties of statistical information sources/channels and establish coding limits under explicit assumptions. | O | E5 | F-S001 |
| F-IC-02 | Compression with loss is only meaningful relative to a distortion/fidelity criterion; rate-distortion theory exposes an explicit information–fidelity frontier. | O | E5 | F-S002 |
| F-IC-03 | Short-description principles can be used for statistical model selection, linking regularity extraction with coding length. | O | E4 | F-S003 |
| F-IC-04 | The information-bottleneck objective formalizes preserving information about a relevant variable while discarding other information about the input. | O | E4 | F-S004 |
| F-IC-05 | The claim that hidden-state information compression is a universal causal explanation of deep-network generalization does not hold generally; compression behavior depends on representation/nonlinearity and can be absent in generalizing networks. | O | E4 | F-S005, F-S006 |

## What seems established

### Information has a cost only relative to a channel/storage/computation regime

Shannon-style results give rigorous limits for communication and coding, but those limits are parameterized by source/channel assumptions. An intelligent system must care not simply about “information” in the abstract but about **which information is worth the bits, bandwidth, latency or compute required to preserve and move it**.

### Lossy compression requires a relevance criterion

There is no implementation-neutral reason to minimize representation size without specifying what loss is acceptable. Rate-distortion makes this explicit: the useful optimum is a frontier between rate and distortion. For intelligence, the harder question is defining distortion in terms of future utility, prediction, controllability, uncertainty, or task families rather than visual/input reconstruction alone.

### Compression and generalization must not be conflated

Information bottleneck gives a useful formal lens, but empirical/theoretical work on deterministic deep networks shows that measured compression can depend strongly on how mutual information is estimated or on clustering induced by nonlinearities. Generalization can occur without the claimed compression phase. Therefore the Atlas must not promote “compress internal state” into a universal architecture rule.

## Important distinction

Three ideas that are often merged should remain separate:

1. **Coding compression:** fewer bits for equivalent/relevant reconstruction.
2. **Statistical simplicity:** a shorter/effective explanation or model.
3. **Task-selective invariance:** discarding variation irrelevant to a downstream purpose.

They can align, but no theorem makes them universally identical.

## Clean-sheet restatement

The system needs mechanisms that allocate finite representational and communication capacity according to **future relevance**. The design variable is not maximal compression; it is the trade between retained information, expected utility, uncertainty, and resource cost.

## Open questions

- Can a general system learn its own distortion/relevance functions as goals and environments change?
- When should information be preserved losslessly because future relevance is unknown?
- How should provenance and uncertainty alter the value assigned to stored information?
- What is the correct accounting unit when moving a representation is more expensive than computing it again?
- Can learned internal representations be measured in a way invariant to harmless invertible transformations while still predicting practical utility?

## Discriminating experiments

Intervene directly on retained task-relevant and task-irrelevant information while holding model capacity, fit and compute constant. Measure causal effects on generalization, transfer, robustness and future-task adaptation.

## Failure modes

Compression-as-goal cargo cult; mutual-information estimator artifacts; preserving reconstructive detail with no decision value; prematurely discarding currently irrelevant information that later becomes useful; ignoring bandwidth/latency costs.
