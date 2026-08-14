# Learning & Training

## Required function

Acquire useful behavior and representations from data, interaction and feedback, while preserving prior capability and allocating learning to the correct substrate.

## Status

**First evidence pass completed on 2026-08-14; not saturated.**

Detailed notes now live under [`learning-adaptation/`](learning-adaptation/INDEX.md). The first pass separates learning signals from update algorithms and storage substrates, then maps continual learning, fast/test-time adaptation, distillation, curricula/self-play and information migration across timescales.

## Mechanism families to map

Self-supervised learning; supervised learning; reinforcement learning; RL with verifiable rewards; preference learning; imitation; self-play; curriculum learning; active learning; meta-learning; continual learning; test-time learning; distillation; synthetic data; data selection; exploration; multi-objective optimization; offline/online learning.

## First-pass findings

1. **Signal, update rule and storage are separable.** A preference/reward/label does not dictate whether learning belongs in context, memory, adapters or shared weights.
2. **Learning extends through deployment.** In-context/meta-learning, test-time training and learned mutable state show useful adaptation can occur without conventional offline retraining.
3. **Durability has a cost.** Shared-weight changes amortize behavior but create interference, rollback and provenance costs.
4. **Continual learning is an interference problem.** Replay helps conditionally; more replay is not universally safer.
5. **Data policy is part of the learner.** Curriculum, self-play, imitation-state collection and augmentation change the effective objective/distribution.
6. **Expensive computation can be compiled.** Distillation is one concrete form of amortizing repeated expensive inference into reusable learned competence.
7. **Multiple timescales are plausible.** Fast tentative adaptation and slower consolidation should be compared against one-timescale permanent updates.
8. **Forgetting can be intentional.** Obsolete information should sometimes be retired rather than preserved indefinitely.

## Clean-sheet questions

- Which knowledge should be learned slowly into weights versus rapidly into memory/skills?
- What feedback signals provide genuine task information rather than proxy exploitation?
- How can exploration be preserved as competence increases?
- How should learning avoid erasing rare but important capabilities?
- When is training-time compute preferable to inference-time search?
- Can training dynamically create or retire specialized computational modules?
- Can the learner estimate confidence, scope, volatility and future reuse strongly enough to choose its own storage substrate?
- When should repeated expensive reasoning/search be consolidated into a cheaper skill or parameter update?

## Anti-assumptions

Do not assume learning means gradient descent on all model weights. Do not assume deployment state must be immutable. Do not assume all durable knowledge belongs in one parameter store, nor that external memory is always superior. Treat persistence, reversibility, integration and interference as measurable properties.