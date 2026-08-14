# Multimodal Grounding and Action

## Required function

Fuse heterogeneous observations into task-relevant state and connect that state to actions without requiring every modality to be translated into human language.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| P-MM-01 | Natural-language supervision can align visual concepts with a reusable semantic space and support broad zero-shot transfer. | O | E5 | P-S024 |
| P-MM-02 | General architectures can process heterogeneous structured inputs/outputs without modality-specific core architectures for every task. | O | E4 | P-S025 |
| P-MM-03 | Interleaved multimodal conditioning enables few-shot transfer across image/video/language tasks. | O | E4 | P-S026 |
| P-MM-04 | A shared embedding can align six modalities using image-paired data, enabling cross-modal retrieval/composition without all modality pairs being directly supervised. | O | E3 | P-S027 |
| P-MM-05 | Continuous sensor state can be injected alongside language/vision for embodied planning and positive cross-domain transfer. | O | E3 | P-S028 |
| P-MM-06 | Web-scale visual/language knowledge can transfer into robotic action policies when action is included in the learned multimodal interface. | O | E3 | P-S029 |

## Shared space does not mean identical representation

Cross-modal alignment is useful for identity and concept correspondence:

`spoken word "cup" <-> image <-> depth shape <-> object track <-> manipulation target`.

But forcing every modality into one homogeneous code can discard information needed only by one subsystem, such as high-frequency audio timing, exact motor state or geometric precision.

A cleaner abstraction is:

- modality-local features when specialized detail matters;
- shared latent concepts/identity where cross-modal binding matters;
- explicit uncertainty per observation source;
- action/state channels that need not become text.

## Language as interface, not required hub

CLIP, Flamingo and PaLM-E show that language is a powerful supervisory/interaction signal. They do not prove that all machine-machine multimodal reasoning should pass through text.

For clean-sheet design, compare:

`modality -> shared latent -> action/reasoning`

against:

`modality -> textual description -> language reasoning -> action`.

The latter is interpretable but can introduce lossy serialization and latency.

## Grounding through action

Perception becomes more informative when the agent can act:

- move viewpoint;
- touch/manipulate;
- run a diagnostic command;
- query a sensor at higher resolution;
- test an affordance;
- ask for missing information.

Action therefore is not only output. It is an information-acquisition operator that changes future observability.

## Persistent object/entity state

Multimodal intelligence over long horizons needs entity continuity across:

- camera frames;
- language references;
- tool identifiers;
- locations;
- user statements;
- action histories.

This entity layer connects multimodal grounding directly to temporal belief state and memory provenance.

## Failure modes

Language bottleneck; cross-modal false binding; modality dominance; sensor disagreement collapsed too early; action tokenization losing control precision; stale object identity; visual semantics transferred where physical affordances differ; confounding correlation with actionable causality.
