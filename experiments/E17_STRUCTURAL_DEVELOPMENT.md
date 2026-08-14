# E17 — Mature Structure: Direct Mutation vs Indirect/Developmental Encoding

**Status:** first structural family implemented and tested. **DL-017 remains unresolved.**

## Question

When should mature system structure be represented and changed directly, and when does an indirect/generative/developmental encoding earn its additional abstraction?

The clean-sheet question is not "should the system use developmental programs?" It is:

> **Does repeated/compressible structural regularity make one coordinated indirect change more valuable than many independent direct changes, after mutation/search/storage cost and exception handling are priced?**

## Family A — repeated regularity vs irregular local change

A 64-unit structure must track a changing target under four candidate evaluations per round.

Two regimes are tested inside the family:

1. **regular repeated structure** — one shared template plus a small stable exception set; the template flips coherently at large shifts;
2. **irregular local structure** — roughly unstructured target state with small independent local changes every 40 rounds.

The target structure is used only by the evaluator; mutation policies do not receive a hidden "regularity" label.

## Variants

- `fixed` — no structural adaptation;
- `direct` — explicit 64-unit state; candidate mutations change one unit;
- `generative` — one template + sparse overrides; one candidate slot is always spent testing a template mutation;
- `adaptive_indirect` — same template + overrides, but global/template mutation is proposed only after an observed coherent performance collapse; otherwise all candidate budget goes to local overrides.

Candidate-evaluation budget is matched for all adaptive variants. Accepted mutation cost and representation/storage cost are explicit.

## 30-seed result

### Repeated regular structure

| variant | net utility/round | mean structural score | first 10 after coherent shift | accepted mutations | final parameters |
|---|---:|---:|---:|---:|---:|
| fixed | 0.6413 | 0.6425 | 0.0724 | 0.0 | 64.0 |
| direct | 0.8754 | 0.8802 | 0.0859 | 132.6 | 64.0 |
| generative | 0.9944 | 0.9974 | **1.0000** | 6.63 | 5.63 |
| **adaptive indirect** | **0.9951** | **0.9980** | **1.0000** | 6.63 | **5.63** |

A coherent target reversal can be handled by one template mutation in the indirect encoding. Direct mutation must rediscover the same correlated change repeatedly across units.

### Irregular local structure

| variant | net utility/round | mean score | first 10 after local shift | accepted mutations | final parameters |
|---|---:|---:|---:|---:|---:|
| fixed | 0.4964 | 0.4977 | — | 0.0 | 64.0 |
| **direct** | **0.9284** | **0.9332** | **0.8939** | 139.4 | 64.0 |
| generative | 0.9190 | 0.9231 | 0.8844 | 132.6 | 32.1 |
| **adaptive indirect** | **0.9290** | **0.9332** | **0.8939** | 139.4 | 33.2 |

Always spending one candidate slot on the global template is harmful when there is no coherent global structure to exploit. The adaptive indirect policy stops paying that search cost and effectively behaves locally.

## Interpretation

The useful observation is conditional:

`coherent reusable structure -> indirect/shared structural encoding can coordinate change cheaply`

`exception-heavy/local structure -> direct/local variation avoids pleiotropic search cost`

This is consistent with existing Atlas results that **sharing follows reusable structure** and **repair scope follows causal scope**, but it does not yet justify a separate new principle.

The strongest current hypothesis is:

> Structural representation and mutation granularity should track the compressible regularity and causal scope of the structure being changed; indirect/developmental rules should retain local override/isolation paths for exceptions.

## Why DL-017 stays open

The two conditions above are still two regularity regimes of the same synthetic structural family. Atlas promotion requires a structurally different second family, not merely a parameter sweep.

A useful E17B should change the problem itself, for example:

- repeated dependency/workflow topology rather than bit-state matching;
- modular graph growth where a developmental rule can create repeated subgraphs but may also create invalid cross-module coupling;
- resource/hardware placement where symmetry is useful until local thermal/bandwidth exceptions dominate.

## Falsifiers

- indirect structure loses once decoding/development/runtime cost is fully priced;
- local overrides recreate explicit structure so completely that the generative layer has no net value;
- apparent regularity shifts too quickly for a shared rule to remain stable;
- direct structure plus good search matches coherent-shift recovery at equal candidate/evaluation cost;
- developmental coupling creates regressions that outweigh coordinated adaptation.

No architecture family is selected from E17A.
