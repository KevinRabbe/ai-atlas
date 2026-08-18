# E25 — Local Training Decomposition / DiffusionBlocks Mechanism Test

Status: **specified, not yet executed**.

Purpose: test the implementation-neutral claim suggested by DiffusionBlocks that a globally useful learned transformation may sometimes be trained through independently or semi-independently optimized local stages, reducing simultaneously active training state and communication without requiring one end-to-end gradient path.

This is **not** a DiffusionBlocks validation benchmark only. DiffusionBlocks is one candidate implementation. The experiment is designed so it can lose.

## Primary question

Under matched task/data/total-learning-compute budgets, what is the resource/quality frontier among:

1. full end-to-end backpropagation;
2. end-to-end + activation checkpointing/rematerialization;
3. end-to-end + parameter/optimizer sharding where hardware permits;
4. fully independent local objectives (DiffusionBlocks-like when applicable);
5. local objectives + sparse global correction;
6. learned/adaptive decomposition if later justified.

## Claim types

- **O:** DiffusionBlocks reports roughly block-proportional active training-memory reduction because only one block requires gradients/optimizer state/activations at a time.
- **O:** reported quality is non-monotonic in block count; moderate block counts can equal/improve baseline, excessive decomposition degrades quality.
- **O:** blocks can train without inter-block communication under the method's local objectives.
- **I:** training-dependency scope may be smaller than inference-dependency scope.
- **H:** there exists a task/architecture-dependent minimum local learner capacity below which independent objectives stop composing adequately.
- **H:** hybrid local + sparse global correction may dominate both fully global and fully independent training across broader regimes.
- **H:** optimal decomposition should be selected by joint memory/communication/quality economics rather than fixed block count.

## Stage E25A — resource accounting reproduction

Use an architecture small enough to run repeatedly on available hardware but large enough that activation/optimizer memory is measurable.

Minimum variants:

- end-to-end;
- end-to-end + activation checkpointing;
- `B=2` local decomposition;
- `B=3`;
- `B=4`;
- `B=6` where depth permits;
- local decomposition + activation checkpointing.

Measure **actual peak allocated/reserved device memory**, not only analytical layer count.

Break memory into as many observable components as practical:

- parameters/master weights;
- gradients;
- optimizer states;
- activations;
- temporary kernels/workspaces;
- framework allocator/reserved memory.

Metrics:

- peak VRAM;
- bytes/parameter and bytes/trainable-active-parameter;
- forward/backward step time;
- total layer/token FLOP proxy;
- examples/tokens per second;
- optimizer updates to target quality;
- total wall-clock to target quality;
- energy proxy if observable.

### E25A falsifier

If practical memory does not materially follow the predicted active-scope reduction after accounting for runtime overhead, the simple `B x` resource interpretation must be weakened.

## Stage E25B — quality/granularity frontier

Run matched-budget sweeps across block counts and absolute block capacity.

Critical design: vary total depth as well as `B` so we can distinguish:

```text
quality depends on B/L ratio
```

from:

```text
quality depends on an absolute minimum stage capacity
```

and from:

```text
quality depends on task/noise/target complexity
```

Metrics:

- task loss/accuracy/generative metric;
- convergence rate;
- calibration if applicable;
- quality per peak-GB;
- quality per total compute;
- quality per wall-clock;
- quality per communication byte.

### E25B key crossover

The experiment should explicitly look for regimes where:

- end-to-end wins;
- moderate local decomposition wins;
- aggressive decomposition loses;
- hybrid local/global wins.

No policy is required to win universally.

## Stage E25C — credit/local-objective ablation

Separate the effect of **independent training** from the effect of the particular denoising target construction.

Compare where possible:

1. arbitrary/local auxiliary losses;
2. DiffusionBlocks-style denoising target field;
3. local target + occasional end-to-end correction;
4. teacher/intermediate representation matching;
5. predictive/JEPA-like local target where technically meaningful;
6. target learned by a controller (future, only if simpler variants justify it).

Question:

> Is the resource benefit caused merely by isolating blocks, or does success require a specifically coherent global objective field?

Expected discriminator:

```text
local independence alone
    !=
useful local credit
```

## Stage E25D — communication topology

