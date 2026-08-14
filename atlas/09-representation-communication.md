# Representation & Communication

## Required function

Encode and exchange information so learning, reasoning, memory, coordination and action preserve the distinctions that matter while minimizing unnecessary serialization, compute and bandwidth.

## Status

**Focused gap-closure evidence pass completed on 2026-08-14; not saturated.**

Detailed notes live under [`representation-communication/`](representation-communication/INDEX.md).

## First-pass findings

1. **Natural language is useful but not proven necessary internally.** Continuous latent reasoning and learned communication protocols can support useful computation without decoding every intermediate state to text.
2. **Representation quality is interface-relative.** The correct form depends on what the receiver/next operation needs, required exactness, uncertainty/provenance and bandwidth.
3. **Discrete and continuous representations are both viable.** Each exposes different compression, stability, auditability and information-loss trade-offs.
4. **Granularity can be adaptive.** Fixed linguistic token boundaries are not a fundamental requirement; compute/representation units can vary with local information complexity.
5. **Communication itself should be selective.** Whether, what, when and how much to send are resource-allocation decisions.
6. **Latent channels create compatibility/versioning problems.** Efficient direct state sharing becomes tightly coupled to sender/receiver representation unless explicit alignment/interface contracts exist.
7. **Machine compute channels and human audit channels can differ.** Human readability need not constrain all internal bandwidth, but audit summaries must not be mistaken for complete causal traces.
8. **Authority/provenance is orthogonal to payload representation.** Text, symbols and latent vectors remain data unless external authority semantics grant otherwise.

## Representation families to continue mapping

Natural-language/discrete symbols; continuous latent state; adaptive byte/patch units; learned inter-agent protocols; graphs; programs/IRs; constraint/proof state; structured tensors; multimodal shared/local representations; hybrid continuous-discrete messages.

## Clean-sheet questions

- Which boundaries require stable cross-version interfaces versus tightly coupled latent sharing?
- How much human-readable audit evidence is necessary without forcing all computation through language?
- Can structured/executable internal states outperform both text and opaque latent states on compositional/verifiable tasks?
- How should protocol compatibility be preserved during self-improvement?
- What representation granularity should vary with uncertainty, exactness requirements and hardware locality?
- How should trust/authority metadata survive translation between representations?

## Anti-assumptions

Do not choose English, tokens, embeddings, graphs or latent tensors as a universal thought language. Define the information contract first, then choose or learn the representation that best satisfies it.
