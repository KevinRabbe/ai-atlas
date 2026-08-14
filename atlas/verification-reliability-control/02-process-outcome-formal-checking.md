# Process, Outcome and Formal Checking

## Required function

Check either the final result, intermediate state transitions, or a formally specified property at the granularity where errors can be detected and corrected economically.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-PO-01 | Outcome verifiers can rank generated solutions and improve final accuracy without supervising every intermediate step. | O | E4 | V-S001 |
| V-PO-02 | On the studied MATH setting, process supervision using step-level human labels substantially outperformed outcome supervision. | O | E3 | V-S002 |
| V-PO-03 | Deterministic/verifiable intermediate checks can provide dense credit and improve structured multi-step reasoning/agent tasks when suitable process oracles exist. | O | E2 | V-S003, V-S005 |
| V-PO-04 | Formal proof assistants provide machine-checkable acceptance of proofs relative to a formal statement and trusted kernel/rules. | O | E5 | V-S006, V-S007 |

## Outcome checks

Advantages:

- cheaper annotation/evaluation;
- representation-agnostic;
- do not require prescribing a reasoning path;
- suitable when the result is objectively checkable.

Limitations:

- poor error localization;
- sparse credit over long horizons;
- a correct final result can be reached through fragile or invalid intermediate assumptions;
- many real actions have irreversible intermediate effects even if final state appears acceptable.

## Process checks

Advantages:

- localize failure;
- support early pruning/recovery;
- produce denser learning/search signals;
- can enforce intermediate safety invariants.

Limitations:

- can reward a human-preferred representation rather than the best machine computation;
- expensive if every internal transition is checked;
- incomplete process specifications can themselves be gamed;
- forcing text-visible reasoning is not required for process verification.

A machine-native process checker can target structured state transitions, executable invariants, tool pre/postconditions or proof obligations without requiring prose.

## Formal verification

Formal methods can provide unusually strong evidence because a small trusted checker determines whether a candidate satisfies a formal specification/proof system. Neural theorem provers demonstrate that powerful generators can search while the proof assistant remains the acceptance authority.

But the guarantee is always relative to:

`formal statement + axioms/specification + trusted checker + modeled environment assumptions`.

Formal verification cannot establish whether the specification captured an unstated human objective.

## Clean-sheet hierarchy

Verification strength roughly increases when the checked property becomes more explicit and mechanically decidable:

`subjective judgment -> learned evaluator -> executable tests/simulation -> deterministic invariants -> formal proof`

This is not a universal quality ranking: a formally proved irrelevant specification is less useful than a well-designed empirical check of the actual objective.

## Failure modes

Lucky final answer accepted despite broken process; process supervision forcing brittle conventions; overchecking every step and destroying efficiency; incomplete test suite; formalization error; verified code/spec mismatch; proof checker trusted beyond assumptions; local invariants satisfied while global objective fails.
