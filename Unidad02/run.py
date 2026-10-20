"""Unidad 02: ejecutar los módulos compartidos sin duplicar entrenamiento."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from loan_renewal.__main__ import main as package_main


if __name__ == "__main__":
    package_main(["train", "--data", str(ROOT / "data/raw/Dataset Renovacion_prestamo.csv"),
                  "--output", str(ROOT / "artifacts"), *sys.argv[1:]])
