# E06 — Single Belief vs Multiple Hypotheses

**Status: first family implemented and replicated; causal second-family ablation added through E23B.**

## Question

When should an intelligent system preserve several plausible world states instead of collapsing immediately to the current best explanation?

## First family

A hidden world is one of four two-bit hypotheses. The system receives four noisy observations and then must either:

- make an irreversible hypothesis-specific commitment; or
- take a lower-value safe action.

`single_belief` keeps only the maximum-posterior hypothesis and always commits to it.

`multiple_hypotheses` preserves the full posterior and chooses the action with highest expected utility across all still-plausible worlds, including the safe action.

## 20-seed reliability sweep

| observation reliability | single utility | single wrong commitment | multi utility | multi wrong commitment | multi safe action |
|---:|---:|---:|---:|---:|---:|
| 0.56 | -0.373 | 0.686 | 0.100 | 0.000 | 1.000 |
| 0.65 | -0.154 | 0.577 | 0.129 | 0.120 | 0.701 |
| 0.80 | 0.274 | 0.363 | 0.409 | 0.053 | 0.539 |
| 0.97 | 0.882 | 0.059 | 0.894 | 0.002 | 0.114 |

The multi-hypothesis policy pays four active hypothesis items versus one for the single-belief policy. Its advantage is therefore conditional rather than free: it is largest when uncertainty and wrong-commitment cost are high, and narrows as evidence becomes decisive.

## Causal second-family ablation

E23B gives all policies the **same single intervention**. Sometimes that intervention uniquely identifies the causal theory; sometimes two theories remain compatible.

The single-theory variant forces a claim. The multi-theory variant leaves the result unresolved when evidence does not identify one theory.

30-seed means at one fixed intervention:

| wrong-theory utility | forced single net utility | preserve ambiguity net utility | unresolved rate |
|---:|---:|---:|---:|
| -0.2 | 0.576 | 0.308 | 0.662 |
| -1.0 | 0.314 | 0.308 | 0.662 |
| -2.0 | -0.015 | 0.308 | 0.662 |
| -4.0 | -0.671 | 0.308 | 0.662 |

This establishes a consequence-sensitive crossover: collapsing ambiguity can be efficient when mistakes are cheap, but preserving unresolved alternatives dominates when unsupported commitment is expensive.

## Interpretation

The experiment supports an adaptive rule rather than `always keep one belief` or `always maintain a large hypothesis set`:

> preserve alternatives while ambiguity × consequence justifies their state/coordination cost; collapse them when evidence or low consequence makes the extra state unnecessary.

## What remains open

- learned hypothesis generation rather than a fixed enumerated set;
- continuous/high-dimensional hypotheses;
- approximate posterior representations;
- hypothesis merging/splitting;
- interaction with evidence-linked memory and world-model rollouts;
- resource-aware pruning when the plausible set becomes large.
