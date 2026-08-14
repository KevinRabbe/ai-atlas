# Representation & Machine Communication — Focused Gap Closure

**Status:** focused evidence pass in progress.

This pass closes a Phase-7 gap: what representations should internal reasoning, inter-component communication and human I/O use when natural language and fixed tokenization are no longer assumed.

## Research decomposition

1. [`01-machine-native-reasoning-state.md`](01-machine-native-reasoning-state.md) — latent, structured and language-mediated intermediate computation.
2. [`02-learned-inter-agent-communication.md`](02-learned-inter-agent-communication.md) — learned continuous/discrete protocols and emergent messages.
3. [`03-symbol-granularity-and-tokenization.md`](03-symbol-granularity-and-tokenization.md) — bytes, patches, tokens and adaptive computation granularity.
4. [`04-bandwidth-alignment-and-interfaces.md`](04-bandwidth-alignment-and-interfaces.md) — what to send, compression, sender/receiver alignment and inspectability.
5. [`PROVISIONAL_SYNTHESIS.md`](PROVISIONAL_SYNTHESIS.md) — implementation-neutral deductions.

## Evaluation axes

- information retained across the interface;
- downstream task utility;
- communication bytes/tokens/latency;
- ambiguity and error correction;
- compositionality/systematic transfer;
- cross-model/architecture compatibility;
- inspectability/auditability;
- learnability and stability of the protocol;
- adversarial/security properties;
- robustness to bandwidth constraints;
- hardware/memory locality.

## Anti-assumption

Do not assume human language, fixed discrete tokens, raw hidden-state transfer, one shared latent space or one message granularity is universally optimal. Representation is an interface contract between computations and should be evaluated by future-useful information and realized cost.
