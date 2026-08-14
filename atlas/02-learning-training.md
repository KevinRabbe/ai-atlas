# Learning & Training

## Required function

Acquire useful behavior and representations from data, interaction and feedback, while preserving prior capability and allocating learning to the correct substrate.

## Mechanism families to map

Self-supervised learning; supervised learning; reinforcement learning; RL with verifiable rewards; preference learning; imitation; self-play; curriculum learning; active learning; meta-learning; continual learning; test-time learning; distillation; synthetic data; data selection; exploration; multi-objective optimization; offline/online learning.

## Early evidence anchors

Scaling-law work shows predictable relationships among data, parameters and compute in particular training regimes. Chinchilla demonstrated that model size and token budget must be jointly optimized. InstructGPT/RLHF showed that behavioral alignment can change dramatically without increasing model size. DPO simplified preference optimization relative to a reward-model-plus-RL pipeline. DeepSeek-R1 provides evidence that reinforcement learning with verifiable signals can induce stronger reasoning behaviors, including in a zero-SFT starting regime.

## Clean-sheet questions

- Which knowledge should be learned slowly into weights versus rapidly into memory/skills?
- What feedback signals provide genuine task information rather than proxy exploitation?
- How can exploration be preserved as competence increases?
- How should learning avoid erasing rare but important capabilities?
- When is training-time compute preferable to inference-time search?
- Can training dynamically create or retire specialized computational modules?
