# E07 — Active Information Acquisition

**Status: first family implemented and replicated; second causal-intervention family implemented through E23B.**

## Question

When should the system pay to observe/probe the world rather than keep computing internally or act with current uncertainty?

## First family

A hidden four-state world produces one weak passive observation. Two optional high-quality probes reveal different latent bits. Tasks also vary in downstream value.

Compared policies:

- `passive` — never query;
- `fixed_both` — always buy both probes;
- `voi_myopic` — buy a probe only if its one-step expected decision value exceeds cost;
- `value_of_information` — bounded two-step lookahead that can value complementary probe sequences.

## Instrument failure caught during development

The initial harness accidentally mutated the lookahead policy into the myopic policy after the first task. The full validation group caught the mismatch and the benchmark was fixed before publication.

The experiment also exposed a real algorithmic failure: a one-step VOI controller can reject a first probe that has weak standalone value even when that probe unlocks a highly valuable second probe. Multi-step information can therefore be complementary rather than additive.

## 20-seed cost sweep

| probe cost | passive net | fixed-both net / queries | myopic net / queries | lookahead net / queries |
|---:|---:|---:|---:|---:|
| 0.02 | 0.124 | 1.062 / 2.000 | 1.062 / 2.000 | 1.062 / 2.000 |
| 0.08 | 0.124 | 0.942 / 2.000 | 0.877 / 1.617 | 0.942 / 2.000 |
| 0.20 | 0.124 | 0.702 / 2.000 | 0.161 / 0.069 | 0.702 / 1.986 |
| 0.60 | 0.124 | -0.098 / 2.000 | 0.124 / 0.000 | 0.183 / 0.612 |
| 2.00 | 0.124 | -2.898 / 2.000 | 0.124 / 0.000 | 0.124 / 0.000 |

The bounded lookahead policy buys everything when information is cheap, becomes selective in the intermediate regime, and stops entirely when probes are too expensive. At intermediate prices it can outperform myopic VOI because the value of a probe depends on what later observation it enables.

## Second family — causal interventions

E23B starts from candidate causal theories that are indistinguishable under inherited passive evidence. The system must actively intervene to distinguish them. This tests information acquisition as experiment design rather than sensor lookup.

The active policy identifies the hidden theory exactly while using about 1.66 interventions/task when experiments are cheap. When experiment cost reaches the point where expected epistemic benefit is non-positive, it performs zero interventions and leaves the claim unresolved.

## Interpretation

The evidence supports:

> information acquisition should be selected by expected downstream/epistemic value relative to interaction cost and risk, and the value calculation must sometimes include sequences of complementary observations rather than only one-step gain.

The exact VOI planner used here is a toy mechanism, not an architecture selection.
