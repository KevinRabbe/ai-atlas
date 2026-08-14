from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class StructuralDevelopmentConfig:
    seed: int = 0
    units: int = 64
    rounds: int = 600
    candidates_per_round: int = 4
    mutation_cost: float = 0.003
    evaluation_cost: float = 0.0007
    storage_cost: float = 0.00002
    shift_rounds: tuple[int, int] = (200, 400)
    regular_exception_rate: float = 0.08
    irregular_shift_every: int = 40
    irregular_flip_count: int = 8


def _regular_targets(config: StructuralDevelopmentConfig) -> list[tuple[int, ...]]:
    rng = random.Random(config.seed)
    exceptions = {
        index
        for index in range(config.units)
        if rng.random() < config.regular_exception_rate
    }
    targets: list[tuple[int, ...]] = []
    for step in range(config.rounds):
        template = 0 if step < config.shift_rounds[0] else 1 if step < config.shift_rounds[1] else 0
        targets.append(
            tuple(template ^ int(index in exceptions) for index in range(config.units))
        )
    return targets


def _irregular_targets(config: StructuralDevelopmentConfig) -> list[tuple[int, ...]]:
    rng = random.Random(config.seed + 999)
    current = [rng.randrange(2) for _ in range(config.units)]
    targets: list[tuple[int, ...]] = []
    for step in range(config.rounds):
        if step > 0 and step % config.irregular_shift_every == 0:
            for index in rng.sample(range(config.units), config.irregular_flip_count):
                current[index] ^= 1
        targets.append(tuple(current))
    return targets


def _match(state: tuple[int, ...], target: tuple[int, ...]) -> float:
    return sum(left == right for left, right in zip(state, target)) / len(target)


class _DirectStructure:
    def __init__(self, units: int) -> None:
        self.bits = [0] * units

    def state(self) -> tuple[int, ...]:
        return tuple(self.bits)

    def parameter_count(self) -> int:
        return len(self.bits)

    def candidates(self, rng: random.Random, count: int) -> list[tuple[str, int | None, tuple[int, ...]]]:
        result = []
        for index in rng.sample(range(len(self.bits)), count):
            candidate = self.bits.copy()
            candidate[index] ^= 1
            result.append(("local", index, tuple(candidate)))
        return result

    def apply(self, candidate: tuple[str, int | None, tuple[int, ...]]) -> None:
        index = candidate[1]
        assert index is not None
        self.bits[index] ^= 1


class _GenerativeStructure:
    def __init__(self, units: int) -> None:
        self.units = units
        self.template = 0
        self.overrides: set[int] = set()

    def state(self) -> tuple[int, ...]:
        return tuple(
            self.template ^ int(index in self.overrides)
            for index in range(self.units)
        )

    def parameter_count(self) -> int:
        return 1 + len(self.overrides)

    def _template_candidate(self) -> tuple[str, int | None, tuple[int, ...]]:
        return (
            "template",
            None,
            tuple(
                (1 - self.template) ^ int(index in self.overrides)
                for index in range(self.units)
            ),
        )

    def _local_candidates(
        self,
        rng: random.Random,
        count: int,
    ) -> list[tuple[str, int | None, tuple[int, ...]]]:
        result = []
        for index in rng.sample(range(self.units), count):
            overrides = set(self.overrides)
            if index in overrides:
                overrides.remove(index)
            else:
                overrides.add(index)
            result.append(
                (
                    "override",
                    index,
                    tuple(
                        self.template ^ int(item in overrides)
                        for item in range(self.units)
                    ),
                )
            )
        return result

    def candidates(
        self,
        rng: random.Random,
        count: int,
        include_template: bool = True,
    ) -> list[tuple[str, int | None, tuple[int, ...]]]:
        if include_template:
            return [self._template_candidate()] + self._local_candidates(rng, count - 1)
        return self._local_candidates(rng, count)

    def apply(self, candidate: tuple[str, int | None, tuple[int, ...]]) -> None:
        kind, index, _ = candidate
        if kind == "template":
            self.template ^= 1
            return
        assert index is not None
        if index in self.overrides:
            self.overrides.remove(index)
        else:
            self.overrides.add(index)


