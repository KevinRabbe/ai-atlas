# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The purpose of this repository is **not** to document today's implementations and then assemble them into another conventional AI stack. The purpose is to extract the underlying mechanisms, empirical results, constraints, failure modes, and open questions across AI and adjacent fields; separate evidence from implementation habit; and then use that knowledge to derive clean-sheet architectures.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

After a research area has been mapped, synthesis should restate the problem in implementation-neutral terms and ask what computational mechanism is actually required. Named model blocks, natural-language reasoning, vector databases, agents, recursive systems, harnesses, biological mechanisms, particular learning algorithms, world-model products, verifier products, self-improvement frameworks, and current hardware are candidates or evidence—not axioms.

## Repository layers

- `atlas/` — mechanism-centric notes covering the knowledge base.
- `sources/` — source registry and evidence trail.
- `research/` — research roadmap, claims ledger, contradictions, and open questions.
- `synthesis/` — cross-domain deductions that are supported by the atlas.
- `clean-sheet/` — architecture design after implementation assumptions are deliberately removed.

## Current research state

- Foundations: first evidence pass complete; not saturated.
- Architecture + systems/hardware: first coupled evidence pass complete; not saturated.
- Biological intelligence, development & evolution: first evidence pass complete; not saturated.
- Learning & adaptation: first evidence pass complete; not saturated.
- Inference-time intelligence: first evidence pass complete; not saturated.
- Persistent intelligence: first evidence pass complete; not saturated.
- Verification, reliability & control: first evidence pass complete; not saturated.
- Self-improvement: first evidence pass complete; not saturated.
- Phase 7 cross-domain synthesis: next active area.
- Clean-sheet architecture selection: deliberately **not started**.

Four recurring allocation problems currently span the Atlas:

1. **compute allocation** — what operation should run next, where and for how long;
2. **change allocation** — what state should change, how durable it should be and when it should consolidate or be forgotten;
3. **information allocation** — what evidence/state remains active, what is abstracted or archived, and what can safely be discarded;
4. **assurance allocation** — how much independent evidence, restriction or authorization a proposed transition needs before it may propagate.

Self-improvement adds a meta-level: the system may search over its own future implementations, but candidate mutations must remain subject to causal diagnosis, independent assurance, lineage/versioning and lifetime-cost comparison.

These are provisional cross-domain patterns, not yet a final theory of intelligence.

## Evidence discipline

Every important claim should distinguish:

1. **Observation** — directly measured or reported.
2. **Inference** — conclusion supported by observations.
3. **Hypothesis** — plausible but not established.
4. **Design choice** — a deliberate engineering decision, not a scientific fact.

Negative results, replications, contradictory evidence, scaling limits, and failure cases are first-class knowledge. A mechanism is not considered understood merely because a benchmark improved or evolution happened to use it.

## End goal

Produce a defensible answer to:

> If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?

The eventual architecture should be traceable back to evidence in the atlas and should make its assumptions explicit enough to be falsified experimentally.
