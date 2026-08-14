from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
import random


@dataclass(frozen=True)
class MetacognitiveFeedbackConfig:
    seed: int = 0
    tasks: int = 6000
    shift_task: int = 3000
    verify_cost: float = 0.10
    discovery_value: float = 2.0
    false_durable_penalty: float = 8.0
    passive_coverage: float = 0.28
    passive_noise: float = 0.14
    passive_delay_min: int = 8
    passive_delay_max: int = 35
    active_noise: float = 0.03
    active_delay_min: int = 3
    active_delay_max: int = 10
    active_audit_cost: float = 0.07
    decay: float = 0.992
    active_audit_threshold: float = 2.4


@dataclass
class _Rate:
    successes: float = 2.0
    total: float = 3.0

    @property
    def mean(self) -> float:
        return self.successes / self.total

    @property
    def variance_proxy(self) -> float:
        probability = self.mean
        return probability * (1.0 - probability) / (self.total + 1.0)

    def update(self, success: bool, decay: float) -> None:
        self.successes *= decay
        self.total *= decay
        self.successes += float(success)
        self.total += 1.0


class _FeedbackEstimator:
    def __init__(self, config: MetacognitiveFeedbackConfig) -> None:
        self.config = config
        self.visible_correct = [_Rate(), _Rate()]
        self.secondary_true = [_Rate(2.7, 3.0), _Rate(2.7, 3.0)]
        self.secondary_false = [_Rate(0.2, 3.0), _Rate(0.2, 3.0)]

    def expected_verification_utility(self, family: int, value: float) -> float:
        p_correct = self.visible_correct[family].mean
        true_approve = self.secondary_true[family].mean
        false_approve = self.secondary_false[family].mean
        return (
            p_correct * true_approve * self.config.discovery_value * value
            - (1.0 - p_correct)
            * false_approve
            * self.config.false_durable_penalty
            * value
            - self.config.verify_cost
        )

    def uncertainty(self, family: int) -> float:
        return (
            math.sqrt(self.visible_correct[family].variance_proxy)
            + math.sqrt(self.secondary_true[family].variance_proxy)
            + math.sqrt(self.secondary_false[family].variance_proxy)
        )

    def update(
        self,
        family: int,
        audited_correct: bool,
        secondary_approved: bool | None,
    ) -> None:
        self.visible_correct[family].update(audited_correct, self.config.decay)
        if secondary_approved is None:
            return
        target = self.secondary_true if audited_correct else self.secondary_false
        target[family].update(secondary_approved, self.config.decay)


def _family_parameters(family: int, regime: int) -> tuple[float, float, float, float]:
    """candidate-correct, primary-false-approve, secondary-true, secondary-false."""
    if regime == 0:
        return (
            (0.82, 0.03, 0.99, 0.02),
            (0.45, 0.55, 0.92, 0.60),
        )[family]
    return (
        (0.47, 0.50, 0.92, 0.55),
        (0.84, 0.025, 0.99, 0.02),
    )[family]


def run_metacognitive_feedback(
    config: MetacognitiveFeedbackConfig,
    feedback_mode: str,
) -> dict[str, float | int]:
    if feedback_mode not in {"exact", "passive", "active", "none"}:
        raise ValueError(f"unknown feedback mode: {feedback_mode}")

    rng = random.Random(config.seed)
    estimator = _FeedbackEstimator(config)
    # due_task, sequence, family, audited_correct, secondary_approved
    queue: list[tuple[int, int, int, bool, bool | None]] = []
    sequence = 0

    total_utility = 0.0
    false_durable_writes = 0
    correct_durable_writes = 0
    verifications = 0
    active_audits = 0
    feedback_events = 0

    segment_utility = [0.0, 0.0, 0.0]
    segment_count = [0, 0, 0]
    segment_active_audits = [0, 0, 0]

    for task_index in range(config.tasks):
        while queue and queue[0][0] <= task_index:
            _, _, family, audited_correct, secondary_approved = heapq.heappop(queue)
            estimator.update(family, audited_correct, secondary_approved)
            feedback_events += 1

        before = total_utility
        regime = int(task_index >= config.shift_task)
        family = rng.randrange(2)
        value = rng.choice((1.0, 2.0, 4.0))
        (
            candidate_correct_probability,
            primary_false_approve,
            secondary_true_approve,
            secondary_false_approve,
        ) = _family_parameters(family, regime)

        candidate_correct = rng.random() < candidate_correct_probability
        visible_approved = candidate_correct or rng.random() < primary_false_approve
        secondary_approved: bool | None = None

        if visible_approved and estimator.expected_verification_utility(family, value) > 0.0:
            verifications += 1
            total_utility -= config.verify_cost
            secondary_approved = rng.random() < (
                secondary_true_approve if candidate_correct else secondary_false_approve
            )
            if secondary_approved:
                if candidate_correct:
                    total_utility += config.discovery_value * value
                    correct_durable_writes += 1
                else:
                    total_utility -= config.false_durable_penalty * value
                    false_durable_writes += 1

        segment = (
            0
            if task_index < config.shift_task
            else 1
            if task_index < config.shift_task + 500
            else 2
        )

        if visible_approved:
            schedule_feedback = False
            noise = 0.0
            delay_min = delay_max = 0

            if feedback_mode == "exact":
                schedule_feedback = True
                delay_min = delay_max = 8
            elif feedback_mode == "passive":
                schedule_feedback = rng.random() < config.passive_coverage
                noise = config.passive_noise
                delay_min = config.passive_delay_min
                delay_max = config.passive_delay_max
            elif feedback_mode == "active":
                information_value = (
                    estimator.uncertainty(family)
                    * value
                    * config.false_durable_penalty
                )
                buy_audit = information_value > config.active_audit_threshold
                if buy_audit:
                    schedule_feedback = True
                    noise = config.active_noise
                    delay_min = config.active_delay_min
                    delay_max = config.active_delay_max
                    total_utility -= config.active_audit_cost
                    active_audits += 1
                    segment_active_audits[segment] += 1
                else:
                    schedule_feedback = rng.random() < config.passive_coverage
                    noise = config.passive_noise
                    delay_min = config.passive_delay_min
                    delay_max = config.passive_delay_max

            if schedule_feedback:
                audited_correct = candidate_correct
                if rng.random() < noise:
                    audited_correct = not audited_correct
                sequence += 1
                heapq.heappush(
                    queue,
                    (
                        task_index + rng.randint(delay_min, delay_max),
                        sequence,
                        family,
                        audited_correct,
                        secondary_approved,
                    ),
                )

        segment_utility[segment] += total_utility - before
        segment_count[segment] += 1

    return {
        "net_utility_per_task": total_utility / config.tasks,
        "false_durable_writes": false_durable_writes,
        "correct_durable_writes": correct_durable_writes,
        "verifications_per_task": verifications / config.tasks,
        "active_audits_per_task": active_audits / config.tasks,
        "feedback_events_per_task": feedback_events / config.tasks,
        "pre_shift_utility": segment_utility[0] / segment_count[0],
        "early_post_shift_utility": segment_utility[1] / segment_count[1],
        "late_post_shift_utility": segment_utility[2] / segment_count[2],
        "pre_shift_active_audit_rate": segment_active_audits[0] / segment_count[0],
        "early_post_shift_active_audit_rate": segment_active_audits[1] / segment_count[1],
        "late_post_shift_active_audit_rate": segment_active_audits[2] / segment_count[2],
    }


def run_metacognitive_feedback_experiment(
    config: MetacognitiveFeedbackConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        (mode, run_metacognitive_feedback(config, mode))
        for mode in ("exact", "passive", "active", "none")
    ]
