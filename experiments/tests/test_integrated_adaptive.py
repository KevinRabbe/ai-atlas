from statistics import mean

from ai_atlas_lab.integrated_adaptive import (
    AdaptiveIntegratedConfig,
    run_adaptive_integrated_experiment,
)


def _rows(seed=0, **kwargs):
    return dict(
        run_adaptive_integrated_experiment(
            AdaptiveIntegratedConfig(seed=seed, **kwargs)
        )
    )


def _mean_metric(name: str, metric: str, *, seeds=range(6), **kwargs) -> float:
    values = []
    for seed in seeds:
        values.append(_rows(seed=seed, **kwargs)[name][metric])
    return mean(values)


def test_conditional_estimator_adapts_better_than_frozen_after_quality_drift():
    conditional = _mean_metric(
        "adaptive_conditional", "utility_per_task_regime_1", batches=600
    )
    frozen = _mean_metric(
        "frozen_initial_quality", "utility_per_task_regime_1", batches=600
    )
    assert conditional > frozen + 0.08


def test_conditional_estimator_beats_shared_across_opposed_resource_families():
    conditional = _mean_metric(
        "adaptive_conditional", "net_utility_per_task", batches=600
    )
    shared = _mean_metric(
        "all_shared_quality", "net_utility_per_task", batches=600
    )
    assert conditional > shared + 0.03


def test_conditional_estimator_beats_private_with_limited_per_domain_feedback():
    conditional = _mean_metric(
        "adaptive_conditional", "net_utility_per_task", batches=360
    )
    private = _mean_metric(
        "all_private_quality", "net_utility_per_task", batches=360
    )
    assert conditional > private


def test_adaptive_assurance_reduces_false_knowledge_vs_single_primary():
    adaptive = _mean_metric(
        "adaptive_conditional", "false_durable_writes", batches=600
    )
    primary = _mean_metric(
        "single_primary_verifier", "false_durable_writes", batches=600
    )
    assert adaptive < primary * 0.20


def test_adaptive_assurance_spends_less_than_uniform_double_verification():
    adaptive = _mean_metric(
        "adaptive_conditional", "secondary_verify_per_task", batches=600
    )
    uniform = _mean_metric(
        "uniform_double_verify", "secondary_verify_per_task", batches=600
    )
    assert adaptive < uniform
