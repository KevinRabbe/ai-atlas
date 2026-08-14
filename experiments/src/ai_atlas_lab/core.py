from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CostMeter:
    operations: int = 0
    reads: int = 0
    writes: int = 0
    comparisons: int = 0
    samples: int = 0
    messages: int = 0
    verifications: int = 0

    def add(self, other: "CostMeter") -> None:
        for name in self.__dataclass_fields__:
            setattr(self, name, getattr(self, name) + getattr(other, name))

    def snapshot(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class TraceEvent:
    step: int
    kind: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentResult:
    experiment: str
    variant: str
    seed: int
    metrics: dict[str, float | int]
    costs: dict[str, int]
    trace: list[TraceEvent] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)

    def to_dict(self, include_trace: bool = False) -> dict[str, Any]:
        data = {
            "experiment": self.experiment,
            "variant": self.variant,
            "seed": self.seed,
            "metrics": self.metrics,
            "costs": self.costs,
            "config": self.config,
        }
        if include_trace:
            data["trace"] = [asdict(item) for item in self.trace]
        return data
