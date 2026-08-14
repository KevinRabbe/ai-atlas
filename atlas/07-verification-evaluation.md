# Verification & Evaluation

## Required function

Produce scoped evidence about whether outputs, intermediate states, plans and state transitions satisfy the properties that matter strongly enough to guide selection, search, learning or authorization.

## Status

**First coupled verification/reliability/control evidence pass completed on 2026-08-14; not saturated.**

Detailed notes live under [`verification-reliability-control/`](verification-reliability-control/INDEX.md).

## First-pass findings

1. **Verification is property-specific.** A checker establishes only the property it actually tests under its assumptions.
2. **Evaluator strength changes search economics.** Reliable verification supports stronger search; exploitable proxies become less trustworthy as optimization pressure rises.
3. **Outcome and process checks are complementary.** Outcome checks are cheap/representation-agnostic; process checks localize failures when intermediate properties are verifiable.
4. **Formal proof is specification-relative.** Mechanically checked guarantees are unusually strong for explicit formal properties but do not prove that the specification captured unstated intent.
5. **Evaluator independence matters.** Correlated judges can agree confidently on the same error.
6. **Calibration must alter behavior.** Confidence is useful when it triggers verification, evidence acquisition, scope reduction, authorization or abstention.
7. **Interpretability is diagnostic evidence.** Internal features/monitors can reveal useful signals but do not constitute proof of correctness or safety.
8. **Reliability belongs to state transitions.** Correct answers are insufficient when memory writes, tool effects or self-modifications can be unsafe.

## Mechanism families to map

Unit/integration tests; formal proof; theorem provers; static analysis; simulators; reward/evaluator models; process/outcome supervision; deterministic process oracles; cross-model critique; calibration; selective prediction; adversarial testing; red teaming; property-based testing; human/scalable oversight; interpretability/monitoring.

## Clean-sheet questions

- Which properties of this proposed transition are objectively verifiable, and which remain judgment calls?
- What evidence is independent of the generator's likely failure modes?
- How should evaluator uncertainty and specification coverage be represented?
- How much optimization pressure can a particular evaluator safely support?
- When should process checks be added instead of relying on outcomes?
- Which properties can be formalized without throwing away the actual human objective?
- What assurance level should be required before persistent/privileged/irreversible changes?

## Anti-assumptions

Do not assume an LLM judge is ground truth, majority agreement is independence, process supervision is always superior, or formal verification proves the intended real-world objective. Treat every verification result as scoped evidence.
