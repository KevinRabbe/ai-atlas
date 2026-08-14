from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class AssuranceConfig:
    seed: int = 0
    batches: int = 500
    tasks_per_batch: int = 12
    base_final_correct: float = 0.78
    base_process_valid: float = 0.88
    exploit_probability_on_wrong: float = 0.16
    primary_true_approve: float = 0.98
    primary_false_approve: float = 0.08
    primary_exploit_approve: float = 0.995
    correlated_true_approve: float = 0.98
    correlated_false_approve: float = 0.07
    correlated_exploit_approve: float = 0.99
    independent_true_approve: float = 0.97
    independent_false_approve: float = 0.04
    process_true_approve: float = 0.97
    process_false_approve: float = 0.05
    primary_cost: float = 0.08
    correlated_cost: float = 0.18
    independent_cost: float = 0.45
    process_cost: float = 0.32
    final_wrong_multiplier: float = 2.5
    adaptive_final_base_risk: float = 0.05
    adaptive_final_pressure_scale: float = 0.030
    adaptive_process_risk: float = 0.12
    adaptive_margin: float = 1.0
    secondary_capacity: int = 4
    process_capacity: int = 4


@dataclass(frozen=True)
class Candidate:
    final_correct: bool
    process_valid: bool
    shared_exploit: bool
    visible_score: float
    primary_approved: bool
    correlated_approved: bool
    independent_approved: bool
    process_approved: bool


@dataclass(frozen=True)
class AssuranceTask:
    task_id: int
    batch: int
    value: float
    process_consequence: float
    search_pressure: int
    candidate: Candidate


def _candidate(rng: random.Random, config: AssuranceConfig) -> Candidate:
    final_correct = rng.random() < config.base_final_correct
    process_valid = rng.random() < config.base_process_valid
    shared_exploit = (
        (not final_correct)
        and rng.random() < config.exploit_probability_on_wrong
    )
    visible_score = (
        (1.0 if final_correct else 0.15)
        + (1.25 if shared_exploit else 0.0)
        + rng.uniform(-0.08, 0.08)
    )

    if final_correct:
        primary = rng.random() < config.primary_true_approve
        correlated = rng.random() < config.correlated_true_approve
        independent = rng.random() < config.independent_true_approve
    elif shared_exploit:
        primary = rng.random() < config.primary_exploit_approve
        correlated = rng.random() < config.correlated_exploit_approve
        independent = rng.random() < config.independent_false_approve
    else:
        primary = rng.random() < config.primary_false_approve
        correlated = rng.random() < config.correlated_false_approve
        independent = rng.random() < config.independent_false_approve

    process = rng.random() < (
        config.process_true_approve
        if process_valid
        else config.process_false_approve
    )
    return Candidate(
        final_correct,
        process_valid,
        shared_exploit,
        visible_score,
        primary,
        correlated,
        independent,
        process,
    )


def _selected_candidate(
    rng: random.Random,
    config: AssuranceConfig,
    search_pressure: int,
) -> Candidate:
    pool = [_candidate(rng, config) for _ in range(search_pressure)]
    return max(pool, key=lambda item: item.visible_score)


def generate_assurance_batches(
    config: AssuranceConfig,
    *,
    fixed_search_pressure: int | None = None,
) -> tuple[tuple[AssuranceTask, ...], ...]:
    rng = random.Random(config.seed)
    batches = []
    task_id = 0
    pressures = (1, 4, 16)
    for batch_index in range(config.batches):
        batch = []
        for _ in range(config.tasks_per_batch):
            pressure = fixed_search_pressure or rng.choice(pressures)
            batch.append(
                AssuranceTask(
                    task_id=task_id,
                    batch=batch_index,
                    value=rng.choice((1.0, 2.0, 5.0)),
                    process_consequence=rng.choice((1.0, 3.0, 8.0)),
                    search_pressure=pressure,
                    candidate=_selected_candidate(rng, config, pressure),
                )
            )
            task_id += 1
        batches.append(tuple(batch))
    return tuple(batches)


def _accepted_utility(task: AssuranceTask, config: AssuranceConfig) -> float:
    candidate = task.candidate
    if candidate.final_correct and candidate.process_valid:
        return task.value
    penalty = 0.0
    if not candidate.final_correct:
        penalty += config.final_wrong_multiplier * task.value
    if not candidate.process_valid:
        penalty += task.process_consequence * task.value
    return -penalty


