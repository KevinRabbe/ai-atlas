from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class EvidenceTask:
    task_id: int
    label: int
    signal: float
    seed: int

    def sample(self, sample_index: int) -> float:
        rng = random.Random((self.seed + 1) * 1_000_003 + self.task_id * 1009 + sample_index)
        return rng.gauss(self.label * self.signal, 1.0)


def generate_evidence_tasks(*, seed: int, count: int = 1200) -> tuple[EvidenceTask, ...]:
    rng = random.Random(seed)
    # Mix easy, medium and hard items while hiding class behind the signal strength.
    signals = (1.75, 0.90, 0.45)
    tasks: list[EvidenceTask] = []
    for task_id in range(count):
        tasks.append(
            EvidenceTask(
                task_id=task_id,
                label=1 if rng.random() < 0.5 else -1,
                signal=rng.choice(signals),
                seed=seed,
            )
        )
    return tuple(tasks)
