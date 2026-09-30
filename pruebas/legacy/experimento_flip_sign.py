import numpy as np
import sys
from itertools import permutations

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xjam.libjamstd import (
    disc_equivalents as disc_old,
    conv2pseudocanonic,
)

from prueba_grupo import (
    rot, transp, flip, sign, nparray2chain,
    elementos_S3,
)


def construir_grupo(S3, flip_ops, sign_ops):
    """Construye el grupo a partir de S3, las ops de flip y las de sign."""
    ops = []
    for s in S3:
        for f in flip_ops:
            for c in sign_ops:
                def op(a, s=s, f=f, c=c):
                    x = s(a)
                    x = f(x)
                    x = c(x)
                    return x
                ops.append(op)
    return ops


def contar_clases(candidatos, ops):
    """Cuenta clases usando las operaciones dadas."""
    claves = set()
    for a in candidatos:
        cadenas = [nparray2chain(op(a.copy())) for op in ops]
        claves.add(min(cadenas))
    return len(claves)


def generar_estructuras_n(n, optionx):
    from validacion import filas_para_opcion
    filsnparray = filas_para_opcion(optionx)
    arraynorep = [np.array(i) for i in filas_para_opcion(optionx)]
    for case in range(2, n + 1, 1):
        if case == 2:
            nparraylist = [np.vstack([ai, newrow])
                           for ai in arraynorep for newrow in filsnparray]
        else:
            down = [np.vstack([ai, newrow])
                    for ai in arraynorep for newrow in filsnparray]
            up = [np.vstack([newrow, ai])
                  for ai in arraynorep for newrow in filsnparray]
            nparraylist = down + up
        canonic = [conv2pseudocanonic(ai) for ai in nparraylist]
        arraynorep = disc_old(canonic, optionx, 1)
        arraynorep = disc_old(arraynorep, optionx, 2)
    return nparraylist

# Definir grupos candidatos

S3 = elementos_S3()
Z2_id = [lambda a: a]
Z2_flip = [lambda a: a, lambda a: flip(a)]
Z2_sign = [lambda a: a, lambda a: sign(a)]
Z2_flip_sign = [lambda a: a, lambda a: sign(flip(a))]

# Grupo A: solo S3 (12 ops sin flip ni sign)
grupo_A = construir_grupo(S3, Z2_id, Z2_id)

# Grupo B: S3 * flip (12 ops)
grupo_B = construir_grupo(S3, Z2_flip, Z2_id)

# Grupo C: S3 * sign (12 ops)
grupo_C = construir_grupo(S3, Z2_id, Z2_sign)

# Grupo D: S3 * flip * sign (24 ops)
grupo_D = construir_grupo(S3, Z2_flip, Z2_sign)

# Grupo E: S3 * (flip·sign) (12 ops)
grupo_E = construir_grupo(S3, Z2_flip_sign, Z2_id)


if __name__ == "__main__":
    for optionx in [3, 4, 5, 6, 7, 8]:
        print(f"\n=== Opción {optionx} ===")
        candidatos = generar_estructuras_n(2, optionx)
        print(f"  Candidatos: {len(candidatos)}")
        
        for nombre, grupo in [
            ("A: S3 solo", grupo_A),
            ("B: S3 × flip", grupo_B),
            ("C: S3 × sign", grupo_C),
            ("D: S3 × flip × sign", grupo_D),
            ("E: S3 × (flip·sign)", grupo_E),
        ]:
            n = contar_clases(candidatos, grupo)
            print(f"  {nombre}: {n} clases")
