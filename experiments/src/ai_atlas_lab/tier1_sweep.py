from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean, pstdev

from .computation_integration import ComputationIntegrationExperimentConfig, run_computation_integration_experiment
from .control_topology import ControlTopologyExperimentConfig, run_control_topology_experiment
from .representation_interface import RepresentationExperimentConfig, run_representation_experiment


def _aggregate(records: list[dict]) -> dict:
    grouped: dict[tuple[str, str, str], list[float]] = {}
    for record in records:
        experiment = record["experiment"]
        regime = record["regime"]
        for variant, metrics in record["variants"].items():
            for metric, value in metrics.items():
                if isinstance(value, (int, float)):
                    grouped.setdefault((experiment, regime, f"{variant}:{metric}"), []).append(float(value))
    result: dict[str, dict] = {}
    for (experiment, regime, key), values in grouped.items():
        result.setdefault(experiment, {}).setdefault(regime, {})[key] = {"mean": mean(values), "pstdev": pstdev(values), "n": len(values)}
    return result


def run_sweep(seeds: int = 12) -> dict:
    records: list[dict] = []
    for seed in range(seeds):
        for density in (0.04, 0.35, 0.72):
            rows = run_control_topology_experiment(ControlTopologyExperimentConfig(seed=seed, task_count=1000, dependency_density=density))
            records.append({"experiment": "E01", "regime": f"dependency_density={density}", "variants": {name: metrics for name, metrics, _cost in rows}})
        for sharedness in (0.98, 0.75, 0.15):
            rows = run_computation_integration_experiment(ComputationIntegrationExperimentConfig(seed=seed, sharedness=sharedness, train_examples=1200, test_examples_per_task=300, adaptation_examples=240, primary_task_fraction=0.80))
            records.append({"experiment": "E02", "regime": f"sharedness={sharedness}", "variants": {name: metrics for name, metrics, _cost in rows}})
        rows = run_representation_experiment(RepresentationExperimentConfig(seed=seed, state_count=300, corruption_trials=100))
        records.append({"experiment": "E04", "regime": "large_exact_ids+version_shift+corruption", "variants": {name: metrics for name, metrics, _cost in rows}})
    return {"schema_version": 1, "seed_count": seeds, "warning": "Synthetic Tier-1 evidence only; not an architecture selection.", "aggregates": _aggregate(records)}


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m ai_atlas_lab.tier1_sweep")
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--output")
    args = parser.parse_args()
    data = run_sweep(args.seeds)
    text = json.dumps(data, indent=2, sort_keys=True)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        print(path)
    else:
        print(text)


if __name__ == "__main__":
    main()
