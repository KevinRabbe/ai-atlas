# I04 — Typed State-Transition / Resource Kernel

**Status:** implemented, tested and swept. Composition evidence only; not an architecture-family selection.

## Question

Can several previously separate Atlas rules be implemented by one common transition allocator without collapsing authority, durability, consequence and assurance semantics into one scalar score?

I04 is the first explicit attempt to compress the recurring Phase-10 laws into a smaller mechanism boundary.

## Common transition abstraction

Each optional operation is represented as a transition proposal with fields including:

- task identity;
- transition kind;
- resource class;
- estimated downstream gain;
- explicit cost;
- authority class;
- reversibility;
- whether sufficiently independent evidence is required.

The shared allocator can rank work across cognition, observation, external preparation and verification. The experiment then asks whether the same rank score may also grant permission for consequential effects or durable knowledge changes.

## Variants

### `typed_shared_kernel`

One common allocator owns five total slots per batch and may move them between ordinary work and verification. Verification also has a two-slot physical ceiling. Durable research claims require independent evidence; consequential external actions remain subject to consequence-aware authority even when their preparation step has high expected value.

### `typed_siloed_controllers`

Uses the same typed authority rules but permanently partitions the five slots into four work slots and one verification slot.

### `flat_scalar_kernel`

Uses a common ranking score but removes the semantic boundary between local value/confidence and authority. High visible research score can directly create durable knowledge, and an apparently positive ordinary action score can authorize an external effect.

This is intentionally the dangerous clean-sheet alternative: if one scalar really is sufficient, it should win after downstream consequences are priced.

## Workload

The lifetime has a hidden task-mix shift.

Phase 0 is cognition/observation heavy:

`think .40 / observe .25 / external .20 / research .15`

Phase 1 becomes consequence/knowledge heavy:

`think .15 / observe .15 / external .35 / research .35`

The allocator receives no phase label. Candidate research claims are correct with probability 0.72. The visible evaluator is intentionally exploitable: it falsely approves 55% of wrong candidates. The independent check falsely approves 4% of wrong candidates.

External actions have a stronger failure penalty than ordinary answer errors, creating a typed consequence difference that a flattened controller must either preserve explicitly or pay for.

## 30-seed results

| variant | net utility/task | false durable writes/run | unsafe external effects/run | authority-boundary violations/run |
|---|---:|---:|---:|---:|
| **typed shared kernel** | **0.9758** | 5.13 | **5.03** | **0.0** |
| typed fixed silos | 0.7846 | **2.67** | 6.57 | **0.0** |
| flat scalar kernel | **-0.3494** | **194.13** | **68.43** | **1144.7** |

The flattened policy produces many more correct durable writes (~912.8/run versus ~629.1 typed shared), but this is not a win: it simultaneously promotes ~194 false durable claims/run and suffers strongly negative lifetime utility.

## Reallocation under hidden workload shift

The shared typed allocator changes its resource mix without receiving the hidden regime label:

| metric | phase 0 | phase 1 |
|---|---:|---:|
| verification allocations/task | 0.1003 | **0.1546** |
| ordinary work allocations/task | 0.3164 | **0.2620** |

The fixed typed silos remain near their built-in partition:

- verification ~0.0676 -> ~0.0824/task;
- work ~0.3333 -> ~0.3328/task.

This is the main positive composition result: **resource allocation can be shared and adaptive across transition kinds without requiring separate permanent controllers.**

## Boundary result

The negative result is equally important:

> **The allocator score is not itself authority.**

A common marginal-value calculation can decide which optional work deserves scarce resources. It does not safely erase distinctions between:

- temporary/reversible internal computation;
- durable epistemic mutation;
- consequential external effects;
- evidence that grants authority for either.

When these are flattened, optimizer pressure selects transitions that look locally valuable precisely because they bypass the expensive evidence/consequence semantics that protect lifetime utility.

## Architectural implication

I04 supports a smaller organization than one-controller-per-principle:

`typed transition proposals -> shared resource/value allocator -> authority/evidence gate -> execute/state transition -> outcome/credit`

The evidence does **not** support:

`all state changes -> one scalar score -> execute if score > threshold`.

So the current compression hypothesis is:

- **allocation may unify** across compute, retrieval, observation, assurance and other optional work;
- **authority must remain typed** where transitions differ in durability, reversibility, external consequence or epistemic standing.

This strengthens PS-001, PS-003, PS-005, PS-010, PS-013 and PS-014 jointly without creating a new provisional principle yet.

## Falsifiers / next tests

- learn the gain/cost/authority estimates rather than supplying calibrated task reliabilities;
- introduce delayed side effects where authority cost is not immediately observable;
- let typed categories be partially wrong or incomplete;
- compare soft consequence-sensitive gates against explicit hard capability boundaries in E14;
- test whether verification granularity can use the same transition kernel while retaining independent failure semantics;
- test asynchronous/event-driven execution later under E18.

I04 is evidence that the Atlas may need fewer controllers than its principle count suggests, but also that some semantic boundaries are structural rather than implementation accidents.
