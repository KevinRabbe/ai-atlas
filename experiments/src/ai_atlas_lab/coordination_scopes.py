from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class CoordinationScope:
    scope_id: int
    members: frozenset[int]
    persistent: bool
    created_epoch: int


class CoordinationScopeRegistry:
    """Non-owning coordination memberships over a TypedScopeRuntime.

    Coordination scopes may overlap. They reference stable runtime subjects but
    do not own evidence, predictive state, resource leases or capability
    authority. Closing a coordination scope therefore cannot delete or transfer
    semantic state.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.scopes: dict[int, CoordinationScope] = {}
        self._next_scope_id = 0

    def create(
        self,
        members: Iterable[int],
        *,
        persistent: bool = False,
    ) -> CoordinationScope:
        member_set = frozenset(members)
        if len(member_set) < 2:
            raise ValueError("coordination scope requires at least two subjects")
        for subject_id in member_set:
            self.runtime._require_subject(subject_id)

        scope = CoordinationScope(
            scope_id=self._next_scope_id,
            members=member_set,
            persistent=persistent,
            created_epoch=self.runtime.topology_epoch,
        )
        self._next_scope_id += 1
        self.scopes[scope.scope_id] = scope
        self.runtime.costs.writes += 1
        self.runtime.costs.messages += len(member_set)
        return scope

    def close(self, scope_id: int) -> CoordinationScope:
        scope = self.scopes.pop(scope_id)
        self.runtime.costs.writes += 1
        self.runtime.costs.messages += len(scope.members)
        return scope

    def for_subject(self, subject_id: int) -> tuple[CoordinationScope, ...]:
        self.runtime._require_subject(subject_id)
        self.runtime.costs.reads += 1
        return tuple(
            scope
            for scope in self.scopes.values()
            if subject_id in scope.members
        )

    def represented_pairs(self) -> frozenset[tuple[int, int]]:
        pairs: set[tuple[int, int]] = set()
        for scope in self.scopes.values():
            members = sorted(scope.members)
            pairs.update(
                (left, right)
                for index, left in enumerate(members)
                for right in members[index + 1 :]
            )
        return frozenset(pairs)
