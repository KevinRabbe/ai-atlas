# Learning & Adaptation — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

## P-L01 — Learning signal, update algorithm and storage substrate are distinct choices

Labels, self-supervised targets, demonstrations, preferences and rewards provide information about desired change. Gradient descent, RL, direct preference objectives or local rules determine how that signal is converted into change. Context, memory, adapters, weights or policies determine where it persists.

**Confidence:** very high.

## P-L02 — Adaptation exists on a continuum of persistence

Useful adaptation can occur in transient context, recurrent/test-time state, external memory, parameter deltas or durable shared weights. The train/inference boundary does not define a fundamental learning boundary.

**Confidence:** high.

## P-L03 — Durable shared updates should face a higher evidence threshold than reversible local updates

Shared weights provide cheap integrated reuse but create interference, provenance and rollback costs. Fast/external state is easier to revise. This creates a rational asymmetry in how much evidence should be required before consolidation.

**Confidence:** medium-high as a systems inference; threshold policy open.

## P-L04 — Continual learning is fundamentally an interference-allocation problem

Forgetting depends on how new updates interact with shared representations, not only whether old examples remain available. Replay, parameter protection and modular isolation address different aspects of the problem.

**Confidence:** high.

## P-L05 — Replay is conditional, not universally beneficial

Replay often helps but can increase forgetting under particular task/sample/feature geometries. Replay selection therefore belongs to the learning policy rather than being an unconditional stability mechanism.

**Confidence:** high that non-monotonic/harmful regimes exist; prevalence at frontier scale remains open.

## P-L06 — The learner can learn how to learn

Meta-learning can shape initialization, update algorithms or forward-pass adaptation so that new tasks are learned faster. The object of learning therefore includes the future adaptation process itself.

**Confidence:** high.

## P-L07 — Data generation and ordering are part of the algorithm

Curriculum, augmentation, imitation-state collection, self-play and self-training all change the effective learning problem. Dataset construction carries inductive bias and can be optimized.

**Confidence:** very high.

## P-L08 — Expensive computation can be amortized into reusable competence

Distillation demonstrates that behavior produced by ensembles/teachers can be compiled into cheaper models. More generally, repeated search, tool or evaluator-supported computation may be worth consolidating into skills or parameters when future reuse is high.

**Confidence:** high for distillation; medium for autonomous cross-substrate compilation.

## P-L09 — Feedback reliability should constrain optimization pressure

Verifiable outcomes support stronger optimization than ambiguous, learned or subjective evaluators because exploitability and misspecification risk differ.

**Confidence:** high as a qualitative principle; quantitative policy open.

## P-L10 — One permanent learning rate/timescale is unnecessarily restrictive

Evidence from test-time adaptation, parameter-efficient adaptation, continual learning and biology supports multiple useful mutation lifetimes. The correct number and control policy remain open.

**Confidence:** high for heterogeneity; medium for an explicit migration hierarchy.

## P-L11 — Consolidation is a value-of-computation decision

Moving information into a durable, fast-to-use substrate is worthwhile when expected repeated future savings/generalization exceed training, validation, interference and loss-of-provenance costs.

**Confidence:** medium; this is a synthesis hypothesis.

## P-L12 — Forgetting can be functional

Preserving every old behavior is not always desirable under changing environments. A learning system needs to distinguish destructive interference from deliberate retirement of obsolete beliefs/policies.

**Confidence:** high conceptually; operational criteria open.

---

## Emerging learning architecture hypothesis

A clean-sheet learner may look less like one global optimizer and more like a **change-management system**:

`evidence -> estimate confidence/scope/volatility -> choose substrate/timescale -> update -> validate -> consolidate, retain, revise or forget`

This unifies several independent findings without selecting a specific neural implementation.

## Strong anti-conclusions

This pass does **not** justify:

- “all knowledge should stay outside weights”;
- “test-time training should always be enabled”;
- “replay solves forgetting”;
- “RL is superior to supervised learning”;
- “self-supervision is enough for all capabilities”;
- “LoRA proves low-rank adaptation is universally sufficient”;
- “biology proves staged consolidation is optimal for AI.”

## Most valuable experiment family

Create a matched continual environment and allow the same learner to place new information in different substrates: transient state, explicit memory, isolated adapter/skill or shared weights. Hold total compute/storage constant and measure adaptation speed, transfer, forgetting, rollback, provenance, inference cost and long-horizon performance. Then learn the routing/migration policy and compare it against fixed human-designed rules.