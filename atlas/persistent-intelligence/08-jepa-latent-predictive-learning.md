# Joint-Embedding Predictive Learning (JEPA Family)

**Status:** candidate mechanism family; explicit Atlas evidence, **not** a selected architecture component.

## Required function

Learn a compact state representation that preserves distinctions useful for predicting missing/future state, understanding dynamics and potentially planning, without requiring reconstruction of every raw observable detail.

The implementation-neutral question is not "should the system use JEPA?" It is:

> **What should a predictive representation be required to preserve, and what information can it safely treat as nuisance?**

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-JEPA-01 | I-JEPA learns image representations by predicting target-block representations from context rather than reconstructing target pixels. | O | E4 | P-S030 / R-S010 |
| P-JEPA-02 | V-JEPA demonstrates stand-alone feature prediction from video without pixel reconstruction, text supervision, negative examples or a pretrained image encoder, producing transferable frozen visual representations. | O | E4 | P-S031 / R-S011 |
| P-JEPA-03 | V-JEPA 2 combines large-scale action-free predictive pretraining with a comparatively small action-conditioned robot-data stage and uses the learned latent predictor for model-predictive robot planning. | O | E3 | P-S022 |
| P-JEPA-04 | V-JEPA 2.1 adds dense predictive losses and deep self-supervision to improve spatial/temporal grounding, indicating that "abstract latent prediction" does not imply that fine spatial structure is always dispensable. | O/I | E2 | P-S032 / R-S013 |
| P-JEPA-05 | Early LLM-JEPA work reports benefits from JEPA-style objectives in language-model pretraining/fine-tuning, but evidence is currently workshop-level and does not establish a general replacement for autoregressive objectives. | O | E1 | R-S012 |

## Mechanism decomposition

The useful mechanism can be stated without inheriting a particular encoder, transformer, masking schedule or modality:

1. encode an observed/context state into a learned representation;
2. define a target representation for missing, future or otherwise withheld state;
3. predict the target **in representation space** rather than necessarily reconstructing the raw observation;
4. shape the representation so useful predictable structure is retained and nuisance/unpredictable detail need not dominate the learning objective;
5. prevent degenerate/collapsed representations by whatever mechanism the chosen implementation requires;
6. optionally condition prediction on action/intervention when the task is control rather than passive understanding.

A minimal abstraction is:

`context state + optional action/context -> predicted future/hidden representation`

rather than:

`context state -> reproduce every missing pixel/token/sensor value`.

## Why this is relevant to Atlas

### PS-012 — adaptive predictive-state breadth

JEPA supplies concrete evidence for the possibility that useful predictive state can be narrower than raw observation state.

But PS-012 adds a requirement that JEPA by itself does not settle: a distinction that is irrelevant to the current prediction objective may become important under a future objective. Therefore the Atlas should test whether latent predictive compression preserves **future optionality**, not only current benchmark accuracy.

### PS-005 / PS-010 — priced computation and resources

Predicting compact latent targets may avoid spending compute on nuisance detail. That is valuable only if the saved computation/storage exceeds the downstream cost of information discarded too early.

### PS-009 — shared reusable structure

A predictive latent may expose reusable regularities shared across tasks/modalities. The same mechanism can become harmful if forcing shared prediction creates interference between unrelated task factors.

### PS-001 — typed representation

Even if a learned predictive latent is useful for tolerant state, exact identity, provenance, control constraints and authority need not be encoded into the same latent channel. JEPA evidence therefore does **not** falsify typed exact side state.

### PS-007 / PS-008 — active evidence and discovery

A world representation that predicts consequences can help choose informative interventions. However, prediction is not evidence of truth: discovered causal claims still require interaction/verification outside the learned model when consequence warrants it.

## Competing mechanism families

JEPA must compete experimentally against at least:

1. **raw reconstruction / generative prediction** — preserve enough information to reconstruct pixels, tokens or sensor values;
2. **task-specific sufficient-state prediction** — retain only quantities directly optimized for the current decision/reward/policy objective (MuZero-like clean-sheet principle);
3. **generative latent dynamics** — predict a compact latent while retaining a generative decoder/objective;
4. **contrastive / discriminative representation learning** — organize representations through relative similarity/separation rather than target prediction;
5. **recoverable external evidence + narrow active state** — avoid requiring any learned hot representation to preserve every future-useful distinction.

No current evidence establishes one family as universally dominant.

## Important distinction: abstraction vs information destruction

The attractive JEPA intuition is:

`raw observation = predictable structure + unpredictable/nuisance detail`

and prediction should emphasize the first term.

The dangerous version is:

`not useful to today's objective -> permanently discard`.

Those are not equivalent.

V-JEPA 2.1 is particularly useful evidence here because it strengthens dense spatial/temporal prediction rather than assuming coarse semantics are always enough. The Atlas should therefore treat **target granularity** as an allocatable design dimension.

## Failure modes / falsifiers

- latent state discards a rare variable that becomes decisive after objective shift;
- representation predicts observational regularities but not intervention consequences;
- collapse or shortcut solutions satisfy the predictive objective without useful world structure;
- latent distance is treated as calibrated probability or causal confidence when it is not;
- action-free predictive training is assumed sufficient for control without action-conditioned evidence;
- opaque latent state absorbs exact authority/provenance semantics that should remain explicit;
- a generative/reconstructive objective retains transfer-critical detail at acceptable extra cost and dominates lifetime utility;
- learned representation geometry transfers poorly across model/version changes;
- benchmark-relevant predictable structure is learned while safety-critical low-frequency state is suppressed.

## Atlas conclusion today

**Retain JEPA as a serious candidate mechanism, not a commitment.**

The strongest neutral lesson is:

> A useful world/predictive state need not reconstruct the observation. Prediction can be performed over learned representations, and the target representation itself determines which structure the learner is pressured to preserve.

The unresolved question is whether that selective pressure produces the best **lifetime** state once objectives, actions, rare events and future unknown tasks change.

See `experiments/E24_JEPA_PREDICTIVE_REPRESENTATION.md` for the planned discriminator.