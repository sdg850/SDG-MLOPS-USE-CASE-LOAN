# SDG-MLOPS-USE-CASE-LOAN

Renovación de préstamos: caso educativo de **propensión comercial**, refactorizado desde el notebook original de 186 celdas. El flujo se ejecuta desde CLI o desde [el notebook de 16 celdas](notebooks/Caso_Renovacion_Prestamo_refactorizado.ipynb).

## Adaptación de las unidades 1–6

El proyecto sigue ahora los patrones del repositorio de curso autorizado. Las carpetas `Unidad01` a `Unidad06` son entradas didácticas que reutilizan una sola implementación. Ver [correspondencia y diferencias](docs/unidades_01_06.md).

```bash
source .venv/bin/activate
python -m pip install -e '.[dev,api,mlops]'
python Unidad01/entorno.py --include-dev
python Unidad03/versionar.py --dvc
python Unidad04/run_pipeline.py --tune --track
python Unidad06/pipeline/run_pipeline.py
```

La última orden ejecuta baseline, GridSearch, RandomizedSearch, comparación por validación y registro con alias `candidato`, en SQLite local. La comparación exige hashes del dataset y del protocolo. Las salidas están en `artifacts/course`; el registro no despliega el servicio ni cambia modelos de producción. El baseline y las búsquedas usan la misma partición de evaluación y tienen sus presupuestos documentados.

La base de tracking compartida es `artifacts/mlflow.db`. Puede abrirse localmente con:

```bash
mlflow ui --backend-store-uri "sqlite:///$(pwd)/artifacts/mlflow.db" --host 127.0.0.1 --port 5000
```

Serving con el artefacto de `artifacts/model.joblib`:

```bash
python -m uvicorn loan_renewal.api:app --host 127.0.0.1 --port 8000
docker compose up --build -d
```

La API expone `POST /predecir`, `GET /health` y `/docs`. Los artefactos se montan de solo lectura y el puerto Docker se limita a localhost. DVC agrega el CSV a caché local y crea un puntero; no se configura remoto ni se afirma que los bytes estén respaldados externamente.

## Ejecutar en este Codespace

El entorno preparado está en `.venv` con Python 3.12. El Python global del Codespace puede ser 3.14, por lo que debe activarse el entorno:

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
python -m loan_renewal train --data "data/raw/Dataset Renovacion_prestamo.csv" --output artifacts
```

Para abrir el notebook, seleccionar el kernel **Loan renewal (.venv)**. Desde otro entorno:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m ipykernel install --user --name loan-renewal --display-name "Loan renewal (.venv)"
```

Si el Python 3.12 del Codespace no incluye `ensurepip`, se puede crear el entorno con `python3.12 -m venv --without-pip .venv` y completar `python -m pip --python .venv/bin/python install pip -e '.[dev]'` usando el pip global. El entorno de esta entrega ya está preparado.

Colocar el CSV original separado por punto y coma en `data/raw/Dataset Renovacion_prestamo.csv`. El archivo **no se versiona**; no sustituirlo por datos inventados. El devcontainer fija Python 3.12 para reconstrucciones futuras.

```bash
python scripts/execute_notebook.py notebooks/Caso_Renovacion_Prestamo_refactorizado.ipynb
python -m loan_renewal predict --model artifacts/model.joblib --input entrada_raw.csv --output artifacts/predicciones.csv
```

`entrada_raw.csv` usa `;` y las 19 columnas originales del contrato. Puede incluir `MES`, `CLIENTE` y `FLAG_VENTA`, que se excluyen de los predictores. Las columnas requeridas ausentes generan error. No construir `_LOG`, dummies ni clusters manualmente.

## Organización

| Ruta | Responsabilidad |
|---|---|
| `src/loan_renewal/schema.py` | Contrato de columnas y tipos |
| `src/loan_renewal/data.py` | Carga, validación y corte temporal |
| `src/loan_renewal/features.py` | Logs, imputación, escalado, encoding y KMeans |
| `src/loan_renewal/modeling.py` | Candidatos y muestreo solo en fit |
| `src/loan_renewal/evaluation.py` | Scores, métricas y umbral |
| `src/loan_renewal/pipeline.py` | Orquestación, selección y manifiesto |
| `src/loan_renewal/predict.py` | Inferencia sobre datos raw |
| `tests/` | Contratos, aislamiento de datos y paridad |
| `docs/` | Auditoría por celda y diccionario |
| `.agents/skills/` | Procedimientos recuperados y contratos de agentes |

## Protocolo y cambios respecto del original

Se entrena con enero–junio de 2015, se seleccionan modelo y umbral en julio–agosto y se evalúa el seleccionado en septiembre. Ningún transformer aprende del test. El pipeline completo y el umbral se guardan juntos. El modelo ganador permanece ajustado a train, sin un refit oculto con validación.

Se comparan seis candidatos por defecto: Dummy, tres árboles (sin balanceo, under y over), Random Forest base y regularizado con under. La selección maximiza F1 de renovación en validación; AP desempata. El umbral usa una cuadrícula explícita. Es una comparación acotada, no GridSearch exhaustivo.

Para conservar el ajuste del original, `--tune` agrega un Random Forest elegido por GridSearchCV sobre tres folds temporales internos de train. Cada fold reajusta todas las transformaciones y el muestreo; son cuatro combinaciones (12 ajustes CV y un refit). Después se compara ese candidato con los seis base usando julio–agosto. El notebook habilita esta búsqueda por defecto.

```bash
python -m loan_renewal train --data "data/raw/Dataset Renovacion_prestamo.csv" --output artifacts --tune
```

SMOTE y XGBoost son **extensiones opcionales** y no se incluyen en la corrida base:

```bash
python -m pip install -e '.[smote,xgboost]'
python -m loan_renewal train --data "data/raw/Dataset Renovacion_prestamo.csv" --output artifacts/extended --smote --xgboost
```

No comparar retrospectivamente opciones usando test para escoger. SMOTE interpola también las columnas one-hot transformadas; su pertinencia requiere validación específica.

## Resultados y límites

Las métricas observadas se generan en `artifacts/metrics.json`, con comparación de validación en `comparison.csv` y linaje en `manifest.json`: hash del CSV y código, entorno, semilla, meses, conteos, criterio de selección y hash del artefacto.

El score no está calibrado y no determina aprobación ni elegibilidad de crédito. Faltan costes/capacidad de campaña, confirmación de disponibilidad temporal de features y evaluación de uso de atributos demográficos antes de uso operativo. El análisis histórico ya observó todo el archivo; el nuevo split no convierte septiembre en una campaña prospectiva nunca explorada. No se presenta como sistema productivo.

Ver [auditoría y diferencias metodológicas](docs/refactorizacion.md), [diccionario](docs/diccionario.md) y [fuentes](docs/fuentes.json). El notebook original adjunto permanece como fuente, sin modificaciones. Las tablas de resultados del original no se reutilizan como resultados actuales.

## Agentes y skills

Se recuperaron de las definiciones de la conversación tres procedimientos: diseño, pipeline y ajuste/evaluación. Se usaron agentes de datos/features, modelado y verificación con archivos de trabajo separados. Estas definiciones están versionadas en el proyecto; no implican instalación global de Skills ni procesos permanentes.

El CSV, originales y artefactos no se publican en este repositorio. Los modelos joblib deben cargarse solo cuando su origen sea confiable.
