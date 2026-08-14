from ai_atlas_lab.integrated_organism import IntegratedConfig, run_integrated_experiment


def _rows(seed=0, **kwargs):
    return dict(run_integrated_experiment(IntegratedConfig(seed=seed, **kwargs)))


def test_full_avoids_false_durable_knowledge():
    rows = _rows(seed=2, batches=250)
    assert rows["integrated_full"]["false_durable_writes"] == 0
    assert rows["immediate_consolidation"]["false_durable_writes"] > 0


def test_applicability_retrieval_reduces_memory_errors():
    rows = _rows(seed=3, batches=250, stale_conflict_probability=0.55)
    assert rows["integrated_full"]["retrieval_error_rate"] < rows["similarity_retrieval"]["retrieval_error_rate"]


def test_plurality_reduces_harm_when_wrong_commitment_is_expensive():
    rows = _rows(seed=4, batches=250)
    assert rows["integrated_full"]["net_utility_per_task"] > rows["no_plurality"]["net_utility_per_task"]


def test_joint_allocation_beats_first_come_under_scarcity():
    rows = _rows(seed=5, batches=300, deep_retrieval_capacity=1, probe_capacity=1, verify_capacity=1)
    assert rows["integrated_full"]["net_utility_per_task"] > rows["independent_allocation"]["net_utility_per_task"]


def test_full_composition_beats_each_single_ablation_on_default_stream():
    rows = _rows(seed=7, batches=400)
    full = rows["integrated_full"]["net_utility_per_task"]
    for name, metrics in rows.items():
        if name != "integrated_full":
            assert full > metrics["net_utility_per_task"], (name, full, metrics["net_utility_per_task"])
