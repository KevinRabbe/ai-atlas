# Learning Timescales and Information Migration

## Required function

Decide not merely **whether to learn**, but how long a change should persist and whether it should migrate to a different representation after accumulating evidence.

## Proposed substrate ladder

This is a synthesis scaffold, not an architecture decision:

1. **working state** — seconds/steps; cheap and disposable;
2. **episode/session state** — minutes/hours; local adaptation with easy reset;
3. **episodic/external memory** — durable but explicit/editable;
4. **procedure/skill/adapter** — reusable behavior isolated from core state;
5. **shared weights** — highly amortized integrated knowledge;
6. **routing/meta-policy** — changes how future computation/learning is allocated;
7. **architecture/developmental program** — rare changes with system-wide consequences.

## Evidence joining the Atlas

- MAML shows parameters can be optimized for later change rather than static performance alone.
- Test-time training and TTT layers show useful updates can occur during deployment/sequence processing.
- LoRA shows durable adaptation can be isolated into a small parameter subspace.
- EWC/replay results show shared durable updates can interfere with older knowledge.
- Distillation shows repeated expensive competence can be amortized into cheaper learned form.
- Biological eligibility/tagging/replay provides an independent example of tentative changes preceding stabilization.

## Migration decision variables

For an item of newly acquired information, estimate:

- **confidence** — how likely is it true/useful?
- **scope** — one episode, user, task, domain, or broadly general?
- **volatility** — how quickly might it become false?
- **frequency** — how often will it be needed?
- **integration value** — does it need interaction with many existing features?
- **retrieval cost** — cost if left external/explicit;
- **interference risk** — what old competence could durable integration damage?
- **provenance need** — must it be inspectable/removable?
- **compression opportunity** — can many experiences be summarized into a reusable rule?
- **validation coverage** — can regression/evaluator checks detect damage?

## Provisional migration logic

`new observation`

`-> fast state if immediately useful`

`-> explicit memory if potentially reusable but uncertain/volatile`

`-> skill/adapter if repeated in a bounded domain`

`-> shared weights if broadly reusable, stable, repeatedly expensive to retrieve/compute, and sufficiently validated`

`-> routing/meta-policy if the lesson is about how to allocate future learning/compute`

`-> architecture only after broad repeated evidence and regression tests`

## Demotion/forgetting matters too

Migration must be reversible where possible. Knowledge can move *out* of weights or skills conceptually when it becomes stale, dangerous or overly specific. Current neural systems make this difficult; explicit memories/adapters are easier to remove.

## Core research hypothesis

**The optimal learning system is multi-timescale and substrate-selective.** It learns both task content and the policy governing where/how long that content should persist.

Evidence supports every ingredient separately; the full unified policy is not yet established.