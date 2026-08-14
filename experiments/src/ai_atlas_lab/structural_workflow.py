from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class StructuralWorkflowConfig:
    seed: int = 0
    modules: int = 16
    rounds: int = 600
    candidates_per_round: int = 4
    evaluation_cost: float = 0.0008
    mutation_cost: float = 0.0025
    blast_cost: float = 0.00025
    storage_cost: float = 0.00002
    shift_rounds: tuple[int, int] = (200, 400)
    exception_rate: float = 0.10
    irregular_shift_every: int = 30
    irregular_flip_count: int = 3


def _targets(config: StructuralWorkflowConfig, family: str) -> list[tuple[int, ...]]:
    if family == "repeated_workflow":
        rng = random.Random(config.seed + 100)
        exceptions = {
            index
            for index in range(config.modules)
            if rng.random() < config.exception_rate
        }
        result: list[tuple[int, ...]] = []
        for step in range(config.rounds):
            template = 0 if step < config.shift_rounds[0] else 1 if step < config.shift_rounds[1] else 0
            result.append(
                tuple(template ^ int(index in exceptions) for index in range(config.modules))
            )
        return result

    if family != "irregular_workflow":
        raise ValueError(f"unknown family: {family}")

    rng = random.Random(config.seed + 200)
    current = [rng.randrange(2) for _ in range(config.modules)]
    result = []
    for step in range(config.rounds):
        if step > 0 and step % config.irregular_shift_every == 0:
            for index in rng.sample(range(config.modules), config.irregular_flip_count):
                current[index] ^= 1
        result.append(tuple(current))
    return result


def _workflow_metrics(
    state: tuple[int, ...],
    target: tuple[int, ...],
) -> tuple[float, int, int, float]:
    """Score two dependency motifs as an operational workflow rather than a bit match.

    Motif 0 represents a parallel/fork-join dependency pattern. Motif 1 represents
    a serial dependency pattern. Running motif 0 where serial ordering is required
    creates a hard dependency violation; running motif 1 where parallelism is
    expected remains valid but incurs avoidable latency.
    """
    qualities: list[float] = []
    dependency_violations = 0
    latency_mismatches = 0
    for actual, required in zip(state, target):
        if actual == required:
            quality = 1.0
        elif required == 1 and actual == 0:
            quality = 0.45
            dependency_violations += 1
        else:
            quality = 0.75
            latency_mismatches += 1
        qualities.append(quality)

    score = 0.80 * (sum(qualities) / len(qualities)) + 0.20 * min(qualities)
    latency = 1.0 + 0.10 * dependency_violations + 0.06 * latency_mismatches
    return score, dependency_violations, latency_mismatches, latency


class _DirectWorkflow:
    def __init__(self, modules: int) -> None:
        self.modes = [0] * modules

    def state(self) -> tuple[int, ...]:
        return tuple(self.modes)

    def parameter_count(self) -> int:
        return len(self.modes)

    def candidates(
        self,
        rng: random.Random,
        count: int,
    ) -> list[tuple[str, int | None, tuple[int, ...], int]]:
        result = []
        for index in rng.sample(range(len(self.modes)), count):
            candidate = self.modes.copy()
            candidate[index] ^= 1
            result.append(("module", index, tuple(candidate), 1))
        return result

    def apply(self, candidate: tuple[str, int | None, tuple[int, ...], int]) -> None:
        index = candidate[1]
        assert index is not None
        self.modes[index] ^= 1


class _IndirectWorkflow:
    def __init__(self, modules: int) -> None:
        self.modules = modules
        self.template = 0
        self.overrides: set[int] = set()

    def state(self) -> tuple[int, ...]:
        return tuple(
            self.template ^ int(index in self.overrides)
            for index in range(self.modules)
        )

    def parameter_count(self) -> int:
        return 1 + len(self.overrides)

    def candidates(
        self,
        rng: random.Random,
        count: int,
        include_template: bool,
    ) -> list[tuple[str, int | None, tuple[int, ...], int]]:
        result: list[tuple[str, int | None, tuple[int, ...], int]] = []
        local_count = count
        if include_template:
            new_state = tuple(
                (1 - self.template) ^ int(index in self.overrides)
                for index in range(self.modules)
            )
            changed = sum(left != right for left, right in zip(self.state(), new_state))
            result.append(("template", None, new_state, changed))
            local_count -= 1

        for index in rng.sample(range(self.modules), local_count):
            overrides = set(self.overrides)
            if index in overrides:
                overrides.remove(index)
            else:
                overrides.add(index)
            new_state = tuple(
                self.template ^ int(item in overrides)
                for item in range(self.modules)
            )
            result.append(("override", index, new_state, 1))
        return result

    def apply(self, candidate: tuple[str, int | None, tuple[int, ...], int]) -> None:
        kind, index, _, _ = candidate
        if kind == "template":
            self.template ^= 1
            return
        assert index is not None
        if index in self.overrides:
            self.overrides.remove(index)
        else:
            self.overrides.add(index)


