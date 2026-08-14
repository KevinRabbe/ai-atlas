from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class LearnedKernelConfig:
    seed: int = 0
    batches: int = 600
    tasks_per_batch: int = 14
    shift_batch: int = 300
    shared_capacity: int = 4
    verify_capacity: int = 1
    operation_cost: float = 0.06
    verify_cost: float = 0.12
    unsafe_action_penalty: float = 5.0
    false_durable_penalty: float = 7.0
    discovery_value: float = 2.2
    decay: float = 0.985
    exploration: float = 0.18


@dataclass(frozen=True)
class LearnedKernelTask:
    task_id: int
    batch: int
    kind: str
    family: int
    value: float
    consequence: float
    authorized: bool
    base_reliability: float
    enhanced_reliability: float
    candidate_prior: float
    primary_false_approve: float
    secondary_true_approve: float
    secondary_false_approve: float
    candidate_correct: bool
    visible_approved: bool
    secondary_approved: bool


@dataclass(frozen=True)
class LearnedKernelVariant:
    name: str
    estimator: str
    oracle: bool = False


ORACLE_UPPER_BOUND = LearnedKernelVariant("oracle_typed_upper_bound", "conditional", True)
LEARNED_CONDITIONAL = LearnedKernelVariant("learned_conditional_typed", "conditional")
LEARNED_GLOBAL = LearnedKernelVariant("learned_global_typed", "global")
FROZEN_CONDITIONAL = LearnedKernelVariant("frozen_conditional_typed", "frozen")
VARIANTS = (ORACLE_UPPER_BOUND, LEARNED_CONDITIONAL, LEARNED_GLOBAL, FROZEN_CONDITIONAL)


@dataclass
class _Rate:
    successes: float = 2.0
    total: float = 3.0

    @property
    def mean(self) -> float:
        return self.successes / self.total

    def optimistic(self, scale: float) -> float:
        return min(0.99, self.mean + scale / math.sqrt(max(1.0, self.total)))

    def update(self, success: bool, decay: float) -> None:
        self.successes *= decay
        self.total *= decay
        self.successes += float(success)
        self.total += 1.0


class _Estimator:
    def __init__(self, config: LearnedKernelConfig, mode: str) -> None:
        self.config = config
        self.mode = mode
        self.work: dict[tuple[str, object, str], _Rate] = defaultdict(_Rate)
        self.visible_correct: dict[object, _Rate] = defaultdict(_Rate)
        self.secondary_good: dict[object, _Rate] = defaultdict(lambda: _Rate(2.8, 3.0))
        self.secondary_bad: dict[object, _Rate] = defaultdict(lambda: _Rate(0.1, 3.0))

    def _family(self, task: LearnedKernelTask) -> object:
        return "*" if self.mode == "global" else task.family

    def _work_key(self, task: LearnedKernelTask, arm: str) -> tuple[str, object, str]:
        return task.kind, self._family(task), arm

    def _frozen(self, task: LearnedKernelTask) -> bool:
        return self.mode == "frozen" and task.batch >= self.config.shift_batch

    def work_estimate(self, task: LearnedKernelTask, oracle: bool) -> tuple[float, float]:
        if oracle:
            return task.base_reliability, task.enhanced_reliability
        base = self.work[self._work_key(task, "base")]
        enhanced = self.work[self._work_key(task, "enhanced")]
        return base.mean, enhanced.optimistic(self.config.exploration)

    def research_estimate(self, task: LearnedKernelTask, oracle: bool) -> tuple[float, float, float]:
        if oracle:
            numerator = task.candidate_prior
            denominator = numerator + (1.0 - numerator) * task.primary_false_approve
            return numerator / denominator, task.secondary_true_approve, task.secondary_false_approve
        family = self._family(task)
        return (
            self.visible_correct[family].mean,
            self.secondary_good[family].mean,
            self.secondary_bad[family].mean,
        )

    def update_work(self, task: LearnedKernelTask, enhanced: bool, success: bool) -> None:
        if self._frozen(task):
            return
        arm = "enhanced" if enhanced else "base"
        self.work[self._work_key(task, arm)].update(success, self.config.decay)

    def update_research(self, task: LearnedKernelTask) -> None:
        if self._frozen(task):
            return
        family = self._family(task)
        self.visible_correct[family].update(task.candidate_correct, self.config.decay)
        target = self.secondary_good if task.candidate_correct else self.secondary_bad
        target[family].update(task.secondary_approved, self.config.decay)


def _regime(batch: int, config: LearnedKernelConfig) -> int:
    return int(batch >= config.shift_batch)


