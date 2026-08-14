# Claims Ledger

This file tracks cross-domain claims that may affect architecture. Detailed evidence belongs in atlas notes.

| Claim ID | Claim | Type | Strength | Status | Needed evidence |
|---|---|---|---|---|---|
| C-001 | Larger parametric models are not the only way to increase effective system capability. | I | E3 | active | broader controlled comparisons of model-vs-system scaling |
| C-002 | Conditional computation can increase model capacity without proportional active compute. | O | E4 | active | end-to-end communication/energy comparisons across routing regimes |
| C-003 | External non-parametric state can improve access to knowledge beyond parametric memory alone. | O | E4 | active | characterize optimal division between stores |
| C-004 | Inference-time search/sampling can trade additional compute for higher task performance. | O | E4 | active | task-conditional scaling laws and stopping policies |
| C-005 | Agent/harness interface design can materially change capability while holding backbone weights fixed. | O | E3 | active | independent replications across environments |
| C-006 | Recursion is useful only when its decomposition benefit exceeds coordination/context cost. | H | E2 | active | controlled depth/branching studies |
| C-007 | Automated evaluators enable stronger iterative search where objective feedback is reliable. | I | E4 | active | map evaluator failure regimes |
| C-008 | Some improvements should be stored as memory, skills or harness policy rather than weight updates. | H | E2 | active | head-to-head retention/generalization/cost studies |
| C-009 | Human natural language is not proven to be an optimal internal communication representation for machine reasoning. | O | E1 | active | latent/structured communication comparisons |
| C-010 | Assumption-free superiority of one learner over all problem distributions is unavailable; practical generalization exploits structure/inductive bias. | I | E5 | active | characterize adaptive bias acquisition rather than existence |
| C-011 | Expressive capacity alone does not establish learnability, generalization or computational efficiency. | I | E5 | active | map practical capacity metrics across architectures |
| C-012 | Optimization/search procedure can select among otherwise fitting solutions and therefore acts as part of the inductive bias. | O | E4 | active | extend controlled comparisons beyond studied model classes |
| C-013 | Parameter count and training interpolation alone do not determine generalization; interpolating/overparameterized solutions can generalize in important regimes. | O | E4 | active | moderators under distribution shift and structured tasks |
| C-014 | Compression is useful only relative to a fidelity/relevance criterion; generic representation compression is not established as a universal cause of generalization. | I | E4 | active | causal interventions on retained information under fixed fit/compute |
| C-015 | Formal universal induction/control can be theoretically powerful while uncomputable or prohibitively expensive; practical intelligence must trade ideality against finite resources. | I | E4 | active | practical universal-search approximation comparisons |
| C-016 | Useful uncertainty should be externally testable through calibration/proper scoring and should affect decisions about action or information acquisition. | I | E4 | active | high-dimensional structured-output and distribution-shift studies |
| C-017 | Passive observational prediction does not by itself identify intervention effects without additional causal assumptions or interaction. | O | E5 | active | map what inductive biases/experiments minimize interaction cost |
| C-018 | Sequential learning under uncertainty contains an exploration–exploitation trade-off; information acquisition can have decision value and cost. | O | E5 | active | bounded/safe exploration in rich environments |
| C-019 | Compute-optimal learning depends on joint allocation across data, capacity and compute and shifts by regime; empirical scaling laws are not universal constants. | I | E4 | active | system-level scaling including memory, tools, retrieval and inference compute |
| C-020 | Differentiability is not necessary for credit assignment; alternative estimators/bootstrapping mechanisms have different information, variance and memory requirements. | I | E5 | active | hybrid credit across neural/tool/program boundaries |
| C-021 | Directly addressable history and bounded recurrent state have different capability/cost profiles; neither is established as universally dominant. | I | E4 | active | matched large-scale studies across recall, state tracking and generalization |
| C-022 | Parallel training and recurrent inference can be two execution forms of the same learned sequence operator. | O | E4 | active | broader operator/hardware replication |
| C-023 | Realized cost cannot be inferred from FLOPs/asymptotic complexity alone; memory traffic, utilization and synchronization can dominate. | O | E5 | active | standardized multi-hardware cost reporting |
| C-024 | Persistent inference state representation can materially determine memory bandwidth, feasible context/batch size and throughput. | O | E4 | active | state-quality trade-offs beyond language decoding |
| C-025 | Conditional computation introduces routing, load-balance and communication costs that can offset sparse arithmetic savings. | O | E4 | active | topology-aware end-to-end energy/latency studies |
| C-026 | Numerical sensitivity is non-uniform; precision can often be reduced selectively without proportional capability loss. | O | E4 | active | recurrent/persistent-state and safety-critical precision studies |
| C-027 | Functional heterogeneity can outperform homogeneous computation in some matched regimes, but its advantage is workload and systems dependent. | I | E3 | active | fixed-budget ablations across hardware/task regimes |
| C-028 | Architecture and hardware are coupled through locality, dataflow and communication, while specific accelerator details remain transient constraints. | I | E5 | active | alternative-hardware comparisons using equivalent functional workloads |
| C-029 | Biological synaptic plasticity is local but strongly context dependent; timing, cell type, state and location can alter update direction/magnitude. | O | E4 | active | systematic cross-circuit mapping; artificial matched-rule tests |
| C-030 | Temporary local eligibility state can bridge delayed outcome feedback and later durable updates. | O | E3 | active | artificial scaling studies vs full backprop/trajectory retention |
| C-031 | Learning-related plasticity and homeostatic stability regulation can be separate coupled processes. | O | E4 | active | continual-learning ablations with independent stabilizers |
| C-032 | Biological memory uses multiple plasticity/consolidation timescales rather than one permanent update timescale. | O | E4 | active | map when artificial multi-timescale stores improve retention/adaptation |
| C-033 | Dendritic compartments can perform nonlinear local computation before global neuronal output. | O | E4 | active | matched artificial locality/communication experiments |
| C-034 | Neural signaling has substantial energy cost, making activity level, locality and communication relevant computational constraints. | O | E4 | active | compare event-driven/dense artificial regimes on matched hardware |
| C-035 | Complex neural structure can be produced by developmental regulatory programs and local interactions rather than explicit connection-by-connection genomic specification. | I | E5 | active | quantify indirect encoding/evolvability benefits in artificial systems |
| C-036 | Human/mammalian brain evolution includes substantial regulatory/developmental changes that reuse conserved machinery rather than only introducing new primitives. | O | E4 | active | stronger causal links from regulatory changes to circuit/computation phenotypes |

Rules: every claim must remain falsifiable; confidence changes only when evidence changes; contradictions are linked rather than hidden.