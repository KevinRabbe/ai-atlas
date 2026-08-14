# Information Access and Persistent State

## Required function

Make previously observed information available when future computation needs it, while controlling memory, bandwidth and latency costs.

## Core trade-off

The central architectural distinction is better expressed as **direct addressability versus compressed state** than as Transformer versus RNN.

- Direct-address mechanisms retain individually accessible past items or derived keys/values. They make content-dependent retrieval easy but generally accumulate state and/or pairwise work with sequence length.
- Recurrent/state mechanisms update a bounded state. They make incremental execution cheap but must decide what to preserve, overwrite, decay or compose.
- External/writable-memory mechanisms separate controller computation from a memory store and introduce explicit read/write policies.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-IA-01 | Gated recurrence can preserve information/credit over much longer lags than simple recurrent dynamics. | O | E5 | AS-S001 |
| AS-IA-02 | Full self-attention provides content-dependent token-to-token access and is highly parallel during training, but dense pairwise attention grows quadratically in sequence work. | O | E5 | AS-S002 |
| AS-IA-03 | Multi-query/grouped-query/latent attention show that the inference state associated with attention can be compressed substantially while retaining much of the useful capability. | O | E4 | AS-S005, AS-S006, AS-S007 |
| AS-IA-04 | Modern recurrent/SSM/linear-attention families can be trained in parallel forms while decoded recurrently with bounded state. | O | E4 | AS-S010, AS-S011, AS-S013, AS-S016, AS-S017 |
| AS-IA-05 | Bounded-state models can lose exact or flexible access to old associations when memory update rules are insufficiently expressive; newer delta/SSM designs explicitly improve erase/write/state tracking. | I | E3 | AS-S016, AS-S017, AS-S018 |
| AS-IA-06 | Sparse/hierarchical attention can reduce long-context work while retaining selective global access when sparsity is trained as part of the model. | O | E3 | AS-S008 |

## Important deductions

### Access pattern is the primitive

A future architecture should specify what kind of historical access a computation actually needs:

- exact item lookup;
- associative lookup;
- local continuity;
- aggregate/statistical state;
- ordered state tracking;
- episodic retrieval;
- writable associative memory.

Using one mechanism for all six is not justified by current evidence.

### State size is not enough

Two mechanisms with identical state size can differ sharply in what they can remember because update algebra matters. Forget, erase, write, normalization and addressing rules determine interference and effective capacity.

### Training form and inference form may differ

RetNet, RWKV, Mamba-style systems and related linear mechanisms show that an operator can admit a parallel/chunked training formulation and a recurrent inference formulation. Therefore, sequential state need not imply fully sequential training.

## Clean-sheet restatement

Design a family of memory-access operations whose cost grows with **needed access**, not automatically with all available history. Preserve directly addressable detail only where its expected future value exceeds the cost of retaining and moving it; summarize the rest into state whose update rule is explicitly designed for interference, overwrite and uncertainty.

## Open questions

- What minimal directly addressable memory is needed to complement bounded learned state?
- Can a learned controller dynamically choose between local state update, compressed global state and exact retrieval?
- How should memory capacity be measured: bytes, rank, associative slots, mutual information, retrievable distinctions, or downstream task value?
- How should state expose uncertainty about what it has forgotten?

## Failure modes

State saturation; catastrophic overwrite; attention-cache growth; retrieval aliasing; stale state; position/content entanglement; long-range recall that works on needles but fails on compositional state tracking.