def _summarize(
    tasks: list[AssuranceTask],
    accepted: list[bool],
    costs: list[float],
    config: AssuranceConfig,
) -> dict[str, float | int]:
    total_utility = 0.0
    false_accepts = valid_accepts = rejects = process_fail_accepts = final_fail_accepts = 0
    exploit_accepts = 0
    for task, accept, cost in zip(tasks, accepted, costs):
        if accept:
            utility = _accepted_utility(task, config)
            total_utility += utility - cost
            valid = task.candidate.final_correct and task.candidate.process_valid
            valid_accepts += int(valid)
            false_accepts += int(not valid)
            process_fail_accepts += int(not task.candidate.process_valid)
            final_fail_accepts += int(not task.candidate.final_correct)
            exploit_accepts += int(task.candidate.shared_exploit and not task.candidate.final_correct)
        else:
            rejects += 1
            total_utility -= cost
    n = len(tasks)
    return {
        "net_utility_per_task": total_utility / n,
        "false_accept_rate": false_accepts / n,
        "valid_accept_rate": valid_accepts / n,
        "reject_rate": rejects / n,
        "process_failure_accept_rate": process_fail_accepts / n,
        "final_failure_accept_rate": final_fail_accepts / n,
        "exploit_accept_rate": exploit_accepts / n,
        "verification_cost_per_task": sum(costs) / n,
    }


def _run_static_policy(
    config: AssuranceConfig,
    batches: tuple[tuple[AssuranceTask, ...], ...],
    policy: str,
) -> dict[str, float | int]:
    tasks: list[AssuranceTask] = []
    accepted: list[bool] = []
    costs: list[float] = []

    for batch in batches:
        for task in batch:
            candidate = task.candidate
            if policy == "outcome_only":
                accept = candidate.primary_approved
                cost = config.primary_cost
            elif policy == "process_only":
                accept = candidate.process_approved
                cost = config.process_cost
            elif policy == "uniform_both":
                accept = candidate.primary_approved and candidate.process_approved
                cost = config.primary_cost + config.process_cost
            elif policy == "correlated_double":
                accept = candidate.primary_approved and candidate.correlated_approved
                cost = config.primary_cost + config.correlated_cost
            elif policy == "independent_double":
                accept = candidate.primary_approved and candidate.independent_approved
                cost = config.primary_cost + config.independent_cost
            else:
                raise ValueError(policy)
            tasks.append(task)
            accepted.append(accept)
            costs.append(cost)
    return _summarize(tasks, accepted, costs, config)


def _adaptive_granularity(
    config: AssuranceConfig,
    batches: tuple[tuple[AssuranceTask, ...], ...],
) -> dict[str, float | int]:
    tasks: list[AssuranceTask] = []
    accepted: list[bool] = []
    costs: list[float] = []
    outcome_checks = process_checks = 0

    for batch in batches:
        for task in batch:
            estimated_final_risk = min(
                0.75,
                config.adaptive_final_base_risk
                + config.adaptive_final_pressure_scale * task.search_pressure,
            )
            estimated_process_risk = config.adaptive_process_risk
            final_harm = (
                estimated_final_risk
                * config.final_wrong_multiplier
                * task.value
            )
            process_harm = (
                estimated_process_risk
                * task.process_consequence
                * task.value
            )
            use_outcome = final_harm * config.adaptive_margin > config.primary_cost
            use_process = process_harm * config.adaptive_margin > config.process_cost
            checks = []
            cost = 0.0
            if use_outcome:
                checks.append(task.candidate.primary_approved)
                cost += config.primary_cost
                outcome_checks += 1
            if use_process:
                checks.append(task.candidate.process_approved)
                cost += config.process_cost
                process_checks += 1
            accept = all(checks) if checks else True
            tasks.append(task)
            accepted.append(accept)
            costs.append(cost)

    metrics = _summarize(tasks, accepted, costs, config)
    n = len(tasks)
    metrics["outcome_checks_per_task"] = outcome_checks / n
    metrics["process_checks_per_task"] = process_checks / n
    return metrics


