# Adaptación del flujo de las unidades 01–06

## Alcance

Se revisaron los puntos de entrada, orquestación, API, schemas, Docker y scripts de experimentación de la referencia de curso autorizada. Sus patrones se adaptan al caso **Renovación de Préstamo** mediante módulos propios compartidos. No se copia el código fuente privado ni se publican sus datos. La referencia alterna default crediticio y Picos Intensidad; esta adaptación conserva únicamente `FLAG_VENTA` y el contrato loan.

## Correspondencia y ejecución

| Unidad | Patrón de referencia inspeccionado | Implementación del caso loan | Evidencia esperada |
|---|---|---|---|
| 01 | `Unidad01/src/main.py`: verificación inicial del entorno | `Unidad01/entorno.py`, `pyproject.toml`, devcontainer | Python compatible y dependencias identificadas, código de salida verificable |
| 02 | `Unidad02/src/main.py`: funciones separadas por responsabilidad | `Unidad02/run.py` y `src/loan_renewal/` | Carga validada, módulos ejecutables y pruebas de contrato |
| 03 | Versionamiento de datos y experimentos del curso | `Unidad03/versionar.py`, manifiesto y tracking compartido | Hash del CSV; puntero DVC solo si se solicita; run y modelo ligados a datos/código |
| 04 | `Unidad04/run_pipeline.py`: etapas secuenciales, duración y fallo explícito | `Unidad04/run_pipeline.py` y `loan_renewal.orchestration` | Estado y duración por etapa, fallo trazable y reportes persistidos |
| 05 | `Unidad05/api/app.py`, `schemas.py`, Dockerfile: servicio y readiness | `loan_renewal.api`, Dockerfile y Compose raíz | Schema raw, 422/503 adecuados, paridad con artefacto y prueba del contenedor cuando se ejecute |
| 06 | `02_gridsearch_mlflow.py`, `04_comparar_runs.py`, `06_model_registry.py` | Entradas de `Unidad06/pipeline/`, `course`, `modeling`, `tracking` y `experimentos` | Folds temporales, tracking homogéneo, candidato/URI/versión comprobables |

Activar `.venv` desde la raíz. Ejecutar `python Unidad01/entorno.py --include-dev` y `python -m unittest discover -s tests -v` antes de usar los flujos. Consultar cada README de unidad para su punto de entrada; todos reutilizan el paquete instalado editable.

## Diferencias deliberadas respecto de la referencia

### Separación temporal y estado aprendido

La referencia de Unidad 02 prepara y selecciona variables antes del split; aquí la partición se realiza primero. Train contiene enero–junio, validación julio–agosto y test septiembre de 2015. Ni `MES`, `CLIENTE` ni `FLAG_VENTA` entran como predictores. La configuración de variables heredadas está documentada y no se presenta como descubrimiento independiente de todo conocimiento anterior del CSV.

La Unidad 04 del curso materializa features para separar etapas. Aquí se conserva la separación de responsabilidades y evidencia, pero no se exige escribir una matriz transformada con información del holdout ni duplicar pipelines: el artefacto persistido contiene el transformer completo y el modelo. La etapa de features valida el contrato sin preajustar matrices fuera de CV. La etapa de evaluación verifica métricas, paridad y gates; un fallo de calidad conserva las métricas que lo explican.

### Balanceo y búsqueda

El script de búsqueda de referencia consume datos ya balanceados. En loan, el muestreo reside dentro de `fit` del estimador y se vuelve a aplicar dentro de cada fold, después de aprender únicamente con el train de ese fold. Se usan folds expansivos de meses anteriores, con validación interna en abril, mayo y junio.

El presupuesto acotado de grid por defecto es cuatro combinaciones por tres folds, más un refit; no se hereda el grid de 600 ajustes del otro problema. RandomizedSearch es una alternativa con presupuesto y semilla declarados. El umbral del candidato se elige después en validación externa, sin usar test para comparar métodos.

### Tracking, comparación y Registry

El script de comparación de referencia ordena runs por una métrica F1 calculada en test. La adaptación usa evidencia de **validación** y exige identidad de datos y protocolo compatibles. Un run vacío, fallido, sin artefacto o de otro dataset no se convierte en ganador por ocupar la primera fila.

La URI de tracking debe resolverse explícitamente; el backend local del proyecto no se deduce de una carpeta relativa del terminal. Conservar la URI retornada al registrar el modelo, en lugar de reconstruirla a partir de una convención de nombres. El artefacto mantiene preprocesamiento y umbral junto al estimador. El registro y los alias dependen de la API instalada y no equivalen a un despliegue ni a una aprobación productiva.

### Serving y contenedores

La referencia de default utiliza campos, umbrales y decisiones de riesgo propios de otro problema. La API loan recibe las 19 variables predictoras originales y devuelve propensión comercial; no crea columnas `_LOG`, dummies o clusters a mano y no emite decisiones de crédito. Un campo null es distinto de una clave requerida ausente.

El servicio carga el artefacto una vez durante lifespan y mantiene readiness 503 si no está disponible. Las pruebas funcionales comparan el camino offline y HTTP. Docker usa el mismo paquete; los datos y modelos se montan o conservan fuera de las capas públicas. Los errores HTTP deben hacer fallar el healthcheck. Un `/health` correcto solo acredita disponibilidad.

## Persistencia y límites de evidencia

Los directorios por unidad son entradas didácticas, no seis copias del proyecto. El paquete `src/loan_renewal` es la implementación autoritativa; el notebook es una vista del flujo y los scripts de unidad adaptan sus argumentos. Datos, outputs, caches, credenciales y originales con salidas no se versionan públicamente.

DVC es opt-in: el helper calcula un hash por defecto y solo inicializa/agrega al solicitar `--dvc`. No configura remotos ni ejecuta publicación. Git guarda el puntero; los bytes se recuperan desde una caché o remoto disponible. MLflow es también una dependencia opcional y los resultados solo se afirman cuando se hayan ejecutado.

Las pruebas de funciones, notebook, API, Docker y Registry son evidencias distintas. El reporte de entrega debe indicar cuáles se ejecutaron, sus resultados y qué quedó pendiente, sin convertir la existencia de archivos en prueba de operación completa.
