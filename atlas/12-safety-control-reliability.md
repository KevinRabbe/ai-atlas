# Safety, Control & Reliability

## Required function

Keep system behavior and state transitions within intended constraints under uncertainty, adversarial input, distribution shift, tool use, long horizons and self-improvement.

## Status

**First coupled verification/reliability/control evidence pass completed on 2026-08-14; not saturated.**

Detailed notes live under [`verification-reliability-control/`](verification-reliability-control/INDEX.md).

## First-pass findings

1. **Capability != authority.** Powerful components can remain externally permission-limited.
2. **Instructions and data require explicit provenance/authority.** Untrusted content should not gain command authority because it contains imperative text or persists in memory.
3. **Least privilege reduces dependence on model obedience.** Read/write/execute scope, resource limits and duration should match the task.
4. **High-consequence actions benefit from staged execution.** Propose, check, sandbox/preview, authorize, execute and verify effects can be separated when stakes justify it.
5. **Proxy/evaluator optimization can become unsafe.** Stronger optimization pressure can exploit omissions and even incentivize reward/evaluator tampering.
6. **Defense in depth should use heterogeneous barriers.** Permissions, formal/precondition checks, monitors, independent verification, audit and rollback catch different failures.
7. **Self-modification needs transactional gates.** Durable changes should be versioned, regression-tested, activated atomically and rollback-capable.
8. **Interpretability is not a safety proof.** Internal monitoring is one evidence channel among several.
9. **Assurance should scale with scope, persistence, privilege, irreversibility, uncertainty and consequence.**

## Mechanism families to map

Preference/constitutional training; uncertainty calibration; selective prediction; capability and permission boundaries; sandboxing; reversible actions; human/external approval gates; monitoring; anomaly detection; interpretability; provenance; policy enforcement; adversarial robustness; scalable oversight; AI-control protocols; shutdown/rollback; audit logs; containment; hidden/rotating regression suites.

## Clean-sheet questions

- Which safety/control invariants must live outside self-modifiable components?
- What actions must remain reversible or require independent authorization?
- How should uncertainty and evaluator quality affect permission to act?
- How can self-improvement be activated and rolled back atomically?
- How do we detect evaluator manipulation, memory poisoning or reward tampering?
- What provenance/authority metadata must survive memory/context transformations?
- Which controls should be deterministic runtime constraints versus learned policies?
- How should hidden/adversarial tests remain outside the optimizer's direct target?

## Anti-assumptions

Do not assume safety can be solved entirely in model weights, that refusal behavior equals capability control, that a sandbox alone is sufficient, or that passing a fixed regression suite proves a self-change safe.
