from statistics import mean

from ai_atlas_lab.integrated_assurance import (
    AssuranceConfig,
    run_assurance_allocation_experiment,
    run_evaluator_independence_experiment,
    run_verification_granularity_experiment,
)


def _mean_runner(runner, variant, metric, *, seeds=range(5), **kwargs):
    values = []
    for seed in seeds:
        rows = dict(runner(AssuranceConfig(seed=seed, batches=180), **kwargs))
        values.append(rows[variant][metric])
    return mean(values)


def test_outcome_and_process_checks_catch_different_failure_classes():
    final_process = _mean_runner(
        run_verification_granularity_experiment,
        "outcome_only",
        "process_failure_accept_rate",
    )
    process_final = _mean_runner(
        run_verification_granularity_experiment,
        "process_only",
        "final_failure_accept_rate",
    )
    both_process = _mean_runner(
        run_verification_granularity_experiment,
        "uniform_both",
        "process_failure_accept_rate",
    )
    both_final = _mean_runner(
        run_verification_granularity_experiment,
        "uniform_both",
        "final_failure_accept_rate",
    )
    assert both_process < final_process
    assert both_final < process_final


def test_adaptive_granularity_improves_net_over_uniform_both():
    adaptive = _mean_runner(
        run_verification_granularity_experiment,
        "adaptive_granularity",
        "net_utility_per_task",
    )
    uniform = _mean_runner(
        run_verification_granularity_experiment,
        "uniform_both",
        "net_utility_per_task",
    )
    assert adaptive > uniform


def test_correlated_double_does_not_fix_shared_evaluator_exploit_at_high_pressure():
    correlated = _mean_runner(
        run_evaluator_independence_experiment,
        "correlated_double",
        "exploit_accept_rate",
        search_pressure=16,
    )
    independent = _mean_runner(
        run_evaluator_independence_experiment,
        "independent_double",
        "exploit_accept_rate",
        search_pressure=16,
    )
    assert independent < correlated * 0.25


def test_search_pressure_increases_correlated_evaluator_exploitation():
    low = _mean_runner(
        run_evaluator_independence_experiment,
        "correlated_double",
        "exploit_accept_rate",
        search_pressure=1,
    )
    high = _mean_runner(
        run_evaluator_independence_experiment,
        "correlated_double",
        "exploit_accept_rate",
        search_pressure=16,
    )
    assert high > low * 2.0


def test_explicit_assurance_beats_implicit_self_check():
    explicit = _mean_runner(
        run_assurance_allocation_experiment,
        "explicit_adaptive",
        "net_utility_per_task",
    )
    implicit = _mean_runner(
        run_assurance_allocation_experiment,
        "implicit_self_check",
        "net_utility_per_task",
    )
    assert explicit > implicit


def test_explicit_assurance_uses_less_checking_than_uniform_heavy():
    explicit = _mean_runner(
        run_assurance_allocation_experiment,
        "explicit_adaptive",
        "verification_cost_per_task",
    )
    uniform = _mean_runner(
        run_assurance_allocation_experiment,
        "uniform_heavy",
        "verification_cost_per_task",
    )
    assert explicit < uniform
