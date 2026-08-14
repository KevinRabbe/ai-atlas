# Learning & Adaptation — Source Registry

Primary/original sources for the first Phase-2 evidence pass.

## Self-supervised representation learning

- **L-S001** — Devlin, J. et al. (2018), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. https://arxiv.org/abs/1810.04805
- **L-S002** — Chen, T. et al. (2020), *A Simple Framework for Contrastive Learning of Visual Representations (SimCLR)*, ICML/PMLR. https://proceedings.mlr.press/v119/chen20j.html

## Human/preference/verifiable feedback

- **L-S004** — Ouyang, L. et al. (2022), *Training language models to follow instructions with human feedback*. https://arxiv.org/abs/2203.02155
- **L-S005** — Rafailov, R. et al. (2023), *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. https://arxiv.org/abs/2305.18290
- **L-S006** — DeepSeek-AI (2025), *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. https://arxiv.org/abs/2501.12948

## Meta-learning and test-time adaptation

- **L-S007** — Finn, C., Abbeel, P. & Levine, S. (2017), *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*, ICML/PMLR. https://proceedings.mlr.press/v70/finn17a.html
- **L-S008** — Sun, Y. et al. (2019/2020), *Test-Time Training with Self-Supervision for Generalization under Distribution Shifts*. https://arxiv.org/abs/1909.13231
- **L-S009** — Sun, Y. et al. (2024), *Learning to (Learn at Test Time): RNNs with Expressive Hidden States*. https://arxiv.org/abs/2407.04620
- **L-S010** — Behrouz, A., Zhong, P. & Mirrokni, V. (2025), *Titans: Learning to Memorize at Test Time*. https://arxiv.org/abs/2501.00663
- **L-S019** — Kirsch, L. et al. (2022), *General-Purpose In-Context Learning by Meta-Learning Transformers*. https://arxiv.org/abs/2212.04458
- **L-S020** — von Oswald, J. et al. (2022), *Transformers learn in-context by gradient descent*. https://arxiv.org/abs/2212.07677

## Parameter-efficient adaptation and continual learning

- **L-S011** — Hu, E. J. et al. (2021), *LoRA: Low-Rank Adaptation of Large Language Models*. https://arxiv.org/abs/2106.09685
- **L-S012** — Kirkpatrick, J. et al. (2017), *Overcoming catastrophic forgetting in neural networks*. https://arxiv.org/abs/1612.00796
- **L-S013** — Mahdaviyeh, Y. et al. (2025), *Replay Can Provably Increase Forgetting*. https://arxiv.org/abs/2506.04377
- **L-S014** — Ding, M., Xu, J. & Ji, K. (2026), *Provable Effects of Data Replay in Continual Learning: A Feature Learning Perspective*. https://arxiv.org/abs/2602.02767

## Distillation and consolidation

- **L-S015** — Hinton, G., Vinyals, O. & Dean, J. (2015), *Distilling the Knowledge in a Neural Network*. https://research.google/pubs/distilling-the-knowledge-in-a-neural-network/

## Curriculum, self-play, imitation and self-training

- **L-S016** — Silver, D. et al. (2017), *Mastering the game of Go without human knowledge*, Nature 550, 354–359. https://doi.org/10.1038/nature24270
- **L-S018** — Ross, S., Gordon, G. & Bagnell, D. (2011), *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*, AISTATS/PMLR. https://proceedings.mlr.press/v15/ross11a.html
- **L-S021** — Bengio, Y. et al. (2009), *Curriculum Learning*, ICML. https://icml.cc/2009/abstracts.html#119
- **L-S022** — Xie, Q. et al. (2019/2020), *Self-training with Noisy Student improves ImageNet classification*. https://arxiv.org/abs/1911.04252

## Expansion targets

- active learning/value-of-information data acquisition;
- synthetic-data collapse and model-generated-data feedback loops;
- online meta-learning under unannounced distribution changes;
- task-free continual learning at frontier scale;
- knowledge editing/unlearning and substrate demotion;
- optimizer-state learning and learned update rules;
- multi-objective/Pareto learning and constraint satisfaction;
- credit assignment across tools/programs/non-differentiable modules;
- autonomous skill formation and skill retirement;
- empirical comparisons of context vs memory vs adapters vs full weights under equal lifetime compute/storage budgets.