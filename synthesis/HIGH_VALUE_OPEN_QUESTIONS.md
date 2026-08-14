# Highest-Value Open Questions Before Clean-Sheet Architecture

This is a priority list for uncertainty removal, not a request to maximize bibliography size.

## Q1 — What representation should machine reasoning and communication use internally?

Evidence rejects the assumption that human language is necessary, but the Atlas has not yet saturated alternatives: latent continuous state, structured graphs, executable intermediate representation, symbolic constraints, learned discrete codes and hybrids.

**Why high value:** representation choice affects reasoning efficiency, multi-agent bandwidth, memory, interpretability, learning and hardware.

## Q2 — Where should allocation/control live?

The synthesis repeatedly requires allocation of compute, information, change and assurance. It is unresolved whether these policies should be:

- one learned global controller;
- distributed local controllers;
- hierarchical;
- mostly implicit in learned dynamics;
- explicit programmatic policy;
- hybrid.

**Why high value:** a centralized controller can become a bottleneck/single point of failure; distributed control can lose global coherence and incur communication cost.

## Q3 — What is the correct utility/objective representation?

The system needs to trade task quality, future reuse, uncertainty, cost, safety, user intent and long-term consequences. One scalar proxy is exploitable; a purely hand-written constraint set may be incomplete.

**Why high value:** every learning, inference, self-improvement and assurance decision depends on what counts as value.

## Q4 — Can marginal value of computation/information/change be learned accurately enough to control the system?

The meta-hypothesis depends on estimating whether another computation, observation, memory write, consolidation or self-improvement step is worth its cost.

**Why high value:** if these estimates are poor, adaptive allocation can be worse than simple fixed heuristics.

## Q5 — What is the best division between directly addressable evidence and compressed learned state?

This trade-off recurs in sequence modeling, context, memory, world state and self-improvement lineage.

**Why high value:** it determines memory growth, recall fidelity, inference bandwidth, provenance and transfer.

## Q6 — How should causal responsibility be assigned across a heterogeneous system?

When a task fails, the cause may be representation, model knowledge, memory, retrieval, world model, tool, harness, evaluator, authority or environment shift.

**Why high value:** self-improvement cannot safely choose mutation surfaces without system-level causal attribution.

## Q7 — How should uncertainty propagate across composed modules?

Local calibration does not automatically produce calibrated system-level confidence after retrieval, tool calls, simulation, delegation, summarization and verification.

**Why high value:** assurance and active information acquisition depend on end-to-end uncertainty.

## Q8 — How can a system retain information for unknown future objectives without storing everything?

Decision-sufficient compression is objective-relative, but indefinite raw retention is physically expensive and harms retrieval.

**Why high value:** this is central to generality, continual learning and future task transfer.

## Q9 — Which functions need separate state/learning timescales?

Evidence supports heterogeneous timescales, but the correct boundaries between working state, fast adaptation, memory, skills, parameters and structural change remain unknown.

**Why high value:** determines adaptation speed, forgetting, rollback and complexity.

## Q10 — How much evaluator independence is enough under optimization pressure?

Formal checks are narrow; learned evaluators are broad but exploitable. Ensemble agreement can be correlated.

**Why high value:** search, RL, agents and self-improvement all become more dangerous as optimization pressure exceeds evaluator reliability.

## Q11 — How should trusted/assurance components themselves improve?

An immutable trusted root may become obsolete; allowing it to self-modify creates circular approval.

**Why high value:** long-lived self-improving systems eventually need control-system migration without losing authority continuity.

## Q12 — What system-level capacity/scaling metric replaces parameter count?

Useful capacity may depend on parametric knowledge, active compute, persistent state, external memory/tools, bandwidth, communication, search and evaluation.

**Why high value:** without a system-level resource model, architecture comparisons will remain misleading.

## Q13 — When does modularity beat integration?

Separating memory, specialists, tools, evaluators and control improves isolation and editability but adds routing, interfaces and communication.

**Why high value:** this determines whether the eventual system should be a small number of deeply integrated mechanisms or a heterogeneous ecology.

## Q14 — How should learned world models preserve optionality for changing goals?

Compact predictive state can be efficient but goal-specific.

**Why high value:** a general system must avoid becoming excellent at predicting exactly the variables yesterday's task required while discarding tomorrow's.

## Q15 — What is the smallest experimental organism that can discriminate these choices?

The project does not need a frontier-scale model to test every architectural hypothesis.

**Why high value:** a deliberately small instrumented system could test state/memory/control/learning boundaries orders of magnitude more cheaply and make later scaling evidence-driven.

---

# Priority before Phase 9

The strongest gap requiring a dedicated additional evidence pass is **representation & machine communication**. It touches Q1, Q2, Q7 and Q13 and has not yet received the same depth as memory, learning, inference or verification.

A second focused gap is **objective/utility and metareasoning**: how expected value is represented and how operation/change/assurance budgets are actually allocated.

These two gap closures should occur before committing to a clean-sheet architecture candidate.
