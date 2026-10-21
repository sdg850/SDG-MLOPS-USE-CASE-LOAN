# SDG-MLOPS-USE-CASE-LOAN

Caso educativo de **propensión comercial a renovar un préstamo**. El notebook original de `docs/` se transforma en [un notebook delgado](notebooks/01_renovacion_prestamo.ipynb) que utiliza el mismo paquete que CLI, pipeline, MLflow y API. Los datos y los artefactos derivados permanecen fuera de Git.

La organización sigue Cookiecutter Data Science, con el paquete instalado desde `src/`. Las unidades 1–6 del curso se integran por responsabilidad; ya no requieren seis carpetas con puntos de entrada repetidos. Consulta [la estructura](docs/cookiecutter.md), [la correspondencia con el curso](docs/unidades_01_06.md) y [la auditoría del original](docs/refactorizacion.md).

## Preparar Codespaces

Usar Python 3.12 y el entorno del proyecto:

```bash
make install
source .venv/bin/activate
python -m loan_renewal check-env --include-dev
make test
```

Si se configura el entorno manualmente:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,api,mlops]'
python -m ipykernel install --user --name loan-renewal --display-name "Loan renewal (.venv)"
```

Colocar el CSV original separado por `;` en `data/raw/Dataset Renovacion_prestamo.csv`, o indicar otra ruta con `--data`. No sustituirlo por datos sintéticos para reportar resultados del caso. En Jupyter, seleccionar **Loan renewal (.venv)**.

## Ejecutar el flujo

```bash
make pipeline
make notebook
```

También se pueden usar los puntos de entrada del paquete:

```bash
python -m loan_renewal pipeline --tune --track
python -m loan_renewal train --data "data/raw/Dataset Renovacion_prestamo.csv" --output models --reports reports/training --tune --track
python -m loan_renewal predict --model models/model.joblib --input entrada_raw.csv --output reports/predicciones.csv
```

El pipeline valida datos y features, entrena, selecciona mediante validación, calcula la evaluación final, comprueba paridad de recarga y registra el experimento cuando se solicita `--track`. El modelo completo se guarda en `models/model.joblib`; métricas, comparación y manifiesto quedan en `reports/training/`.

`entrada_raw.csv` usa `;` y las 19 variables originales del contrato. No construir logs, dummies ni clusters a mano. Las columnas requeridas ausentes generan error; las categorías nuevas utilizan el encoder persistido.

## Experimentos y MLflow

```bash
python -m loan_renewal experiments base
python -m loan_renewal experiments grid
python -m loan_renewal experiments random
python -m loan_renewal experiments compare
python -m loan_renewal experiments best
python -m loan_renewal experiments registry
```

`python -m loan_renewal experiments all` realiza la secuencia completa. La comparación exige el mismo hash de datos y protocolo y ordena por métricas de validación. El registro conserva umbral, URI exacta y alias `candidato`, y verifica paridad tras recargarlo. Registrar un candidato no lo despliega ni lo aprueba para producción.

El backend compartido es SQLite local:

```bash
mlflow ui --backend-store-uri "sqlite:///$(pwd)/reports/tracking/mlflow.db" --host 127.0.0.1 --port 5000
```

## DVC y reproducción

```bash
python -m loan_renewal version-data --dvc
make dvc
```

El primer comando agrega el CSV a la caché DVC y genera su puntero. `make dvc` reproduce el stage de `dvc.yaml`, que ejecuta el pipeline con tracking y declara el modelo, las métricas y el estado local de tracking. Git conserva únicamente código y metadatos DVC. No se configura un remoto ni se ejecuta `dvc push`: disponer de un puntero no garantiza recuperar los bytes fuera de este Codespace.

## API y Docker

Entrenar primero para disponer de `models/model.joblib`:

```bash
make api
# Alternativa en contenedor:
make docker
```

FastAPI expone `GET /health`, `POST /predecir` y `/docs`. Recibe variables crudas y carga el mismo bundle de entrenamiento. La comprobación de salud falla si el modelo no está listo. Compose monta `models/` como solo lectura y publica el servicio en localhost; los datos y modelos no se incorporan a las capas de la imagen.

## Protocolo de evaluación

Se entrena con enero–junio de 2015, se seleccionan modelo y umbral con julio–agosto y se evalúa el seleccionado con septiembre. Imputación, escalado, categorías, clustering y balanceo se ajustan únicamente con train o con el train de cada fold. F1 positiva es el criterio de selección y Average Precision desempata; ROC-AUC y AP se calculan con scores.

El ajuste opcional conserva GridSearchCV y RandomizedSearchCV con folds temporales internos y presupuesto acotado. SMOTE y XGBoost requieren extras específicos; SMOTE sobre one-hot transformado necesita validación de pertinencia. No volver a elegir candidatos usando resultados de test. El notebook histórico ya exploró todo el CSV: una evaluación prospectiva necesita campañas nuevas.

El score es una salida sin calibración; no determina aprobación ni elegibilidad de crédito. Faltan costes y capacidad de campaña, confirmación de disponibilidad temporal de las variables y evaluación del uso de atributos demográficos antes de un uso operativo.

## Agentes y evidencia

`.agents/skills/` conserva procedimientos y contratos para diseño, pipelines y evaluación. Los especialistas trabajan en áreas asignadas y el coordinador integra y verifica. Las definiciones no implican agentes permanentes ni instalación global.

Las pruebas de contrato, notebook, API, Docker, DVC y Registry comprueban aspectos distintos. Los reportes locales documentan cada ejecución concreta; la presencia de una configuración no demuestra por sí sola que un servicio haya sido ejecutado. Consultar [diccionario](docs/diccionario.md) y [fuentes](docs/fuentes.json) para trazabilidad.
