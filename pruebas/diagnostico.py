import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xjam.libjamstd import (
    disc_equivalents as disc_old,
    conv2pseudocanonic,
    cambio_de_signo,
)
from prueba_grupo import (
    generar_grupo_std,
    canonical_key_std,
    disc_equivalents_canonical_std,
)

# ─────────────────────────────────────────────
# Caso: opción 3, n=3, estructura con filas distintas
# ─────────────────────────────────────────────

a = np.array([['+0', '+j', '-j'],
              ['+j', '-j', '+0'],
              ['-j', '+0', '+j']])

b = cambio_de_signo(a.copy())  # sign(a)

print("=== Estructuras ===")
print("a:")
print(a)
print()
print("b = sign(a):")
print(b)
print()

def son_equivalentes_viejo(x, y, optionx):
    """Verifica si x ~ y usando la lógica del método viejo."""
    x_can = conv2pseudocanonic(x.copy())
    y_can = conv2pseudocanonic(y.copy())
    
    # Paso 1: ask_equivalents1
    y1 = np.copy(y_can)
    y4 = np.array(y_can[:, [0, 2, 1]])
    for yi in [y1, y4]:
        if np.array_equal(x_can, yi):
            return True, "eqnum=1"
    
    # Paso 2: ask_equivalents2
    y0 = np.copy(y_can)
    y1 = np.flipud(y0)
    y1 = conv2pseudocanonic(y1)
    y4 = np.array(y1[:, [0, 2, 1]])
    if optionx in [3, 4, 6]:
        y1 = cambio_de_signo(y1)
        y4 = cambio_de_signo(y4)
    for yi in [y1, y4]:
        if np.array_equal(x_can, yi):
            return True, "eqnum=2"
    
    return False, "ninguno"

print("=== Método viejo ===")
print("a canonicalizada:")
print(conv2pseudocanonic(a.copy()))
print()
print("b canonicalizada:")
print(conv2pseudocanonic(b.copy()))
print()
equiv, donde = son_equivalentes_viejo(a, b, 3)
print(f"¿a ~ b según el viejo? {equiv} ({donde})")
print()

# ¿Son equivalentes según el método nuevo?

key_a = canonical_key_std(a, 3)
key_b = canonical_key_std(b, 3)
print("=== Método nuevo ===")
print(f"key(a) = {key_a}")
print(f"key(b) = {key_b}")
print(f"¿a ~ b según el nuevo? {key_a == key_b}")
print()

# ¿Está sign(b) en la órbita de b?

ops = generar_grupo_std(3)
print("=== ¿En qué operación de la órbita cae a? ===")
for i, op in enumerate(ops):
    result = op(b.copy())
    if np.array_equal(result, a):
        print(f"  Operación {i}: a = op_{i}(b)")
        break
else:
    print("  a NO está en la órbita de b (pero las claves coinciden)")
