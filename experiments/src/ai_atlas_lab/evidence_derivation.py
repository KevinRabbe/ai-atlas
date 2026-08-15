from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DerivationEstimate:
    parent_source: str
    child_source: str
    score: float
    inherits_failures: bool
    confidence: float
    context_key: str | None = None


class EvidenceDerivationModel:
    """Revisable directional model of error/evidence inheritance.

    This relation is intentionally distinct from symmetric shared-failure
    dependence. `parent -> child` means the child's errors are disproportionately
    contained within the parent's errors while the child may sometimes repair or
    independently revise the upstream result.

    The current estimator is a model-free experimental mechanism, not a selected
    causal-discovery implementation.
    """

    def __init__(
        self,
        *,
        decay: float = 0.995,
        direction_threshold: float = 0.20,
        min_parent_error_gap: float = 0.015,
        confidence_scale: float = 0.20,
        prior_error: float = 0.15,
    ) -> None:
        if not 0.0 < decay < 1.0:
            raise ValueError("decay must lie in (0, 1)")
        if direction_threshold < 0.0:
            raise ValueError("direction_threshold cannot be negative")
        if min_parent_error_gap < 0.0:
            raise ValueError("min_parent_error_gap cannot be negative")
        if confidence_scale <= 0.0:
            raise ValueError("confidence_scale must be positive")
        if not 0.0 <= prior_error <= 1.0:
            raise ValueError("prior_error must lie in [0, 1]")

        self.decay = decay
        self.direction_threshold = direction_threshold
        self.min_parent_error_gap = min_parent_error_gap
        self.confidence_scale = confidence_scale
        self.prior_error = prior_error
        self.sources: set[str] = set()
        self.error_rate: dict[str, dict[str, float]] = {}
        self.joint_error: dict[str, dict[tuple[str, str], float]] = {}

    def register_source(self, source_id: str) -> None:
        if not source_id:
            raise ValueError("source identity must be non-empty")
        if source_id in self.sources:
            return
        existing = sorted(self.sources)
        self.sources.add(source_id)
        for context, rates in self.error_rate.items():
            rates[source_id] = self.prior_error
            for other in existing:
                pair = tuple(sorted((source_id, other)))
                self.joint_error[context][pair] = self.prior_error**2

    def _require_source(self, source_id: str) -> None:
        if source_id not in self.sources:
            raise KeyError(f"unknown source {source_id!r}")

    def _ensure_context(self, context_key: str) -> None:
        if not context_key:
            raise ValueError("context_key must be non-empty")
        if context_key in self.error_rate:
            return
        ordered = sorted(self.sources)
        self.error_rate[context_key] = {
            source: self.prior_error for source in ordered
        }
        self.joint_error[context_key] = {
            (left, right): self.prior_error**2
            for index, left in enumerate(ordered)
            for right in ordered[index + 1 :]
        }

    def _pair(self, left: str, right: str) -> tuple[str, str]:
        self._require_source(left)
        self._require_source(right)
        return tuple(sorted((left, right)))

    def observe_resolution(
        self,
        labels: dict[str, bool],
        truth: bool,
        *,
        context_key: str = "default",
    ) -> None:
        if len(labels) < 2:
            raise ValueError("derivation learning requires at least two sources")
        for source in labels:
            self._require_source(source)
        self._ensure_context(context_key)

        errors = {source: int(label != truth) for source, label in labels.items()}
        decay = self.decay
        rates = self.error_rate[context_key]
        joints = self.joint_error[context_key]
        for source, error in errors.items():
            rates[source] = decay * rates[source] + (1.0 - decay) * error
        ordered = sorted(errors)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                pair = (left, right)
                if pair not in joints:
                    joints[pair] = self.prior_error**2
                joints[pair] = (
                    decay * joints[pair]
                    + (1.0 - decay) * errors[left] * errors[right]
                )

    def direction_score(
        self,
        parent: str,
        child: str,
        *,
        context_key: str | None = None,
    ) -> float:
        if parent == child:
            self._require_source(parent)
            return -1.0
        pair = self._pair(parent, child)
        if not self.error_rate:
            return -1.0

        contexts = (
            (context_key,)
            if context_key is not None
            else tuple(self.error_rate)
        )
        scores: list[float] = []
        for context in contexts:
            if context not in self.error_rate:
                continue
            rates = self.error_rate[context]
            child_error = max(rates[child], 1e-9)
            accuracy_gap = rates[parent] - rates[child]
            if accuracy_gap <= self.min_parent_error_gap:
                scores.append(-1.0)
                continue
            joint = self.joint_error[context].get(pair, self.prior_error**2)
            parent_given_child_error = joint / child_error
            scores.append(parent_given_child_error - rates[parent])
        return sum(scores) / len(scores) if scores else -1.0

    def estimate(
        self,
        parent: str,
        child: str,
        *,
        context_key: str | None = None,
    ) -> DerivationEstimate:
        score = self.direction_score(
            parent,
            child,
            context_key=context_key,
        )
        confidence = min(
            1.0,
            max(0.0, abs(score - self.direction_threshold) / self.confidence_scale),
        )
        return DerivationEstimate(
            parent_source=parent,
            child_source=child,
            score=score,
            inherits_failures=score > self.direction_threshold,
            confidence=confidence,
            context_key=context_key,
        )

    def inferred_parent(
        self,
        child: str,
        *,
        context_key: str | None = None,
    ) -> str | None:
        self._require_source(child)
        candidates = [
            self.estimate(parent, child, context_key=context_key)
            for parent in self.sources
            if parent != child
        ]
        if not candidates:
            return None
        best = max(candidates, key=lambda estimate: estimate.score)
        return best.parent_source if best.inherits_failures else None

    def children_of(
        self,
        parent: str,
        *,
        context_key: str | None = None,
    ) -> tuple[str, ...]:
        self._require_source(parent)
        return tuple(
            sorted(
                child
                for child in self.sources
                if child != parent
                and self.estimate(
                    parent,
                    child,
                    context_key=context_key,
                ).inherits_failures
            )
        )
