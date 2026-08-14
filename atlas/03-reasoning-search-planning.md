# Reasoning, Search & Planning

## Required function

Allocate computation to transform an initial problem state into a reliable solution/action when direct amortized prediction is insufficient.

## Status

**First evidence pass completed on 2026-08-14; not saturated.**

Detailed notes now live under [`inference-time-intelligence/`](inference-time-intelligence/INDEX.md). This pass maps deliberation, branching/search, compute allocation/stopping, tools/execution, external context/RLM recursion, delegation/multi-agent computation, harness policy and evaluator-guided evolutionary loops.

## First-pass findings

1. **Intermediate state matters, but its representation is open.** Textual chain-of-thought proves utility of revisable intermediate computation, not language as a necessary internal format.
2. **Inference compute has diminishing/conditional returns.** Problem difficulty and verification determine which scaling strategy pays off.
3. **Verification changes search economics.** Reliable evaluators turn generation into directed optimization; weak evaluators cap safe optimization pressure.
4. **Tools are specialist compute.** The controller should route arithmetic, retrieval, execution or proof to external mechanisms when cheaper/more reliable.
5. **Interfaces are capability.** Agent-computer/harness design can change performance with fixed weights.
6. **Large contexts can be environments.** Selective programmatic access and recursion can replace repeated full-context ingestion.
7. **Recursion/delegation are conditional.** Their decomposition/parallelism benefit must exceed setup, communication and aggregation cost.
8. **Harness policy is optimizable state.** Context, scheduling and tool policies can be evolved/edited independently and regression-tested.
9. **Stopping is an operation.** More tokens/agents are not intrinsically better; the target is marginal expected utility.

## Clean-sheet questions

- What representation should intermediate computation use when humans do not need to inspect it?
- How should a controller estimate the expected value of another reasoning/search/tool step?
- When should uncertainty trigger retrieval, action, branching, delegation, recursion or a question to the user/environment?
- How independent must candidate paths/workers be before consensus adds evidence?
- How should verifier reliability limit search/optimization pressure?
- When should a successful expensive trajectory be distilled into a reusable skill/weight update?
- How can inference state be replayed/recovered without forcing every event back through the model?

## Anti-assumptions

Do not assume reasoning equals text generation, planning equals a natural-language plan, recursion is inherently superior, multi-agent means diversity, or more test-time compute monotonically improves performance. Treat every inference operation as a resource allocation with measurable marginal value.