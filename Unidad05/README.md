# Unidad 05 · Inferencia local con FastAPI y Docker

La API se implementa en `src/loan_renewal/api.py`; el Dockerfile y `compose.yaml` están en la raíz para reutilizar el mismo paquete y artefacto. Entrenar antes para obtener `artifacts/model.joblib`.

```bash
python -m pip install -e '.[api]'
python -m uvicorn loan_renewal.api:app --host 127.0.0.1 --port 8000
```

- `GET /health`: readiness; devuelve 503 si no se cargó el artefacto.
- `POST /predecir`: acepta las 19 variables predictoras crudas, con claves requeridas; permite null cuando el imputador aprendido puede resolverlo.
- `GET /docs`: contrato OpenAPI interactivo.

La respuesta contiene score de propensión, etiqueta comercial, umbral persistido y modelo. No devuelve decisiones APROBAR/RECHAZAR. El endpoint rechaza metadatos, columnas derivadas, extras y valores no finitos; `predict_frame` del paquete admite metadatos para uso local pero los excluye siempre del modelo.

```bash
docker compose up --build
curl --fail http://127.0.0.1:8000/health
```

Compose publica el puerto solo en loopback y monta los artefactos como lectura. Ni CSV ni modelos se incorporan a las capas de la imagen. El healthcheck verifica errores HTTP, pero no mide calidad predictiva: exigir paridad entre inferencia offline y API con los mismos registros crudos. La documentación del repositorio distingue pruebas realmente ejecutadas y validación Docker pendiente.