def run_structural_development(
    config: StructuralDevelopmentConfig,
    family: str,
    variant: str,
) -> dict[str, float | int]:
    if family not in {"regular_repeated", "irregular_local"}:
        raise ValueError(f"unknown family: {family}")
    if variant not in {"fixed", "direct", "generative", "adaptive_indirect"}:
        raise ValueError(f"unknown variant: {variant}")

    targets = _regular_targets(config) if family == "regular_repeated" else _irregular_targets(config)
    rng = random.Random(config.seed * 97 + 3)

    if variant == "fixed":
        state = tuple([0] * config.units)
        scores = [_match(state, target) for target in targets]
        utility = sum(score - config.storage_cost * config.units for score in scores)
        shifts = (
            list(config.shift_rounds)
            if family == "regular_repeated"
            else list(range(config.irregular_shift_every, config.rounds, config.irregular_shift_every))
        )
        recovery = sum(
            sum(scores[shift : shift + 10]) / min(10, config.rounds - shift)
            for shift in shifts
        ) / len(shifts)
        return {
            "net_utility_per_round": utility / config.rounds,
            "mean_score": sum(scores) / config.rounds,
            "candidate_evaluations": 0,
            "accepted_mutations": 0,
            "first10_after_shift": recovery,
            "final_parameters": config.units,
        }

    structure: _DirectStructure | _GenerativeStructure
    structure = _DirectStructure(config.units) if variant == "direct" else _GenerativeStructure(config.units)

    total_utility = 0.0
    evaluations = 0
    mutations = 0
    scores: list[float] = []
    previous_score: float | None = None

    for target in targets:
        current_score = _match(structure.state(), target)

        if variant == "adaptive_indirect":
            assert isinstance(structure, _GenerativeStructure)
            coherent_drop = previous_score is not None and previous_score - current_score > 0.25
            candidates = structure.candidates(
                rng,
                config.candidates_per_round,
                include_template=coherent_drop,
            )
        elif variant == "generative":
            assert isinstance(structure, _GenerativeStructure)
            candidates = structure.candidates(rng, config.candidates_per_round, include_template=True)
        else:
            assert isinstance(structure, _DirectStructure)
            candidates = structure.candidates(rng, config.candidates_per_round)

        evaluations += len(candidates)
        best = None
        best_score = current_score
        for candidate in candidates:
            candidate_score = _match(candidate[2], target)
            if candidate_score > best_score:
                best_score = candidate_score
                best = candidate

        if best is not None:
            structure.apply(best)
            mutations += 1
            current_score = best_score

        scores.append(current_score)
        previous_score = current_score
        total_utility += (
            current_score
            - config.evaluation_cost * len(candidates)
            - config.mutation_cost * int(best is not None)
            - config.storage_cost * structure.parameter_count()
        )

    shifts = (
        list(config.shift_rounds)
        if family == "regular_repeated"
        else list(range(config.irregular_shift_every, config.rounds, config.irregular_shift_every))
    )
    recovery = sum(
        sum(scores[shift : shift + 10]) / min(10, config.rounds - shift)
        for shift in shifts
    ) / len(shifts)

    return {
        "net_utility_per_round": total_utility / config.rounds,
        "mean_score": sum(scores) / config.rounds,
        "candidate_evaluations": evaluations,
        "accepted_mutations": mutations,
        "first10_after_shift": recovery,
        "final_parameters": structure.parameter_count(),
    }


def run_structural_development_experiment(
    config: StructuralDevelopmentConfig,
) -> dict[str, list[tuple[str, dict[str, float | int]]]]:
    return {
        family: [
            (variant, run_structural_development(config, family, variant))
            for variant in ("fixed", "direct", "generative", "adaptive_indirect")
        ]
        for family in ("regular_repeated", "irregular_local")
    }
