# AI Atlas Experimental Organism

Phase 10 begins with a deliberately small, model-free research organism. Its purpose is to **discriminate architecture hypotheses**, not to approximate a production assistant.

## Why model-free first

The first architecture questions are about state semantics and resource allocation. A large learned model would add uncontrolled variables: pretrained knowledge, opaque representation, model-specific context behavior and expensive stochasticity.

Synthetic environments provide:

- hidden ground truth;
- exact task difficulty;
- reproducibility;
- controlled state changes;
- resource counters;
- cheap repeated ablations.

Existing learned models can be introduced later only when an experiment specifically requires capabilities that the synthetic organism cannot represent.

## Current experiments

### E03 — history access versus compressed state

`ai-atlas-lab memory`

Compares three state policies over the exact same temporal event stream:

- `direct_address` — retain history and search it directly;
- `compressed_state` — retain only current entity state;
- `hybrid_state` — retain cheap current state plus indexed source history.

Queries test three distinct requirements:

- current state;
- historical state at an earlier time;
- exact event payload recovery.

Instrumentation reports accuracy by query class, reads/writes/comparisons and logical active/archive/index state size.

This is the first probe for Phase-9 E03. It does **not** prove that the toy hybrid is a final memory architecture; it establishes a reusable benchmark shape for measuring the direct-address/compression frontier.

### E05 — fixed versus adaptive computation

`ai-atlas-lab adaptive-compute`

Tasks contain a hidden binary answer and noisy evidence. Easy/medium/hard tasks differ only in evidence signal strength.

Compared policies:

- fixed evidence budgets;
- an adaptive policy that stops when accumulated evidence crosses a confidence threshold or a hard maximum budget is reached.

Instrumentation reports accuracy, average samples and compute allocation by difficulty.

The central test is whether adaptive compute spends less on easy tasks and more on hard ones while remaining competitive on the quality/cost frontier.

## Setup

Requires Python 3.11+ and has no runtime dependencies.

```bash
cd experiments
python -m pip install -e .
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Run the experiments:

```bash
ai-atlas-lab memory --seed 7
ai-atlas-lab adaptive-compute --seed 7
```

Write machine-readable results:

```bash
ai-atlas-lab memory --seed 7 --output results/e03_seed7.json
ai-atlas-lab adaptive-compute --seed 7 --output results/e05_seed7.json
```

## Experimental discipline

Every new mechanism should use the same pattern:

1. environment hides ground truth from the policy;
2. variants receive identical tasks/evidence and budgets;
3. resource use is instrumented inside the mechanism;
4. metrics separate capability from cost;
5. the benchmark contains a regime where each candidate should plausibly win;
6. tests verify the benchmark itself before interpreting architecture results;
7. raw results are machine-readable and seed/version identified.

## Next Tier-1 additions

1. E01 hierarchical versus distributed operation allocation;
2. E02 integrated versus heterogeneous computation;
3. E04 internal representation/interface format;
4. E09 immediate versus staged persistence/consolidation.

The harness should remain small enough that these mechanisms can be replaced rather than patched around each other.