Compare at least three deployment modes when hardware is available:

### D1 — sequential one-device local blocks

Train one block at a time on one GPU.

Purpose: maximum-memory-pressure case.

### D2 — independent blocks on separate devices

Each device trains one block independently.

Measure:

- inter-block bytes transferred;
- data/input duplication cost;
- checkpoint/output synchronization;
- wall-clock scaling;
- device utilization.

### D3 — one block itself distributed

Choose a block too large or a batch too large for one device and distribute **inside the block**.

Purpose: falsify the overclaim that block independence makes distributed communication disappear.

Expected result if the paper's mechanism holds:

- inter-block gradient/activation communication can approach zero;
- intra-block data/tensor/optimizer communication can remain substantial.

## Stage E25E — language-model capability test

This is mandatory before treating the method as relevant to frontier-style LLM training.

A generative similarity metric is insufficient.

For a scaled-but-feasible language model, compare under matched training tokens/compute:

- held-out next-token/log-likelihood measure when mathematically meaningful;
- generative perplexity;
- MAUVE or equivalent distributional metric;
- factual retrieval;
- compositional reasoning;
- simple code generation;
- long-context dependency;
- in-context adaptation;
- calibration/uncertainty;
- robustness after distribution shift.

A method that matches MAUVE while losing learned algorithmic/reasoning capability has **not** matched the relevant global behavior.

## Stage E25F — scale trend

Run at multiple model sizes on the same architecture/task family.

Track:

```text
relative quality gap vs parameter count
optimal B vs parameter count
minimum layers/parameters per block
memory reduction vs parameter count
communication reduction vs parameter count
```

Do **not** extrapolate a billion-parameter result from one small model without trend evidence.

Desired sequence if resources permit:

- very small sanity model;
- tens of millions;
- ~100M-class;
- several hundred million;
- only then >=1B.

The scale study should stop as soon as a clear adverse scaling trend falsifies the premise.

## Stage E25G — recurrent-depth / shared-parameter case

Because DiffusionBlocks reports a particularly different training path for recurrent-depth models, test separately:

- ordinary BPTT/full unroll;
- truncated BPTT;
- diffusion/local denoising training;
- optional sparse global correction.

Measure both activation memory and total training compute.

This may be more relevant to Atlas than a conventional deep transformer because Atlas already retains recurrent/iterative computation as an open architecture dimension.

## Required controls

- same dataset split;
- same effective number of samples/tokens;
- report optimizer/update-count differences;
- matched or explicitly normalized total layer evaluations;
- same evaluation pipeline;
- multiple seeds;
- report best checkpoint and final checkpoint separately if selection differs;
- acquisition/checkpoint-selection semantics recorded under PS-027;
- distinguish hyperparameter tuning budget from training budget.

## Hardware/accounting caution

Do not estimate consumer-GPU feasibility by comparing only `model parameters * bytes`.

Actual feasibility must include:

- active optimizer state;
- activations;
- conditioning/input duplication;
- attention buffers;
- temporary kernel workspace;
- CUDA/runtime reserve;
- batch/sequence length;
- checkpointing;
- offload/prefetch if used.

The paper's autoregressive adaptation can also alter sequence memory through its clean/noisy conditioning strategy; this must be measured rather than hidden inside a theoretical `B x` label.

## Promotion gate

E25 alone cannot select DiffusionBlocks.

A new Atlas principle should be considered only if at least two structurally different learning families show that:

1. useful global learning quality survives a smaller-than-global training dependency scope;
2. the local objective semantics, not merely a benchmark trick, explain the survival;
3. resource savings remain after real implementation overhead;
4. a crossover demonstrates when global credit is still necessary.

Until then this evidence only strengthens/open-tests PS-009, PS-010, PS-015, PS-021 and PS-023.

## Candidate architecture implication if supported

If E25 survives, the organism's learning plane should not assume one global differentiable update graph. It should expose a typed concept closer to:

```text
LearningRegion
  state/parameter scope
  target/objective semantics
  dependency scope
  credit source
  active resource footprint
  synchronization requirements
  global validation path
```

The allocator could then decide whether a learning transition is local, shared, recurrent, or globally corrected using the same value/coupling machinery already derived elsewhere in Atlas.
