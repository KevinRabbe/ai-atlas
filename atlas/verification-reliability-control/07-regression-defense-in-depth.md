# Regression Gates and Defense in Depth

## Required function

Prevent local improvements or self-modifications from silently degrading other capabilities, bypassing controls or creating irreversible failure before problems can be detected and rolled back.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-RD-01 | Self-modifying harness work can improve performance when proposed changes are subjected to regression testing rather than accepted directly. | O | E3 | earlier Self-Harness evidence |
| V-RD-02 | Static defenses against adaptive agent attacks are incomplete; security evaluation benefits from environments where attacks and defenses can co-evolve. | O | E3 | V-S020, V-S021 |
| V-RD-03 | Control protocols combining multiple checks can outperform simple trust/no-trust baselines against an intentionally subversive model. | O | E3 | V-S023 |
| V-RD-04 | Adversarial training/testing can improve robustness in studied settings but does not establish universal robustness outside the attack distribution. | O/I | E4 | V-S019, V-S004 |

## Durable change needs stronger gates

A temporary low-scope action and a permanent architecture/weight change should not require the same evidence.

A useful risk surface is approximately:

`required assurance increases with scope × persistence × privilege × irreversibility × uncertainty`.

Examples:

- transient reasoning state: cheap local checks;
- memory write: provenance + consistency checks;
- reusable skill/harness change: regression suite + sandbox;
- shared-weight update: broad hidden capability tests + rollback artifact;
- architecture/control-policy change: adversarial validation and independent authorization.

## Defense in depth

No single mechanism should carry the full safety argument. Layers can include:

1. capability/permission restriction;
2. input provenance and trust labeling;
3. precondition/invariant checking;
4. sandbox/preview;
5. independent evaluator(s);
6. effect-level verification;
7. audit trail;
8. rollback/recovery;
9. adversarial/holdout regression testing;
10. runtime monitoring after deployment.

Failures should have to cross multiple **different** barriers, not ten copies of the same learned judge.

## Regression suites

A regression suite should include more than the metric being optimized. Important dimensions:

- previous task/capability retention;
- safety/security invariants;
- calibration;
- resource/latency behavior;
- memory/world-state integrity;
- tool permission behavior;
- adversarial hidden tests;
- distribution-shift probes;
- rare but high-consequence capabilities.

Public/fixed tests are vulnerable to overfitting during repeated self-improvement. Preserve hidden/rotating tests or independent evaluators where possible.

## Atomicity and rollback

Persistent changes should be versioned so the system can:

`stage -> test -> activate -> monitor -> rollback`.

If a change mutates its own evaluator, rollback mechanism or audit history, the trust boundary is compromised. Core recovery/control state should be independently protected.

## Clean-sheet restatement

Self-improvement and autonomous operation require **transactional trust**: proposed changes/actions remain tentative until evidence sufficient for their consequence level has been accumulated, and durable activation remains reversible where technically possible.

## Failure modes

Benchmark overfitting; regression tests updated to hide regressions; evaluator/control code modified by the candidate change; no rollback artifact; correlated defense layers; irreversible action before verification; gradual drift below alarm thresholds; hidden capability loss; adversarial behavior delayed until after acceptance.
