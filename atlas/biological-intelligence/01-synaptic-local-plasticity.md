# Synaptic Local Plasticity

## Required function

Modify stored interaction strengths using information available locally or nearly locally while preserving useful causal/temporal associations.

## Evidence

- **B-S001 — Bi & Poo (1998):** paired pre/post activity in cultured hippocampal neurons produced timing-dependent potentiation or depression, with direction depending on relative spike timing and additional dependence on initial synaptic strength and postsynaptic cell type.
- **B-S002 — Froemke, Poo & Dan (2005):** timing-dependent plasticity rules varied with dendritic location, showing that the same nominal synapse rule is not spatially uniform.
- **B-S003 — Turrigiano et al. (1998):** cortical neurons also exhibit activity-dependent scaling of many synapses together, showing task/local plasticity is not the only weight-changing process.

## What seems established

### Plasticity is context dependent

Biological synaptic change is not well described by one scalar Hebbian rule. Timing, existing strength, cell type, dendritic location, recent activity and modulatory state can change the update.

### Locality does not imply isolation

A synapse can maintain local state while its final update is gated by signals originating at larger circuit scales. This distinction becomes important in the neuromodulation/eligibility-trace note.

## Clean-sheet restatement

A learning substrate may benefit from **local candidate updates plus contextual gating**, rather than requiring every adaptation event to receive the full global system state.

This does not establish that local biological rules can replace backpropagation at modern AI scale. The useful hypothesis is about factorizing credit information.

## Failure modes

Purely local correlation can reinforce spurious coincidences; unconstrained potentiation can destabilize activity; location/cell-context dependence can make a nominally simple rule difficult to analyze.