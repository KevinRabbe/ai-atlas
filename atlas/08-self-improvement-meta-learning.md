# Self-Improvement & Meta-Learning

## Required function

Convert observed weaknesses/opportunities into independently validated improvements to the correct system layer while controlling regression, evaluator corruption, search collapse and lifetime cost.

## Status

**First self-improvement evidence pass completed on 2026-08-14; not saturated.**

Detailed notes live under [`self-improvement/`](self-improvement/INDEX.md).

## First-pass findings

1. **Self-improvement has multiple mutation surfaces.** Context policy, memory, tools, skills, harnesses, data, weights, evaluators and architecture are distinct targets.
2. **Diagnosis precedes mutation.** Wrong-output symptoms do not identify the causal layer; controlled repair/ablation evidence should guide scope.
3. **Runtime/harness is a real learning substrate.** Fixed-model systems can improve substantially through automated harness changes.
4. **Harness and weights co-evolve through data.** Runtime policy shapes the traces that later train the model; weight changes reshape future traces.
5. **Alternative lineages can preserve stepping stones.** Greedy replacement of one incumbent is not universally justified.
6. **Structural search can discover new architectures/algorithms.** Improvement can eventually search computation itself, but structural/meta-mutations have a larger assurance surface.
7. **Acceptance must remain sufficiently independent.** A candidate should not be able to win solely by changing its evaluator, tests, permissions, audit or rollback path.
8. **Improvement should be transactional and lineage-preserving.** Branch, test, activate, monitor and rollback rather than opaque in-place mutation.
9. **Benchmark gain != net improvement.** Lifetime utility includes transfer, inference cost, trace quality, maintenance, assurance and regression risk.
10. **Self-improvement needs stopping.** Another improvement iteration is useful only while expected future value exceeds search/evaluation/risk cost.

## Candidate improvement substrates

Active state; retrieval/context policy; episodic/semantic memory; executable skills; prompts/instructions; tool/interface design; routing/scheduling; harness code; training data/curriculum; reward/evaluator models; task-model adapters/weights; architecture/developmental program; compiler/hardware-specific algorithms.

## Clean-sheet questions

- Can a mutation router correctly attribute failures to the responsible layer?
- When should local patches be consolidated into skills, weights or structural changes?
- How much variant diversity should be retained versus pruned?
- How should harness quality include the future value of generated traces?
- Which evaluator/control components must remain outside each mutation scope?
- How can an assurance/control layer itself be upgraded without circular self-approval?
- What lifetime utility function best decides whether an improvement is worth keeping?
- When should the system stop improving and return compute to actual tasks?

## Anti-assumptions

Do not assume recursive self-rewriting is intrinsically beneficial, that self-improvement means weight updates, that all accepted variants should replace their ancestors, or that a candidate can safely mutate the only machinery used to evaluate and recover from itself.
