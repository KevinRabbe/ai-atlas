# Discovery & Epistemic Growth — Source Registry

Primary/original sources for the focused evidence pass on AI systems that can exceed the demonstrated knowledge/capability of their teachers, generate candidates beyond one-shot model output, and produce new externally verifiable knowledge.

## Weak supervision without a hard teacher ceiling

- **DEG-S001** — OpenAI (2023), *Weak-to-Strong Generalization*. https://openai.com/index/weak-to-strong-generalization/
  - Weak model supervision can elicit behavior above the weak supervisor's own task performance in studied settings.
  - Important limitation: weak supervision does not automatically recover the strong model's full latent capability.

## Generator + evaluator discovery loops

- **DEG-S002** — Romera-Paredes, B. et al. (2023), *Mathematical discoveries from program search with large language models (FunSearch)*. Nature 625, 468–475. https://doi.org/10.1038/s41586-023-06924-6
  - A frozen pretrained LLM generates candidate programs; executable evaluators score them; evolutionary selection retains and recombines useful candidates.
  - The system produced new constructions for established open mathematical problems and new algorithmic heuristics.

- **DEG-S003** — Google DeepMind (2025), *AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms*. https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
  - Generator/evaluator/evolution loops were applied to algorithms and more than 50 open mathematical problems.
  - DeepMind reports rediscovering state-of-the-art solutions in roughly 75% of those problems and improving the previously best-known result in about 20%.

## Frontier mathematical reasoning and independent checking

- **DEG-S004** — OpenAI (2026), *Our First Proof submissions*. https://openai.com/index/first-proof-submissions/
  - An internal model attempted all 10 research-level First Proof problems.
  - Expert feedback judged at least five attempts as having a high chance of being correct at publication time; another initially promising attempt was later judged incorrect.
  - Useful evidence that frontier proposals require external review rather than self-certification.

- **DEG-S005** — OpenAI (2026), *An OpenAI model has disproved a central conjecture in discrete geometry*. https://openai.com/index/model-disproves-discrete-geometry-conjecture/
  - A general-purpose reasoning model produced an infinite family of constructions disproving a longstanding conjecture on the planar unit-distance problem.
  - The proof was checked by external mathematicians and used an unexpected connection to algebraic number theory.

## Evidence interpretation

These sources support three distinct claims that must not be collapsed:

1. **Teacher capability need not be a hard ceiling.** A learner can generalize beyond weak supervision when it has additional latent capacity/inductive structure.
2. **Generator capability need not be the system discovery ceiling.** Search plus reliable external evaluation can accumulate candidates beyond one-shot generator performance.
3. **Novelty is not knowledge.** A proposal becomes a knowledge candidate only after evidence appropriate to the domain supports it; promotion to durable knowledge should require verification/replication proportional to consequence and evaluator reliability.

## Discovery regimes

The current evidence distinguishes at least two regimes:

- **deductive/constructive discovery** — the result is implicit in axioms/rules/current observations but has not previously been derived; formal proof, exhaustive computation or executable evaluation may provide strong checking;
- **empirical discovery** — the relevant information is not present in the current corpus and must be acquired from new measurement, intervention or observation of the world.

The second regime is less directly demonstrated by the sources above and remains a high-value gap for the Atlas.

## First-pass gaps

- autonomous experimental design tied to real instruments or trustworthy simulators;
- distinguishing genuine novelty from obscure-result rediscovery at scale;
- evaluator independence under sustained discovery optimization pressure;
- discovery when no cheap objective verifier exists;
- negative-result retention and publication to prevent repeated dead-end search;
- value-of-experiment policies across compute, simulation and physical interaction;
- representation invention where the useful latent variables are absent from human conceptual vocabularies;
- teacher/student systems where the student discovers genuinely new externally verified knowledge rather than merely outperforming a weak supervisor on known labels;
- safe automation of empirical research under consequential actions/materials/experiments.
