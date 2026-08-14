from __future__ import annotations

from dataclasses import dataclass
import random

from .core import CostMeter

Candidate = tuple[int, ...]


@dataclass(frozen=True)
class DiscoveryLandscape:
    group_size: int = 3
    group_count: int = 5
    evaluator_defect_bonus: int = 0

    @property
    def width(self) -> int:
        return self.group_size * self.group_count

    @property
    def teacher(self) -> Candidate:
        return (0,) * self.width

    @property
    def optimum(self) -> Candidate:
        return (1,) * self.width

    def hidden_score(self, candidate: Candidate) -> int:
        score = 0
        for group in range(self.group_count):
            start = group * self.group_size
            ones = sum(candidate[start : start + self.group_size])
            if ones == self.group_size:
                score += self.group_size
            elif ones == 0:
                score += self.group_size - 1
            else:
                score += ones - 1
        return score

    def visible_score(self, candidate: Candidate) -> int:
        score = self.hidden_score(candidate)
        if self.evaluator_defect_bonus and candidate[-5:] == (1, 0, 1, 0, 1):
            score += self.evaluator_defect_bonus
        return score

    def descriptor(self, candidate: Candidate) -> tuple[int, ...]:
        return tuple(
            sum(candidate[g * self.group_size : (g + 1) * self.group_size])
            for g in range(self.group_count)
        )

    def mutate_one(self, candidate: Candidate, rng: random.Random) -> Candidate:
        bits = list(candidate)
        idx = rng.randrange(self.width)
        bits[idx] = 1 - bits[idx]
        return tuple(bits)


@dataclass(frozen=True)
class DiscoveryExperimentConfig:
    seed: int = 0
    proposal_budget: int = 1500
    evaluator_defect_bonus: int = 0
    verification_budget: int = 100


@dataclass
class _RunState:
    selected: Candidate
    best_generated_hidden: int
    unique_candidates: set[Candidate]
    rejected_candidates: set[Candidate]
    duplicate_failed_verifications: int = 0
    promotions: int = 0


def _metrics(
    *,
    landscape: DiscoveryLandscape,
    state: _RunState,
    cost: CostMeter,
) -> dict[str, float | int]:
    teacher_hidden = landscape.hidden_score(landscape.teacher)
    selected_hidden = landscape.hidden_score(state.selected)
    selected_visible = landscape.visible_score(state.selected)
    visible_claims_improvement = selected_visible > landscape.visible_score(landscape.teacher)
    false_discovery = int(visible_claims_improvement and selected_hidden <= teacher_hidden)
    return {
        "teacher_frontier": teacher_hidden,
        "selected_hidden_score": selected_hidden,
        "selected_visible_score": selected_visible,
        "best_generated_hidden_score": state.best_generated_hidden,
        "beyond_teacher": int(selected_hidden > teacher_hidden),
        "false_discovery": false_discovery,
        "unique_candidates": len(state.unique_candidates),
        "rejected_candidates": len(state.rejected_candidates),
        "duplicate_failed_verifications": state.duplicate_failed_verifications,
        "promotions": state.promotions,
        "verification_calls": cost.verifications,
    }


def run_teacher_imitation(landscape: DiscoveryLandscape) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    teacher = landscape.teacher
    state = _RunState(
        selected=teacher,
        best_generated_hidden=landscape.hidden_score(teacher),
        unique_candidates={teacher},
        rejected_candidates=set(),
    )
    return _metrics(landscape=landscape, state=state, cost=cost), cost


def run_unguided_search(
    landscape: DiscoveryLandscape,
    *,
    seed: int,
    proposal_budget: int,
) -> tuple[dict[str, float | int], CostMeter]:
    rng = random.Random(seed)
    cost = CostMeter()
    current = landscape.teacher
    unique = {current}
    best_generated_hidden = landscape.hidden_score(current)
    for _ in range(proposal_budget):
        current = landscape.mutate_one(current, rng)
        unique.add(current)
        best_generated_hidden = max(best_generated_hidden, landscape.hidden_score(current))
        cost.operations += 1
        cost.samples += 1
    state = _RunState(
        selected=current,
        best_generated_hidden=best_generated_hidden,
        unique_candidates=unique,
        rejected_candidates=set(),
    )
    return _metrics(landscape=landscape, state=state, cost=cost), cost


def run_greedy_visible(
    landscape: DiscoveryLandscape,
    *,
    seed: int,
    proposal_budget: int,
) -> tuple[dict[str, float | int], CostMeter]:
    rng = random.Random(seed)
    cost = CostMeter()
    current = landscape.teacher
    current_visible = landscape.visible_score(current)
    unique = {current}
    best_generated_hidden = landscape.hidden_score(current)
    for _ in range(proposal_budget):
        candidate = landscape.mutate_one(current, rng)
        unique.add(candidate)
        best_generated_hidden = max(best_generated_hidden, landscape.hidden_score(candidate))
        candidate_visible = landscape.visible_score(candidate)
        cost.operations += 2
        cost.samples += 1
        cost.comparisons += 1
        if candidate_visible > current_visible:
            current = candidate
            current_visible = candidate_visible
            cost.writes += 1
    state = _RunState(
        selected=current,
        best_generated_hidden=best_generated_hidden,
        unique_candidates=unique,
        rejected_candidates=set(),
    )
    return _metrics(landscape=landscape, state=state, cost=cost), cost


