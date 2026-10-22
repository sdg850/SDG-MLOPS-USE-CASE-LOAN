# Contrato del proyecto

Objetivo: propensión comercial de renovación, no riesgo de default ni decisiones de elegibilidad. Leer docs/refactorizacion.md antes de cambiar protocolo o interpretación.

- Aplicar las skills locales de .agents/skills para diseño, pipelines y evaluación.
- Separar train, validación y test antes de fit de cualquier transformación. No escoger candidatos usando test.
- Aceptar columnas raw; persistir todo preprocessing y umbral con el modelo.
- Mantener fuentes intactas y métricas calculadas, con evidencia de qué se ejecutó.
- No versionar CSV, registros de clientes, originales con salidas, modelos o credenciales.
- Ejecutar python -m unittest discover -s tests -v. Para cambios de ejecución, validar CLI y notebook completo en .venv.
- Roles delegables: datos/features (schema/data/features), modelado (modeling/evaluation/pipeline/predict), verificación (tests/docs); el coordinador integra. Cada agente posee solo sus archivos asignados.

- Estructura CCDS: código en src/loan_renewal, notebook en notebooks, fuentes privadas en references/original, datos en data/raw, modelos en models, informes en reports. No recrear carpetas Unidad01–06; conservar correspondencia en docs.
- Validar CLI, notebook, tracking, DVC y API/Docker tras cambios en rutas; hacer checkpoints Git sin datos ni resultados privados.

- Separación de servicios: entradas en pipelines/, HTTP en api/, estado MLflow privado en mlruns/. Conservar historial al migrar tracking y verificar recarga por alias.
