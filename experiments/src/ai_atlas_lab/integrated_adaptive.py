from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

RESOURCES = ("retrieve", "probe")
# [regime][family][resource]
QUALITY = (
    ((0.94, 0.78), (0.70, 0.93)),
    ((0.72, 0.94), (0.91, 0.76)),
    ((0.86, 0.82), (0.78, 0.91)),
)
PRICES = (
    (0.05, 0.12),
    (0.14, 0.05),
    (0.07, 0.10),
)


@dataclass(frozen=True)
class AdaptiveIntegratedConfig:
    seed: int = 0
    batches: int = 600
    tasks_per_batch: int = 10
    domains: int = 8
    claims_per_domain: int = 30
    frontier_start: int = 4
    research_fraction: float = 0.25
    signal_reliability: float = 0.60
    candidate_reliability: float = 0.72
    primary_true_approve: float = 0.97
    primary_false_approve_risky: float = 0.65
    primary_false_approve_normal: float = 0.02
    secondary_true_approve: float = 0.96
    secondary_false_approve: float = 0.04
    retrieve_capacity: int = 3
    probe_capacity: int = 3
    primary_verify_capacity: int = 4
    secondary_verify_capacity: int = 4
    primary_verify_cost: float = 0.05
    secondary_verify_cost: float = 0.55
    discovery_value: float = 2.4
    false_knowledge_penalty: float = 3.0
    quality_prior_successes: float = 8.0
    quality_prior_trials: float = 10.0
    private_blend_scale: float = 14.0
    assurance_prior_false: float = 0.12
    assurance_prior_trials: float = 8.0
    assurance_ucb_scale: float = 1.35
    assurance_explore_rate: float = 0.05
    future_contamination_cost_per_reuse: float = 0.2


@dataclass(frozen=True)
class AdaptiveTask:
    task_id: int
    batch: int
    regime: int
    domain: int
    claim: int
    family: int
    kind: str
    hidden_action: int
    value: float
    wrong_multiplier: float
    signal: int
    resource_outcomes: tuple[bool, bool]
    candidate: int | None
    primary_approved: bool
    secondary_approved: bool

    @property
    def key(self) -> tuple[int, int]:
        return (self.domain, self.claim)


@dataclass
class DurableItem:
    action: int
    evidence_task: int
    independently_checked: bool


@dataclass
class State:
    durable: dict[tuple[int, int], DurableItem] = field(default_factory=dict)
    rejected: set[tuple[int, int, int]] = field(default_factory=set)


@dataclass(frozen=True)
class Variant:
    name: str
    estimator_mode: str = "conditional"  # conditional | shared | private | frozen
    assurance_mode: str = "adaptive"  # adaptive | primary_only | double


VARIANTS = (
    Variant("adaptive_conditional"),
    Variant("all_shared_quality", estimator_mode="shared"),
    Variant("all_private_quality", estimator_mode="private"),
    Variant("frozen_initial_quality", estimator_mode="frozen"),
    Variant("single_primary_verifier", assurance_mode="primary_only"),
    Variant("uniform_double_verify", assurance_mode="double"),
)


class QualityEstimator:
    """Online operation-quality estimate with shared/private interpolation."""

    def __init__(self, config: AdaptiveIntegratedConfig, mode: str) -> None:
        self.config = config
        self.mode = mode
        r = len(RESOURCES)
        self.global_s = [config.quality_prior_successes] * r
        self.global_n = [config.quality_prior_trials] * r
        self.family_s = [[config.quality_prior_successes] * r for _ in range(2)]
        self.family_n = [[config.quality_prior_trials] * r for _ in range(2)]
        self.domain_s = [[config.quality_prior_successes] * r for _ in range(config.domains)]
        self.domain_n = [[config.quality_prior_trials] * r for _ in range(config.domains)]

    @staticmethod
    def _ratio(s: float, n: float) -> float:
        return s / n

    def estimate(self, task: AdaptiveTask, resource: int) -> float:
        if self.mode == "frozen":
            # Fixed policy knows the initial regime's resource economics but never adapts.
            return QUALITY[0][task.family][resource]
        if self.mode == "shared":
            return self._ratio(self.global_s[resource], self.global_n[resource])
        private = self._ratio(self.domain_s[task.domain][resource], self.domain_n[task.domain][resource])
        if self.mode == "private":
            return private
        family = self._ratio(self.family_s[task.family][resource], self.family_n[task.family][resource])
        private_real_trials = max(
            0.0,
            self.domain_n[task.domain][resource] - self.config.quality_prior_trials,
        )
        weight_private = private_real_trials / (
            private_real_trials + self.config.private_blend_scale
        )
        return (1.0 - weight_private) * family + weight_private * private

    def update(self, task: AdaptiveTask, resource: int, success: bool) -> None:
        value = 1.0 if success else 0.0
        self.global_n[resource] += 1.0
        self.global_s[resource] += value
        self.family_n[task.family][resource] += 1.0
        self.family_s[task.family][resource] += value
        self.domain_n[task.domain][resource] += 1.0
        self.domain_s[task.domain][resource] += value


