# Claims Ledger

This file tracks cross-domain claims that may affect architecture. Detailed evidence belongs in atlas notes.

| Claim ID | Claim | Type | Strength | Status | Needed evidence |
|---|---|---|---|---|---|
| C-001 | Larger parametric models are not the only way to increase effective system capability. | I | E3 | active | broader controlled comparisons of model-vs-system scaling |
| C-002 | Conditional computation can increase model capacity without proportional active compute. | O | E3 | active | broader architecture/hardware replication |
| C-003 | External non-parametric state can improve access to knowledge beyond parametric memory alone. | O | E4 | active | characterize optimal division between stores |
| C-004 | Inference-time search/sampling can trade additional compute for higher task performance. | O | E4 | active | task-conditional scaling laws and stopping policies |
| C-005 | Agent/harness interface design can materially change capability while holding backbone weights fixed. | O | E3 | active | independent replications across environments |
| C-006 | Recursion is useful only when its decomposition benefit exceeds coordination/context cost. | H | E2 | active | controlled depth/branching studies |
| C-007 | Automated evaluators enable stronger iterative search where objective feedback is reliable. | I | E4 | active | map evaluator failure regimes |
| C-008 | Some improvements should be stored as memory, skills or harness policy rather than weight updates. | H | E2 | active | head-to-head retention/generalization/cost studies |
| C-009 | Human natural language is not proven to be an optimal internal communication representation for machine reasoning. | O | E1 | active | latent/structured communication comparisons |

Rules: every claim must remain falsifiable; confidence changes only when evidence changes; contradictions are linked rather than hidden.
