# Representation & Communication

## Required function

Encode information so that learning, reasoning, memory, modular communication and action preserve the distinctions that matter while minimizing compute and bandwidth.

## Mechanism families to map

Discrete tokens; continuous embeddings; latent recurrent state; learned communication protocols; graphs; programs/IRs; symbolic expressions; structured tensors; multimodal shared spaces; compressed summaries; semantic pointers; hybrid discrete-continuous representations.

## Early evidence anchors

Current language models demonstrate the enormous utility of discrete token interfaces, but this does not establish natural language as an optimal internal reasoning medium. Differentiable multi-agent communication shows that task-specific protocols can be learned end-to-end. Coconut explores feeding hidden reasoning states back into the model without decoding them into language and reports advantages on some planning/backtracking tasks.

## Clean-sheet questions

- Which system boundaries genuinely require human-readable language?
- What representation minimizes repeated encode/decode loss among machine components?
- Should reasoning state support superposition of alternative futures instead of early discrete commitment?
- How can latent communication remain debuggable and controllable?
- Which information should be explicit structure versus distributed representation?
- Can the system compile high-level learned procedures into cheaper executable representations?
