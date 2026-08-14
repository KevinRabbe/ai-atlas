# E20B — Long-Horizon Self-Change Regression

**Status:** implemented, tested and swept. Second structurally different family for DL-020.

## Question

Can a self-change regression regime detect changes that improve short tests but introduce slow instability that only appears after much longer state accumulation?

E20's first family attacked distribution/coverage shift. E20B attacks **timescale shift**.

## Environment

The system runs 300 self-change rounds and selects among 30 candidate changes per round using a fixed visible horizon of 10 steps.

Candidates contain:

- a general improvement term;
- a visible short-horizon boost favored by search;
- a latent instability term whose cost grows superlinearly with execution horizon.

Deployment horizon changes halfway through the lifetime:

- phase 0: horizon 30;
- phase 1: horizon 100.

A change can therefore look excellent in the visible 10-step suite and still become harmful in real long sessions.

## Policies

- `visible_only` — accept if the short visible test improves;
- `fixed_hidden` — also require positive performance at one fixed hidden horizon 20;
- `rotating_hidden` — sample hidden horizons from the currently relevant horizon range (20–40 before shift, 20–120 after);
- `adversarial_rotating` — always test at horizon 120, paying a larger evaluation cost.

## 30-seed results

| policy | pre-shift true score | post-shift true score | harmful accepted | good rejected | lifetime utility |
|---|---:|---:|---:|---:|---:|
| visible only | 0.9813 | **0.0697** | 109.37 | **0.0** | 0.5316 |
| fixed hidden | 0.9951 | **0.0951** | 88.00 | **0.0** | 0.5562 |
| **rotating hidden** | 0.9993 | **0.9416** | 19.23 | 4.23 | **0.9380** |
| adversarial rotating | **1.0000** | **1.0000** | **0.0** | 47.40 | 0.9300 |

The fixed hidden horizon is useful while deployment remains close to it, but becomes a poor regression proxy after long-session deployment changes.

## Interpretation

E20B reproduces E20's core lesson without relying on a new scenario family:

- visible evidence is optimized against directly and misses hidden instability;
- fixed hidden evidence can be too narrow in **timescale**, not only state-space coverage;
- rotating independent evidence tracks the changing deployment envelope and preserves much more true capability;
- maximal adversarial testing is strongest on regression prevention but rejects many more useful changes and costs more.

## DL-020 promotion implication

E20 and E20B now support a provisional rule across two structurally different self-change failure families:

> **Evidence used to promote self-change should remain sufficiently independent from the proposal/optimization path and refresh coverage across changing state-space regions, failure modes and timescales. Adversarial/targeted regression pressure should scale with consequence rather than be universally maximal.**

The selected object is the **regression-evidence exposure/refresh rule**, not a particular train/test split or secret benchmark service.

## Relation to other selections

- **PS-013:** rotating evidence must add genuinely different failure coverage, not just more votes;
- **PS-014:** regression depth and adversarial targeting are priced assurance resources;
- **PS-016:** regression evidence must target the actual layer/timescale that can invalidate the change;
- **PS-002:** self-change promotion is another durable transition and therefore should be staged;
- **PS-004:** accepted/rejected change evidence should remain traceable for future revision.

## Next self-improvement gate

With E20/E20B, the Atlas can now begin E15/E16 experiments without letting the change-proposal mechanism judge itself solely on a fixed visible objective.

The next questions are:

1. whether a single greedy incumbent is enough or a bounded variant archive preserves future option value (E15);
2. whether repair should target local reversible state, isolated durable components or broad structural change (E16).

## Falsifiers

- rotating suites still become predictable enough for the proposer to exploit;
- regression coverage refresh costs dominate prevented regressions;
- long-horizon tests introduce simulator/model error larger than the regressions they detect;
- an alternative uncertainty/proof mechanism provides equivalent independent evidence more cheaply;
- hidden evidence becomes unavailable for open-ended real-world effects, requiring live staged deployment rather than offline suites.
