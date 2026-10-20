---
name: mlops-ajustar-modelos
description: Comparar candidatos con evidencia verificable. Usar en el proyecto MLOPS para modularizar, evaluar y reproducir el caso Renovación de Préstamo.
---

# Evaluación MLOps

Comparar baseline y candidatos en las mismas particiones de validación. Mantener muestreo dentro de cada fold y transformar test con estado train. Definir métrica positiva, umbral y presupuesto antes del ajuste. Calcular ROC-AUC con probabilidades, PR-AUC/AP y precision/recall/F1. Elegir candidato por validación; consultar test final una vez. No confundir probabilidades sin calibración con certezas ni datos sintéticos con reales. Probar recarga y paridad.

Seguir el contrato de [agente](agents/especialista.md).