def _archive_search(
    landscape: DiscoveryLandscape,
    *,
    seed: int,
    proposal_budget: int,
    verification_budget: int | None,
    remember_rejections: bool,
) -> tuple[_RunState, CostMeter]:
    rng = random.Random(seed)
    cost = CostMeter()
    teacher = landscape.teacher
    archive: dict[tuple[int, ...], Candidate] = {landscape.descriptor(teacher): teacher}
    values: list[Candidate] = [teacher]
    unique = {teacher}
    best_generated_hidden = landscape.hidden_score(teacher)

    consolidated = teacher
    consolidated_hidden = landscape.hidden_score(teacher)
    rejected: set[Candidate] = set()
    failed_seen: set[Candidate] = set()
    duplicate_failed = 0
    promotions = 0

    for _ in range(proposal_budget):
        parent = rng.choice(values)
        candidate = landscape.mutate_one(parent, rng)
        unique.add(candidate)
        hidden_for_measurement = landscape.hidden_score(candidate)
        best_generated_hidden = max(best_generated_hidden, hidden_for_measurement)

        descriptor = landscape.descriptor(candidate)
        old = archive.get(descriptor)
        candidate_visible = landscape.visible_score(candidate)
        old_visible = landscape.visible_score(old) if old is not None else None
        cost.operations += 2
        cost.samples += 1
        if old is None or candidate_visible > old_visible:
            archive[descriptor] = candidate
            values = list(archive.values())
            cost.writes += 1

        if verification_budget is None:
            continue
        if cost.verifications >= verification_budget:
            continue
        if candidate_visible <= consolidated_hidden:
            continue
        if remember_rejections and candidate in rejected:
            continue

        cost.verifications += 1
        candidate_hidden = hidden_for_measurement
        if candidate_hidden > consolidated_hidden:
            consolidated = candidate
            consolidated_hidden = candidate_hidden
            promotions += 1
            cost.writes += 1
        else:
            if candidate in failed_seen:
                duplicate_failed += 1
            failed_seen.add(candidate)
            if remember_rejections:
                rejected.add(candidate)
                cost.writes += 1

    if verification_budget is None:
        selected = max(values, key=landscape.visible_score)
    else:
        selected = consolidated

    return (
        _RunState(
            selected=selected,
            best_generated_hidden=best_generated_hidden,
            unique_candidates=unique,
            rejected_candidates=rejected,
            duplicate_failed_verifications=duplicate_failed,
            promotions=promotions,
        ),
        cost,
    )


def run_diverse_archive(
    landscape: DiscoveryLandscape,
    *,
    seed: int,
    proposal_budget: int,
) -> tuple[dict[str, float | int], CostMeter]:
    state, cost = _archive_search(
        landscape,
        seed=seed,
        proposal_budget=proposal_budget,
        verification_budget=None,
        remember_rejections=False,
    )
    return _metrics(landscape=landscape, state=state, cost=cost), cost


def run_epistemic_lifecycle(
    landscape: DiscoveryLandscape,
    *,
    seed: int,
    proposal_budget: int,
    verification_budget: int,
    remember_rejections: bool = True,
) -> tuple[dict[str, float | int], CostMeter]:
    state, cost = _archive_search(
        landscape,
        seed=seed,
        proposal_budget=proposal_budget,
        verification_budget=verification_budget,
        remember_rejections=remember_rejections,
    )
    return _metrics(landscape=landscape, state=state, cost=cost), cost


def run_discovery_experiment(
    config: DiscoveryExperimentConfig,
) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    landscape = DiscoveryLandscape(evaluator_defect_bonus=config.evaluator_defect_bonus)
    rows = []
    for name, runner in (
        ("teacher_imitation", lambda: run_teacher_imitation(landscape)),
        (
            "unguided_search",
            lambda: run_unguided_search(
                landscape, seed=config.seed, proposal_budget=config.proposal_budget
            ),
        ),
        (
            "greedy_visible",
            lambda: run_greedy_visible(
                landscape, seed=config.seed, proposal_budget=config.proposal_budget
            ),
        ),
        (
            "diverse_archive",
            lambda: run_diverse_archive(
                landscape, seed=config.seed, proposal_budget=config.proposal_budget
            ),
        ),
        (
            "epistemic_lifecycle",
            lambda: run_epistemic_lifecycle(
                landscape,
                seed=config.seed,
                proposal_budget=config.proposal_budget,
                verification_budget=config.verification_budget,
                remember_rejections=True,
            ),
        ),
        (
            "epistemic_no_negative_memory",
            lambda: run_epistemic_lifecycle(
                landscape,
                seed=config.seed,
                proposal_budget=config.proposal_budget,
                verification_budget=config.verification_budget,
                remember_rejections=False,
            ),
        ),
    ):
        metrics, cost = runner()
        rows.append((name, metrics, cost))
    return rows
