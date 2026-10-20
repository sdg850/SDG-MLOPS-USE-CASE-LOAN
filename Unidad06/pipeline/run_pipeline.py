"""Compatibility entry matching the reference course's pipeline directory."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

if __name__ == "__main__":
    from loan_renewal.course import main
    main("all")
