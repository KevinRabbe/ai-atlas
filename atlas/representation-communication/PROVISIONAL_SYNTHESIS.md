# Representation & Machine Communication — Provisional Synthesis

**Status: focused gap-closure synthesis, not architecture.**

## P-R01 — Natural language is a valuable interface, not an established universal internal substrate

Language provides semantic pretraining, interoperability and inspectability, but latent reasoning and learned communication show that useful computation/communication can occur without decoding every intermediate state into words.

**Confidence:** high for non-necessity; optimal alternatives remain open.

## P-R02 — Representation quality is interface-relative

The best representation depends on what the receiver/next operation must do, what information must remain exact, what uncertainty/provenance must survive, and what bandwidth/latency is available.

**Confidence:** very high.

## P-R03 — Discreteness and continuity are both useful tools

Learned systems can communicate with continuous latent vectors or emergent discrete symbols. Discrete boundaries aid compression, identity, logging and robust interchange; continuous state can preserve richer information and avoid premature quantization.

**Confidence:** high that both are viable; task-dependent frontier unresolved.

## P-R04 — Representation granularity can be adaptive

Byte-level adaptive patching and bandwidth-aware communication support allocating finer representation/compute to locally difficult or important information rather than using one fixed token/message unit everywhere.

**Confidence:** medium-high.

## P-R05 — Communication is information allocation

A sender should decide whether to communicate, what subset/delta to send, at what fidelity, to whom and when. Always broadcasting full state is not a neutral baseline under physical cost.

**Confidence:** high.

## P-R06 — Latent communication creates a compatibility problem

Raw hidden state is tied to model architecture, layer and training history. Direct latent channels can be efficient among tightly coupled components but require alignment/versioning/adapters when components differ or self-improve.

**Confidence:** high conceptually; engineering frontier immature.

## P-R07 — Machine channel and audit channel may differ

The representation best for machine computation need not be human-readable. A separate structured provenance/audit channel can expose decisions, evidence and uncertainty without forcing all internal state through natural language.

**Confidence:** medium-high.

## P-R08 — Authority/provenance must survive representation conversion

Text, latent vectors, structured messages and memory entries are data formats; none gains instruction authority merely from representation. Trust metadata should remain orthogonal to payload encoding.

**Confidence:** high.

## P-R09 — Stable interface semantics may matter more than stable internal representation

Self-improving components can change their internal spaces while maintaining typed, versioned interface contracts. This can preserve modularity without freezing internal representation development.

**Confidence:** medium-high.

---

## Clean-sheet implication

Do not choose “English,” “tokens,” “embeddings,” or “graphs” as the universal thought language. Define the information contract first:

`what must be preserved -> who/what consumes it -> required fidelity/uncertainty/provenance -> bandwidth/latency -> choose/learn representation`.

This suggests a heterogeneous representation hierarchy may be more plausible than one universal format, but that remains an architecture hypothesis.

## Strong anti-conclusions

This pass does **not** justify:

- “latent thought is always better than text”;
- “continuous communication is lossless in practice”;
- “fixed tokenization is obsolete for every workload”;
- “every module should share one latent space”;
- “machine-native communication removes security problems”;
- “human-readable summaries faithfully expose every internal computation.”

## Most valuable experiments

1. Equal-compute comparison of language, latent, structured/executable and hybrid reasoning state on backtracking/compositional tasks.
2. Train agents with constrained communication budgets and measure what information they learn to transmit versus full-state baselines.
3. Update one sender/receiver model and measure protocol breakage for latent versus structured/versioned interfaces.
4. Compare fixed token/unit granularity with uncertainty/information-adaptive granularity under matched hardware cost.
5. Use a high-bandwidth latent compute channel plus a separate audit channel and measure whether audit evidence remains causally faithful enough for verification.
