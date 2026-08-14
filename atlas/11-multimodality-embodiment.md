# Multimodality & Embodiment

## Required function

Integrate heterogeneous observations and actions into coherent persistent state, concepts and control without forcing every modality through a lossy human-language bottleneck.

## Status

**First persistent-intelligence evidence pass completed on 2026-08-14; not saturated.**

Detailed evidence is in [`persistent-intelligence/06-multimodal-grounding-and-action.md`](persistent-intelligence/06-multimodal-grounding-and-action.md) and the temporal/world-state notes around it.

## First-pass findings

1. **Cross-modal alignment is powerful.** Shared semantic spaces support transfer and correspondence across modalities.
2. **Shared representation need not mean identical representation.** Modality-specific precision/detail can remain local while concepts/identity are bound across channels.
3. **Language is a useful interface and supervision source, not a proven universal internal hub.**
4. **Continuous sensor state can coexist with language/vision reasoning.** Embodied models demonstrate direct integration of non-text state.
5. **Action can be part of the multimodal interface.** Vision-language knowledge can transfer into action policies when action is represented and trained jointly.
6. **Action is also perception.** Viewpoint changes, probes and tool/sensor queries can reduce uncertainty and should be valued as information acquisition.
7. **Long-horizon grounding requires entity continuity.** A persistent object/person/tool identity must survive changing observations and modalities.

## Modalities to map

Text; images; video; audio; speech; spatial/3D data; proprioception; touch; time series; software/UI state; structured data; sensors; motor/action spaces.

## Clean-sheet questions

- Which representations should be shared across modalities and which should remain specialized?
- Is language a useful semantic hub or an unnecessary serialization bottleneck for particular modality pairs?
- How should temporal/spatial entity state persist beyond an observation/context window?
- When should perception be active—choosing what to observe next—rather than passive?
- How should uncertainty from different sensors be fused without collapsing disagreement too early?
- What action representation preserves control precision while still supporting semantic transfer?
- What capabilities truly require physical embodiment versus simulated/digital interaction?

## Anti-assumptions

Do not assume every modality should become text tokens, every modality belongs in one embedding, or embodiment implies a humanoid robot. The underlying requirements are grounding, persistent state, action and uncertainty-aware information acquisition.
