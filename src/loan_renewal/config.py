"""Shared locations for course adapters; no import-time filesystem mutations."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = Path(os.environ.get("LOAN_DATA", ROOT / "data/raw/Dataset Renovacion_prestamo.csv"))
ARTIFACTS = ROOT / "artifacts"
EXPERIMENT = "loan-renewal"


def tracking_uri():
    return "sqlite:///" + str((ARTIFACTS / "mlflow.db").resolve())
