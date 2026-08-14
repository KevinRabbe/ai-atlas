from __future__ import annotations

from dataclasses import dataclass
import random
from collections import defaultdict


@dataclass(frozen=True)
class TransitionKernelConfig:
    seed: int = 0
    batches: int = 500
    tasks_per_batch: int = 12
    shared_capacity: int = 5
    verify_capacity: int = 2
    operation_cost: float = 0.06
    verify_cost: float = 0.12
    unsafe_action_penalty: float = 8.0
    false_durable_penalty: float = 10.0
    shift_batch: int = 250


@dataclass(frozen=True)
class KernelTask:
    task_id: int
    batch: int
    kind: str
    value: float
    consequence: float
    base_reliability: float
    enhanced_reliability: float
    candidate_correct: bool
    visible_approved: bool
    independent_approved: bool


@dataclass(frozen=True)
class TransitionProposal:
    task_id: int
    kind: str
    resource: str
    expected_gain: float
    cost: float
    authority: str
    reversible: bool
    requires_independent_evidence: bool = False


@dataclass(frozen=True)
class KernelVariant:
    name: str
    typed_authority: bool
    shared_allocator: bool


TYPED_SHARED = KernelVariant("typed_shared_kernel", True, True)
TYPED_SILOED = KernelVariant("typed_siloed_controllers", True, False)
FLAT_SHARED = KernelVariant("flat_scalar_kernel", False, True)


def _expected_utility(task: KernelTask, reliability: float) -> float:
    return reliability * task.value - (1.0 - reliability) * task.consequence * task.value


def _external_expected_utility(task: KernelTask, reliability: float, config: TransitionKernelConfig) -> float:
    return (
        reliability * task.value
        - (1.0 - reliability) * config.unsafe_action_penalty * task.consequence * task.value
    )


def generate_kernel_tasks(config: TransitionKernelConfig) -> list[list[KernelTask]]:
    rng = random.Random(config.seed)
    batches: list[list[KernelTask]] = []
    task_id = 0
    for batch_index in range(config.batches):
        if batch_index < config.shift_batch:
            mix = (("think", 0.40), ("observe", 0.25), ("external", 0.20), ("research", 0.15))
        else:
            mix = (("think", 0.15), ("observe", 0.15), ("external", 0.35), ("research", 0.35))

        cumulative: list[tuple[str, float]] = []
        running = 0.0
        for kind, probability in mix:
            running += probability
            cumulative.append((kind, running))

        batch: list[KernelTask] = []
        for _ in range(config.tasks_per_batch):
            draw = rng.random()
            kind = next(kind for kind, boundary in cumulative if draw <= boundary)
            value = rng.choice((1.0, 2.0, 4.0))
            consequence = rng.choice((1.0, 2.0, 4.0))
            base = rng.uniform(0.55, 0.78)
            enhanced = min(0.97, base + rng.uniform(0.12, 0.28))
            candidate_correct = rng.random() < 0.72
            visible_approved = candidate_correct or rng.random() < 0.55
            independent_approved = candidate_correct or rng.random() < 0.04
            batch.append(
                KernelTask(
                    task_id=task_id,
                    batch=batch_index,
                    kind=kind,
                    value=value,
                    consequence=consequence,
                    base_reliability=base,
                    enhanced_reliability=enhanced,
                    candidate_correct=candidate_correct,
                    visible_approved=visible_approved,
                    independent_approved=independent_approved,
                )
            )
            task_id += 1
        batches.append(batch)
    return batches


def _typed_proposals(task: KernelTask, config: TransitionKernelConfig) -> list[TransitionProposal]:
    proposals: list[TransitionProposal] = []
    if task.kind in {"think", "observe", "external"}:
        gain = (
            _expected_utility(task, task.enhanced_reliability)
            - _expected_utility(task, task.base_reliability)
            - config.operation_cost
        )
        if gain > 0.0:
            proposals.append(
                TransitionProposal(
                    task_id=task.task_id,
                    kind=task.kind,
                    resource="work",
                    expected_gain=gain,
                    cost=config.operation_cost,
                    authority="external_effect" if task.kind == "external" else "temporary_state",
                    reversible=task.kind != "external",
                )
            )
    elif task.kind == "research" and task.visible_approved:
        apparent_discovery_value = 0.85 * 2.2 * task.value
        gain = apparent_discovery_value - config.verify_cost
        if gain > 0.0:
            proposals.append(
                TransitionProposal(
                    task_id=task.task_id,
                    kind="verify_research",
                    resource="verify",
                    expected_gain=gain,
                    cost=config.verify_cost,
                    authority="durable_knowledge",
                    reversible=True,
                    requires_independent_evidence=True,
                )
            )
    return proposals


def _flat_proposals(task: KernelTask, config: TransitionKernelConfig) -> list[TransitionProposal]:
    proposals = _typed_proposals(task, config)
    if task.kind == "research" and task.visible_approved:
        proposals.append(
            TransitionProposal(
                task_id=task.task_id,
                kind="direct_research",
                resource="work",
                expected_gain=2.0 * task.value,
                cost=0.0,
                authority="temporary_state",
                reversible=True,
            )
        )
    if task.kind == "external":
        apparent = _expected_utility(task, task.base_reliability)
        if apparent > 0.0:
            proposals.append(
                TransitionProposal(
                    task_id=task.task_id,
                    kind="direct_external",
                    resource="work",
                    expected_gain=apparent,
                    cost=0.0,
                    authority="temporary_state",
                    reversible=True,
                )
            )
    return proposals


