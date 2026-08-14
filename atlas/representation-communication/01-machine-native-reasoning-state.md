# Machine-Native Reasoning State

## Required function

Represent intermediate computational state in a form that supports decomposition, revision, branching, composition and transfer without unnecessary serialization loss or ambiguity.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| R-MR-01 | Explicit language reasoning can improve difficult tasks but is not established as the only useful intermediate representation. | I | E4 | prior Inference evidence |
| R-MR-02 | Coconut feeds hidden-state reasoning representations back into the model without decoding each intermediate step into text and improves some planning/backtracking tasks with fewer thinking tokens. | O | E2 | R-S001 |
| R-MR-03 | Continuous latent reasoning can represent multiple candidate next steps before discrete commitment in studied tasks, suggesting discretization timing affects search behavior. | O/I | E2 | R-S001 |
| R-MR-04 | Direct latent communication between LLM agents has shown feasibility and efficiency/quality gains in recent controlled studies, but cross-model generality remains immature. | O | E2 | R-S007, R-S008 |

## Text is one useful external representation

Natural language provides:

- human interpretability;
- pretrained semantic structure;
- easy logging and interchange;
- discrete editable units;
- compatibility across otherwise unrelated systems.

Its costs include:

- ambiguity;
- redundancy;
- forced sequential serialization;
- vocabulary/token boundaries;
- possible loss when rich internal state is decoded then re-encoded.

## Continuous state is not automatically superior

Latent representations can preserve more internal information and avoid decoding cost, but introduce:

- difficult cross-model alignment;
- weaker direct auditability;
- instability under distribution/weight changes;
- unclear semantics/provenance;
- security/steering challenges.

## Structured/executable state remains open

Another possibility is machine-native intermediate representation with explicit structure:

- graphs/dependency structures;
- constraints;
- typed variables/state machines;
- executable programs/procedures;
- proof obligations;
- mixed continuous + discrete representations.

These can preserve compositional structure and enable deterministic verification, but may constrain problems that do not fit the chosen schema.

## Clean-sheet restatement

The system needs a reasoning state that optimizes:

`future computational utility + revisability + communication compatibility + verification value - serialization/bandwidth cost`.

No evidence currently establishes one representational family as universal.

## Failure modes

Human-language bottleneck; opaque latent state trusted without validation; latent-space mismatch after model update; premature discrete commitment; structured IR too rigid; reasoning state loses uncertainty; direct hidden-state communication leaks irrelevant/private state; representations optimized for benchmark rather than transfer.
