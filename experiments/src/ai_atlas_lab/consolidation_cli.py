from __future__ import annotations

import argparse
import json
from pathlib import Path

from .consolidation import ConsolidationExperimentConfig, run_consolidation_experiment


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m ai_atlas_lab.consolidation_cli")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--steps", type=int, default=4000)
    parser.add_argument("--switch-probability", type=float, default=0.012)
    parser.add_argument("--observation-reliability", type=float, default=0.82)
    parser.add_argument("--output")
    args = parser.parse_args()

    rows = run_consolidation_experiment(
        ConsolidationExperimentConfig(
            seed=args.seed,
            steps=args.steps,
            switch_probability=args.switch_probability,
            observation_reliability=args.observation_reliability,
        )
    )
    payload = {
        "schema_version": 1,
        "experiment": "E09_consolidation",
        "seed": args.seed,
        "variants": [
            {"variant": name, "metrics": metrics, "costs": cost.snapshot()}
            for name, metrics, cost in rows
        ],
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        print(path)
    else:
        print(text)


if __name__ == "__main__":
    main()
