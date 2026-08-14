# Long-Horizon Stateful Agents

## Required function

Use accumulated experience and changing world state to improve actions across sessions, tasks and long temporal gaps.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-LH-01 | Long-term conversational/agent memory can preserve information across context-window boundaries, but retrieval alone is not a sufficient evaluation target. | O/I | E4 | P-S008, P-S010, P-S011, P-S012 |
| P-LH-02 | MemoryArena reports that systems strong on conventional long-context/memory benchmarks can perform poorly on interdependent multi-session tasks requiring remembered information to affect actions. | O | E2 | P-S010 |
| P-LH-03 | Mem2ActBench finds current memory frameworks remain inadequate when memory must proactively ground tool selection/arguments. | O | E2 | P-S011 |
| P-LH-04 | LongMemEval-V2 separates static recall, dynamic state tracking, workflow knowledge, environment gotchas and premise awareness over very large histories. | O | E2 | P-S013 |
| P-LH-05 | WorldLines identifies partial observability, overwritten world state and translation of memory into embodied plans as persistent long-horizon failures. | O | E2 | P-S014 |
| P-LH-06 | EvoMemBench finds long-context baselines remain competitive and no single memory method dominates across knowledge/execution settings. | O | E2 | P-S012 |

## The memory-to-action gap

A system can answer:

> “What did the user say three weeks ago?”

and still fail:

> “Use that preference correctly while completing today's task.”

Persistent intelligence therefore requires a chain:

`past evidence -> current belief -> task relevance -> action constraint/affordance -> execution -> new evidence`.

Any memory evaluation that stops at retrieval misses failures in the second half of the loop.

## Premise awareness

Old procedures can become invalid because:

- UI/API changed;
- permissions changed;
- object state changed;
- user preference was superseded;
- previous workaround is no longer needed;
- old failure was caused by a temporary outage.

A memory should therefore carry applicability conditions. “Experienced” behavior includes recognizing when **not** to reuse experience.

## Operational memory

For long-lived agents, high-value memory often includes:

- environment affordances;
- workflows;
- exception conditions;
- tool-specific quirks;
- previous failures and fixes;
- user/task constraints;
- state transitions caused by actions;
- uncertainty and unresolved hypotheses.

This is closer to a runbook + state model + episode archive than a list of facts.

## Evaluation should be longitudinal

Required metrics include:

- task success over many sessions;
- false carry-over from obsolete state;
- correct use of old constraints without explicit reminders;
- recovery after environment change;
- memory growth/cost;
- ability to explain which memory affected an action;
- contamination from erroneous earlier experiences;
- correction speed after a false memory is discovered.

## Failure modes

Passive recall without action use; preference/state over-application; procedural rigidity; memory-induced tool errors; old state overriding live observation; silent cross-session contamination; inability to determine whether a memory is still applicable; local success that corrupts long-term state.
