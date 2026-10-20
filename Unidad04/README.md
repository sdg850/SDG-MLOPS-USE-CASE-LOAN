# Unidad 04 · Orquestación reproducible por etapas

Desde la raíz y con `.venv` activo:

```bash
python Unidad04/run_pipeline.py
python Unidad04/run_pipeline.py --tune --search-method grid --track
```

`run_pipeline.py` es una entrada delgada a `loan_renewal.orchestration.run_stages`; las etapas y su evidencia se implementan una sola vez en el paquete. Los errores detienen el flujo y conservan la causa; la selección y el test mantienen su separación temporal. Las opciones de tracking requieren el extra correspondiente. Las rutas por defecto se resuelven desde el repositorio, incluso si se ejecuta el script desde otro directorio.

La etapa de features comprueba el contrato; no preajusta una matriz fuera de CV. Entrenamiento aprende transformaciones dentro de cada fold. Evaluación verifica métricas, paridad y gates, conservando los reportes aunque un gate falle.
