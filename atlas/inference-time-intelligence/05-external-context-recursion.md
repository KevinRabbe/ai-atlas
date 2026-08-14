# External Context and Recursion

## Required function

Solve problems whose relevant information is larger than the model's active working state by selectively examining, decomposing and recombining external information rather than ingesting all of it repeatedly.

## Evidence

- **I-S011 — Recursive Language Models:** treating long prompts as an external environment and allowing programmatic examination plus recursive model calls handled contexts far beyond the base model window and improved several long-context tasks at comparable or lower query cost in the reported evaluations.
- **I-S012 — Recursive Agent Harnesses:** replacing a bare recursive model call with a full tool-capable agent harness improved a held-fixed coding-agent backbone on long-context evaluation, showing the recursive unit's capabilities matter.

## Fundamental abstraction

`large context != prompt`.

A corpus/repository/history can be an addressable environment. The active reasoner needs only a working set plus operations such as:

- search/filter;
- map/reduce;
- chunk/select;
- execute queries/programs;
- spawn focused child computation;
- merge structured results;
- retain provenance back to source state.

## Why recursion can help

Recursion is useful when a subproblem can be isolated with a smaller relevant state and solved more cheaply/accurately than carrying the full parent context through every step.

But recursion adds:

- child setup/context cost;
- information loss at boundaries;
- aggregation cost;
- duplicated work;
- error propagation;
- termination complexity.

Therefore recursion is a conditional decomposition tool, not a universal next level.

## Clean-sheet restatement

The system needs a **working-set manager** that can externalize large state and create bounded subcomputations over selected views. Recursion is one scheduling form for this property.

## Failure modes

Bad decomposition; lossy child summaries; unbounded spawn trees; repeated context scanning; parent unable to integrate heterogeneous child outputs; hidden provenance loss; children solving incompatible interpretations of the task.