# Runtime, Harness and Skill Improvement

## Required function

Improve information flow, tool use, context policy, procedures and runtime control without requiring a change to the base model's shared weights.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-RH-01 | Meta-Harness can automatically search harness code and improve held-out models while reducing context usage in reported settings. | O | E3 | SI-S001 |
| SI-RH-02 | Self-Harness mines execution failures, proposes minimal model-specific harness edits and accepts them through regression testing, improving held-out terminal tasks across several model families. | O | E3 | SI-S002 |
| SI-RH-03 | Recursive Harness Self-Improvement reports substantial task gains and lower inference cost after a few harness revisions, primarily through better context/inter-agent information flow. | O | E2 | SI-S003 |
| SI-RH-04 | Reflexion/learning evidence shows retained feedback/procedures can alter future behavior without updating weights. | O | E3 | prior inference/learning evidence |

## Runtime improvement surface

Examples include:

- context selection/compaction;
- retrieval query policy;
- task decomposition;
- tool schemas and wrappers;
- retry/error recovery;
- scheduling/parallelism;
- verification placement;
- skill/program libraries;
- memory write/retrieval policy;
- permissions/transaction flow;
- subagent interfaces.

These are not merely “prompts.” They determine what information and capabilities the model sees and how its outputs become state transitions.

## Why runtime changes are attractive

They are often:

- fast to test;
- versionable/rollbackable;
- model-specific without retraining;
- interpretable at the procedure level;
- cheaper than parameter updates;
- transferable across some models/tasks.

But accumulating patches can create a brittle meta-program that hides base-model deficiencies and consumes increasing context/latency.

## Skill compilation

When an expensive successful trajectory repeats, a self-improver can test whether to convert it into:

- executable function/program;
- structured workflow;
- tool;
- retrieval template;
- policy rule;
- specialized subagent;
- later weight update.

The compiled skill should retain applicability conditions and regression provenance.

## Harness-data feedback

The harness changes which traces the system produces. Therefore optimizing a harness changes future training data even if weights remain fixed today. This makes harness improvement part of long-term learning, not purely inference optimization.

## Clean-sheet restatement

The runtime is a mutable **computation policy** around learned primitives. It should be optimized as an independent substrate while tracking patch complexity, lifetime cost and its effect on future data.

## Failure modes

Prompt/harness bloat; context policies overfit benchmarks; tool wrappers hide errors; retry loops; skill library explosion; base-model weakness masked rather than fixed; control/permission logic accidentally weakened; traces optimized for current benchmark but harmful for future learning; model-specific harness transferred blindly.
