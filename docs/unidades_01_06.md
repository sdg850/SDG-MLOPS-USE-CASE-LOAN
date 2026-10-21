# Unidades 1–6 integradas en la estructura Cookiecutter

Se toman como referencia los patrones inspeccionados del repositorio de curso `sdg850/SDC-MLOPS-4-FORK`. La adaptación conserva el caso comercial **Renovación de Préstamo**, su etiqueta `FLAG_VENTA` y un único paquete compartido. La referencia utiliza también problemas de default crediticio y Picos Intensidad; sus nombres de columnas, métricas y artefactos no se trasladan como si pertenecieran a este dataset.

## Correspondencia verificable

| Unidad | Ejemplo inspeccionado del curso | Implementación en este repositorio |
|---|---|---|
| 1 | `Unidad01/src/main.py`: entorno, pandas y NumPy | `python -m loan_renewal check-env --include-dev`; `pyproject.toml` y `.devcontainer/` |
| 2 | `Unidad02/src/main.py`: carga, preparación, features y entrenamiento separados | `src/loan_renewal/{data,schema,features,modeling,evaluation,pipeline,predict}.py`; `train` y notebook delgado |
| 3 | `Unidad03/laboratorio/src/train.py` y material de versionamiento: entrenamiento, métricas y trazabilidad | `version-data --dvc`, puntero del CSV, `dvc.yaml`, manifiesto y `tracking.py` |
| 4 | `Unidad04/run_pipeline.py` y `config.py`: etapas secuenciales, configuración, duración y fallo explícito | `python -m loan_renewal pipeline --tune --track`; `orchestration.py`, `config.py` y evidencia en `reports/training/` |
| 5 | `Unidad05/api/app.py`, `schemas.py` y Dockerfile: contratos HTTP, carga al iniciar y contenedor | `src/loan_renewal/api.py`, Dockerfile y Compose de raíz; `/health`, `/predecir` y `/docs` |
| 6 | `02_gridsearch_mlflow.py`, `03_randomsearch_mlflow.py`, `04_comparar_runs.py` y `06_model_registry.py` | `experiments base`, `grid`, `random`, `compare`, `best`, `registry` o `all`; `course.py`, `tracking.py` y `experimentos.py` |

Las unidades son ahora una correspondencia documental. No hay seis carpetas de implementación: los puntos de entrada utilizan el paquete instalado desde `src/` bajo [la organización Cookiecutter](cookiecutter.md).

## Recorrido del caso

Desde la raíz, con `.venv` activado:

```bash
python -m loan_renewal check-env --include-dev
python -m loan_renewal version-data --dvc
python -m loan_renewal pipeline --tune --track
python -m loan_renewal experiments all
docker compose up --build -d
```

La búsqueda y el recorrido completo pueden consumir más tiempo que el entrenamiento base. Para recorrer la unidad 6 por partes, ejecutar `experiments base`, `grid`, `random`, `compare`, `best` y `registry` en ese orden. La API necesita el bundle local de `models/model.joblib`; registrar un candidato en MLflow no cambia automáticamente ese archivo ni despliega el servicio.

`make dvc` reproduce el stage declarado en `dvc.yaml`. El notebook `notebooks/01_renovacion_prestamo.ipynb` ofrece una vista del caso y usa las mismas funciones de datos, pipeline, tracking e inferencia. El original de `docs/` se conserva privado en `references/original/`.

## Adaptaciones metodológicas

### Preparación y separación temporal

En algunos ejemplos del curso la preparación o el balanceo se realiza antes de la evaluación. Aquí train contiene enero–junio de 2015, validación julio–agosto y test septiembre. `MES`, `CLIENTE` y `FLAG_VENTA` no entran como predictores. Cada fold aprende de nuevo imputación, categorías, escalado, clustering y muestreo con su porción de entrenamiento.

Las etapas de ingestión y contrato de features no preajustan una matriz con información del holdout. El objeto persistido conserva todo el preprocesamiento junto al modelo y al umbral. El análisis histórico del notebook ya observó el CSV completo; la nueva separación evita nuevas fugas computacionales, pero no elimina ese conocimiento previo.

### Búsqueda, métricas y selección

La referencia de unidad 6 carga datos ya balanceados desde un pickle y muestra grids amplios. La adaptación usa folds temporales internos y un presupuesto acotado; el balanceo reside dentro de `fit`. GridSearchCV y RandomizedSearchCV son candidatos bajo el mismo protocolo, no pruebas sobre un test distinto para cada método.

La selección utiliza F1 positiva de validación, con Average Precision como desempate, y elige el umbral en validación. ROC-AUC usa scores. Las métricas de test son reporte final del candidato fijado y no participan en la ordenación de runs. Comparar ejecuciones exige hashes compatibles de datos y protocolo; un run fallido, vacío o sin modelo no es elegible.

### MLflow, Registry y DVC

MLflow usa la URI SQLite absoluta de `reports/tracking/mlflow.db`. Cada run conserva parámetros, métricas calculadas, identidad del dataset y protocolo, umbral y pipeline. Se utiliza la URI exacta devuelta por MLflow y se comprueba paridad al recargar.

Registry utiliza el alias reversible `candidato`, con metadatos del umbral y linaje; no equivale a promover a producción. DVC versiona identidad y reproducción del dataset/pipeline. Agregar a caché o guardar un puntero no significa haber publicado ni respaldado los bytes en un remoto.

### API y Docker

La API recibe las 19 variables originales y transforma con el bundle compartido. No requiere crear logs, dummies o clusters manualmente y no emite decisiones de elegibilidad crediticia. Distingue entradas inválidas de un modelo no disponible mediante códigos HTTP adecuados.

El contenedor carga el modelo al iniciar y verifica readiness. A diferencia del ejemplo que copia artefactos a la imagen, este proyecto monta `models/` como solo lectura; los datos de clientes y modelos no se incorporan a las capas públicas. Una respuesta saludable solo demuestra disponibilidad; la prueba de paridad compara además el camino HTTP y el offline.

## Evidencia de ejecución

Las pruebas de funciones, CLI, notebook, DVC, MLflow, Registry y Docker acreditan cosas distintas. Los comandos anteriores describen cómo obtener evidencia; no sustituyen sus resultados. Los informes deben indicar qué se ejecutó, sus resultados y cualquier comprobación pendiente. No se copian métricas ilustrativas del curso ni del notebook original como resultados actuales.
