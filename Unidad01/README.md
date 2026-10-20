# Unidad 01 · Entorno y repositorio

Comprobar Python y las dependencias, sin instalar paquetes ni modificar credenciales:

```bash
source .venv/bin/activate
python Unidad01/entorno.py --include-dev
```

La verificación devuelve un código distinto de cero si falta una dependencia requerida o Python no satisface el rango del proyecto. La estructura, dependencias y punto de entrada viven en la raíz, no se copian por unidad.
