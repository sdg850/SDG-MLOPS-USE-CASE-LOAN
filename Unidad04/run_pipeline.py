"""Unidad 04: orquestación por etapas sobre módulos compartidos."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Unidad 04: ejecutar y registrar etapas del pipeline loan")
    parser.add_argument("--data", type=Path, default=ROOT / "data/raw/Dataset Renovacion_prestamo.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts")
    parser.add_argument("--tune", action="store_true")
    parser.add_argument("--search-method", choices=["grid", "random"], default="grid")
    parser.add_argument("--track", action="store_true")
    args = parser.parse_args(argv)
    from loan_renewal.orchestration import run_stages
    result = run_stages(args.data, args.output, tune=args.tune,
                        search_method=args.search_method, track=args.track)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
