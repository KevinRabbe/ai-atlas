from __future__ import annotations

from dataclasses import dataclass, field
import random


@dataclass(frozen=True)
class EvidenceRecord:
    source_id: int
    domain: int
    action: int
    version: int
    current: bool
    mechanism_match: bool
    reliability: float


@dataclass(frozen=True)
class Task:
    task_id: int
    batch: int
    kind: str
    domain: int
    hidden_action: int
    value: float
    wrong_multiplier: float
    signal: int
    surface_record: EvidenceRecord | None
    causal_record: EvidenceRecord | None
    candidate: int | None
    visible_approved: bool


@dataclass(frozen=True)
class IntegratedConfig:
    seed: int = 0
    batches: int = 400
    tasks_per_batch: int = 12
    domains: int = 8
    bootstrap_domains: int = 4
    research_fraction: float = 0.22
    signal_reliability: float = 0.65
    stale_conflict_probability: float = 0.38
    candidate_reliability: float = 0.70
    evaluator_false_approve_probability: float = 0.35
    deep_retrieval_cost: float = 0.04
    probe_cost: float = 0.11
    verify_cost: float = 0.08
    deep_retrieval_capacity: int = 3
    probe_capacity: int = 3
    verify_capacity: int = 2
    discovery_value: float = 2.2
    false_knowledge_penalty: float = 4.0


@dataclass
class DurableKnowledge:
    action: int
    verified: bool
    evidence_ids: tuple[int, ...]


@dataclass
class EpistemicState:
    durable: dict[int, DurableKnowledge] = field(default_factory=dict)
    rejected: set[tuple[int, int]] = field(default_factory=set)
    tentative: dict[int, int] = field(default_factory=dict)


@dataclass(frozen=True)
class OperationProposal:
    task_id: int
    resource: str
    expected_gain: float
    cost: float


@dataclass(frozen=True)
class OrganismVariant:
    name: str
    plurality: bool = True
    active_information: bool = True
    applicability_retrieval: bool = True
    staged_verification: bool = True
    joint_allocation: bool = True


FULL = OrganismVariant("integrated_full")
ABLATIONS = (
    OrganismVariant("no_plurality", plurality=False),
    OrganismVariant("no_active_information", active_information=False),
    OrganismVariant("similarity_retrieval", applicability_retrieval=False),
    OrganismVariant("immediate_consolidation", staged_verification=False),
    OrganismVariant("independent_allocation", joint_allocation=False),
)


def _expected_commit_utility(prob_correct: float, value: float, wrong_multiplier: float) -> float:
    return prob_correct * value - (1.0 - prob_correct) * wrong_multiplier * value


def _fallback_expected_utility(task: Task, variant: OrganismVariant, state: EpistemicState, config: IntegratedConfig) -> float:
    if task.kind == "research":
        return 0.0
    if task.domain in state.durable:
        return task.value
    if task.surface_record is not None:
        p = 1.0 - config.stale_conflict_probability
    else:
        p = config.signal_reliability
    commit = _expected_commit_utility(p, task.value, task.wrong_multiplier)
    return commit if (not variant.plurality or commit > 0.0) else 0.0


def _candidate_posterior_after_visible_approval(config: IntegratedConfig) -> float:
    numerator = config.candidate_reliability
    denominator = numerator + (1.0 - config.candidate_reliability) * config.evaluator_false_approve_probability
    return numerator / denominator


def _proposals(task: Task, variant: OrganismVariant, state: EpistemicState, config: IntegratedConfig) -> list[OperationProposal]:
    if task.kind == "research":
        if not task.visible_approved or task.candidate is None or not variant.staged_verification:
            return []
        if (task.domain, task.candidate) in state.rejected:
            return []
        p = _candidate_posterior_after_visible_approval(config)
        gain = p * config.discovery_value * task.value - config.verify_cost
        return [OperationProposal(task.task_id, "verify", gain, config.verify_cost)] if gain > 0 else []

    if task.domain in state.durable:
        return []

    fallback = _fallback_expected_utility(task, variant, state, config)
    proposals: list[OperationProposal] = []
    exact_action_utility = task.value

    if variant.applicability_retrieval and task.causal_record is not None:
        gain = exact_action_utility - config.deep_retrieval_cost - fallback
        if gain > 0:
            proposals.append(OperationProposal(task.task_id, "retrieve", gain, config.deep_retrieval_cost))

    if variant.active_information:
        gain = exact_action_utility - config.probe_cost - fallback
        if gain > 0:
            proposals.append(OperationProposal(task.task_id, "probe", gain, config.probe_cost))
    return proposals


