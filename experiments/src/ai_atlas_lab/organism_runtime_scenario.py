from __future__ import annotations

from dataclasses import dataclass
import random
import statistics

from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class I10ScenarioConfig:
    seed: int = 0
    steps: int = 900
    regime_duration: int = 150
    decision_interval: int = 15
    evidence_decay: float = 0.94
    coupling_threshold: float = 0.32


def _components(
    nodes: int,
    evidence: dict[tuple[int, int], float],
    threshold: float,
) -> tuple[int, ...]:
    adjacency: list[list[int]] = [[] for _ in range(nodes)]
    for (left, right), value in evidence.items():
        if value >= threshold:
            adjacency[left].append(right)
            adjacency[right].append(left)

    labels = [-1] * nodes
    group = 0
    for start in range(nodes):
        if labels[start] >= 0:
            continue
        labels[start] = group
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in adjacency[node]:
                if labels[neighbor] < 0:
                    labels[neighbor] = group
                    stack.append(neighbor)
        group += 1
    return tuple(labels)


def _changed_pairs(
    old: tuple[int, ...],
    new: tuple[int, ...],
) -> list[tuple[int, int]]:
    return [
        (left, right)
        for left in range(len(old))
        for right in range(left + 1, len(old))
        if (old[left] == old[right]) != (new[left] == new[right])
    ]


def run_i10_scenario(config: I10ScenarioConfig) -> dict[str, float | int | bool]:
    rng = random.Random(config.seed)
    nodes = 6
    runtime = TypedScopeRuntime(
        range(nodes),
        structural_assurance_threshold=6.0,
    )

    for node in range(nodes):
        runtime.attach_evidence(node, f"source:{node}:bootstrap")
        runtime.register_predictive_state(
            node,
            f"latent:{node}",
            f"raw:{node}",
        )
    runtime.lease_resource("verify", 0)
    runtime.lease_resource("compute", 1)

    regimes = (
        (0, 0, 0, 1, 1, 1),
        (0, 0, 1, 1, 2, 2),
        (0, 1, 0, 1, 0, 1),
    )
    coupling_evidence = {
        (left, right): 0.10
        for left in range(nodes)
        for right in range(left + 1, nodes)
    }

    utility = 0.0
    topology_proposals = 0
    approved_changes = 0
    rejected_changes = 0
    rematerializations = 0
    bundle_values: list[float] = []

    for step in range(config.steps):
        true_partition = regimes[(step // config.regime_duration) % len(regimes)]

        for edge in coupling_evidence:
            left, right = edge
            probability = 0.68 if true_partition[left] == true_partition[right] else 0.04
            observed = rng.random() < probability
            coupling_evidence[edge] = (
                config.evidence_decay * coupling_evidence[edge]
                + (1.0 - config.evidence_decay) * float(observed)
            )

        # Authority changes while external work can remain queued.
        if step % 137 == 40:
            node = (step // 137) % nodes
            runtime.set_authority(node, False)
            runtime.enqueue_event(node, due_step=step + 25, external=True)
        if step % 137 == 90:
            node = (step // 137) % nodes
            runtime.set_authority(node, True)

        if rng.random() < 0.12:
            runtime.enqueue_event(
                rng.randrange(nodes),
                due_step=step + rng.randint(2, 9),
                external=False,
            )

        if step % config.decision_interval == 0:
            candidate = _components(
                nodes,
                coupling_evidence,
                config.coupling_threshold,
            )
            if candidate != runtime.topology_labels:
                change = runtime.stage_scope_change(candidate, consequence=1.5)
                topology_proposals += 1
                changed = _changed_pairs(runtime.topology_labels, candidate)

                agreements = 0
                for left, right in changed:
                    positives = sum(
                        rng.random()
                        < (
                            0.82
                            if true_partition[left] == true_partition[right]
                            else 0.02
                        )
                        for _ in range(5)
                    )
                    independently_same = positives >= 2
                    agreements += int(
                        independently_same == (candidate[left] == candidate[right])
                    )
                approved = not changed or agreements / len(changed) >= 0.70

                if change.requires_assurance:
                    token = runtime.request_assurance(
                        change.proposal_id,
                        independent=True,
                        approved=approved,
                        evidence_ref=f"topology-audit:{step}",
                    )
                    if approved:
                        runtime.commit_scope_change(
                            change.change_id,
                            assurance_token_id=token.token_id,
                        )
                        approved_changes += 1
                    else:
                        runtime.rollback_scope_change(change.change_id)
                        rejected_changes += 1
                elif approved:
                    runtime.commit_scope_change(change.change_id)
                    approved_changes += 1
                else:
                    runtime.rollback_scope_change(change.change_id)
                    rejected_changes += 1

        # Small interaction-aware runtime decision through the common allocator.
        node = rng.randrange(nodes)
        think = runtime.propose_transition(
            "think",
            target_id=node,
            expected_value=1.4,
            cost=0.25,
            uncertainty=0.20,
            consequence=0.5,
            reversible=True,
        )
        observe = runtime.propose_transition(
            "observe",
            target_id=node,
            expected_value=1.2,
            cost=0.25,
            uncertainty=0.15,
            consequence=0.5,
            reversible=True,
        )
        high_fidelity = runtime.propose_transition(
            "high-fidelity",
            target_id=node,
            expected_value=2.6,
            cost=0.55,
            uncertainty=0.05,
            consequence=0.5,
            reversible=True,
            resource_units=2,
        )
        allocation = runtime.allocate_bundle(
            (think, observe, high_fidelity),
            capacity=2,
            interactions={
                frozenset((think.proposal_id, observe.proposal_id)): 0.45,
            },
        )
        bundle_values.append(allocation.net_value)
        for proposal_id in allocation.proposal_ids:
            runtime.execute_transition(proposal_id)
            utility += runtime.proposals[proposal_id].net_value

        if rng.random() < 0.04:
            runtime.rematerialize(rng.randrange(nodes))
            rematerializations += 1

        runtime.process_due_events(step)

    runtime.process_due_events(config.steps + 100)
    processed_events = sum(event.processed for event in runtime.events.values())
    invariant_values = runtime.semantic_invariants()

    return {
        "utility_per_step": utility / config.steps,
        "topology_epochs": runtime.topology_epoch,
        "topology_proposals": topology_proposals,
        "approved_changes": approved_changes,
        "rejected_changes": rejected_changes,
        "forwarded_events": runtime.forwarded_events,
        "blocked_external_events": runtime.blocked_external_events,
        "queued_events": len(runtime.events),
        "processed_events": processed_events,
        "rematerializations": rematerializations,
        "mean_bundle_value": statistics.mean(bundle_values),
        "all_semantic_invariants": all(invariant_values.values()),
        "resource_leases_singular": len(runtime.leases) == 2,
    }
