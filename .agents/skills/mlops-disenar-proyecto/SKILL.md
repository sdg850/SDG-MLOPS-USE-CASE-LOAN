---
name: mlops-disenar-proyecto
description: Refactorizar notebooks y contratos de datos. Usar en el proyecto MLOPS para modularizar, evaluar y reproducir el caso Renovación de Préstamo.
---

# Arquitectura MLOps

Inspeccionar notebook, CSV, diccionario y objetivo de negocio. Separar EDA de ejecución. Definir módulos de datos, features, modelado, evaluación e inferencia. Validar columnas, nulos, tipos y etiqueta. Dividir cronológicamente cuando exista tiempo; no aprender imputación, escalado, categorías ni clustering con validación/test. Persistir preprocesamiento junto al estimador. Mantener EDA en notebook delgado. Declarar diferencias metodológicas y pruebas ejecutadas. No convertir scores comerciales en decisiones de elegibilidad crediticia.

Seguir el contrato de [agente](agents/especialista.md).
