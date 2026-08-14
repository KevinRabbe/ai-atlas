# Synthesis

Synthesis is where findings across atlas domains are combined. It is intentionally separate from both raw research and architecture design.

A synthesis document must:

1. cite the atlas claims/evidence it depends on;
2. distinguish observation from inference;
3. include evidence against its conclusion;
4. state the range of conditions where it is expected to hold;
5. avoid turning a successful implementation into a universal principle;
6. produce implementation-neutral requirements where possible.

Example progression:

`paper result -> mechanism evidence -> cross-domain pattern -> requirement -> clean-sheet candidate`

Not:

`paper result -> add that component to our AI`.

## Initial synthesis questions

- Which information belongs in weights, active state, persistent memory, executable skills, external knowledge, or environment state?
- When is additional model capacity better than conditional computation or external computation?
- What is the optimal unit of inference-time search: token, latent state, program, plan, model call, agent, or full harness?
- How should a system estimate expected value of more computation before spending it?
- Which functions require a learned neural substrate and which are better served by deterministic computation?
- What forms of verification are trustworthy enough to drive autonomous improvement?
- How should short-term adaptation become durable knowledge without catastrophic accumulation of errors?