class AssuranceEstimator:
    """Estimate how unsafe a primary approval is, including epistemic uncertainty.

    The system never observes hidden correctness. Independent secondary disagreement is
    used as an imperfect observable proxy for unsafe primary approvals. Allocation uses
    an upper confidence estimate rather than the posterior mean so sparse evidence does
    not masquerade as certainty.
    """

    def __init__(self, config: AdaptiveIntegratedConfig) -> None:
        self.config = config
        self.false_s = [
            config.assurance_prior_false * config.assurance_prior_trials
            for _ in range(2)
        ]
        self.trials = [config.assurance_prior_trials for _ in range(2)]

    def estimated_false_approval(self, family: int) -> float:
        return self.false_s[family] / self.trials[family]

    def upper_false_approval(self, family: int) -> float:
        p = self.estimated_false_approval(family)
        n = self.trials[family]
        standard_error = math.sqrt(max(1e-9, p * (1.0 - p)) / (n + 1.0))
        return min(1.0, p + self.config.assurance_ucb_scale * standard_error)

    def update_from_secondary(self, family: int, secondary_approved: bool) -> None:
        self.trials[family] += 1.0
        if not secondary_approved:
            self.false_s[family] += 1.0


def _regime_for(batch: int, batches: int) -> int:
    return min(2, (3 * batch) // batches)


def generate_tasks(
    config: AdaptiveIntegratedConfig,
) -> tuple[list[list[AdaptiveTask]], dict[tuple[int, int], int]]:
    rng = random.Random(config.seed)
    rules = {
        (domain, claim): rng.randrange(2)
        for domain in range(config.domains)
        for claim in range(config.claims_per_domain)
    }
    batches: list[list[AdaptiveTask]] = []
    task_id = 0
    for batch_index in range(config.batches):
        regime = _regime_for(batch_index, config.batches)
        batch: list[AdaptiveTask] = []
        for _ in range(config.tasks_per_batch):
            domain = rng.randrange(config.domains)
            claim = rng.randrange(config.claims_per_domain)
            family = domain % 2
            hidden = rules[(domain, claim)]
            frontier = domain >= config.frontier_start
            kind = (
                "research"
                if frontier and rng.random() < config.research_fraction
                else "application"
            )
            value = rng.choice((1.0, 2.0, 4.0))
            wrong_multiplier = rng.choice((1.0, 2.5, 4.0))
            signal = (
                hidden
                if rng.random() < config.signal_reliability
                else 1 - hidden
            )
            outcomes = tuple(
                rng.random() < QUALITY[regime][family][resource]
                for resource in range(len(RESOURCES))
            )

            candidate = None
            primary_approved = secondary_approved = False
            if kind == "research":
                candidate = (
                    hidden
                    if rng.random() < config.candidate_reliability
                    else 1 - hidden
                )
                if candidate == hidden:
                    primary_approved = rng.random() < config.primary_true_approve
                    secondary_approved = rng.random() < config.secondary_true_approve
                else:
                    false_rate = (
                        config.primary_false_approve_risky
                        if family == 0
                        else config.primary_false_approve_normal
                    )
                    primary_approved = rng.random() < false_rate
                    secondary_approved = rng.random() < config.secondary_false_approve

            batch.append(
                AdaptiveTask(
                    task_id,
                    batch_index,
                    regime,
                    domain,
                    claim,
                    family,
                    kind,
                    hidden,
                    value,
                    wrong_multiplier,
                    signal,
                    outcomes,
                    candidate,
                    primary_approved,
                    secondary_approved,
                )
            )
            task_id += 1
        batches.append(batch)
    return batches, rules


def _expected_utility(p: float, value: float, wrong: float) -> float:
    return p * value - (1.0 - p) * wrong * value


def _choose_no_operation(
    task: AdaptiveTask,
    config: AdaptiveIntegratedConfig,
) -> tuple[int | None, float]:
    expected = _expected_utility(
        config.signal_reliability,
        task.value,
        task.wrong_multiplier,
    )
    if expected <= 0:
        return None, 0.0
    return task.signal, expected


def _application_proposals(
    task: AdaptiveTask,
    estimator: QualityEstimator,
    config: AdaptiveIntegratedConfig,
    state: State,
) -> list[tuple[float, int]]:
    if task.key in state.durable:
        return []
    _, fallback = _choose_no_operation(task, config)
    proposals = []
    for resource in range(len(RESOURCES)):
        probability = estimator.estimate(task, resource)
        price = PRICES[task.regime][resource]
        expected = (
            _expected_utility(
                probability,
                task.value,
                task.wrong_multiplier,
            )
            - price
        )
        gain = expected - fallback
        if gain > 0:
            proposals.append((gain, resource))
    return proposals


def _allocate_applications(
    tasks: list[AdaptiveTask],
    estimator: QualityEstimator,
    config: AdaptiveIntegratedConfig,
    state: State,
) -> dict[int, int]:
    capacities = [config.retrieve_capacity, config.probe_capacity]
    proposals: list[tuple[float, int, int]] = []
    for task in tasks:
        if task.kind != "application":
            continue
        for gain, resource in _application_proposals(
            task, estimator, config, state
        ):
            proposals.append((gain, task.task_id, resource))
    proposals.sort(reverse=True)
    chosen: dict[int, int] = {}
    for _, task_id, resource in proposals:
        if task_id in chosen or capacities[resource] <= 0:
            continue
        chosen[task_id] = resource
        capacities[resource] -= 1
    return chosen


def _allocate_primary(
    tasks: list[AdaptiveTask],
    config: AdaptiveIntegratedConfig,
    state: State,
) -> set[int]:
    proposals: list[tuple[float, int]] = []
    for task in tasks:
        if (
            task.kind != "research"
            or task.key in state.durable
            or task.candidate is None
        ):
            continue
        if (task.domain, task.claim, task.candidate) in state.rejected:
            continue
        expected = (
            config.candidate_reliability
            * config.discovery_value
            * task.value
            - config.primary_verify_cost
        )
        if expected > 0:
            proposals.append((expected, task.task_id))
    proposals.sort(reverse=True)
    return {
        task_id
        for _, task_id in proposals[: config.primary_verify_capacity]
    }


def _secondary_policy(
    approved_tasks: list[AdaptiveTask],
    variant: Variant,
    assurance: AssuranceEstimator,
    config: AdaptiveIntegratedConfig,
    rng: random.Random,
) -> tuple[set[int], set[int]]:
    """Return (must_wait_for_secondary, allocated_secondary).

    If a claim is judged risky enough to require secondary evidence but capacity is
    unavailable, it stays tentative instead of silently falling back to primary-only
    consolidation. This is essential under scarce assurance.
    """
    if variant.assurance_mode == "primary_only":
        return set(), set()

    proposals: list[tuple[float, int]] = []
    required: set[int] = set()
    for task in approved_tasks:
        if variant.assurance_mode == "double":
            required.add(task.task_id)
            priority = 1_000_000.0 + task.value
        else:
            upper_false = assurance.upper_false_approval(task.family)
            remaining_tasks = max(0, config.batches - task.batch - 1) * config.tasks_per_batch
            expected_future_reuses = (
                remaining_tasks
                / (config.domains * config.claims_per_domain)
                * (1.0 - config.research_fraction)
            )
            false_consequence = (
                config.false_knowledge_penalty * task.value
                + expected_future_reuses * config.future_contamination_cost_per_reuse
            )
            risk = upper_false * false_consequence
            explore = rng.random() < config.assurance_explore_rate
            if risk <= config.secondary_verify_cost and not explore:
                continue
            required.add(task.task_id)
            priority = (
                risk - config.secondary_verify_cost + (0.001 if explore else 0.0)
            )
        proposals.append((priority, task.task_id))

    proposals.sort(reverse=True)
    allocated = {
        task_id
        for _, task_id in proposals[: config.secondary_verify_capacity]
    }
    return required, allocated


def run_variant(
    config: AdaptiveIntegratedConfig,
    variant: Variant,
) -> dict[str, float | int]:
    batches, rules = generate_tasks(config)
    estimator = QualityEstimator(config, variant.estimator_mode)
    assurance = AssuranceEstimator(config)
    state = State()
    rng = random.Random(config.seed + 9001)

    total_utility = 0.0
    app_count = research_count = 0
    resource_counts = [0, 0]
    false_writes = durable_writes = 0
    primary_calls = secondary_calls = 0
    assurance_waits = 0
    safe_actions = 0
    regime_utility = [0.0, 0.0, 0.0]
    regime_tasks = [0, 0, 0]

    for batch in batches:
        app_choice = _allocate_applications(batch, estimator, config, state)
        primary_choice = _allocate_primary(batch, config, state)

        primary_approved_tasks: list[AdaptiveTask] = []
        for task in batch:
            if task.kind == "research" and task.task_id in primary_choice:
                primary_calls += 1
                total_utility -= config.primary_verify_cost
                regime_utility[task.regime] -= config.primary_verify_cost
                if task.primary_approved:
                    primary_approved_tasks.append(task)
                elif task.candidate is not None:
                    state.rejected.add((task.domain, task.claim, task.candidate))

        required_secondary, secondary_choice = _secondary_policy(
            primary_approved_tasks,
            variant,
            assurance,
            config,
            rng,
        )
        approved_by_id = {
            task.task_id: task for task in primary_approved_tasks
        }
        for task_id in secondary_choice:
            task = approved_by_id[task_id]
            secondary_calls += 1
            total_utility -= config.secondary_verify_cost
            regime_utility[task.regime] -= config.secondary_verify_cost
            assurance.update_from_secondary(
                task.family,
                task.secondary_approved,
            )

        for task in batch:
            regime_tasks[task.regime] += 1
            if task.kind == "application":
                app_count += 1
                if task.key in state.durable:
                    action = state.durable[task.key].action
                    correct = action == task.hidden_action
                    utility = (
                        task.value
                        if correct
                        else -task.wrong_multiplier * task.value
                    )
                elif task.task_id in app_choice:
                    resource = app_choice[task.task_id]
                    resource_counts[resource] += 1
                    success = task.resource_outcomes[resource]
                    estimator.update(task, resource, success)
                    utility = (
                        task.value
                        if success
                        else -task.wrong_multiplier * task.value
                    ) - PRICES[task.regime][resource]
                else:
                    action, _ = _choose_no_operation(task, config)
                    if action is None:
                        safe_actions += 1
                        utility = 0.0
                    else:
                        correct = action == task.hidden_action
                        utility = (
                            task.value
                            if correct
                            else -task.wrong_multiplier * task.value
                        )
                total_utility += utility
                regime_utility[task.regime] += utility
                continue

            research_count += 1
            if (
                task.key in state.durable
                or task.task_id not in primary_choice
                or not task.primary_approved
                or task.candidate is None
            ):
                continue

            needs_secondary = task.task_id in required_secondary
            got_secondary = task.task_id in secondary_choice
            if needs_secondary and not got_secondary:
                assurance_waits += 1
                # Evidence was judged insufficient and scarce assurance was unavailable.
                # Keep the claim tentative by declining durable promotion.
                continue

            if got_secondary and not task.secondary_approved:
                state.rejected.add((task.domain, task.claim, task.candidate))
                continue

            correct = task.candidate == task.hidden_action
            state.durable[task.key] = DurableItem(
                task.candidate,
                task.task_id,
                got_secondary,
            )
            durable_writes += 1
            if correct:
                reward = config.discovery_value * task.value
            else:
                false_writes += 1
                reward = -config.false_knowledge_penalty * task.value
            total_utility += reward
            regime_utility[task.regime] += reward

    correct_durable = sum(
        1
        for key, item in state.durable.items()
        if item.action == rules[key]
    )
    wrong_durable = len(state.durable) - correct_durable
    total_tasks = app_count + research_count
    metrics: dict[str, float | int] = {
        "net_utility_per_task": total_utility / total_tasks,
        "safe_action_rate": safe_actions / max(1, app_count),
        "retrieve_ops_per_task": resource_counts[0] / total_tasks,
        "probe_ops_per_task": resource_counts[1] / total_tasks,
        "primary_verify_per_task": primary_calls / total_tasks,
        "secondary_verify_per_task": secondary_calls / total_tasks,
        "false_durable_writes": false_writes,
        "durable_writes": durable_writes,
        "wrong_durable_domains": wrong_durable,
        "correct_durable_domains": correct_durable,
        "assurance_waits": assurance_waits,
        "secondary_rate_among_primary": secondary_calls / max(1, primary_calls),
        "estimated_false_family_0": assurance.estimated_false_approval(0),
        "estimated_false_family_1": assurance.estimated_false_approval(1),
        "upper_false_family_0": assurance.upper_false_approval(0),
        "upper_false_family_1": assurance.upper_false_approval(1),
    }
    for regime in range(3):
        metrics[f"utility_per_task_regime_{regime}"] = (
            regime_utility[regime] / regime_tasks[regime]
        )
    return metrics


def run_adaptive_integrated_experiment(
    config: AdaptiveIntegratedConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        (variant.name, run_variant(config, variant))
        for variant in VARIANTS
    ]
