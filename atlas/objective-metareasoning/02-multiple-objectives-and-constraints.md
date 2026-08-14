# Multiple Objectives and Constraints

## Required function

Represent competing goals, hard/soft constraints and trade-offs without assuming every decision can safely be reduced to one fixed scalar proxy.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| O-MO-01 | Multi-objective sequential decision problems can require Pareto/coverage sets rather than one policy when scalarization is unknown, changing or inadequate. | O/I | E4 | O-S007 |
| O-MO-02 | Constrained policy optimization explicitly separates reward maximization from safety/cost constraints and provides near-constraint-satisfaction guarantees under its assumptions. | O | E4 | O-S008 |
| O-MO-03 | Reward-constrained methods demonstrate a distinct optimization role for constraint signals rather than encoding every requirement into the reward itself. | O | E3 | O-S009 |
| O-MO-04 | Phase-5 reward-hacking evidence shows a single measured objective can be optimized while hidden/desirable dimensions deteriorate. | O | E4 | prior Verification evidence |

## Why scalarization is attractive

One number enables straightforward ranking/search. But choosing weights silently decides trade-offs such as:

- quality versus latency;
- capability versus energy;
- immediate reward versus long-term optionality;
- task success versus side-effect risk;
- user preference versus policy constraint;
- exploration versus safety;
- current benchmark versus future transfer.

If those weights are uncertain or context-dependent, a single fixed scalar can hide rather than solve the decision problem.

## Constraints vs preferences

Some objectives may be:

- **hard constraints** — actions never authorized without exception process;
- **risk limits** — probability/severity bounds;
- **soft preferences** — optimize when feasible;
- **resource budgets** — compute/time/energy/financial limits;
- **lexicographic priorities** — satisfy A before optimizing B;
- **Pareto objectives** — retain alternatives until a trade-off is chosen.

The exact hierarchy is domain/user/policy dependent.

## Dynamic trade-offs

Trade-offs can change with context:

- emergency versus normal operation;
- reversible versus irreversible action;
- low versus high uncertainty;
- local private task versus shared infrastructure;
- exploration phase versus production execution.

Therefore an objective representation may itself be state-dependent.

## Clean-sheet restatement

Represent **value as structured constraints/preferences under uncertainty**, with scalarization performed only when the decision actually requires choosing among alternatives and with the chosen trade-off recorded/provenanced.

## Failure modes

Hidden scalar weights dominate outcomes; impossible hard constraints cause deadlock; soft preferences accidentally treated as hard; constraint satisfaction locally causes worse global outcome; Pareto archive explosion; objective priorities change without provenance; policy constraints optimized around semantically; resource costs omitted from utility.
