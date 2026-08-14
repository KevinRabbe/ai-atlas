from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .adaptive_compute import AdaptiveComputeExperimentConfig, run_adaptive_compute_experiment
from .memory import MemoryExperimentConfig, run_memory_experiment


def _write_or_print(data: dict[str, Any], output: str | None) -> None:
    text = json.dumps(data, indent=2, sort_keys=True)
    if output is None:
        print(text)
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    print(path)


def _result_payload(experiment: str, seed: int, rows: list[tuple[str, dict, object]]) -> dict[str, Any]:
    variants = []
    for name, metrics, cost in rows:
        variants.append({"variant": name, "metrics": metrics, "costs": cost.snapshot()})
    return {"schema_version": 1, "experiment": experiment, "seed": seed, "variants": variants}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-atlas-lab")
    sub = parser.add_subparsers(dest="command", required=True)

    memory = sub.add_parser("memory", help="E03: history access versus compressed state")
    memory.add_argument("--seed", type=int, default=0)
    memory.add_argument("--events", type=int, default=240)
    memory.add_argument("--entities", type=int, default=12)
    memory.add_argument("--queries-per-kind", type=int, default=60)
    memory.add_argument("--output")

    adaptive = sub.add_parser("adaptive-compute", help="E05: fixed versus adaptive compute")
    adaptive.add_argument("--seed", type=int, default=0)
    adaptive.add_argument("--tasks", type=int, default=1200)
    adaptive.add_argument("--threshold", type=float, default=1.75)
    adaptive.add_argument("--max-samples", type=int, default=15)
    adaptive.add_argument("--output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "memory":
        config = MemoryExperimentConfig(
            seed=args.seed,
            num_entities=args.entities,
            num_events=args.events,
            current_queries=args.queries_per_kind,
            historical_queries=args.queries_per_kind,
            exact_queries=args.queries_per_kind,
        )
        rows = run_memory_experiment(config)
        _write_or_print(_result_payload("E03_memory_state", args.seed, rows), args.output)
        return

    config = AdaptiveComputeExperimentConfig(
        seed=args.seed,
        task_count=args.tasks,
        threshold=args.threshold,
        max_samples=args.max_samples,
    )
    rows = run_adaptive_compute_experiment(config)
    _write_or_print(_result_payload("E05_adaptive_compute", args.seed, rows), args.output)


if __name__ == "__main__":
    main()
