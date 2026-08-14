# Induction and Generalization

## Required function

Use finite observations to perform well on unobserved cases drawn from some future environment or task distribution.

The central question is not whether a learner can fit observed data. It is why the particular regularities it extracts should remain useful outside those observations.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| F-IG-01 | Learnability depends jointly on a hypothesis/representation family, an information-gathering protocol, a target distribution and computational resources. | I | E5 | F-S007, F-S008 |
| F-IG-02 | There is no assumption-free ranking in which one learning/optimization algorithm dominates across all possible problem distributions covered by no-free-lunch constructions. | O | E5 | F-S008, F-S009 |
| F-IG-03 | Useful representation structure cannot in general be identified from observations alone without inductive assumptions; unsupervised disentanglement gives a concrete impossibility result. | O | E4 | F-S010 |
| F-IG-04 | A model family may be able to represent a target function while saying little about whether finite-data training will find it efficiently or generalize. | I | E5 | F-S011, F-S007 |
| F-IG-05 | Interpolating and heavily overparameterized solutions can generalize in important regimes; training error and raw parameter count are therefore insufficient predictors of generalization. | O | E4 | F-S012, F-S013, F-S014 |
| F-IG-06 | Which interpolating solution is selected matters; data geometry and algorithmic/implicit regularization can make overfitting benign or harmful. | I | E4 | F-S014, F-S023, F-S024 |

## What seems established

### 1. Inductive bias is unavoidable

A finite dataset is compatible with many possible continuations. Generalization requires preferring some continuations over others. That preference can be located in architecture, objective, optimizer, initialization, data collection, augmentation, prior knowledge, external memory, search policy, environmental interaction, or combinations of them. Calling a system “general” does not remove those preferences; it changes their scope or how they are acquired.

The no-free-lunch results are often overstated. They do **not** say that all algorithms perform equally on the structured distributions encountered in reality. They say that superiority requires exploiting non-uniform structure or assumptions. Real intelligence should therefore be studied as **bias matched to environment structure**, potentially with the bias itself learned or adapted.

### 2. Capacity is not competence

Universal approximation results establish representational possibility under mathematical conditions. They do not establish sample efficiency, optimization tractability, robustness, transfer, calibration, or resource efficiency. “Can represent” and “can learn/use under finite resources” must remain separate Atlas properties.

### 3. Fit is not the generalization mechanism

Modern interpolation results rule out the simple story that a model must stay below an effective capacity threshold to generalize. In some regimes, moving past the interpolation threshold improves test performance again. This does not mean that overparameterization is always beneficial; it means that **solution selection and problem geometry matter at least as much as nominal capacity**.

## What is not established

- A single scalar notion of model complexity that predicts generalization across modern learning systems.
- That scale alone produces the right inductive bias.
- That human-like priors are necessary for general intelligence.
- That an architecture should contain fixed inductive biases rather than learning them at another level.
- That benchmark average performance identifies a universally superior learner.

## Clean-sheet restatement

A practical intelligent system needs a mechanism for **selecting regularities that are likely to remain useful under its expected future distribution**. Any architecture proposal must state where that selection bias comes from, how it changes, and what happens when the environment violates it.

## Discriminating experiments

1. Hold total compute/data fixed and relocate the same prior between architecture, training data, optimizer, retrieval and inference-time search. Measure transfer and adaptation speed.
2. Construct task families with controlled changes in latent structure to measure how quickly a system can replace a previously useful bias.
3. Compare equal-training-error solutions selected by different algorithms while measuring robustness, calibration, transfer and description complexity rather than test loss alone.

## Failure modes

Distribution-blind algorithm rankings; equating expressivity with learnability; interpreting interpolation as automatic overfit; hidden benchmark priors; rigid inductive bias under regime shift.
