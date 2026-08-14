# Tools, Environment Interaction and Execution

## Required function

Move computation or information acquisition outside the learned model when an external mechanism can provide a more accurate, current, verifiable or efficient result.

## Evidence

- **I-S004 — ReAct:** interleaving reasoning and environment actions improved several knowledge/decision tasks and allowed external observations to correct purely internal trajectories.
- **I-S005 — Toolformer:** a language model learned when/how to invoke several APIs and incorporated results into subsequent prediction, showing tool-selection policy can itself be learned.
- **I-S006 — Reflexion:** agents improved across attempts by storing feedback/reflections in episodic text state without weight updates, demonstrating runtime feedback can alter future action policy.
- **I-S007 — SWE-agent:** changing the agent-computer interface substantially improved software-engineering performance, establishing that tool/interface design changes effective capability while model weights can remain fixed.

## Tool-use decomposition

A robust tool operation contains separate decisions:

1. recognize a capability/knowledge gap;
2. choose tool/provider;
3. construct arguments/query;
4. execute with permissions/budget;
5. validate/interpret result;
6. update task state;
7. retry/fallback only when expected value is positive.

## Tools are computational specialization

A calculator, search engine, compiler, theorem prover, simulator or database is not “extra intelligence” in the same sense as a bigger model. It is a specialist computational substrate. The reasoning system's job is partly **routing problems to the cheapest reliable substrate**.

## Interfaces matter

If the tool exposes huge noisy output or difficult action primitives, the model must spend capacity interpreting the interface rather than solving the underlying problem. Interface/harness design is therefore part of end-to-end capability and cost.

## Clean-sheet question

What is the minimal machine-native interface that exposes sufficient state/action affordances without translating every operation through verbose human text?

## Failure modes

Wrong tool selection; malformed arguments; stale/untrusted results; prompt/tool injection; permission errors; irreversible side effects; excessive retry loops; tool output flooding context; trusting execution without validation.