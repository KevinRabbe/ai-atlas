from __future__ import annotations

from dataclasses import dataclass

from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class DirectionalDependency:
    dependency_id: int
    source_id: int
    target_id: int
    kind: str
    persistent: bool
    created_epoch: int


class DependencyRegistry:
    """Typed directed relationships over stable runtime subject identities.

    A dependency describes one-way required flow from `source_id` to
    `target_id`. The registry never creates the reverse edge, capability
    authority, resource ownership or a shared coordination scope implicitly.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.dependencies: dict[int, DirectionalDependency] = {}
        self._next_dependency_id = 0

    def add(
        self,
        source_id: int,
        target_id: int,
        *,
        kind: str = "information",
        persistent: bool = False,
    ) -> DirectionalDependency:
        self.runtime._require_subject(source_id)
        self.runtime._require_subject(target_id)
        if source_id == target_id:
            raise ValueError("directional dependency requires distinct subjects")

        for dependency in self.dependencies.values():
            if (
                dependency.source_id == source_id
                and dependency.target_id == target_id
                and dependency.kind == kind
            ):
                return dependency

        dependency = DirectionalDependency(
            dependency_id=self._next_dependency_id,
            source_id=source_id,
            target_id=target_id,
            kind=kind,
            persistent=persistent,
            created_epoch=self.runtime.topology_epoch,
        )
        self._next_dependency_id += 1
        self.dependencies[dependency.dependency_id] = dependency
        self.runtime.costs.writes += 1
        return dependency

    def remove(self, dependency_id: int) -> DirectionalDependency:
        dependency = self.dependencies.pop(dependency_id)
        self.runtime.costs.writes += 1
        return dependency

    def outgoing(self, source_id: int) -> tuple[DirectionalDependency, ...]:
        self.runtime._require_subject(source_id)
        self.runtime.costs.reads += 1
        return tuple(
            dependency
            for dependency in self.dependencies.values()
            if dependency.source_id == source_id
        )

    def incoming(self, target_id: int) -> tuple[DirectionalDependency, ...]:
        self.runtime._require_subject(target_id)
        self.runtime.costs.reads += 1
        return tuple(
            dependency
            for dependency in self.dependencies.values()
            if dependency.target_id == target_id
        )

    def reciprocal_pairs(self, *, kind: str | None = None) -> frozenset[frozenset[int]]:
        edges = {
            (dependency.source_id, dependency.target_id)
            for dependency in self.dependencies.values()
            if kind is None or dependency.kind == kind
        }
        pairs = {
            frozenset((left, right))
            for left, right in edges
            if (right, left) in edges and left != right
        }
        return frozenset(pairs)