def run_verification_granularity_experiment(
    config: AssuranceConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    batches = generate_assurance_batches(config)
    return [
        ("outcome_only", _run_static_policy(config, batches, "outcome_only")),
        ("process_only", _run_static_policy(config, batches, "process_only")),
        ("uniform_both", _run_static_policy(config, batches, "uniform_both")),
        ("adaptive_granularity", _adaptive_granularity(config, batches)),
    ]


def run_evaluator_independence_experiment(
    config: AssuranceConfig,
    *,
    search_pressure: int,
) -> list[tuple[str, dict[str, float | int]]]:
    batches = generate_assurance_batches(
        config,
        fixed_search_pressure=search_pressure,
    )
    return [
        ("single_primary", _run_static_policy(config, batches, "outcome_only")),
        ("correlated_double", _run_static_policy(config, batches, "correlated_double")),
        ("independent_double", _run_static_policy(config, batches, "independent_double")),
    ]


def _explicit_assurance_batch(
    batch: tuple[AssuranceTask, ...],
    config: AssuranceConfig,
) -> tuple[dict[int, bool], dict[int, bool]]:
    secondary_scores = []
    process_scores = []
    for task in batch:
        final_risk = min(
            0.75,
            config.adaptive_final_base_risk
            + config.adaptive_final_pressure_scale * task.search_pressure,
        )
        final_harm = final_risk * config.final_wrong_multiplier * task.value
        process_harm = (
            config.adaptive_process_risk
            * task.process_consequence
            * task.value
        )
        if final_harm > config.independent_cost:
            secondary_scores.append((final_harm - config.independent_cost, task.task_id))
        if process_harm > config.process_cost:
            process_scores.append((process_harm - config.process_cost, task.task_id))
    secondary_scores.sort(reverse=True)
    process_scores.sort(reverse=True)
    secondary = {
        task_id: True
        for _, task_id in secondary_scores[: config.secondary_capacity]
    }
    process = {
        task_id: True
        for _, task_id in process_scores[: config.process_capacity]
    }
    return secondary, process


def _run_assurance_allocator(
    config: AssuranceConfig,
    batches: tuple[tuple[AssuranceTask, ...], ...],
    policy: str,
) -> dict[str, float | int]:
    tasks: list[AssuranceTask] = []
    accepted: list[bool] = []
    costs: list[float] = []
    secondary_checks = process_checks = 0

    for batch in batches:
        if policy == "explicit_adaptive":
            secondary_map, process_map = _explicit_assurance_batch(batch, config)
        else:
            secondary_map = process_map = {}

        for task in batch:
            candidate = task.candidate
            checks = [candidate.primary_approved]
            cost = config.primary_cost
            if policy == "implicit_self_check":
                # High visible confidence suppresses checking; exploit candidates are
                # intentionally overconfident under the correlated proposal/evaluator.
                uncertainty = max(0.0, 1.05 - candidate.visible_score)
                if uncertainty * task.value > config.independent_cost:
                    checks.append(candidate.independent_approved)
                    cost += config.independent_cost
                    secondary_checks += 1
            elif policy == "explicit_adaptive":
                if task.task_id in secondary_map:
                    checks.append(candidate.independent_approved)
                    cost += config.independent_cost
                    secondary_checks += 1
                if task.task_id in process_map:
                    checks.append(candidate.process_approved)
                    cost += config.process_cost
                    process_checks += 1
            elif policy == "uniform_heavy":
                checks.extend((candidate.independent_approved, candidate.process_approved))
                cost += config.independent_cost + config.process_cost
                secondary_checks += 1
                process_checks += 1
            else:
                raise ValueError(policy)
            tasks.append(task)
            accepted.append(all(checks))
            costs.append(cost)

    metrics = _summarize(tasks, accepted, costs, config)
    n = len(tasks)
    metrics["independent_checks_per_task"] = secondary_checks / n
    metrics["process_checks_per_task"] = process_checks / n
    return metrics


def run_assurance_allocation_experiment(
    config: AssuranceConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    batches = generate_assurance_batches(config)
    return [
        (
            "implicit_self_check",
            _run_assurance_allocator(config, batches, "implicit_self_check"),
        ),
        (
            "explicit_adaptive",
            _run_assurance_allocator(config, batches, "explicit_adaptive"),
        ),
        (
            "uniform_heavy",
            _run_assurance_allocator(config, batches, "uniform_heavy"),
        ),
    ]
