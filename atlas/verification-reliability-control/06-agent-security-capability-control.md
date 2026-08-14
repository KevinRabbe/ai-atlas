# Agent Security and Capability Control

## Required function

Prevent untrusted information, model errors or adversarial behavior from turning available capabilities into unauthorized or irreversible effects.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-AS-01 | Tool-using agents are vulnerable to prompt injection delivered through untrusted tool/environment data; current defenses remain incomplete. | O | E4 | V-S020 |
| V-AS-02 | Agent security failures occur across prompt handling, tool use, memory and planning layers, including memory poisoning/backdoor attacks. | O | E3 | V-S021 |
| V-AS-03 | Sandboxed/emulated tool environments can expose high-stakes failure modes before real-world deployment. | O | E3 | V-S022 |
| V-AS-04 | Protocols combining an untrusted powerful model with trusted monitoring/editing can improve safety against intentional subversion in studied coding tasks. | O | E3 | V-S023 |

## Instructions and data need different authority

A web page, email, document, retrieved memory or tool output is usually **data**, even when it contains imperative language. Treating all text inside the model context as equivalent instructions creates a fundamental confused-deputy problem.

A robust runtime should preserve authority/provenance such as:

`system policy > explicit authorized task > trusted tool schema > untrusted external content`.

This ordering should be enforced outside free-form model reasoning where possible.

## Least privilege

Capabilities should be scoped by:

- which tools/resources can be accessed;
- read vs write vs execute;
- object/range affected;
- monetary/resource limits;
- network/filesystem scope;
- duration/session;
- whether action is reversible;
- whether additional approval is required.

The model should not receive broad ambient authority merely because a task might eventually need it.

## Staged execution

High-consequence operations can use:

`propose -> static/precondition checks -> preview/sandbox -> independent verification -> authorization -> execute -> effect verification -> audit/rollback`.

Low-risk reversible operations may collapse several steps. The gate should scale with consequence rather than forcing identical friction everywhere.

## Untrusted powerful components

AI-control work demonstrates an important clean-sheet idea: a component can be useful even when it is not fully trusted, provided its outputs pass through a protocol with trusted checks, restricted capabilities and limited escalation paths.

This separates **capability** from **authority**.

## Memory as security boundary

Persistent memory can carry attacks across sessions. Memory writes derived from untrusted content need provenance, validation and restricted authority; a retrieved memory should not automatically become a trusted instruction because it persisted.

## Clean-sheet restatement

Safety-critical capability control should be enforced by the runtime/environment, not solely by asking the cognitive model to remember policy. The system should grant the minimum authority justified by current evidence and task scope.

## Failure modes

Prompt injection; confused-deputy behavior; overprivileged tools; memory poisoning; approval spoofing; unsafe retries; side effects before validation; privilege persistence after task completion; sandbox escape; monitor/model collusion; untrusted content promoted to policy; audit log mutation.
