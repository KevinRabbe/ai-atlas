# Dendritic and Local Neuron Computation

## Required function

Perform nonlinear integration close to incoming signals before information is broadcast to the wider network.

## Evidence

- **B-S004 — Polsky, Mel & Schiller (2004):** thin dendritic branches of cortical pyramidal neurons behaved as partially independent nonlinear computational subunits; nearby same-branch inputs summed differently from distributed inputs.
- **B-S005 — Xu et al. (2012):** nonlinear dendritic integration contributed to sensory/motor integration during behavior.
- **B-S006 — Gidon et al. (2020):** human layer 2/3 pyramidal dendrites exhibited calcium-mediated action potentials and could implement linearly non-separable input classification in the tested preparation/model.
- **B-S007 — Cazé et al. (2024):** experimental dendritic nonlinearities enabled linearly non-separable computations in cerebellar stellate cells.
- **B-S008 — Aizenbud et al. (2026):** modeling/measurement-based comparisons found human cortical neuron morphology and synaptic nonlinearities associated with higher functional input-output complexity than matched rat models.

## What seems established

The biological neuron is not generally a pointwise weighted sum followed by one nonlinearity. Spatial morphology, local conductances and compartment-specific dynamics can create multiple stages of computation before the axon output.

## Clean-sheet restatement

**Local hierarchical computation can reduce the amount of information that must be globally communicated.** A module may contain semi-independent subcomputations that aggregate only selected results upward.

The artificial analogue need not be a dendrite or spike. Candidate abstractions include hierarchical local circuits, conditional submodules, structured state partitions, or near-data compute.

## Important caution

Claims about extraordinary single-human-neuron capability are still based on limited tissue types, experimental conditions and models. The robust conclusion is compartmentalized nonlinear computation, not that human neurons implement a particular logic gate or should replace artificial network layers.