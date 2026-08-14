# Research Methodology

## Objective

Map the mechanisms, evidence, constraints, and unknowns required to reason about intelligence as a computational system. The atlas is an evidence base for later clean-sheet architecture work, not a catalogue of fashionable implementations.

## Unit of research

The primary unit is a **mechanism**, not a paper, product, model, or framework.

For every mechanism ask:

1. What problem is being solved?
2. What information enters and leaves the mechanism?
3. What computation does it perform?
4. What capability does it add?
5. What is the empirical evidence?
6. What does it cost in training, inference, memory, bandwidth, latency, data, and engineering complexity?
7. How does it scale?
8. Where does it fail?
9. Which assumptions are essential and which are historical accidents?
10. What simpler or fundamentally different mechanism could provide the same function?

## Evidence classes

- **O — Observation:** directly measured/reported result.
- **I — Inference:** deduction supported by observations.
- **H — Hypothesis:** plausible proposition requiring testing.
- **D — Design choice:** engineering preference or constraint.

Never silently promote I/H/D into O.

## Evidence strength

Use `E0` through `E5`:

- `E0`: speculation / no empirical support.
- `E1`: anecdote or uncontrolled demonstration.
- `E2`: one controlled study or narrow benchmark.
- `E3`: multiple experiments / meaningful ablations.
- `E4`: independent replication across models/tasks/settings.
- `E5`: robustly established across methods and environments.

Evidence strength is not importance. A high-value hypothesis can be E0.

## Source priority

Prefer: original papers and technical reports; official code/data; replications; strong negative results; systems measurements; then high-quality syntheses. Secondary commentary is useful for discovery but should not be the evidentiary anchor when a primary source exists.

## Anti-cargo-cult rule

Named implementations belong under `Evidence / examples`, not in the abstract problem statement. During clean-sheet synthesis, restate each problem without implementation vocabulary before proposing architecture.

## Contradictions

Do not average conflicting findings into a vague sentence. Record the conflict, experimental conditions, likely moderators, and what experiment would discriminate between explanations.

## Saturation criterion

A topic is ready for synthesis only when we have mapped: strong positive evidence, important negative results, alternatives, scaling behavior, system costs, and unresolved questions. 'Many papers read' is not a saturation criterion.
