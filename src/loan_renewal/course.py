"""Unit 06 entry points adapted to loan renewal, with one shared implementation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import DATA_PATH, ARTIFACTS, EXPERIMENT, tracking_uri as default_tracking_uri


def _write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def main(action, argv=None):
    """Execute a course action; paths default to the project, never the cwd."""
    parser = argparse.ArgumentParser(description=f"Loan renewal Unit 06: {action}")
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    parser.add_argument("--output", type=Path, default=ARTIFACTS / "course")
    parser.add_argument("--tracking-uri", default=None)
    parser.add_argument("--experiment", default=EXPERIMENT)
    parser.add_argument("--registry-name", default="LoanRenewal-Propensity")
    parser.add_argument("--alias", default="candidato")
    args = parser.parse_args(argv)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    uri = args.tracking_uri or default_tracking_uri()

    def execute_experiment(method):
        from .pipeline import train
        from .tracking import track_report
        destination = output / method
        report = train(args.data, destination, tune=method != "base", search_method="random" if method == "random" else "grid")
        record = track_report(report, destination, tracking_uri=uri, experiment=args.experiment)
        _write(destination / "tracking.json", record)
        return record

    def compare():
        from .experimentos import compare_runs
        source = next((output / name / "tracking.json" for name in ("grid", "random", "base")
                       if (output / name / "tracking.json").exists()), None)
        if source is None:
            raise FileNotFoundError("Run a tracked grid/random experiment before comparison.")
        identity = json.loads(source.read_text())
        records = compare_runs(uri, experiment=args.experiment,
                               dataset_sha256=identity["dataset_sha256"], protocol_id=identity["protocol_id"])
        if not records:
            raise ValueError("No finished comparable runs with valid validation metrics.")
        _write(output / "comparison_runs.json", records)
        return records

    def best():
        record = compare()[0]
        _write(output / "best_run.json", record)
        return record

    def registry():
        from .experimentos import registrar_modelo
        source = output / "best_run.json"
        if not source.exists():
            raise FileNotFoundError("Run 05_mejor_modelo.py before registry.")
        selected = json.loads(source.read_text())
        record = registrar_modelo(selected["model_uri"], args.registry_name,
                                  alias=args.alias, tracking_uri=uri, threshold=selected["threshold"])
        _write(output / "registry.json", record)
        return record

    if action in {"base", "grid", "random"}:
        result = execute_experiment(action)
    elif action == "compare":
        result = compare()
    elif action == "best":
        result = best()
    elif action == "registry":
        result = registry()
    elif action == "all":
        result = {method: execute_experiment(method) for method in ("base", "grid", "random")}
        result["best"] = best()
        result["registry"] = registry()
    else:
        raise ValueError(f"Unknown course action: {action}")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return result
