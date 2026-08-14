from statistics import mean

from ai_atlas_lab.credit_assignment import (
    CreditConfig,
    run_credit_assignment_experiment,
)


def _mean(name, metric, *, reliability=0.78):
    values = []
    for seed in range(6):
        rows = dict(
            run_credit_assignment_experiment(
                CreditConfig(
                    seed=seed,
                    episodes=3500,
                    local_diagnostic_reliability=reliability,
                )
            )
        )
        values.append(rows[name][metric])
    return mean(values)


def test_global_credit_false_blames_correct_stages_on_partial_failures():
    global_false = _mean("global_trajectory", "false_blame_per_episode")
    local_false = _mean("local_diagnostics", "false_blame_per_episode")
    assert global_false > local_false


def test_local_credit_does_not_need_delayed_trajectory_storage():
    local = _mean("local_diagnostics", "retained_items_per_episode")
    global_items = _mean("global_trajectory", "retained_items_per_episode")
    assert local == 0
    assert global_items == CreditConfig().stages


def test_factorized_local_learning_beats_sparse_global_credit():
    local_tail = _mean("local_diagnostics", "tail_success_rate")
    global_tail = _mean("global_trajectory", "tail_success_rate")
    assert local_tail > global_tail + 0.15


def test_hybrid_retains_less_state_than_global_history():
    hybrid = _mean("eligibility_hybrid", "retained_items_per_episode")
    global_items = _mean("global_trajectory", "retained_items_per_episode")
    assert 0 < hybrid < global_items


def test_local_signal_advantage_shrinks_when_diagnostics_are_noisy():
    good_gap = (
        _mean("local_diagnostics", "tail_success_rate", reliability=0.82)
        - _mean("global_trajectory", "tail_success_rate", reliability=0.82)
    )
    weak_gap = (
        _mean("local_diagnostics", "tail_success_rate", reliability=0.55)
        - _mean("global_trajectory", "tail_success_rate", reliability=0.55)
    )
    assert good_gap > weak_gap
