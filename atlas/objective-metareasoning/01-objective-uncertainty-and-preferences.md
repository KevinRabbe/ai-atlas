# Objective Uncertainty and Preferences

## Required function

Represent what outcomes matter while acknowledging that observed rewards, instructions, preferences and demonstrations are incomplete evidence about the underlying objective rather than perfect ground truth.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| O-OU-01 | Human pairwise preferences can train useful reward models/policies on complex tasks without a hand-written environment reward. | O | E4 | O-S001, O-S002 |
| O-OU-02 | Cooperative inverse reinforcement learning models the human objective as hidden state and yields active teaching/learning behavior rather than treating a fixed reward as known. | O/I | E4 | O-S003 |
| O-OU-03 | Inverse Reward Design treats a designed proxy reward as evidence about designer intent conditioned on the training environment, enabling uncertainty/risk sensitivity under environment change. | O | E3 | O-S004 |
| O-OU-04 | Active IRD can choose queries about reward functions to reduce uncertainty about the true objective. | O | E2 | O-S005 |
| O-OU-05 | Reward misspecification becomes more dangerous as optimization/capability rises in controlled environments. | O | E3 | O-S006, Phase-5 Goodhart evidence |

## Objective evidence types

A long-lived system may receive:

- explicit instructions;
- preferences/comparisons;
- demonstrations;
- written rules/constraints;
- success metrics;
- downstream human corrections;
- organizational policy;
- inferred user state/intent;
- environmental consequences.

These sources can conflict, be noisy, change over time, or carry different authority.

## Reward is an observation about intent

A key clean-sheet distinction is:

`objective evidence != objective itself`.

The written metric may have been designed for one environment and fail elsewhere. A user choice may reflect limited information or short-term preference. Demonstrations may be suboptimal. Therefore the system should preserve uncertainty and provenance rather than silently compiling every signal into one unquestioned scalar.

## Authority and scope

Objective evidence needs metadata analogous to memory/control:

- who/what supplied it;
- authority level;
- time/scope;
- confidence/noise;
- context in which it was elicited;
- whether superseded;
- conflicts with other objectives/constraints.

## Active clarification

When objective uncertainty changes the best action enough to matter, the system can acquire information:

- ask a user for a comparison/clarification;
- present alternatives/trade-offs;
- run reversible probes;
- defer irreversible action;
- consult higher-authority policy.

This is value-of-information applied to intent.

## Clean-sheet restatement

The system needs an **uncertain objective model**, not merely a reward register. It should distinguish evidence about value from the latent value/preferences it is trying to satisfy and know when additional clarification is worth acquiring.

## Failure modes

Proxy treated as literal intent; stale preference; low-authority signal overrides policy; human demonstration assumed optimal; preference model overconfident under distribution shift; conflicting goals silently averaged; manipulative query strategy; objective inference becomes excuse to disregard explicit instruction; reward hacking during active elicitation.
