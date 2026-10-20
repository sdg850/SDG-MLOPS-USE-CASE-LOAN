# Unidad 06 · Ajuste, comparación y registro

Las entradas de `pipeline/` conservan el orden didáctico de la referencia y delegan a `loan_renewal.course`. No duplican el preprocesamiento ni copian código del caso de default o Picos Intensidad.

| Entrada | Acción compartida |
|---|---|
| `01_base_pipeline.py` | `base`: baseline |
| `02_gridsearch_mlflow.py` | `grid`: búsqueda en cuadrícula y tracking |
| `03_randomsearch_mlflow.py` | `random`: búsqueda aleatoria y tracking |
| `04_comparar_runs.py` | `compare`: comparar evidencia de validación |
| `05_mejor_modelo.py` | `best`: identificar candidato elegible y su artefacto |
| `06_model_registry.py` | `registry`: registro trazable solicitado explícitamente |
| `run_pipeline.py` y `../run_pipeline.py` | `all`: flujo coordinado |

Las entradas de esta unidad registran en MLflow; requieren el extra `mlops`. Para un entrenamiento sin tracking, usar la CLI base de la raíz. Desde la raíz y con `.venv` activo:

```bash
python -m pip install -e '.[mlops]'
python Unidad06/pipeline/01_base_pipeline.py --help
python Unidad06/pipeline/02_gridsearch_mlflow.py --help
python Unidad06/pipeline/03_randomsearch_mlflow.py --help
python Unidad06/run_pipeline.py --help
```

Consultar `--help` de cada entrada para las rutas, URI de tracking y nombre/alias de registro. `run_pipeline.py` ejecuta base, grid, random, selección y registro; cada entrada individual permite ejecutar una parte del recorrido. El baseline y las búsquedas usan el mismo contrato, datos y particiones. El ajuste usa folds temporales expansivos dentro de enero–junio; cada fold aprende sus imputadores, escalas, categorías, clusters y muestreo desde cero. Julio–agosto sirve para selección externa del candidato/umbral, septiembre para evaluación final del seleccionado.

MLflow registra identidad de datos y protocolo, parámetros efectivos, métricas de validación y la URI exacta devuelta del modelo. Una tabla ordenada por test F1 no es un criterio de promoción. Registrar una versión o asignar un alias no despliega el servicio ni acredita monitoreo continuo. Preservar el backend y los artefactos para recuperación; no borrar runs para resolver una interfaz vacía.

Las búsquedas agregan su candidato ajustado al conjunto base y registran el ganador elegido en validación; ese ganador puede seguir siendo un modelo base. El informe de cada run conserva también las métricas del candidato ajustado.
