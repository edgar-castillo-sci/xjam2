import numpy as np
import sys
from itertools import permutations

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xjam.libjamstd import (
    disc_equivalents as disc_old_std,
    conv2pseudocanonic as conv_std,
)
from xjam.libjamtdm import (
    disc_equivalents as disc_old_tdm,
    conv2pseudocanonic as conv_tdm,
)

from prueba_grupo import (
    canonical_key_std,
    disc_equivalents_canonical_std,
)


def get_funcs(optionx):
    """Devuelve las funciones del paquete correctas según la opción."""
    if optionx in [1, 2, 3, 4]:
        return disc_old_std, conv_std
    else:
        return disc_old_tdm, conv_tdm


# Generación de candidatos

def filas_para_opcion(optionx):
    if optionx == 1:
        opt = ['+0', '+j', '+j']
    elif optionx == 2:
        opt = ['+0', '+j', '+k']
    elif optionx == 3:
        opt = ['+0', '+j', '-j']
    elif optionx == 4:
        opt4a = ['+0', '+j', '-k']
        opt4b = ['+0', '-j', '+k']
        filas = list(set(permutations(opt4a, 3))) + list(set(permutations(opt4b, 3)))
        return [np.array(i) for i in filas]
    elif optionx == 5:
        opt = ['+0', '*j', '(+k-k)']
    elif optionx == 6:
        opt = ['*j', '+k', '-k']
    elif optionx == 7:
        opt7a = ['+0', '*j', '(+k-l)']
        opt7b = ['+0', '*j', '(-k+l)']
        filas = list(set(permutations(opt7a, 3))) + list(set(permutations(opt7b, 3)))
        return [np.array(i) for i in filas]
    elif optionx == 8:
        opt8a = ['*j', '+k', '-l']
        opt8b = ['*j', '-k', '+l']
        filas = list(set(permutations(opt8a, 3))) + list(set(permutations(opt8b, 3)))
        return [np.array(i) for i in filas]
    filas = list(set(permutations(opt, 3)))
    return [np.array(i) for i in filas]


def generar_candidatos(num_layers, optionx):
    disc_old, conv = get_funcs(optionx)
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

        canonicstacks = [conv(ai) for ai in nparraylist]
        arraynorep = disc_old(canonicstacks, optionx, 1)
        arraynorep = disc_old(arraynorep, optionx, 2)

    return nparraylist



# Validación

def validar_opcion(optionx, num_layers):
    disc_old, conv = get_funcs(optionx)

    print(f"  Opción {optionx}, n={num_layers}...", end=" ", flush=True)

    candidatos = generar_candidatos(num_layers, optionx)

    # Método viejo
    candidatos_canonicos = [conv(c.copy()) for c in candidatos]
    viejas = disc_old(candidatos_canonicos, optionx, 1)
    viejas = disc_old(viejas, optionx, 2)

    # Método nuevo
    nuevas = disc_equivalents_canonical_std(candidatos, optionx)

    if len(viejas) != len(nuevas):
        print(f"✗ FALLO: {len(viejas)} vs {len(nuevas)}")
        return False

    keys_viejas = set(canonical_key_std(v, optionx) for v in viejas)
    keys_nuevas = set(canonical_key_std(v, optionx) for v in nuevas)

    if keys_viejas != keys_nuevas:
        print(f"✗ FALLO: clases distintas "
              f"(solo viejo: {len(keys_viejas - keys_nuevas)}, "
              f"solo nuevo: {len(keys_nuevas - keys_viejas)})")
        return False

    print(f"✓ ({len(viejas)} clases)")
    return True
    # 5. Comparar clases (por claves canónicas, no por arrays)
    keys_viejas = set(canonical_key_std(v, optionx) for v in viejas)
    keys_nuevas = set(canonical_key_std(v, optionx) for v in nuevas)

    if keys_viejas != keys_nuevas:
        print(f"✗ FALLO: clases distintas")
        print(f"    solo viejo: {len(keys_viejas - keys_nuevas)}")
        print(f"    solo nuevo: {len(keys_nuevas - keys_viejas)}")
        return False

    print(f"✓ {len(viejas)} clases, claves idénticas")
    return True

if __name__ == "__main__":
    print("=== Validación: método viejo vs método canónico ===\n")

    niveles = [2, 3]
    todas_pasan = True

    for optionx in [1, 2, 3, 4, 5, 6, 7, 8]:
        print(f"Opción {optionx}:")
        for num_layers in niveles:
            if not validar_opcion(optionx, num_layers):
                todas_pasan = False
        print()

    if todas_pasan:
        print("✓ Todas las validaciones pasan.")
    else:
        print("✗ Algunas validaciones fallaron.")
