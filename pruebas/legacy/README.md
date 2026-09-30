# Scripts legacy

Scripts de exploración que llevaron a la formulación final del método.
Se conservan por trazabilidad, pero no forman parte del flujo de
validación actual.

## Contenido

**`debug_validacion.py`**
Diagnóstico inicial para opción 4, n=2. Mostró que el método actual
devolvía 16 estructuras pero solo 11 clases, bajo la hipótesis
(incorrecta) de sign como operación independiente.

**`diagnostico.py`**
Primer caso concreto de discrepancia (opción 3).

**`experimento_flip_sign.py`**
Comparación de 5 grupos candidatos (S3, S3×flip, S3×sign,
S3×flip×sign, S3×(flip·sign)) contra el método actual.

**`experimento_sign_v2.py`**
Análisis por pares (elemento_arriba, elemento_abajo) por capa.

**`experimento_sign.py`**
Primera versión del análisis. Usaba conjuntos de elementos en lugar
de pares. Resultado descartado.

## Estado

Estos scripts documentan el proceso de exploración. La conclusión
final (sign·flip como simetría vertical, no sign independiente) fue
confirmada por la Dra. Arcudia y está implementada en `../prueba_grupo.py`.

No se mantienen. Si se encuentran bugs, no se corrigen.
