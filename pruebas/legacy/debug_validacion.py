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
    canonical_key_std,
    disc_equivalents_canonical_std,
    generar_grupo_std,
)


def filas_para_opcion(optionx):
    if optionx == 4:
        opt4a = ['+0', '+j', '-k']
        opt4b = ['+0', '-j', '+k']
        filas = list(set(permutations(opt4a, 3))) + list(set(permutations(opt4b, 3)))
        return [np.array(i) for i in filas]
    raise ValueError("Solo opción 4 en este debug")


def generar_candidatos(num_layers, optionx):
    filsnparray = filas_para_opcion(optionx)
    arraynorep = [np.array(i) for i in filas_para_opcion(optionx)]

    for case in range(2, num_layers + 1, 1):
        if case == 2:
            nparraylist = [np.vstack([ai, newrow])
                           for ai in arraynorep for newrow in filsnparray]
        else:
            down = [np.vstack([ai, newrow])
                    for ai in arraynorep for newrow in filsnparray]
            up = [np.vstack([newrow, ai])
                  for ai in arraynorep for newrow in filsnparray]
            nparraylist = down + up

        canonicstacks = [conv2pseudocanonic(ai) for ai in nparraylist]
        arraynorep = disc_old(canonicstacks, optionx, 1)
        arraynorep = disc_old(arraynorep, optionx, 2)

    return nparraylist


if __name__ == "__main__":
    optionx = 4
    n = 2

    print(f"=== Debug opción {optionx}, n={n} ===")
    print(f"Grupo: {len(generar_grupo_std(optionx))} operaciones")
    print()

    candidatos = generar_candidatos(n, optionx)
    print(f"Candidatos generados: {len(candidatos)}")

    # Método viejo
    candidatos_canonicos = [conv2pseudocanonic(c.copy()) for c in candidatos]
    viejas = disc_old(candidatos_canonicos, optionx, 1)
    viejas = disc_old(viejas, optionx, 2)
    print(f"Método viejo: {len(viejas)} estructuras")

    # Método nuevo
    nuevas = disc_equivalents_canonical_std(candidatos, optionx)
    print(f"Método nuevo: {len(nuevas)} estructuras")
    print()

    # Calcular claves
    keys_viejas = set(canonical_key_std(v, optionx) for v in viejas)
    keys_nuevas = set(canonical_key_std(v, optionx) for v in nuevas)

    print(f"Claves únicas en viejo: {len(keys_viejas)}")
    print(f"Claves únicas en nuevo: {len(keys_nuevas)}")
    print()

    solo_viejo = keys_viejas - keys_nuevas
    solo_nuevo = keys_nuevas - keys_viejas

    print(f"Claves solo en viejo: {len(solo_viejo)}")
    if solo_viejo:
        for k in list(solo_viejo)[:3]:
            print(f"  {k}")
    print()

    print(f"Claves solo en nuevo: {len(solo_nuevo)}")
    if solo_nuevo:
        for k in list(solo_nuevo)[:3]:
            print(f"  {k}")
