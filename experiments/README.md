# AI Atlas Experimental Organism

Phase 10 uses a deliberately small research organism to **discriminate architecture hypotheses**, not to approximate a production assistant.

## Why controlled probes first

Early architecture questions concern state semantics, control topology, representation, persistence and resource allocation. A large pretrained model would add uncontrolled variables. Controlled environments provide hidden ground truth, reproducibility, exact regime changes and cheap ablations. Learned models are introduced only where the hypothesis itself requires learning; E02 is currently the first such case and uses a tiny stdlib-only online learner.

## Tier-1 implementation status

All six Tier-1 experiment shapes are now implemented:

- **E01** — hierarchical versus distributed operation allocation;
- **E02** — integrated versus heterogeneous learned computation;
- **E03** — direct-address history versus compressed current state;
- **E04** — internal representation/interface format;
- **E05** — fixed versus adaptive computation;
- **E09** — immediate durable update versus staged consolidation.

This means the Tier-1 instrumentation layer is complete. It does **not** mean the architectural questions are resolved.

Detailed notes: `E01_CONTROL_TOPOLOGY.md`, `E02_COMPUTATION_INTEGRATION.md`, `E04_REPRESENTATION_INTERFACE.md`, `E09_CONSOLIDATION.md`, `PRELIMINARY_TIER1_RESULTS.md`.

## Runtime

Python 3.11+; no runtime dependencies.

```bash
cd experiments
python -m pip install -e .
python -m unittest discover -s tests -v
```

Original probes:

```bash
ai-atlas-lab memory --seed 7
ai-atlas-lab adaptive-compute --seed 7
python -m ai_atlas_lab.consolidation_cli --seed 7
```

New probes:

```bash
python -m ai_atlas_lab.tier1_cli control-topology --seed 7 --dependency-density 0.35
python -m ai_atlas_lab.tier1_cli computation-integration --seed 7 --sharedness 0.75
python -m ai_atlas_lab.tier1_cli representation --seed 7
```

Reproducible E01/E02/E04 sweep:

```bash
python -m ai_atlas_lab.tier1_sweep --seeds 12 --output results/tier1_full_12seeds.json
```

## Experimental discipline

Hide ground truth from the policy; give variants identical tasks/evidence and matched budgets; instrument resource use inside the mechanism; separate capability from cost; include regimes where competitors can plausibly win; test benchmark semantics before interpretation; emit machine-readable results; do not promote a design preference from one synthetic family.

## Current next step

Tier-1 code coverage is no longer the bottleneck. The next work is evidence saturation: second task families, resource-regime shifts, partial/hybrid mechanisms only where measured failures justify them, adaptive E09 consolidation, then Tier-2 belief/active-information experiments.

Do not add a large language model merely to make the organism resemble current AI.
