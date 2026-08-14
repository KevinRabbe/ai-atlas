# Reasoning, Search & Planning

## Required function

Transform a problem state into a high-quality decision or solution while allocating finite compute intelligently.

## Mechanism families to map

Direct amortized prediction; explicit intermediate reasoning; sampling and aggregation; tree/graph search; planning; program synthesis/execution; verifier-guided search; test-time compute scaling; decomposition; recursive model calls; recursive harnesses; theorem proving; hybrid neural-symbolic search.

## Early evidence anchors

Chain-of-thought shows that externalized intermediate steps can improve some complex reasoning tasks; self-consistency shows gains from sampling diverse paths; Tree of Thoughts demonstrates explicit search/backtracking; ReAct interleaves inference and environmental actions; RLM externalizes large context and recursively operates over relevant pieces; Recursive Agent Harnesses move the recursive unit from a model call to a tool-capable harness.

These results establish that **inference procedure is itself an architectural variable**. They do not establish that textual chains, trees, recursion, or any particular agent loop are universally optimal.

## Clean-sheet questions

- What should count as a reasoning state?
- Can useful deliberation occur in compact learned/structured state rather than natural language?
- How should expected value of another computation be estimated?
- What decomposition structures minimize coordination overhead?
- Which tasks benefit from recursion versus iterative/local computation?
- Can stopping and branching policies be learned independently of the task solver?

See seed sources: Wei 2022; Wang 2022; Yao 2022/2023; Zhang 2025; Lumer 2026.
