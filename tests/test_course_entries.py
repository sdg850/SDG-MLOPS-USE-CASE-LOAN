"""CLI contract regressions for the thin course entry points."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CourseEntryTests(unittest.TestCase):
    def test_basic_entries_offer_help_from_an_unrelated_working_directory(self):
        scripts = [
            "Unidad01/entorno.py", "Unidad02/run.py", "Unidad03/versionar.py", "Unidad04/run_pipeline.py",
            "Unidad06/pipeline/01_base_pipeline.py", "Unidad06/pipeline/02_gridsearch_mlflow.py",
            "Unidad06/pipeline/03_randomsearch_mlflow.py", "Unidad06/pipeline/04_comparar_runs.py",
            "Unidad06/pipeline/05_mejor_modelo.py", "Unidad06/pipeline/06_model_registry.py",
            "Unidad06/run_pipeline.py", "Unidad06/pipeline/run_pipeline.py",
        ]
        with tempfile.TemporaryDirectory() as directory:
            for relative in scripts:
                with self.subTest(script=relative):
                    completed = subprocess.run([sys.executable, str(ROOT / relative), "--help"],
                                               cwd=directory, capture_output=True, text=True, timeout=20)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertIn("usage:", completed.stdout)

    def test_versioning_default_only_reports_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "invented.csv"
            fixture.write_text("synthetic;value\n1;2\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "Unidad03/versionar.py"), "--data", str(fixture)],
                cwd=directory, capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["filename"], "invented.csv")
            self.assertEqual(len(report["sha256"]), 64)
            self.assertEqual(sorted(path.name for path in Path(directory).iterdir()), ["invented.csv"])
            self.assertNotIn("dvc", report)


if __name__ == "__main__":
    unittest.main()
