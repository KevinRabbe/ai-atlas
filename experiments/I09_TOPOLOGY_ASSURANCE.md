# I09 — Assurance for Topology Reconfiguration under Correlated / Adversarial Evidence

**Status:** implemented architecture-reconfiguration stress. No new provisional principle is added; I09 composes PS-013/014/018/020 with the I07/I08 topology runtime.

## Question

I07/I08 let topology change from noisy but honest interaction evidence.

I09 asks:

> what happens when the evidence that proposes a split/merge is itself correlated, spoofable or systematically wrong?

A topology change is consequential because it can move state, change coordination boundaries and alter resource/control relationships. Therefore the evidence authorizing reconfiguration should be tested like any other durable/high-blast-radius transition.

## Environment

The matched twelve-node / three-partition topology family remains.

Primary interaction evidence normally has:

- true-coupled event probability `0.65`;
- uncoupled event probability `0.04`.

During the middle `22%` of each regime, an adversarial/correlated source injects a dense false interaction pattern between two truly separate groups with event probability `0.78`.

This is intentionally stronger than independent random noise. A sustained false source can push raw decayed coupling evidence far above the ordinary merge threshold.

An optional independent audit channel is not affected by that spoof source:

- true-coupled audit positive probability `0.78`;
- uncoupled audit positive probability `0.03`.

The learner receives samples from that channel only when the policy pays for them.

## Policies

1. **raw** — update topology from the primary coupling estimate;
2. **high threshold** — same primary source, but require a much larger coupling score;
3. **uniform independent** — independently sample every pair at every topology decision and construct topology from that audit snapshot;
4. **selective independent** — use cheap primary evidence to propose a topology change, then independently audit only the pair relationships whose grouped/separate status would actually change.

The selective policy approves a reconfiguration only when the independent evidence sufficiently agrees with the proposed split/merge.

## Default 30-seed results

Audit cost `0.00045` per independent sample.

### Honest primary evidence

| policy | utility/step | pairwise scope accuracy | migrations/run | harmful migrations/run | audit samples/step |
|---|---:|---:|---:|---:|---:|
| **raw** | **1.0479** | 0.9061 | 31.7 | 14.03 | 0.00 |
| high threshold | 1.0437 | **0.9498** | 34.6 | 0.23 | 0.00 |
| uniform independent | 1.0414 | 0.8931 | 105.2 | 40.77 | 33.00 |
| selective independent | 1.0406 | 0.9325 | 17.7 | **0.00** | **3.15** |

When the primary stream is honest, assurance is not free. Raw adaptation has the best priced default utility even though it makes more transient topology mistakes.

### Correlated/spoofed primary evidence

| policy | utility/step | pairwise scope accuracy | migrations/run | harmful migrations/run | audit samples/step |
|---|---:|---:|---:|---:|---:|
| raw | 1.0339 | 0.8227 | 62.0 | 29.17 | 0.00 |
| high threshold | 1.0348 | 0.8963 | 64.4 | 15.23 | 0.00 |
| uniform independent | **1.0414** | 0.8931 | 105.2 | 40.77 | 33.00 |
| **selective independent** | **1.0394** | **0.9325** | **17.7** | **0.00** | **5.90** |

The selective policy is not the highest-utility policy at this particular audit price, but it has the strongest assurance/resource profile:

- highest attacked pairwise accuracy;
- zero accepted harmful migrations in this family;
- ~82% fewer independent audit samples than uniform checking;
- far fewer topology migrations.

## Why a higher threshold is insufficient

The spoof source is correlated and sustained.

Increasing the threshold assumes the problem is ordinary random noise. But if one source repeatedly reports the same false relationship, its evidence can cross almost any practical fixed threshold given enough time.

Default attacked means:

- raw harmful migrations: ~`29.2`/run;
- high-threshold harmful migrations: ~`15.2`/run;
- selective independent: `0`/run.

So the relevant quantity is not just **confidence magnitude**. It is whether additional evidence adds a sufficiently different failure mode.

That is PS-013 at topology scale.

## Assurance allocation crossover

Under the attacked stream:

| audit price/sample | uniform independent utility | selective independent utility |
|---:|---:|---:|
| 0.00025 | **1.0480** | 1.0406 |
| 0.00045 | **1.0414** | 1.0394 |
| 0.00080 | 1.0298 | **1.0373** |

Uniform checking consumes ~`33.0` audit samples/step. Selective checking consumes ~`5.9` under attack and ~`3.2` when the primary stream is honest.

This independently reproduces PS-014:

> **heavy assurance is rational when independent evidence is cheap relative to reconfiguration consequence; selective assurance wins when assurance itself becomes costly/scarce.**

## Architecture implication

I09 changes the topology loop from:

```text
interaction evidence
      ↓
estimated coupling
      ↓
split / merge
```

into:

```text
interaction evidence
      ↓
proposed coupling change
      ↓
size / consequence / uncertainty of topology mutation
      ↓
independent assurance when worth its cost
      ↓
approved split / merge
      ↓
I08 typed epoch migration protocol
```

The topology learner is therefore **not its own promotion authority**.

That mirrors the self-change rule from PS-018: evidence used to optimize/propose a structural change should not automatically be sufficient evidence to authorize that same structural change.

## Important negative result

Independent checking is not automatically good just because it is independent.

The `uniform_independent` policy reconstructs a whole graph from small fresh audit batches. At five samples/pair this creates substantial snapshot variance and many topology changes. It can still win when audits are cheap, but it is not a perfect oracle.

So the selected object remains:

- evidence independence;
- assurance allocation;
- consequence-aware promotion;

not "always use a second sensor".

## Validation

Six semantic tests cover:

1. correlated spoofing degrades the raw topology learner;
2. a larger threshold does not eliminate sustained correlated-source failure;
3. selective independent evidence blocks harmful migrations in the matched family;
4. selective assurance improves attacked priced utility over raw updates;
5. assurance loses value when the primary stream is honest;
6. uniform-vs-selective checking crosses over as audit price changes.

## Next architecture checkpoint

I08/I09 now give enough evidence to stop treating the candidate architecture as a diagram.

The next high-value build is a **persistent typed-scope organism API** with explicit operations such as:

- propose transition;
- allocate operation bundle;
- create/merge/split scope;
- stage migration;
- forward in-flight work by topology epoch;
- read current authority version;
- attach/retrieve evidence source;
- rematerialize predictive state;
- request independent assurance;
- commit/rollback structural change.

Then experiments should run through that common API rather than implementing each mechanism in a separate synthetic policy.

That will be the first step from experimental reconstruction into an executable architecture prototype while keeping every boundary falsifiable.
