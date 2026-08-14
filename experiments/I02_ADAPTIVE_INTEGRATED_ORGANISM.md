# I02 — Adaptive Integrated Organism

**Status: implemented; 5/5 replicated semantic tests pass; 30-seed lifetime sweep complete.**

## Why I02 exists

I01 showed that several individually supported principles can improve one mixed epistemic system when combined. But I01 still gave the controller unrealistically clean metacognition:

- operation reliabilities were effectively known;
- resource economics did not need to be learned through drift;
- the independent verifier was exact.

I02 removes those assumptions. The organism must now learn which operations work, decide how much evidence to share across task families/domains, and learn where a primary verifier is unsafe enough to justify an independent second check.

## Lifetime structure

The default run contains 600 batches × 10 tasks and three hidden regimes.

Two application-operation families are available:

- `retrieve`;
- `probe`.

Their quality and prices change across the lifetime. The two task families prefer different operations and those preferences also drift.

The controller only observes outcomes of operations it actually buys.

Frontier/research work contains many reusable claim keys rather than a handful of one-shot domains. Correct or false durable discoveries therefore influence later application behavior.

## Conditional shared/private operation learning

I02 compares four quality estimators:

1. **conditional shared/private** — share evidence within a task family while feedback is scarce, then increasingly use domain-private evidence as it accumulates;
2. **all shared** — one resource-quality estimate across all families/domains;
3. **all private** — domain-only estimates;
4. **frozen initial** — use initial-regime resource quality and never adapt to later drift.

This operationalizes PS-009 inside the integrated organism rather than as a stand-alone classifier task.

## Fallible assurance

The primary verifier has two failure regimes:

- one task family has a strongly correlated blind spot;
- the other family has a much lower false-approval rate.

The system does not observe hidden correctness. It can sample a more independent secondary verifier at a higher cost.

The adaptive assurance controller learns family-specific unsafe-primary-approval rates from secondary disagreement. It uses an **upper confidence estimate**, not only the posterior mean, so sparse evidence does not look certain.

Secondary checking is purchased when estimated false-knowledge consequence exceeds verification price. The consequence includes a small estimate of future contamination from durable reuse.

Comparison variants:

- adaptive assurance;
- trust the primary verifier only;
- require secondary verification uniformly.

## Important benchmark correction discovered during development

The first I02 draft had two measurement defects:

1. there were too few reusable research claims, making full double verification almost free;
2. a high-risk claim that requested secondary verification but lost the scarce assurance slot could silently fall back to primary-only consolidation.

Both were corrected rather than tuning the test result:

- the lifetime now contains many reusable frontier claims;
- a claim judged to require additional evidence cannot become durable merely because assurance capacity is unavailable.

A seed-specific assertion was also replaced by replicated semantic tests because stochastic learning should not be promoted or rejected from one lucky seed.

## Validation

`5/5` I02 tests pass. They check across replicated seeds that:

- conditional quality estimation adapts better than frozen initial economics after resource-quality drift;
- conditional sharing beats all-shared estimation when task families need opposite resources;
- conditional sharing beats all-private estimation when per-domain feedback is scarce;
- adaptive independent checking cuts false durable knowledge sharply relative to primary-only verification;
- adaptive assurance uses less secondary verification than uniform double checking.

Together with E08B and I01, this continuation's local files run **14/14 passing tests**.

## 30-seed default sweep

### Operation learning

| variant | net utility/task | regime 0 | regime 1 | regime 2 |
|---|---:|---:|---:|---:|
| **adaptive conditional** | **1.3511** | 1.6502 | **1.0622** | 1.3408 |
| all shared | 1.2659 | 1.2070 | 1.2741 | 1.3167 |
| all private | 1.3316 | 1.6185 | 1.0238 | 1.3526 |
| frozen initial | 1.3391 | **1.6734** | 0.8804 | **1.4634** |

The table is intentionally not a universal win in every regime. Frozen initial economics is excellent while the world still resembles its initial assumptions and becomes poor when the operation frontier changes. All-shared estimation reacts quickly but averages incompatible task families. All-private estimation avoids that interference but learns more slowly from sparse local feedback. Conditional shared/private estimation produces the best lifetime utility across the changing mixture.

### Assurance

| verifier policy | net utility/task | false durable writes/run | secondary checks/task |
|---|---:|---:|---:|
| **adaptive assurance** | **1.3511** | 0.433 | **0.02022** |
| primary only | 1.1281 | **12.10** | 0.00000 |
| uniform double | 1.3487 | 0.433 | 0.02132 |

Adaptive assurance therefore reaches the same mean false-write count as uniform double verification in this sweep while using about 5% fewer expensive secondary checks and slightly higher lifetime utility.

The learned observable unsafe-approval estimates finish around:

- risky family: `~0.193`;
- safer family: `~0.060`.

The controller is not given those categories as verifier labels; it learns them from independent disagreement associated with the task family.

## Resource drift result

The conditional controller's regime-1 utility is ~`1.062`, compared with ~`0.880` when resource-quality assumptions are frozen at their initial values. This is the integrated version of the earlier E22 lesson: resource choice is only intelligent if the value model itself can change when the environment changes.

## What I02 supports

### A. Metacognition is itself uncertain learned state

The system should not assume it already knows:

- which operation is best;
- which verifier is trustworthy;
- how much sharing is useful;
- what yesterday's resource economics imply today.

Those estimates belong to revisable epistemic state.

### B. Sharing should follow reusable structure

The same conditional-sharing principle that survived E02C also improves online resource-quality learning inside a mixed lifetime.

### C. Assurance should be consequence-sensitive and uncertainty-aware

`Verifier A passed` is insufficient. The system benefits from learning evaluator failure patterns and buying independent evidence where uncertainty × consequence makes it worthwhile.

### D. Durable knowledge increases verification value

A false result is not merely one wrong reward. It can be reused later. Assurance should therefore consider propagation/lifetime consequences, not only the immediate candidate score.

## Still deliberately simplified

- the secondary verifier is independent enough to be a useful reference, though still fallible;
- verifier failure structure is tied to task families rather than discovered through rich latent features;
- quality estimates are simple frequency estimators rather than learned representations;
- operation allocation is still an explicit expected-value calculation;
- adaptive state breadth from PS-012 is not yet embedded directly into I02's hot state.

## Next experiments enabled by I02

The integrated organism is now ready to test several previously isolated Phase-3 verification decisions in one common environment:

1. **E12 — verification granularity:** final-outcome versus process/state-transition checks;
2. **E13 — evaluator independence:** multiple correlated judges versus fewer genuinely independent checks under optimization pressure;
3. **E21 — assurance allocation:** implicit self-check versus explicit consequence-sensitive assurance versus uniform checking;
4. later E10 credit assignment, where learned operation/value errors must be attributed across multi-stage trajectories.

The next question is no longer merely whether verification helps. It is:

> **Which evidence source should check which state transition, how independent must it be, and how should scarce assurance be allocated when the system is uncertain about the verifiers themselves?**
