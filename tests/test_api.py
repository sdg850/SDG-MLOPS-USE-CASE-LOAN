"""Serving contracts and offline/API parity on invented records only.

API checks require the optional api extra and httpx. Core-only environments
report these tests as skipped instead of claiming serving has been verified.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from loan_renewal.modeling import build_model
from loan_renewal.predict import predict_frame
from loan_renewal.schema import FEATURE_COLUMNS, NUMERIC_COLUMNS

API_AVAILABLE = importlib.util.find_spec("fastapi") is not None and importlib.util.find_spec("httpx") is not None
if API_AVAILABLE:
    from fastapi.testclient import TestClient
    from loan_renewal.api import ClienteInput, create_app


def synthetic_rows(rows=24):
    """Schema-shaped synthetic input; not copied from the loan source dataset."""
    frame = pd.DataFrame({name: np.arange(rows, dtype=float) + 2 for name in NUMERIC_COLUMNS})
    frame["REGION"] = ["REGION_A" if i % 2 else "REGION_B" for i in range(rows)]
    frame["SEXO"] = ["F" if i % 2 else "M" for i in range(rows)]
    frame["EST_CIVIL"] = ["S" if i % 3 else "C" for i in range(rows)]
    frame["FLAG_LIMA_PROVINCIA"] = np.arange(rows, dtype=float) % 2
    return frame.loc[:, FEATURE_COLUMNS]


@unittest.skipUnless(API_AVAILABLE, "Install .[api] and httpx to execute API tests.")
class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.path = Path(cls.directory.name) / "model.joblib"
        cls.frame = synthetic_rows()
        model = build_model(
            DecisionTreeClassifier(max_depth=3, random_state=42),
            include_cluster=False,
        )
        model.fit(cls.frame.iloc[:16], np.arange(16) % 2)
        cls.bundle = {"pipeline": model, "threshold": 0.7, "manifest": {"winner": "synthetic_tree"}}
        joblib.dump(cls.bundle, cls.path)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def payload(self):
        return self.frame.iloc[17].to_dict()

    def test_required_nullable_fields_match_the_raw_contract(self):
        self.assertEqual(set(ClienteInput.model_fields), set(FEATURE_COLUMNS))
        self.assertTrue(all(field.is_required() for field in ClienteInput.model_fields.values()))
        with TestClient(create_app(self.path)) as client:
            payload = self.payload()
            payload["EDAD"] = None
            payload["REGION"] = None
            self.assertEqual(client.post("/predecir", json=payload).status_code, 200)

    def test_lifespan_loads_once_and_predictions_equal_the_offline_path(self):
        from loan_renewal import api
        with patch.object(api, "load_artifact", wraps=api.load_artifact) as loading:
            with TestClient(create_app(self.path)) as client:
                self.assertEqual(client.get("/").status_code, 200)
                health = client.get("/health")
                self.assertEqual(health.status_code, 200)
                self.assertEqual(health.json()["modelo"], "synthetic_tree")
                for payload in (self.payload(), dict(reversed(list(self.payload().items())))):
                    offline = predict_frame(self.bundle, pd.DataFrame([payload])).iloc[0]
                    response = client.post("/predecir", json=payload)
                    self.assertEqual(response.status_code, 200)
                    output = response.json()
                    self.assertEqual(set(output), {"score_propension", "flag_venta", "umbral", "modelo"})
                    self.assertAlmostEqual(output["score_propension"], offline["probabilidad_renovacion"], places=14)
                    self.assertEqual(output["flag_venta"], int(offline["prediccion_flag_venta"]))
                    self.assertEqual(output["umbral"], 0.7)
                    self.assertEqual(output["modelo"], "synthetic_tree")
                    self.assertNotIn("decision", output)
                self.assertEqual(loading.call_count, 1)

    def test_missing_extra_wrong_type_and_infinite_inputs_are_422_without_echo(self):
        with TestClient(create_app(self.path)) as client:
            payload = self.payload()
            del payload["EDAD"]
            self.assertEqual(client.post("/predecir", json=payload).status_code, 422)
            payload = self.payload()
            payload["CLIENTE"] = "PRIVATE_IDENTIFIER"
            response = client.post("/predecir", json=payload)
            self.assertEqual(response.status_code, 422)
            self.assertNotIn("PRIVATE_IDENTIFIER", response.text)
            payload = self.payload()
            payload["EDAD"] = "PRIVATE_INVALID_VALUE"
            response = client.post("/predecir", json=payload)
            self.assertEqual(response.status_code, 422)
            self.assertNotIn("PRIVATE_INVALID_VALUE", response.text)
            payload = self.payload()
            payload["EDAD"] = float("inf")
            response = client.post(
                "/predecir", content=json.dumps(payload),
                headers={"content-type": "application/json"},
            )
            self.assertEqual(response.status_code, 422)

    def test_missing_or_invalid_artifact_keeps_readiness_503(self):
        for path in (Path(self.directory.name) / "missing.joblib", Path(self.directory.name) / "invalid.joblib"):
            if path.name == "invalid.joblib":
                joblib.dump({"unexpected": True}, path)
            with TestClient(create_app(path)) as client:
                self.assertEqual(client.get("/").status_code, 200)
                self.assertEqual(client.get("/health").status_code, 503)
                self.assertEqual(client.post("/predecir", json=self.payload()).status_code, 503)

    def test_inference_contract_failure_is_sanitized_422(self):
        from loan_renewal import api
        with TestClient(create_app(self.path)) as client:
            with patch.object(api, "predict_frame", side_effect=ValueError("PRIVATE_MODEL_DETAILS")):
                response = client.post("/predecir", json=self.payload())
                self.assertEqual(response.status_code, 422)
                self.assertNotIn("PRIVATE_MODEL_DETAILS", response.text)


if __name__ == "__main__":
    unittest.main()
