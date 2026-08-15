from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DependenceEstimate:
    left_source: str
    right_source: str
    score: float
    same_failure_lineage: bool
    confidence: float
    explicitly_probed: bool
    context_key: str | None = None


class EvidenceDependenceModel:
    """Revisable model of whether visible sources share failure ancestry.

    Source identity, source reliability and source dependence remain separate.
    The model learns residual co-failure after conditioning on caller-supplied
    contexts. A relation can be queried globally across contexts or within one
    claim/domain context, and bounded explicit probes may be global or scoped.

    This is an experimental semantic substrate, not a selected mature causal-
    discovery algorithm.
    """

    def __init__(
        self,
        *,
        decay: float = 0.995,
        covariance_threshold: float = 0.025,
        confidence_scale: float = 0.035,
        prior_error: float = 0.12,
    ) -> None:
        if not 0.0 < decay < 1.0:
            raise ValueError("decay must lie in (0, 1)")
        if covariance_threshold < 0.0:
            raise ValueError("covariance_threshold cannot be negative")
        if confidence_scale <= 0.0:
            raise ValueError("confidence_scale must be positive")
        if not 0.0 <= prior_error <= 1.0:
            raise ValueError("prior_error must lie in [0, 1]")

        self.decay = decay
        self.covariance_threshold = covariance_threshold
        self.confidence_scale = confidence_scale
        self.prior_error = prior_error
        self.sources: set[str] = set()
        self.error_rate: dict[str, dict[str, float]] = {}
        self.joint_error: dict[str, dict[tuple[str, str], float]] = {}
        self.probe_cache: dict[
            tuple[str, str, str | None],
            tuple[bool, int],
        ] = {}

    def register_source(self, source_id: str) -> None:
        if not source_id:
            raise ValueError("source identity must be non-empty")
        if source_id in self.sources:
            return

        existing_sources = sorted(self.sources)
        self.sources.add(source_id)
        for context_key, rates in self.error_rate.items():
            rates[source_id] = self.prior_error
            joints = self.joint_error[context_key]
            for other in existing_sources:
                pair = tuple(sorted((source_id, other)))
                joints[pair] = self.prior_error**2

    def _pair(self, left: str, right: str) -> tuple[str, str]:
        if left not in self.sources or right not in self.sources:
            missing = left if left not in self.sources else right
            raise KeyError(f"unknown source {missing!r}")
        return (left, right) if left <= right else (right, left)

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

    def observe_resolution(
        self,
        labels: dict[str, bool],
        truth: bool,
        *,
        context_key: str = "default",
    ) -> None:
        if len(labels) < 2:
            raise ValueError("dependence learning requires at least two sources")
        for source in labels:
            if source not in self.sources:
                raise KeyError(f"unknown source {source!r}")
        self._ensure_context(context_key)

        errors = {source: int(label != truth) for source, label in labels.items()}
        rates = self.error_rate[context_key]
        joints = self.joint_error[context_key]
        for source, error in errors.items():
            rates[source] = (
                self.decay * rates[source]
                + (1.0 - self.decay) * error
            )
        ordered = sorted(errors)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                pair = (left, right)
                if pair not in joints:
                    joints[pair] = self.prior_error**2
                joint = errors[left] * errors[right]
                joints[pair] = (
                    self.decay * joints[pair]
                    + (1.0 - self.decay) * joint
                )

    def dependence_score(
        self,
        left: str,
        right: str,
        *,
        context_key: str | None = None,
    ) -> float:
        if left == right:
            self._pair(left, right)
            return self.prior_error * (1.0 - self.prior_error)
        left, right = self._pair(left, right)
        if not self.error_rate:
            return 0.0

        contexts = (
            (context_key,)
            if context_key is not None
            else tuple(self.error_rate)
        )
        residuals: list[float] = []
        for current_context in contexts:
            if current_context not in self.error_rate:
                continue
            rates = self.error_rate[current_context]
            joints = self.joint_error[current_context]
            pair = (left, right)
            if pair not in joints:
                continue
            residuals.append(
                joints[pair] - rates[left] * rates[right]
            )
        return sum(residuals) / len(residuals) if residuals else 0.0

    def _cached_probe(
        self,
        pair: tuple[str, str],
        *,
        context_key: str | None,
        step: int,
    ) -> tuple[bool, int] | None:
        if context_key is not None:
            scoped = self.probe_cache.get((pair[0], pair[1], context_key))
            if scoped is not None and scoped[1] >= step:
                return scoped
        global_probe = self.probe_cache.get((pair[0], pair[1], None))
        if global_probe is not None and global_probe[1] >= step:
            return global_probe
        return None

    def estimate(
        self,
        left: str,
        right: str,
        *,
        step: int,
        context_key: str | None = None,
    ) -> DependenceEstimate:
        if step < 0:
            raise ValueError("step cannot be negative")
        if left == right:
            self._pair(left, right)
            return DependenceEstimate(
                left,
                right,
                self.prior_error * (1.0 - self.prior_error),
                True,
                1.0,
                True,
                context_key,
            )

        pair = self._pair(left, right)
        cached = self._cached_probe(
            pair,
            context_key=context_key,
            step=step,
        )
        if cached is not None:
            return DependenceEstimate(
                pair[0],
                pair[1],
                self.dependence_score(
                    *pair,
                    context_key=context_key,
                ),
                cached[0],
                1.0,
                True,
                context_key,
            )

        score = self.dependence_score(
            *pair,
            context_key=context_key,
        )
        confidence = min(
            1.0,
            abs(score - self.covariance_threshold) / self.confidence_scale,
        )
        return DependenceEstimate(
            pair[0],
            pair[1],
            score,
            score > self.covariance_threshold,
            confidence,
            False,
            context_key,
        )

    def remember_probe(
        self,
        left: str,
        right: str,
        *,
        same_failure_lineage: bool,
        step: int,
        ttl: int,
        context_key: str | None = None,
    ) -> None:
        if step < 0 or ttl < 0:
            raise ValueError("step and ttl must be non-negative")
        pair = self._pair(left, right)
        self.probe_cache[(pair[0], pair[1], context_key)] = (
            same_failure_lineage,
            step + ttl,
        )

    def components(
        self,
        source_ids: tuple[str, ...],
        *,
        step: int,
        context_key: str | None = None,
    ) -> dict[str, str]:
        if len(set(source_ids)) != len(source_ids):
            raise ValueError("source_ids must be unique")
        for source in source_ids:
            if source not in self.sources:
                raise KeyError(f"unknown source {source!r}")

        parent = {source: source for source in source_ids}

        def find(source: str) -> str:
            while parent[source] != source:
                parent[source] = parent[parent[source]]
                source = parent[source]
            return source

        def union(left: str, right: str) -> None:
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parent[right_root] = left_root

        for index, left in enumerate(source_ids):
            for right in source_ids[index + 1 :]:
                if self.estimate(
                    left,
                    right,
                    step=step,
                    context_key=context_key,
                ).same_failure_lineage:
                    union(left, right)
        return {source: find(source) for source in source_ids}