def run_structural_workflow(
    config: StructuralWorkflowConfig,
    family: str,
    variant: str,
) -> dict[str, float | int]:
    if variant not in {"fixed", "direct", "generative", "adaptive_indirect"}:
        raise ValueError(f"unknown variant: {variant}")

    targets = _targets(config, family)
    rng = random.Random(config.seed * 991 + 7)
    structure: _DirectWorkflow | _IndirectWorkflow
    structure = _DirectWorkflow(config.modules) if variant in {"fixed", "direct"} else _IndirectWorkflow(config.modules)

    total_utility = 0.0
    scores: list[float] = []
    hard_rates: list[float] = []
    slow_rates: list[float] = []
    latencies: list[float] = []
    accepted_mutations = 0
    changed_modules = 0
    candidate_evaluations = 0
    previous_score: float | None = None

    for target in targets:
        score, hard, slow, latency = _workflow_metrics(structure.state(), target)
        best = None
        candidates: list[tuple[str, int | None, tuple[int, ...], int]] = []

        if variant != "fixed":
            if variant == "direct":
                assert isinstance(structure, _DirectWorkflow)
                candidates = structure.candidates(rng, config.candidates_per_round)
            else:
                assert isinstance(structure, _IndirectWorkflow)
                include_template = variant == "generative"
                if variant == "adaptive_indirect":
                    include_template = previous_score is not None and previous_score - score > 0.20
                candidates = structure.candidates(rng, config.candidates_per_round, include_template)

            candidate_evaluations += len(candidates)
            best_objective = score
            for candidate in candidates:
                candidate_score, _, _, _ = _workflow_metrics(candidate[2], target)
                objective = candidate_score - config.blast_cost * candidate[3]
                if objective > best_objective:
                    best_objective = objective
                    best = candidate

            if best is not None:
                structure.apply(best)
                accepted_mutations += 1
                changed_modules += best[3]
                score, hard, slow, latency = _workflow_metrics(structure.state(), target)

        scores.append(score)
        hard_rates.append(hard / config.modules)
        slow_rates.append(slow / config.modules)
        latencies.append(latency)
        previous_score = score

        total_utility += (
            score
            - config.evaluation_cost * len(candidates)
            - config.mutation_cost * int(best is not None)
            - config.blast_cost * (best[3] if best is not None else 0)
            - config.storage_cost * structure.parameter_count()
        )

    shifts = (
        list(config.shift_rounds)
        if family == "repeated_workflow"
        else list(range(config.irregular_shift_every, config.rounds, config.irregular_shift_every))
    )
    first10 = sum(
        sum(scores[shift : min(config.rounds, shift + 10)]) / min(10, config.rounds - shift)
        for shift in shifts
    ) / len(shifts)

    return {
        "net_utility_per_round": total_utility / config.rounds,
        "mean_workflow_score": sum(scores) / config.rounds,
        "dependency_violation_rate": sum(hard_rates) / config.rounds,
        "latency_mismatch_rate": sum(slow_rates) / config.rounds,
        "mean_latency": sum(latencies) / config.rounds,
        "first10_after_shift": first10,
        "candidate_evaluations": candidate_evaluations,
        "accepted_mutations": accepted_mutations,
        "changed_modules": changed_modules,
        "final_parameters": structure.parameter_count(),
    }


def run_structural_workflow_experiment(
    config: StructuralWorkflowConfig,
) -> dict[str, list[tuple[str, dict[str, float | int]]]]:
    return {
        family: [
            (variant, run_structural_workflow(config, family, variant))
            for variant in ("fixed", "direct", "generative", "adaptive_indirect")
        ]
        for family in ("repeated_workflow", "irregular_workflow")
    }
