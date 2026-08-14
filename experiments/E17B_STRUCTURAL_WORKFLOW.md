# E17B — Structural Development in Dependency Workflows

**Status:** implemented and tested. Together with E17A, this closes the current DL-017 promotion gate.

## Question

Does the direct-vs-indirect structural trade-off survive when the object being adapted is not a flat state vector but an **operational dependency topology** whose mistakes have different consequences?

Each of 16 workflow modules can use one of two dependency motifs:

- a parallel/fork-join motif;
- a serial dependency motif.

Using the parallel motif where serial ordering is required creates a hard dependency violation. Using the serial motif where parallelism is expected remains valid but creates avoidable latency.

The score therefore prices workflow correctness, bottleneck quality and latency rather than simple bit agreement.

## Families

### Repeated workflow

Most modules share one dependency motif, with a small stable set of local exceptions. The shared motif changes coherently at rounds 200 and 400.

### Irregular workflow

Modules begin with unrelated motifs and three local modules change every 30 rounds. There is no useful global topology shift.

## Variants

- `fixed` — no adaptation;
- `direct` — explicit per-module topology; candidate mutations rewrite one module;
- `generative` — one shared topology template plus local overrides; one candidate slot is always spent testing a global template rewrite;
- `adaptive_indirect` — same indirect representation, but global template rewrites are proposed only after a large coherent performance drop. Otherwise it spends all candidate budget on local overrides.

All adaptive variants receive four candidate evaluations per round. Mutation cost, blast radius, representation size and evaluation cost are explicit.

## 30-seed results

### Repeated dependency topology

| variant | net utility/round | workflow score | dependency-violation rate | mean latency | first 10 after shift | accepted mutations | final parameters |
|---|---:|---:|---:|---:|---:|---:|---:|
| fixed | 0.7476 | 0.7479 | 0.3618 | 1.5789 | 0.6828 | 0.0 | 16.0 |
| direct | 0.9814 | 0.9851 | 0.0123 | 1.0349 | 0.7084 | 33.37 | 16.0 |
| generative | 0.9955 | 0.9988 | 0.00060 | 1.0013 | **1.0000** | 3.60 | 2.57 |
| **adaptive indirect** | **0.9958** | **0.9991** | **0.00051** | **1.0008** | **1.0000** | **3.37** | **2.37** |

The indirect representation changes the repeated dependency rule once and preserves the local exception set. Direct adaptation must perform many separate module rewrites, leaving a temporary tail of dependency and latency errors after each coherent shift.

### Irregular local topology

| variant | net utility/round | workflow score | dependency-violation rate | mean latency | first 10 after shift | accepted mutations |
|---|---:|---:|---:|---:|---:|---:|
| fixed | 0.6736 | 0.6739 | 0.4910 | 1.7857 | 0.6737 | 0.0 |
| **direct** | **0.9680** | **0.9718** | 0.0132 | **1.0315** | **0.9285** | 64.67 |
| generative | 0.9608 | 0.9645 | **0.0129** | 1.0407 | 0.9111 | 66.23 |
| **adaptive indirect** | **0.9681** | **0.9718** | 0.0132 | **1.0315** | **0.9285** | 64.67 |

Always proposing a shared template rewrite wastes search budget and occasionally changes more modules than the causal scope warrants. The adaptive indirect representation detects that there is no coherent global collapse and falls back to local structural mutation, matching direct behavior.

## Cross-family synthesis with E17A

E17A used repeated/irregular structural state. E17B uses an operational workflow topology where mistakes become dependency violations and latency rather than just representation mismatch.

Both produce the same conditional frontier:

`repeated/compressible regularity -> indirect shared structural rule`

`local/exception-heavy structure -> direct/local mutation or override`

`uncertain regularity -> indirect rule must retain a local isolation path and earn global mutation from evidence`

This is enough for a narrow implementation-neutral promotion.

## Proposed principle

> **Regularity-scaled structural encoding:** represent and mutate structure indirectly when a compact generative rule captures reusable organization and coordinated changes; preserve direct/local override paths where exceptions or local causal structure make shared mutation harmful. The degree of indirectness is itself conditional on expected reuse, blast radius, search cost and exception burden.

This does **not** select evolutionary algorithms, developmental programs, graph grammars, modular neural networks or Phase-9 family D.

## Falsifiers

- decoding/development/runtime overhead removes the repeated-structure advantage;
- environment regularity changes faster than the indirect rule can be safely identified;
- exception sets grow until the indirect representation recreates explicit structure with extra overhead;
- direct structural search discovers coordinated changes just as quickly under equal candidate and representation cost;
- shared structural mutations create hidden correlated regressions that local tests miss.
