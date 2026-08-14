# Deliberation and Intermediate Representation

## Required function

Carry intermediate state that allows a solution process to decompose, revise and combine partial results instead of committing immediately to a final output.

## Evidence

- **I-S001 — Chain-of-Thought:** explicit intermediate textual steps substantially improved performance on multiple reasoning tasks for sufficiently capable language models.
- **I-S002 — Self-Consistency:** sampling multiple reasoning paths and aggregating answers improved accuracy beyond greedy chain-of-thought on several arithmetic/common-sense benchmarks.
- **I-S003 — Tree of Thoughts:** exposing intermediate “thoughts” as search nodes enabled branching, evaluation and backtracking on tasks where a single left-to-right trajectory performed poorly.
- Foundations/representation work already warns that textual representation is not proven optimal; these results establish the value of *intermediate computational state*, not English as a necessary thought substrate.

## Key distinction

`deliberation exists` does not imply `deliberation must be emitted as natural language`.

Text has practical advantages: inspectability, easy reuse by language models, tool compatibility and simple branching. It also has costs: token overhead, serialization, ambiguity, possible unfaithfulness to internal computation and pressure to express machine state in human concepts.

## Clean-sheet restatement

A difficult problem may require **revisable intermediate state** whose granularity is larger than one primitive prediction/action. The representation should be selected for downstream computation and verification rather than human readability alone.

Candidate representational families to compare later:

- latent continuous state;
- structured graphs/task states;
- executable programs;
- symbolic constraints;
- compact learned codes;
- natural language;
- hybrids with explicit summaries/provenance.

## Failure modes

Verbose but non-progressive reasoning; early incorrect premises propagated through the trace; plausible narrative replacing actual verification; representation bottleneck; context inflation; committing to a single path when search is needed.