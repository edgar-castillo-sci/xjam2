import numpy as np
import sys
from itertools import permutations

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xjam.libjamstd import (
    conv2pseudocanonic,
    cambio_de_signo,
    disc_equivalents,
)


# Generación de estructuras

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
    filas = list(set(permutations(opt, 3)))
    return [np.array(i) for i in filas]


def generar_estructuras_n(n, optionx):
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
        arraynorep = disc_equivalents(canonic, optionx, 1)
        arraynorep = disc_equivalents(arraynorep, optionx, 2)
    return nparraylist


# Réplica exacta del método viejo

def son_equivalentes_viejo(x, y, optionx):
    x_can = conv2pseudocanonic(x.copy())
    y_can = conv2pseudocanonic(y.copy())

    # eqnum=1
    y1 = np.copy(y_can)
    y4 = np.array(y_can[:, [0, 2, 1]])
    for yi in [y1, y4]:
        if np.array_equal(x_can, yi):
            return True

    # eqnum=2
    y0 = np.copy(y_can)
    y1 = np.flipud(y0)
    y1 = conv2pseudocanonic(y1)
    y4 = np.array(y1[:, [0, 2, 1]])
    if optionx in [3, 4, 6]:
        y1 = cambio_de_signo(y1.copy())
        y4 = cambio_de_signo(y4.copy())
    for yi in [y1, y4]:
        if np.array_equal(x_can, yi):
            return True

    return False

# Análisis de tokens

def analizar_tokens(optionx):
    """Determina si los tokens de una opción tienen elementos idénticos arriba/abajo."""
    filas = filas_para_opcion(optionx)
    elementos_pos = set()
    elementos_neg = set()
    for fila in filas:
        for tok in fila:
            if len(tok) == 2:
                if tok[0] == '+' and tok[1] != '0':
                    elementos_pos.add(tok[1])
                elif tok[0] == '-':
                    elementos_neg.add(tok[1])
            elif len(tok) == 6:
                # paréntesis: (+k-k) → k en pos 2, k en pos 4
                elementos_pos.add(tok[2])
                elementos_neg.add(tok[4])
    return elementos_pos, elementos_neg

# Experimento

def analizar_opcion(optionx, n):
    print(f"\n=== Opción {optionx}, n={n} ===")

    elem_pos, elem_neg = analizar_tokens(optionx)
    print(f"Tokens positivos: {elem_pos}")
    print(f"Tokens negativos: {elem_neg}")
    if elem_pos == elem_neg:
        print("  → Mismo elemento arriba y abajo: sign DEBERÍA ser simetría")
    else:
        print("  → Elementos distintos arriba y abajo: sign NO debería ser simetría")

    candidatos = generar_estructuras_n(n, optionx)
    print(f"Candidatos: {len(candidatos)}")

    discrepancias = 0
    coincidencias = 0
    sin_cambio = 0

    for a in candidatos:
        b = cambio_de_signo(a.copy())
        if np.array_equal(a, b):
            sin_cambio += 1
            continue
        if son_equivalentes_viejo(a, b, optionx):
            coincidencias += 1
        else:
            discrepancias += 1

    print(f"Casos donde sign(a) != a: {coincidencias + discrepancias}")
    print(f"  Viejo dice equivalentes: {coincidencias}")
    print(f"  Viejo dice NO equivalentes: {discrepancias}  ← DISCREPANCIA")


if __name__ == "__main__":
    for optionx in [1, 2, 3, 4]:
        for n in [2, 3]:
            analizar_opcion(optionx, n)
            
