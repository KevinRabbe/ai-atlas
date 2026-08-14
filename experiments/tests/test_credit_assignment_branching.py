from statistics import mean

from ai_atlas_lab.credit_assignment_branching import (
    BranchCreditConfig,
    run_branch_credit_experiment,
)


def _mean(name, metric, *, reliability=0.80):
    values = []
    for seed in range(6):
        rows = dict(
            run_branch_credit_experiment(
                BranchCreditConfig(
                    seed=seed,
                    episodes=3500,
                    local_diagnostic_reliability=reliability,
                )
            )
        )
        values.append(rows[name][metric])
    return mean(values)


def test_global_credit_updates_causally_inactive_branch():
    assert _mean(
        "global_all_branches",
        "cross_branch_updates_per_episode",
    ) > 0
    assert _mean(
        "branch_factorized",
        "cross_branch_updates_per_episode",
    ) == 0


def test_branch_factorization_improves_learning():
    factorized = _mean("branch_factorized", "tail_success_rate")
    global_tail = _mean("global_all_branches", "tail_success_rate")
    assert factorized > global_tail + 0.10


def test_branch_factorization_halves_delayed_state():
    global_items = _mean(
        "global_all_branches",
        "retained_items_per_episode",
    )
    factorized = _mean(
        "branch_factorized",
        "retained_items_per_episode",
    )
    assert factorized == global_items / 2


def test_eligibility_narrows_credit_within_causal_branch():
    eligibility = _mean("branch_eligibility", "false_blame_per_episode")
    factorized = _mean("branch_factorized", "false_blame_per_episode")
    assert eligibility < factorized


def test_eligibility_retains_less_than_full_selected_branch():
    eligibility = _mean(
        "branch_eligibility",
        "retained_items_per_episode",
    )
    factorized = _mean(
        "branch_factorized",
        "retained_items_per_episode",
    )
    assert 0 < eligibility < factorized