def _allocate_joint(proposals_by_task: dict[int, list[OperationProposal]], config: IntegratedConfig) -> dict[int, OperationProposal]:
    capacity = {"retrieve": config.deep_retrieval_capacity, "probe": config.probe_capacity, "verify": config.verify_capacity}
    all_proposals = [proposal for values in proposals_by_task.values() for proposal in values]
    all_proposals.sort(key=lambda item: item.expected_gain, reverse=True)
    chosen: dict[int, OperationProposal] = {}
    for proposal in all_proposals:
        if proposal.task_id in chosen or capacity[proposal.resource] <= 0:
            continue
        chosen[proposal.task_id] = proposal
        capacity[proposal.resource] -= 1
    return chosen


def _allocate_independent(tasks: list[Task], proposals_by_task: dict[int, list[OperationProposal]], config: IntegratedConfig) -> dict[int, OperationProposal]:
    capacity = {"retrieve": config.deep_retrieval_capacity, "probe": config.probe_capacity, "verify": config.verify_capacity}
    chosen: dict[int, OperationProposal] = {}
    for task in tasks:
        options = sorted(proposals_by_task.get(task.task_id, []), key=lambda item: item.expected_gain, reverse=True)
        for proposal in options:
            if capacity[proposal.resource] > 0:
                chosen[task.task_id] = proposal
                capacity[proposal.resource] -= 1
                break
    return chosen


def generate_tasks(config: IntegratedConfig) -> tuple[list[list[Task]], dict[int, int]]:
    rng = random.Random(config.seed)
    hidden_rules = {domain: rng.randrange(2) for domain in range(config.domains)}
    batches: list[list[Task]] = []
    source_id = 0
    task_id = 0
    for batch_index in range(config.batches):
        batch: list[Task] = []
        for _ in range(config.tasks_per_batch):
            domain = rng.randrange(config.domains)
            hidden = hidden_rules[domain]
            frontier = domain >= config.bootstrap_domains
            kind = "research" if frontier and rng.random() < config.research_fraction else "application"
            value = rng.choice((1.0, 2.0, 4.0))
            wrong_multiplier = rng.choice((1.0, 2.5, 4.0))
            signal = hidden if rng.random() < config.signal_reliability else 1 - hidden

            surface = causal = None
            if not frontier:
                stale = rng.random() < config.stale_conflict_probability
                surface = EvidenceRecord(source_id, domain, (1 - hidden) if stale else hidden, 0 if stale else 2, not stale, True, 0.98)
                source_id += 1
                causal = EvidenceRecord(source_id, domain, hidden, 2, True, True, 0.99)
                source_id += 1

            candidate = None
            approved = False
            if kind == "research":
                candidate = hidden if rng.random() < config.candidate_reliability else 1 - hidden
                approved = candidate == hidden or rng.random() < config.evaluator_false_approve_probability

            batch.append(Task(task_id, batch_index, kind, domain, hidden, value, wrong_multiplier, signal, surface, causal, candidate, approved))
            task_id += 1
        batches.append(batch)
    return batches, hidden_rules


def _execute_application(task: Task, operation: OperationProposal | None, variant: OrganismVariant, state: EpistemicState, config: IntegratedConfig) -> tuple[float, bool, bool, str]:
    cost = operation.cost if operation else 0.0
    if task.domain in state.durable:
        action = state.durable[task.domain].action
        source = "durable"
    elif operation and operation.resource in {"retrieve", "probe"}:
        action = task.hidden_action
        source = operation.resource
    elif task.surface_record is not None:
        if variant.applicability_retrieval:
            p = 1.0 - config.stale_conflict_probability
            commit = _expected_commit_utility(p, task.value, task.wrong_multiplier)
            if variant.plurality and commit <= 0:
                return -cost, True, False, "safe"
        action = task.surface_record.action
        source = "surface"
    else:
        commit = _expected_commit_utility(config.signal_reliability, task.value, task.wrong_multiplier)
        if variant.plurality and commit <= 0:
            return -cost, True, False, "safe"
        action = task.signal
        source = "signal"

    correct = action == task.hidden_action
    retrieval_error = source == "surface" and not correct
    utility = (task.value if correct else -task.wrong_multiplier * task.value) - cost
    return utility, False, retrieval_error, source


