"""Command-line entry points: python -m loan_renewal train|predict."""
from __future__ import annotations

import argparse
import json
import logging


def main(argv=None):
    parser = argparse.ArgumentParser(description="Refactored educational loan-renewal pipeline")
    parser.add_argument("--verbose", action="store_true")
    commands = parser.add_subparsers(dest="command", required=True)
    training = commands.add_parser("train", help="Train, choose using validation and evaluate final test")
    training.add_argument("--data", required=True, help="Semicolon-delimited source CSV")
    training.add_argument("--output", default="artifacts")
    training.add_argument("--seed", type=int, default=42)
    training.add_argument("--no-cluster", action="store_true")
    training.add_argument("--tune", action="store_true", help="Add RandomForest GridSearchCV: 4 combinations x 3 train-internal temporal folds + one refit")
    training.add_argument("--search-method", choices=["grid", "random"], default="grid")
    training.add_argument("--track", action="store_true", help="Log the completed run to local MLflow SQLite")
    training.add_argument("--smote", action="store_true", help="Optional educational SMOTE candidate; requires imbalanced-learn")
    training.add_argument("--xgboost", action="store_true", help="Optional candidate; requires xgboost")
    inference = commands.add_parser("predict", help="Predict raw rows with a trusted complete artifact")
    inference.add_argument("--model", required=True)
    inference.add_argument("--input", required=True, help="Semicolon-delimited raw-input CSV")
    inference.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    if args.command == "train":
        from .pipeline import train
        report = train(args.data, args.output, args.seed, not args.no_cluster, args.smote, args.xgboost, args.tune, args.search_method)
        if args.track:
            from .tracking import track_report
            from .config import tracking_uri
            report["tracking"] = track_report(report, args.output, tracking_uri=tracking_uri())
        print(json.dumps({key: report[key] for key in ("winner", "threshold", "test", "model_path", "reload_prediction_parity")}, ensure_ascii=False, indent=2))
    else:
        from .predict import predict_file
        results = predict_file(args.model, args.input, args.output)
        print(json.dumps({"rows": len(results), "output": args.output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