def _allocate_shared(proposals: list[TransitionProposal], config: TransitionKernelConfig) -> list[TransitionProposal]:
    chosen: list[TransitionProposal] = []
    capacity = config.shared_capacity
    verify_capacity = config.verify_capacity
    occupied_tasks: set[int] = set()
    for proposal in sorted(proposals, key=lambda item: item.expected_gain, reverse=True):
        if capacity <= 0:
            break
        if proposal.task_id in occupied_tasks:
            continue
        if proposal.resource == "verify" and verify_capacity <= 0:
            continue
        chosen.append(proposal)
        occupied_tasks.add(proposal.task_id)
        capacity -= 1
        if proposal.resource == "verify":
            verify_capacity -= 1
    return chosen


def _allocate_siloed(proposals: list[TransitionProposal]) -> list[TransitionProposal]:
    work = sorted((item for item in proposals if item.resource == "work"), key=lambda item: item.expected_gain, reverse=True)
    verify = sorted((item for item in proposals if item.resource == "verify"), key=lambda item: item.expected_gain, reverse=True)
    return work[:4] + verify[:1]


def run_transition_kernel(config: TransitionKernelConfig, variant: KernelVariant) -> dict[str, float | int]:
    batches = generate_kernel_tasks(config)
    total_utility = 0.0
    unsafe_external_effects = 0
    false_durable_writes = 0
    correct_durable_writes = 0
    blocked_durable_candidates = 0
    abstained_external = 0
    operations = 0
    verifications = 0
    boundary_violations = 0
    phase_resource_counts = {0: defaultdict(int), 1: defaultdict(int)}

    for batch in batches:
        proposal_fn = _typed_proposals if variant.typed_authority else _flat_proposals
        proposals = [proposal for task in batch for proposal in proposal_fn(task, config)]
        chosen = _allocate_shared(proposals, config) if variant.shared_allocator else _allocate_siloed(proposals)
        chosen_by_task: dict[int, list[TransitionProposal]] = defaultdict(list)
        for proposal in chosen:
            chosen_by_task[proposal.task_id].append(proposal)
            phase = 0 if batch[0].batch < config.shift_batch else 1
            phase_resource_counts[phase][proposal.resource] += 1

        for task in batch:
            task_proposals = chosen_by_task.get(task.task_id, [])
            trial_rng = random.Random(config.seed * 100000 + task.task_id)

            if task.kind == "research":
                if not task.visible_approved:
                    continue
                direct = next((proposal for proposal in task_proposals if proposal.kind == "direct_research"), None)
                verified = next((proposal for proposal in task_proposals if proposal.kind == "verify_research"), None)
                if direct is not None:
                    boundary_violations += 1
                    if task.candidate_correct:
                        total_utility += 2.2 * task.value
                        correct_durable_writes += 1
                    else:
                        total_utility -= config.false_durable_penalty * task.value
                        false_durable_writes += 1
                    continue
                if verified is not None:
                    operations += 1
                    verifications += 1
                    total_utility -= config.verify_cost
                    if task.independent_approved:
                        if task.candidate_correct:
                            total_utility += 2.2 * task.value
                            correct_durable_writes += 1
                        else:
                            total_utility -= config.false_durable_penalty * task.value
                            false_durable_writes += 1
                    continue
                blocked_durable_candidates += 1
                continue

            if task.kind == "external":
                direct = next((proposal for proposal in task_proposals if proposal.kind == "direct_external"), None)
                work = next((proposal for proposal in task_proposals if proposal.kind == "external"), None)
                reliability = task.base_reliability
                if work is not None:
                    reliability = task.enhanced_reliability
                    total_utility -= config.operation_cost
                    operations += 1
                if variant.typed_authority:
                    authorize = _external_expected_utility(task, reliability, config) > 0.0
                else:
                    authorize = direct is not None or work is not None
                    if direct is not None:
                        boundary_violations += 1
                if not authorize:
                    abstained_external += 1
                    continue
                if trial_rng.random() < reliability:
                    total_utility += task.value
                else:
                    total_utility -= config.unsafe_action_penalty * task.consequence * task.value
                    unsafe_external_effects += 1
                continue

            work = next((proposal for proposal in task_proposals if proposal.resource == "work"), None)
            reliability = task.enhanced_reliability if work is not None else task.base_reliability
            if work is not None:
                total_utility -= config.operation_cost
                operations += 1
            if trial_rng.random() < reliability:
                total_utility += task.value
            else:
                total_utility -= task.consequence * task.value

    total_tasks = config.batches * config.tasks_per_batch
    phase_tasks = (
        config.shift_batch * config.tasks_per_batch,
        (config.batches - config.shift_batch) * config.tasks_per_batch,
    )
    return {
        "net_utility_per_task": total_utility / total_tasks,
        "unsafe_external_effects": unsafe_external_effects,
        "false_durable_writes": false_durable_writes,
        "correct_durable_writes": correct_durable_writes,
        "boundary_violations": boundary_violations,
        "blocked_durable_candidates": blocked_durable_candidates,
        "abstained_external": abstained_external,
        "operations_per_task": operations / total_tasks,
        "verifications_per_task": verifications / total_tasks,
        "phase0_verify_alloc_per_task": phase_resource_counts[0]["verify"] / max(1, phase_tasks[0]),
        "phase1_verify_alloc_per_task": phase_resource_counts[1]["verify"] / max(1, phase_tasks[1]),
        "phase0_work_alloc_per_task": phase_resource_counts[0]["work"] / max(1, phase_tasks[0]),
        "phase1_work_alloc_per_task": phase_resource_counts[1]["work"] / max(1, phase_tasks[1]),
    }


def run_transition_kernel_experiment(config: TransitionKernelConfig) -> list[tuple[str, dict[str, float | int]]]:
    return [(variant.name, run_transition_kernel(config, variant)) for variant in (TYPED_SHARED, TYPED_SILOED, FLAT_SHARED)]