def _execute_research(task: Task, operation: OperationProposal | None, variant: OrganismVariant, state: EpistemicState, config: IntegratedConfig) -> tuple[float, bool, bool]:
    if task.candidate is None or not task.visible_approved:
        return 0.0, False, False

    candidate_correct = task.candidate == task.hidden_action
    if not variant.staged_verification:
        state.durable[task.domain] = DurableKnowledge(task.candidate, False, (task.task_id,))
        if candidate_correct:
            return config.discovery_value * task.value, True, False
        return -config.false_knowledge_penalty * task.value, True, True

    state.tentative[task.task_id] = task.candidate
    if operation is None or operation.resource != "verify":
        return 0.0, False, False

    if candidate_correct:
        state.durable[task.domain] = DurableKnowledge(task.candidate, True, (task.task_id,))
        state.tentative.pop(task.task_id, None)
        return config.discovery_value * task.value - operation.cost, True, False

    state.rejected.add((task.domain, task.candidate))
    state.tentative.pop(task.task_id, None)
    return -operation.cost, False, False


def run_variant(config: IntegratedConfig, variant: OrganismVariant) -> dict[str, float | int]:
    batches, hidden_rules = generate_tasks(config)
    state = EpistemicState()
    total_utility = 0.0
    application_tasks = research_tasks = 0
    safe_actions = retrieval_errors = false_durable_writes = durable_writes = 0
    operations = {"retrieve": 0, "probe": 0, "verify": 0}
    source_counts: dict[str, int] = {}

    for batch in batches:
        proposals_by_task = {task.task_id: _proposals(task, variant, state, config) for task in batch}
        chosen = _allocate_joint(proposals_by_task, config) if variant.joint_allocation else _allocate_independent(batch, proposals_by_task, config)
        for proposal in chosen.values():
            operations[proposal.resource] += 1

        for task in batch:
            operation = chosen.get(task.task_id)
            if task.kind == "application":
                application_tasks += 1
                utility, safe, retrieval_error, source = _execute_application(task, operation, variant, state, config)
                total_utility += utility
                safe_actions += int(safe)
                retrieval_errors += int(retrieval_error)
                source_counts[source] = source_counts.get(source, 0) + 1
            else:
                research_tasks += 1
                utility, wrote, false_write = _execute_research(task, operation, variant, state, config)
                total_utility += utility
                durable_writes += int(wrote)
                false_durable_writes += int(false_write)

    correct_durable = sum(1 for domain, item in state.durable.items() if item.action == hidden_rules[domain])
    wrong_durable = len(state.durable) - correct_durable
    total_tasks = application_tasks + research_tasks
    return {
        "net_utility_per_task": total_utility / total_tasks,
        "total_utility": total_utility,
        "application_tasks": application_tasks,
        "research_tasks": research_tasks,
        "safe_action_rate": safe_actions / application_tasks,
        "retrieval_error_rate": retrieval_errors / max(1, application_tasks),
        "durable_domains": len(state.durable),
        "correct_durable_domains": correct_durable,
        "wrong_durable_domains": wrong_durable,
        "false_durable_writes": false_durable_writes,
        "durable_writes": durable_writes,
        "retrieve_ops_per_task": operations["retrieve"] / total_tasks,
        "probe_ops_per_task": operations["probe"] / total_tasks,
        "verify_ops_per_task": operations["verify"] / total_tasks,
        "durable_source_rate": source_counts.get("durable", 0) / max(1, application_tasks),
    }


def run_integrated_experiment(config: IntegratedConfig) -> list[tuple[str, dict[str, float | int]]]:
    variants = (FULL,) + ABLATIONS
    return [(variant.name, run_variant(config, variant)) for variant in variants]
