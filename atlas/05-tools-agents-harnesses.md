# Tools, Agents & Harnesses

## Required function

Allow learned components to acquire information, perform exact/external computation, change environments, coordinate work and persist trajectories safely.

## Mechanism families to map

Tool selection/calling; action-observation loops; agent-computer interfaces; permissions/sandboxing; planners; schedulers; context policy; event streams; subagents; multi-agent coordination; executable procedures; plugin systems; model routing; recursive harnesses; harness optimization.

## Early evidence anchors

Toolformer shows learned decisions about when/how to invoke external APIs. ReAct couples reasoning with actions. SWE-agent shows that the interface presented to an agent can materially change performance. Meta-Harness treats harness code itself as an optimization target. Self-Harness uses execution traces and regression testing to let an agent improve its own scaffold. Recursive Agent Harnesses make complete harness instances composable recursively.

## Central implication to test

System capability is a function of more than model weights. The mapping `model + interface + context policy + tools + execution loop + evaluators` must therefore be studied as a coupled system rather than treating the harness as incidental plumbing.

## Clean-sheet questions

- What belongs inside the learned model versus runtime?
- Should tool calls be mediated by natural language, schemas, executable IR or learned latent interfaces?
- When does delegation outperform local reasoning after coordination cost?
- What state should child computations inherit?
- What invariants must remain outside self-modifiable components?
