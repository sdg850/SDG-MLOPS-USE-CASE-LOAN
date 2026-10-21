# Validación en Codespaces — 21 de octubre de 2026

Validación de la reorganización en la rama refactor/cookiecutter. Primer checkpoint de estructura y código: 704ff49.

| Comprobación | Ejecución y resultado |
|---|---|
| Pruebas | 31 pruebas aprobadas sin omisiones, con API y MLflow/Registry reales |
| Notebook | make notebook: 18 celdas en kernel Python 3.12 sin errores; tracking y paridad HTTP incluidos |
| Pipeline | Ingestión, contrato de features, entrenamiento, evaluación y tracking completados |
| Experimentos | experiments all: base, grid, random, comparación, selección por validación y Registry completados |
| Registry | LoanRenewal-Propensity, versión 1, alias candidato; paridad tras recarga verificada |
| Docker | make docker con --wait: contenedor saludable y modelo montado desde models/ |
| Servicio | Readiness 200, paridad offline/HTTP con entradas sintéticas y campo ausente 422 |
| DVC | CSV identificado por puntero; dvc repro completado, segundo repro omitido por falta de cambios y dvc status actualizado |
| Fuentes | Los hashes de los cuatro originales coinciden con docs/fuentes.json |
| Git | Notebook versionado sin salidas; fuentes privadas, datos y modelos excluidos |

Se generó la plantilla oficial con CCDS 2.3.0; el commit y parámetros están en cookiecutter-generation.json. Las carpetas Unidad01–Unidad06 se consolidaron en src/loan_renewal y su correspondencia se conserva en unidades_01_06.md.

El notebook original, diccionario y presentación permanecen en references/original; el CSV en data/raw. Los modelos y reportes locales se encuentran en models/ y reports/. Los resultados completos no se publican en Git.

DVC conserva datos/modelo en caché local y metadatos en Git; no se configuró remoto ni se hizo dvc push. La base SQLite y los artefactos mutables de MLflow requieren un respaldo separado y no son salidas DVC. El registro de un candidato y la salud del servicio no acreditan aprobación productiva. Las ejecuciones repiten un protocolo histórico; no constituyen evaluaciones prospectivas independientes.
