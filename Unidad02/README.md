# Unidad 02 · Modularización del notebook

La lógica de las 186 celdas originales está separada en `src/loan_renewal/{schema,data,features,modeling,evaluation,pipeline,predict}.py`. El notebook de trabajo llama a ese paquete.

Desde la raíz, con `.venv` activo y el CSV original en `data/raw/`:

```bash
python Unidad02/run.py
python -m unittest discover -s tests -v
```

Se pueden indicar `--data` y `--output`. Esta entrada usa la comparación base sin tuning; el ajuste opcional corresponde a la Unidad 06. El objetivo es renovación comercial, no default.
