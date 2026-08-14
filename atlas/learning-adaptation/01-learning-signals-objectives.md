# Learning Signals and Objectives

## Required function

Extract useful information about desired predictions, representations or behavior from available observations, demonstrations, comparisons, outcomes and interaction.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| L-LS-01 | Large unlabeled datasets can support transferable representation learning through constructed prediction objectives. | O | E5 | L-S001, L-S002 |
| L-LS-02 | The choice of self-supervised target/augmentation determines which invariances and distinctions are encouraged. | O | E4 | L-S002 |
| L-LS-03 | Human demonstrations and ranked preferences can materially alter downstream behavior without increasing model size. | O | E4 | L-S004, L-S005 |
| L-LS-04 | Outcome/verifier-based reinforcement can induce behaviors not explicitly demonstrated, but the learned behavior follows the information and loopholes present in the feedback channel. | I | E4 | L-S006, L-S017 |
| L-LS-05 | Sequential imitation cannot generally be reduced to ordinary i.i.d. supervised learning because the learned policy changes the state distribution it visits. | O | E5 | L-S018 |

## Signal taxonomy

### Observation-derived

Self-supervised objectives manufacture targets from structure already present in data: masked content, future/neighbor relations, transformations, cross-view agreement, etc. Their advantage is scale; their limitation is that the objective itself embeds assumptions about what information should be preserved.

### Demonstration-derived

An expert supplies examples of desired behavior. This can transfer complex policies quickly, but imitation inherits expert coverage and can fail when learner errors shift the state distribution beyond demonstrated regions.

### Preference-derived

Comparisons can be easier to provide than exact target outputs. DPO demonstrates that preference optimization does not inherently require a separate learned reward model plus online RL pipeline; the same preference information can be converted through different optimization formulations.

### Consequence-derived

Rewards or verifiable outcomes provide information about result quality rather than exact actions. This allows discovery beyond demonstrations but creates a credit-assignment and objective-specification problem.

## Clean-sheet restatement

A learning system needs mechanisms for estimating **which distinctions in experience predict future utility**. No single supervision type is universally sufficient. Signal selection should depend on availability, reliability, cost, causal relevance and susceptibility to gaming.

## Important anti-conclusion

“Self-supervised,” “RL,” “preference learning,” and “supervised learning” describe information/optimization regimes, not the location where learned information must ultimately live.

## Failure modes

Proxy optimization; shortcut learning; augmentation-induced loss of task-relevant information; reward hacking; imitation covariate shift; preference inconsistency; verifier overfitting; sparse/ambiguous feedback.