# Neuromodulation, Eligibility and Delayed Credit

## Required function

Assign delayed outcome information to earlier local events without preserving the complete global computation graph.

## Evidence

- **B-S009 — Schultz, Dayan & Montague (1997)** and **B-S010 — Hollerman & Schultz (1998):** dopaminergic activity in primates exhibits reward-prediction-error-like signals and changes as reward timing/predictability is learned.
- **B-S011 — Yagishita et al. (2014):** dopamine promoted structural spine plasticity only within a narrow delay after glutamatergic activity, demonstrating a local biochemical eligibility window.
- **B-S012 — Reynolds et al. (2017):** in vivo corticostriatal plasticity required reinforcement within a limited interval after spike-timing pairings, consistent with an eligibility trace modulated by later reinforcement.

## Computational abstraction

A useful factorization is:

`local event -> temporary eligibility state -> delayed modulatory/evaluation signal -> durable update`

This bridges fast local activity and slower outcome feedback. The temporary trace preserves *where credit might belong* without immediately committing the parameter change.

## Why this matters to the Atlas

This is an experimentally grounded example of credit crossing a nondifferentiable time gap through **state + delayed global modulation**, reinforcing Foundations claim C-020 that backpropagation is not the only possible credit mechanism.

## What is not established

- that a single scalar reward/modulator is sufficient for general intelligence;
- that dopamine is only a reward-prediction-error channel;
- that three-factor local rules can train large general-purpose models competitively;
- that biological delay constants are relevant to artificial systems.

## Clean-sheet question

Can an artificial learner maintain cheap local eligibility summaries and apply richer delayed evaluator signals only to eligible state, reducing global credit/memory cost?