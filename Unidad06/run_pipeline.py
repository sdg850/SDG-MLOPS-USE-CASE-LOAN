"""Unidad 06: flujo completo compartido de experimentación y registro."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

if __name__ == "__main__":
    from loan_renewal.course import main
    main("all")
