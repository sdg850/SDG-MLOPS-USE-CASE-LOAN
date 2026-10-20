# Unidad 03 · Identidad de datos y experimentos

Por defecto solo se calcula el hash del CSV, sin modificar Git o DVC:

```bash
python Unidad03/versionar.py
```

Para crear el puntero DVC local de forma explícita, instalar primero `python -m pip install -e '.[mlops]'` y ejecutar:

```bash
python Unidad03/versionar.py --dvc
```

El script ejecuta `dvc init` cuando no existe `.dvc/` y `dvc add` sobre el CSV del repositorio. No configura un remoto, no hace push y no sube el CSV. Revisar que el puntero `data/raw/*.dvc` no esté ignorado por Git antes de versionar metadatos. Un puntero sin los bytes en caché o remoto no permite recuperar datos perdidos.

El vínculo código/datos/modelo se registra también en `artifacts/manifest.json`. El tracking opcional de experimentos se ofrece en la Unidad 06 con backend MLflow explícito. Conservar secretos y datos fuera del historial público.
