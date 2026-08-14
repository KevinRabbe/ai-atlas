# Adaptation Substrates

## Required function

Place newly acquired information in a substrate whose capacity, speed, persistence, reversibility and interference profile match the information's expected future use.

## Candidate substrate classes

| Substrate | Typical update speed | Persistence | Main advantage | Main risk |
|---|---:|---:|---|---|
| transient activations/context | immediate | very short | zero durable mutation | context/state capacity and loss at reset |
| recurrent/test-time state | per observation/step | session/stream | fast online adaptation | drift/interference in mutable state |
| external episodic/semantic memory | fast | configurable | editable/provenanced/capacity-flexible | retrieval cost and stale/incorrect entries |
| parameter-efficient delta/adapter | moderate | durable/reversible | isolates changes cheaply | composition/routing conflicts |
| full model weights | slow/expensive | durable | deeply integrated/amortized behavior | interference, hard rollback/provenance |
| skills/programs/routing policies | event-driven | durable | executable/composable specialization | interface and verification burden |
| architecture/regulatory state | rare | very durable | changes future learning/computation | broad regressions/high validation cost |

## Evidence

- **L-S007 — MAML:** parameters can be optimized not just for immediate task performance but for *ease of later adaptation* with a few gradient steps.
- **L-S008 — test-time training:** model parameters can be updated on unlabeled test examples using a self-supervised objective to adapt under distribution shift.
- **L-S009 — TTT layers:** the hidden state itself can be a learned model updated by self-supervised learning during sequence processing, blurring “state” and “weights.”
- **L-S010 — Titans:** a learned memory module can be updated at test time and used alongside short-term context mechanisms.
- **L-S011 — LoRA:** useful task adaptation can often be represented in a low-rank trainable parameter delta while base weights remain frozen, demonstrating that full-weight mutation is not always necessary.
- **L-S019 — meta-trained in-context learners:** adaptation can occur entirely inside accessible runtime state without explicit outer-model parameter updates.

## Key deduction

There is no binary distinction between “context” and “training.” Adaptation forms a continuum of mutable state with different lifetimes and integration costs.

A useful clean-sheet abstraction is:

`new evidence -> estimate value/uncertainty/expected lifetime -> choose mutable substrate -> validate -> possibly consolidate/migrate`

## When durable weights appear attractive

- information is repeatedly useful across many future contexts;
- inference-time retrieval/computation would be repeatedly expensive;
- evidence is stable and sufficiently validated;
- integration with many existing features is valuable;
- rollback/provenance requirements are acceptable.

## When fast/external state appears attractive

- information is recent, volatile or user/session-specific;
- confidence is low or evidence is sparse;
- provenance/editability matters;
- usage is rare enough that amortizing into weights is wasteful;
- interference risk from permanent updates is high.

## What is not established

No universal threshold determines when information should move between substrates. Current systems usually hard-code these boundaries. Learning the migration policy itself is an open research direction.

## Failure modes

Premature consolidation; durable memorization of transient noise; adapter proliferation; stale fast state; retrieval failure; weight interference; hidden unprovenanced adaptations; high-frequency test-time updates causing drift.