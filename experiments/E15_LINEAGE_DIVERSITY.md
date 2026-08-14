# E15 — Self-Improvement Lineage Diversity

**Status:** implemented, tested and swept across two structurally different families. DL-015 meets the Atlas promotion gate.

## Question

Should self-improvement keep only the currently best incumbent, or retain a bounded set of alternative lineages when discarded variants may have future option or stepping-stone value?

The archive is explicitly resource-priced and receives the same candidate-generation/evaluation budget as the greedy incumbent.

---

## Family A — recurring objectives with tradeoffs

A variant has two capabilities, A and B. Candidate changes usually improve the currently demanded capability while degrading the other. Demand is either stationary on A or switches every 50 rounds between A and B.

Policies:

- `greedy_incumbent` — keep one current variant and accept only improvements for the current regime;
- `bounded_archive` — retain at most six diverse variants and select the best stored lineage for the current regime. Archive storage costs `0.0008` per retained variant per round.

### 30-seed stationary control

| policy | net performance | raw performance | archive cost/round |
|---|---:|---:|---:|
| **greedy incumbent** | **0.99275** | 0.99275 | **0** |
| bounded archive | 0.98798 | 0.99275 | 0.00477 |

When the objective is stationary, the archive correctly loses because its alternatives never repay their maintenance cost.

### 30-seed switching regime

| policy | net performance | first 10 rounds after switch | best A retained | best B retained |
|---|---:|---:|---:|---:|
| greedy incumbent | 0.95620 | 0.79900 | 0.87129 | 1.00000 |
| **bounded archive** | **0.98040** | **0.95452** | **1.00000** | **1.00000** |

The archive preserves specialists that become useful again instead of repeatedly destroying and relearning them.

---

## Family B — deceptive stepping-stone landscape

An eight-bit genotype starts at `00000000`, a local optimum with score 10. The global optimum `11111111` scores 15, but every intermediate state has lower score:

`score = 10 - 0.7 * number_of_ones`.

Therefore a strict greedy incumbent cannot take any first step toward the global optimum.

Both policies receive eight candidate mutations per round for 180 rounds.

- `greedy_incumbent` mutates only the incumbent and accepts strict score improvements;
- `bounded_archive` retains at most 12 diverse Hamming-radius stepping stones and samples parents from the archive. Storage costs `0.001` per retained variant per round.

### 30-seed result

| policy | mean best score | reached global optimum | mean first global round | retained variants |
|---|---:|---:|---:|---:|
| greedy incumbent | **10.0** | **0/30** | never | 1 |
| **bounded archive** | **15.0** | **30/30** | **74.3** | 12 |

The result does not show that evolutionary populations are universally superior. It shows that immediately deleting temporarily inferior variants can make some improvement paths unreachable.

---

## DL-015 promotion implication

The two families establish both sides of the tradeoff:

- stable objective / locally monotonic landscape -> one incumbent is cheaper;
- recurring objectives / destructive tradeoffs -> retained variants carry future option value;
- deceptive landscapes -> temporarily inferior variants can be necessary stepping stones.

A narrow implementation-neutral principle is justified:

> **Retain multiple self-improvement lineages only while their estimated future reuse, uncertainty reduction or stepping-stone value exceeds storage/evaluation/coordination cost; collapse toward a single incumbent when those option values disappear.**

This is **PS-019 — resource-priced lineage diversity / variant optionality**.

The selected object is the lineage-retention rule, not genetic algorithms, evolution strategies, population size, mutation format or archive implementation.

## Relation to other Atlas principles

- **PS-005 / PS-010:** lineage retention is another resource allocation decision;
- **PS-012:** retained variants are a form of recoverable future optionality;
- **PS-015:** credit for improvements should remain scoped to the lineage/transitions that produced them;
- **PS-018:** promotion of a lineage still requires independent refreshing regression evidence;
- **PS-002:** promising variants can remain reversible/tentative before becoming the durable incumbent.

## Falsifiers / next work

- archive maintenance/selection overhead erases the benefit under realistic high-dimensional variants;
- a single reversible incumbent with sufficiently cheap rollback can provide equivalent option value;
- learned recombination from one compact generative representation dominates explicit variant retention;
- archive diversity preserves obsolete variants but misses genuinely novel stepping stones;
- changing evaluation criteria make archive comparison itself unreliable.

E16 should next test **repair/change scope**: local reversible patch, isolated durable component change, or structural system change, under the same independent regression protocol established by E20/E20B.
