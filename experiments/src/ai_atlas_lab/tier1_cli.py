from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .computation_integration import ComputationIntegrationExperimentConfig, run_computation_integration_experiment
from .control_topology import ControlTopologyExperimentConfig, run_control_topology_experiment
from .representation_interface import RepresentationExperimentConfig, run_representation_experiment


def _payload(experiment: str, seed: int, rows: list[tuple[str, dict, object]]) -> dict[str, Any]:
    return {"schema_version": 1, "experiment": experiment, "seed": seed, "variants": [{"variant": name, "metrics": metrics, "costs": cost.snapshot()} for name, metrics, cost in rows]}


def _write(data: dict[str, Any], output: str | None) -> None:
    text = json.dumps(data, indent=2, sort_keys=True)
    if output is None:
        print(text)
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    print(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m ai_atlas_lab.tier1_cli")
    sub = parser.add_subparsers(dest="command", required=True)
    control = sub.add_parser("control-topology", help="E01: hierarchical vs distributed allocation")
    control.add_argument("--seed", type=int, default=0)
    control.add_argument("--tasks", type=int, default=1500)
    control.add_argument("--dependency-density", type=float, default=0.25)
    control.add_argument("--price-scale", type=float, default=1.0)
    control.add_argument("--output")
    integration = sub.add_parser("computation-integration", help="E02: integrated vs specialists")
    integration.add_argument("--seed", type=int, default=0)
    integration.add_argument("--sharedness", type=float, default=0.75)
    integration.add_argument("--train-examples", type=int, default=2400)
    integration.add_argument("--test-examples-per-task", type=int, default=500)
    integration.add_argument("--primary-task-fraction", type=float, default=0.70)
    integration.add_argument("--output")
    representation = sub.add_parser("representation", help="E04: internal representation/interface")
    representation.add_argument("--seed", type=int, default=0)
    representation.add_argument("--states", type=int, default=800)
    representation.add_argument("--bandwidth-cap", type=int, default=48)
    representation.add_argument("--corruption-trials", type=int, default=250)
    representation.add_argument("--output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "control-topology":
        rows = run_control_topology_experiment(ControlTopologyExperimentConfig(seed=args.seed, task_count=args.tasks, dependency_density=args.dependency_density, price_scale=args.price_scale))
        _write(_payload("E01_control_topology", args.seed, rows), args.output)
        return
    if args.command == "computation-integration":
        rows = run_computation_integration_experiment(ComputationIntegrationExperimentConfig(seed=args.seed, sharedness=args.sharedness, train_examples=args.train_examples, test_examples_per_task=args.test_examples_per_task, primary_task_fraction=args.primary_task_fraction))
        _write(_payload("E02_computation_integration", args.seed, rows), args.output)
        return
    rows = run_representation_experiment(RepresentationExperimentConfig(seed=args.seed, state_count=args.states, bandwidth_cap_bytes=args.bandwidth_cap, corruption_trials=args.corruption_trials))
    _write(_payload("E04_representation_interface", args.seed, rows), args.output)


if __name__ == "__main__":
    main()
