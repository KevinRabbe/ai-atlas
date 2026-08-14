# I06 — Integrated Runtime Allocation

**Status:** implemented; composition checkpoint, not a new provisional principle.

## Question

Do individually useful runtime policies still help when they compete for the same finite resources and change one another's value?

I06 composes four previously separated runtime decisions inside one typed shared allocator:

- **fidelity:** cheap vs high-fidelity computation;
- **predictive-state breadth:** keep a broader hot state vs rematerialize discarded source evidence;
- **execution timing / consistency:** stay event-local vs synchronize a coupled state transition;
- **active information:** remain passive vs purchase an intervention/observation.

The experiment does not give the learned allocator the hidden regime bit that says which task family currently needs the expensive operation. Halfway through the lifetime, the mapping reverses.

## Why composition matters

These operations are not independent.

Examples in the environment:

- high fidelity without the discarded latent distinction can still be wrong;
- precision cannot repair a stale coupled snapshot if synchronization is the missing operation;
- preserving a broad hot state and rematerializing the same source are substitutes, so buying both is redundant;
- passive precision cannot replace an intervention when two worlds are only separable under action.

A controller that prices each operation independently can therefore make locally reasonable but globally wasteful choices.

## Compared variants

1. **oracle joint upper bound** — knows the hidden operation usefulness and solves the same grouped capacity allocation;
2. **learned joint allocator** — learns success for typed operation bundles by task family and jointly allocates the shared runtime budget;
3. **factorized independent controllers** — learns one operation at a time and assumes effects can be priced separately;
4. **uniform safe bundle** — spends the maximum typed bundle on the highest-consequence tasks until capacity is exhausted;
5. **uniform cheap bundle** — never purchases optional runtime work.

All variants see the same tasks, values, consequences, outcome draws and shared capacity.

## Default 30-seed sweep

| policy | net utility/task | error rate | pre-shift | early post-shift | late post-shift | capacity utilization |
|---|---:|---:|---:|---:|---:|---:|
| oracle joint | **1.7482** | **0.0790** | 1.7338 | 1.7608 | 1.7633 | 0.9694 |
| **learned joint** | **1.5640** | **0.1096** | **1.6244** | 1.0682 | **1.6327** | 0.8307 |
| factorized independent | 1.3549 | 0.1409 | 1.6101 | 0.5923 | 1.2500 | 0.9012 |
| uniform safe | 1.4096 | 0.1744 | 1.3973 | 1.4200 | 1.4223 | **0.9930** |
| uniform cheap | 0.4769 | 0.2747 | 0.4685 | 0.5217 | 0.4746 | 0.0000 |

The learned joint allocator is intentionally not oracle-like. Its old bundle estimates become wrong at the hidden shift, producing a real early-post-shift loss. Discounted evidence then lets it recover to roughly its pre-shift performance.

## Interaction failures

30-seed mean failure rates attributable to a missing complementary operation:

| policy | discarded-state failure | consistency failure | intervention failure | sensitivity failure |
|---|---:|---:|---:|---:|
| oracle joint | 0.0003 | 0.0002 | 0.0014 | 0.0003 |
| **learned joint** | **0.0080** | **0.0058** | **0.0084** | **0.0061** |
| factorized independent | 0.0151 | 0.0161 | 0.0227 | 0.0198 |
| uniform safe | 0.0366 | 0.0279 | 0.0323 | 0.0196 |
| uniform cheap | 0.0619 | 0.0543 | 0.0548 | 0.0536 |

Factorized control also purchases both broad hot state and rematerialization on about `1.32%` of all tasks even though they are source-state substitutes. The joint bundle representation makes that redundant combination unavailable by construction.

## Learned operation use

The learned joint policy uses approximately:

- high fidelity on `29.1%` of tasks;
- source rematerialization on `13.6%`;
- broad hot state on only `2.7%`;
- synchronization on `13.7%`;
- active intervention/observation on `10.6%`.

This reproduces E24's optionality result inside a shared runtime budget: recoverable source evidence is often cheaper than carrying every potentially useful distinction hot forever.

## Interpretation

I06 supports the architecture-compression hypothesis more strongly than any single E18/E19/E24 result:

> runtime mechanisms should be represented as typed, substitutable/complementary transition bundles and allocated by expected downstream value under shared scarcity.

It also gives an important negative result:

> learning good local operation values is not sufficient when operations interact.

The system must represent at least the interactions that materially change value, otherwise better local controllers can still waste capacity or leave complementary requirements unmet.

## What I06 does **not** select

I06 does not select:

- a particular scheduler;
- JEPA;
- one precision format;
- one event system;
- one memory implementation;
- one Phase-9 architecture family.

The grouped knapsack is an experimental allocator, not a proposed production implementation.

## Remaining falsifiers

The result should be weakened or reversed if:

- bundle-state explosion makes joint interaction modelling more expensive than the failures it prevents;
- a sparse factor graph or compositional value model matches bundle quality at much lower learning/search cost;
- asynchronous real execution overhead eliminates the synthetic event-locality advantage;
- rematerialization latency becomes large enough that broad hot state wins more often;
- learned uncertainty about interaction effects causes systematic under-exploration.

## Next

Use I06 as the common runtime substrate for matched A/B/C/D family implementations. The architecture-family comparison should vary **organization**, not quietly give one family better operation values, fidelity, source access, verification or total compute.