def _work_parameters(kind: str, family: int, regime: int) -> tuple[float, float]:
    table = {
        0: {
            "think": ((0.62, 0.90), (0.70, 0.75)),
            "observe": ((0.65, 0.88), (0.71, 0.77)),
            "coupled": ((0.76, 0.80), (0.55, 0.90)),
            "external": ((0.72, 0.87), (0.58, 0.82)),
        },
        1: {
            "think": ((0.70, 0.74), (0.58, 0.92)),
            "observe": ((0.73, 0.77), (0.59, 0.91)),
            "coupled": ((0.53, 0.92), (0.77, 0.80)),
            "external": ((0.61, 0.86), (0.78, 0.81)),
        },
    }
    return table[regime][kind][family]


def _research_parameters(family: int, regime: int) -> tuple[float, float, float, float]:
    candidate_prior = ((0.74, 0.68), (0.69, 0.77))[regime][family]
    primary_false = ((0.05, 0.42), (0.36, 0.06))[regime][family]
    secondary_true = ((0.99, 0.96), (0.95, 0.99))[regime][family]
    secondary_false = ((0.015, 0.08), (0.07, 0.015))[regime][family]
    return candidate_prior, primary_false, secondary_true, secondary_false


def generate_learned_kernel_tasks(config: LearnedKernelConfig) -> list[list[LearnedKernelTask]]:
    rng = random.Random(config.seed)
    mix = (("think", 0.24), ("observe", 0.18), ("coupled", 0.18), ("external", 0.20), ("research", 0.20))
    boundaries: list[tuple[str, float]] = []
    running = 0.0
    for kind, probability in mix:
        running += probability
        boundaries.append((kind, running))

    batches: list[list[LearnedKernelTask]] = []
    task_id = 0
    for batch_index in range(config.batches):
        regime = _regime(batch_index, config)
        batch: list[LearnedKernelTask] = []
        for _ in range(config.tasks_per_batch):
            draw = rng.random()
            kind = next(kind for kind, boundary in boundaries if draw <= boundary)
            family = rng.randrange(2)
            value = rng.choice((1.0, 2.0, 3.0))
            consequence = rng.choice((0.5, 1.0, 2.0))
            authorized = rng.random() < 0.80 if kind == "external" else True

            if kind == "research":
                candidate_prior, primary_false, secondary_true, secondary_false = _research_parameters(family, regime)
                candidate_correct = rng.random() < candidate_prior
                visible_approved = candidate_correct or rng.random() < primary_false
                secondary_approved = (
                    rng.random() < secondary_true if candidate_correct else rng.random() < secondary_false
                )
                base_reliability = enhanced_reliability = 0.0
            else:
                base_reliability, enhanced_reliability = _work_parameters(kind, family, regime)
                candidate_prior = primary_false = secondary_true = secondary_false = 0.0
                candidate_correct = visible_approved = secondary_approved = False

            batch.append(
                LearnedKernelTask(
                    task_id=task_id,
                    batch=batch_index,
                    kind=kind,
                    family=family,
                    value=value,
                    consequence=consequence,
                    authorized=authorized,
                    base_reliability=base_reliability,
                    enhanced_reliability=enhanced_reliability,
                    candidate_prior=candidate_prior,
                    primary_false_approve=primary_false,
                    secondary_true_approve=secondary_true,
                    secondary_false_approve=secondary_false,
                    candidate_correct=candidate_correct,
                    visible_approved=visible_approved,
                    secondary_approved=secondary_approved,
                )
            )
            task_id += 1
        batches.append(batch)
    return batches


def _expected_utility(task: LearnedKernelTask, reliability: float, config: LearnedKernelConfig) -> float:
    penalty = (
        config.unsafe_action_penalty * task.consequence
        if task.kind == "external"
        else task.consequence
    )
    return reliability * task.value - (1.0 - reliability) * penalty * task.value


