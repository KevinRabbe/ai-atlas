from ai_atlas_lab.predictive_breadth_adaptive import (
    AdaptiveBreadthConfig,
    run_adaptive_breadth_experiment,
)


def _rows(config: AdaptiveBreadthConfig):
    return dict(run_adaptive_breadth_experiment(config))


def test_narrow_wins_when_goal_is_stable():
    rows = _rows(
        AdaptiveBreadthConfig(
            segment_lengths=(3000,), goal_switch_probabilities=(0.0,), seed=2
        )
    )
    assert rows["always_narrow"]["net_utility"] > rows["always_broad"]["net_utility"]


def test_broad_wins_when_goal_switches_frequently():
    rows = _rows(
        AdaptiveBreadthConfig(
            segment_lengths=(3000,), goal_switch_probabilities=(0.60,), seed=3
        )
    )
    assert rows["always_broad"]["net_utility"] > rows["always_narrow"]["net_utility"]


def test_adaptive_changes_breadth_with_hidden_regime():
    rows = _rows(AdaptiveBreadthConfig(seed=4))
    adaptive = rows["adaptive_breadth"]
    assert adaptive["broad_fraction_segment_0"] < 0.30
    assert adaptive["broad_fraction_segment_1"] > 0.70
    assert adaptive["broad_fraction_segment_2"] < 0.40


def test_adaptive_is_close_to_best_fixed_policy_over_mixed_regime():
    rows = _rows(AdaptiveBreadthConfig(seed=5))
    best_fixed = max(rows["always_broad"]["net_utility"], rows["always_narrow"]["net_utility"])
    assert rows["adaptive_breadth"]["net_utility"] >= best_fixed - 0.002
