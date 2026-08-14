# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The purpose of this repository is **not** to document today's implementations and then assemble them into another conventional AI stack. The purpose is to extract the underlying mechanisms, empirical results, constraints, failure modes, and open questions across AI and adjacent fields; separate evidence from implementation habit; and then use that knowledge to derive clean-sheet architectures.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

After a research area has been mapped, synthesis should restate the problem in implementation-neutral terms and ask what computational mechanism is actually required. Transformers, natural-language chains of thought, vector databases, agents, RLMs, harnesses, particular training algorithms, and current hardware are candidates—not axioms.

## Repository layers

- `atlas/` — mechanism-centric notes covering the knowledge base.
- `sources/` — source registry and evidence trail.
- `research/` — research roadmap, claims ledger, contradictions, and open questions.
- `synthesis/` — cross-domain deductions that are supported by the atlas.
- `clean-sheet/` — architecture design after implementation assumptions are deliberately removed.

## Current research state

- Foundations: first evidence pass complete; not saturated.
- Architecture + systems/hardware: first coupled evidence pass complete; not saturated.
- Clean-sheet architecture selection: deliberately **not started**.

The architecture/systems work is intentionally coupled because information access, persistent state, routing, precision, memory movement, communication and hardware execution form one design surface rather than independent layers.

## Evidence discipline

Every important claim should distinguish:

1. **Observation** — directly measured or reported.
2. **Inference** — conclusion supported by observations.
3. **Hypothesis** — plausible but not established.
4. **Design choice** — a deliberate engineering decision, not a scientific fact.

Negative results, replications, contradictory evidence, scaling limits, and failure cases are first-class knowledge. A mechanism is not considered understood merely because a benchmark improved.

## End goal

Produce a defensible answer to:

> If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?

The eventual architecture should be traceable back to evidence in the atlas and should make its assumptions explicit enough to be falsified experimentally.