def run_learned_transition_kernel(
    config: LearnedKernelConfig,
    variant: LearnedKernelVariant,
) -> dict[str, float | int]:
    estimator = _Estimator(config, variant.estimator)
    batches = generate_learned_kernel_tasks(config)

    total_utility = 0.0
    false_durable_writes = 0
    unsafe_external_effects = 0
    authority_violations = 0
    blocked_by_authority = 0
    operations = 0
    verifications = 0

    segment_utility: dict[str, float] = defaultdict(float)
    segment_tasks: dict[str, int] = defaultdict(int)
    phase_work: list[dict[tuple[str, int], int]] = [defaultdict(int), defaultdict(int)]
    phase_verify: list[dict[int, int]] = [defaultdict(int), defaultdict(int)]

    for batch in batches:
        proposals: list[tuple[float, int, str]] = []
        for task in batch:
            if task.kind == "research":
                if not task.visible_approved:
                    continue
                p_correct, true_approve, false_approve = estimator.research_estimate(task, variant.oracle)
                expected = (
                    p_correct * true_approve * config.discovery_value * task.value
                    - (1.0 - p_correct) * false_approve * config.false_durable_penalty * task.value
                    - config.verify_cost
                )
                if expected > 0.0:
                    proposals.append((expected, task.task_id, "verify"))
                continue

            if task.kind == "external" and not task.authorized:
                continue

            base, enhanced = estimator.work_estimate(task, variant.oracle)
            gain = (
                _expected_utility(task, enhanced, config)
                - _expected_utility(task, base, config)
                - config.operation_cost
            )
            if gain > 0.0:
                proposals.append((gain, task.task_id, "work"))

        chosen: dict[int, str] = {}
        capacity = config.shared_capacity
        verify_capacity = config.verify_capacity
        for _, task_id, resource in sorted(proposals, key=lambda item: item[0], reverse=True):
            if capacity <= 0:
                break
            if task_id in chosen:
                continue
            if resource == "verify" and verify_capacity <= 0:
                continue
            chosen[task_id] = resource
            capacity -= 1
            if resource == "verify":
                verify_capacity -= 1

        for task in batch:
            phase = _regime(task.batch, config)
            if task.batch < config.shift_batch:
                segment = "pre_shift"
            elif task.batch < config.shift_batch + 60:
                segment = "post_shift_early"
            elif task.batch >= config.batches - 100:
                segment = "post_shift_late"
            else:
                segment = "post_shift_mid"
            segment_tasks[segment] += 1

            if task.kind == "research":
                if not task.visible_approved or chosen.get(task.task_id) != "verify":
                    continue
                utility = -config.verify_cost
                verifications += 1
                phase_verify[phase][task.family] += 1
                if task.secondary_approved:
                    if task.candidate_correct:
                        utility += config.discovery_value * task.value
                    else:
                        utility -= config.false_durable_penalty * task.value
                        false_durable_writes += 1
                total_utility += utility
                segment_utility[segment] += utility

                # Synthetic delayed outcome/audit supplies post-decision learning signal.
                estimator.update_research(task)
                continue

            if task.kind == "external" and not task.authorized:
                blocked_by_authority += 1
                continue

            enhanced = chosen.get(task.task_id) == "work"
            utility = -config.operation_cost if enhanced else 0.0
            if enhanced:
                operations += 1
                phase_work[phase][(task.kind, task.family)] += 1

            reliability = task.enhanced_reliability if enhanced else task.base_reliability
            trial_rng = random.Random(config.seed * 1_000_003 + task.task_id * 37 + 11)
            success = trial_rng.random() < reliability
            if success:
                utility += task.value
            else:
                if task.kind == "external":
                    utility -= config.unsafe_action_penalty * task.consequence * task.value
                    unsafe_external_effects += 1
                else:
                    utility -= task.consequence * task.value

            total_utility += utility
            segment_utility[segment] += utility
            estimator.update_work(task, enhanced, success)

    total_tasks = config.batches * config.tasks_per_batch
    phase_tasks = (
        config.shift_batch * config.tasks_per_batch,
        (config.batches - config.shift_batch) * config.tasks_per_batch,
    )

    metrics: dict[str, float | int] = {
        "net_utility_per_task": total_utility / total_tasks,
        "false_durable_writes": false_durable_writes,
        "unsafe_external_effects": unsafe_external_effects,
        "authority_violations": authority_violations,
        "blocked_by_authority": blocked_by_authority,
        "operations_per_task": operations / total_tasks,
        "verifications_per_task": verifications / total_tasks,
    }
    for segment in ("pre_shift", "post_shift_early", "post_shift_mid", "post_shift_late"):
        metrics[f"{segment}_utility"] = segment_utility[segment] / max(1, segment_tasks[segment])
    for phase in (0, 1):
        denominator = max(1, phase_tasks[phase])
        for family in (0, 1):
            metrics[f"phase{phase}_coupled_family{family}_work_rate"] = (
                phase_work[phase][("coupled", family)] / denominator
            )
            metrics[f"phase{phase}_verify_family{family}_rate"] = (
                phase_verify[phase][family] / denominator
            )
    return metrics


def run_learned_transition_experiment(
    config: LearnedKernelConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [(variant.name, run_learned_transition_kernel(config, variant)) for variant in VARIANTS]
