# E10B — Branch-Scoped Credit and Local Eligibility

**Status: second E10 family implemented; 5/5 replicated semantic tests pass; 30-seed sweep complete. Together E10A + E10B satisfy the promotion gate for a narrow credit-assignment principle.**

## Why a second family?

E10A used one serial pipeline where all nine stages were causally required. That established the problem of sparse delayed reward and diffuse blame, but it did not test **causal scope**: what happens when substantial parts of a trajectory were executed but did not actually determine the final outcome?

E10B uses speculative parallel branches.

## Environment

Each episode executes two five-stage branches in parallel.

- both branches choose actions and consume computation;
- only one branch is selected as causally relevant to the final outcome;
- final success depends only on all five actions in the selected branch being correct;
- the inactive branch's actions have no causal effect on that episode's result;
- the selected branch has noisy local stage diagnostics (`0.80` reliable by default).

This resembles systems that generate multiple plans, tool paths, agents or speculative computations and only later commit to one path.

## Policies

### Global all-branches credit

Retain all 10 stage actions and broadcast the delayed outcome to every action in both branches.

This creates **cross-branch credit contamination** because five updates/episode are assigned to a branch that did not affect the outcome.

### Branch-factorized credit

Use the known causal branch boundary and apply the delayed outcome only to the selected five-stage branch.

This still diffuses blame within that branch when one stage fails, but it eliminates updates to causally inactive computation.

### Branch + local eligibility

Keep branch factorization, then use noisy local diagnostics inside the selected branch:

- positive local evidence can be learned immediately;
- only suspicious stages remain eligible for the delayed final outcome.

This narrows both causal scope and delayed state.

## Validation

`5/5` replicated tests pass:

- global credit updates the inactive branch; branch-factorized credit does not;
- branch factorization improves tail task success;
- branch factorization halves delayed retained state;
- eligibility reduces false blame inside the relevant branch;
- eligibility retains less state than the complete selected branch.

## 30-seed result

| policy | overall success | tail success | inactive-branch updates/episode | false blame/episode | delayed items/episode |
|---|---:|---:|---:|---:|---:|
| global all branches | 0.482 | 0.533 | **5.000** | 1.380 | **10.000** |
| branch factorized | 0.745 | **0.812** | **0.000** | 0.878 | 5.000 |
| branch + eligibility | **0.812** | **0.812** | **0.000** | **0.147** | **1.123** |

## Combined E10 conclusion

The two families attack different failure modes:

### E10A — serial sparse reward

A failed nine-stage trajectory makes final-only credit unable to identify which stage was responsible. Local evidence/eligibility protects correct stages from diffuse blame.

### E10B — parallel sparse causal responsibility

A delayed outcome applies only to one of several executed branches. Factorizing by causal scope prevents irrelevant computation from receiving credit at all; local eligibility then narrows blame further inside the relevant branch.

The common implementation-neutral rule is:

> **Delayed outcomes may be globally relevant, but credit should propagate only through state transitions that remain causally or evidentially eligible for that outcome. Preserve full-history/global propagation only where the causal responsibility itself is unresolved and worth the state/communication cost.**

This does not require biological eligibility traces, differentiability, one RL algorithm, or a specific graph structure. `Eligibility` here means any compact retained evidence that a local transition remains plausibly responsible for a later outcome.

## Boundary conditions

The experiments also preserve important limits:

- on short/easy trajectories where final reward already identifies useful behavior, global credit can be adequate;
- when local diagnostics become noisy, the advantage of local factorization shrinks;
- factorization requires some evidence about causal scope; incorrect decomposition can hide genuine responsibility;
- global/broader attribution remains useful when interactions genuinely cross local boundaries.

That last point aligns directly with PS-003 coupling-scoped coordination: **credit scope, like control scope, should expand with actual coupling rather than by default.**

## Promotion

E10A + E10B now provide two structurally different task families, failure ablations, delayed-state accounting and signal-quality boundaries. DL-010 can therefore move to a provisional principle-level selection while the concrete credit mechanism remains open.
