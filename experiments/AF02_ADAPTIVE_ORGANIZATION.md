# AF02 — Adaptive Organizational Mode Selection

**Status:** implemented second architecture-level discriminator. **No fixed A/B/C/D family is selected.** AF02 tests whether organization itself can become a resource-priced adaptive state.

## Question

AF01 found a Pareto frontier:

- local/distributed organization can avoid unnecessary coordination;
- hierarchy can earn its cost under tight coupling;
- integrated pooling can earn its interference risk when structure is strongly shared;
- preserved variants can earn carrying cost when regimes recur.

AF02 asks the stronger question:

> can one system infer those conditions from observable evidence and change organizational mode online, while paying explicit switching and carrying cost?

If yes, asking for one permanent A/B/C/D winner may be the wrong abstraction.

## Important anti-cheating constraint

The adaptive selector never receives:

- the context label (`local`, `coupled`, `shared`, `recurrent`);
- the hidden coupling/sharedness/recurrence values;
- the identity of the best mode.

It receives noisy observable proxies only:

- observed coupling;
- observed conflict/interference;
- observed recurrence;
- observed transfer/sharedness;
- its own realized organizational reward history.

It updates a contextual mode-value estimate only for the mode it actually used. Counterfactual rewards remain hidden.

The oracle comparator may inspect hidden structural state and serves only as an upper bound.

## Second-family organization environment

AF02 is intentionally structurally different from AF01's task-level I06 runtime simulation.

The hidden world varies **continuous organizational economics**:

- coupling;
- reusable shared structure;
- recurrence/return of prior regimes.

Each mode has an implementation-neutral value surface reflecting costs already exposed independently in AF01:

- **A** gains from coupling but pays for unnecessary global arbitration under locality;
- **B** gains from locality but loses as global coupling rises;
- **C** gains from reusable shared structure but loses from interference when sharing is weak;
- **D** gains from recurrence/variant reuse but pays carrying cost when recurrence is low.

Structural state is jittered continuously inside recurring regimes, and both observations and rewards are noisy.

This benchmark therefore tests **organization selection economics**, not another implementation of the I06 task solver.

## Policies

1. fixed A;
2. fixed B;
3. fixed C;
4. fixed D;
5. **adaptive selector** — contextual optimistic value estimates, hysteresis/minimum hold time, explicit switch cost and hybrid carrying cost;
6. oracle selector — hidden structural state available, same switch/carrying prices.

The adaptive policy can reconsider organization every 10 steps and must hold a newly selected organization for at least two decision blocks.

## Default 30-seed result

Eight recurring structural cycles, 100 steps/regime, switch cost `0.18`, hybrid carrying cost `0.01`/step:

| policy | utility/step | switches/run | hidden-best-mode fraction |
|---|---:|---:|---:|
| fixed A | 1.4834 | 0.0 | ~0.250 |
| fixed B | 1.4518 | 0.0 | ~0.250 |
| fixed C | 1.4394 | 0.0 | ~0.250 |
| fixed D | **1.5087** | 0.0 | ~0.250 |
| **adaptive** | **1.5625** | 43.67 | **0.9065** |
| oracle | **1.5762** | 31.43 | 1.0000 |

The adaptive system beats the best permanently fixed mode by roughly `0.054` utility/step while retaining a visible gap to the oracle.

That oracle gap matters: the learned selector is not simply reading a disguised regime label.

## What organization it learns

Mean fraction of steps spent in the theoretically strongest organizational mode for each recurring context:

| hidden regime (not shown to selector) | expected mode | adaptive use |
|---|---|---:|
| local/sparse | B | **0.874** |
| strongly coupled | A | **0.913** |
| highly shared/transferable | C | **0.920** |
| strongly recurrent | D | **0.919** |

The mapping is learned from noisy observable proxies and realized performance.

## Falsifier — organizational plasticity has a timescale

AF02 explicitly varies regime duration and switch cost.

### Adaptive advantage over best fixed family

20-seed mean difference `adaptive - best fixed`:

| regime duration | switch 0.05 | switch 0.18 | switch 0.50 | switch 1.00 |
|---:|---:|---:|---:|---:|
| 20 | **-0.0184** | **-0.0226** | **-0.0348** | **-0.0565** |
| 40 | +0.0405 | +0.0364 | +0.0269 | +0.0094 |
| 80 | +0.0523 | +0.0511 | +0.0458 | +0.0349 |
| 120 | +0.0587 | +0.0572 | +0.0533 | +0.0452 |

When the world changes every ~20 steps, the adaptive architecture loses even at low switching cost. It cannot identify and amortize an organizational change fast enough.

At longer regime durations, organizational plasticity earns itself even under much larger switch cost.

This is a stronger result than simply saying "hybrid beats fixed":

> **organizational adaptation should occur only on timescales where expected regime persistence/value exceeds identification, switching and carrying cost.**

That pattern mirrors PS-005, PS-012, PS-019 and PS-020: adaptation itself is not free and therefore must earn its scope/lifetime.

## Architecture implication

AF01 + AF02 now support a more specific clean-sheet architecture hypothesis:

```text
common typed substrate
        |
observe coupling / transfer / recurrence / contention
        |
learn expected organizational value
        |
        +--> local/distributed mode
        +--> hierarchical arbitration mode
        +--> integrated/shared-core mode
        +--> variant-preserving mode
        |
price switch + carrying cost
        |
retain mode while marginal future value stays positive
```

The labels A/B/C/D may therefore be **modes of organization**, analogous to fidelity/state breadth/verification being adaptive resource decisions.

## Why this still does not select the final architecture

AF02 is deliberately an organization-level abstraction with continuous structural value surfaces. It does not yet reproduce:

- full I06 task execution while switching organizational machinery live;
- transfer of in-flight state across a mode transition;
- real message/latency/state-copy overhead;
- partial failure of the structural cues themselves;
- adversarial cues that make the selector choose the wrong organization;
- nested organization where different subsystems simultaneously need different modes.

So AF02 is strong evidence against **one fixed global family**, not proof of the final hybrid architecture.

## Next discriminator — AF03 / I07

The next architecture test should stop switching the *whole system* at once.

A realistic clean-sheet system may need:

- local organization in one domain;
- integrated sharing in another;
- a hierarchy only around a scarce shared resource;
- preserved variants only for unstable/self-changing subsystems.

AF03 should therefore test **simultaneous heterogeneous organization by scope**, including state-transfer/message costs and partially wrong structural estimates.

The key question becomes:

> can organization itself follow coupling/regularity **locally by scope**, rather than selecting one mode for the entire organism?

That is the architecture-level analogue of PS-003.