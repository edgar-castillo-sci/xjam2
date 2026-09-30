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


# Filas por opción

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



# Análisis de pares (arriba, abajo) por fila

def analizar_fila(fila):
    """
    Dada una fila (array de 3 tokens), devuelve:
    - lista de (elemento_arriba)
    - lista de (elemento_abajo)
    """
    arriba = []
    abajo = []
    for tok in fila:
        if len(tok) == 2:
            signo, letra = tok[0], tok[1]
            if letra == '0':
                continue
            if signo == '+':
                arriba.append(letra)
            elif signo == '-':
                abajo.append(letra)
            # '*' no cuenta (está en el plano medio)
        elif len(tok) == 6:
            # paréntesis: (+k-k) o (+k-l) etc.
            # tok = ['(', signo1, letra1, signo2, letra2, ')']
            s1, l1 = tok[1], tok[2]
            s2, l2 = tok[3], tok[4]
            if s1 == '+': arriba.append(l1)
            elif s1 == '-': abajo.append(l1)
            if s2 == '+': arriba.append(l2)
            elif s2 == '-': abajo.append(l2)
    return arriba, abajo


def sign_es_simetria_para_fila(fila):
    """Para una fila, determina si el reflejo vertical la deja igual."""
    arriba, abajo = analizar_fila(fila)
      # El reflejo es simetría si los elementos de arriba y abajo son el mismo conjunto
    return sorted(arriba) == sorted(abajo)


def sign_es_simetria_para_opcion(optionx):
    """
    Para una opción completa, sign es simetría si TODAS las filas
    posibles tienen los mismos elementos arriba y abajo.
    """
    filas = filas_para_opcion(optionx)
    resultados = []
    for fila in filas:
        arriba, abajo = analizar_fila(fila)
        es_sim = sorted(arriba) == sorted(abajo)
        resultados.append((tuple(fila), tuple(arriba), tuple(abajo), es_sim))
    
    # Es simetría para la opción si lo es para TODAS las filas
    todas_sim = all(r[3] for r in resultados)
    return todas_sim, resultados


# Generación de estructuras

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


def son_equivalentes_viejo(x, y, optionx):
    x_can = conv2pseudocanonic(x.copy())
    y_can = conv2pseudocanonic(y.copy())
    y1 = np.copy(y_can)
    y4 = np.array(y_can[:, [0, 2, 1]])
    for yi in [y1, y4]:
        if np.array_equal(x_can, yi):
            return True
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



# Reporte

def reporte_opcion(optionx):
    print(f"\n{'='*60}")
    print(f"OPCIÓN {optionx}")
    print('='*60)
    
    es_sim, resultados = sign_es_simetria_para_opcion(optionx)
    
    print("\nAnálisis de filas:")
    filas_vistas = set()
    for fila, arriba, abajo, sim in resultados:
        key = tuple(fila)
        if key in filas_vistas:
            continue
        filas_vistas.add(key)
        print(f"  Fila: {list(fila)}")
        print(f"    Arriba: {list(arriba)}")
        print(f"    Abajo:  {list(abajo)}")
        print(f"    ¿Mismo? {'SÍ' if sim else 'NO'}")
        print()
    
    print(f"  → sign ES simetría para la opción: {es_sim}")
    
    if optionx in [1, 2]:
        print("  → Opción plana: sign no aplica de todas formas")
        return
    
    # Verificación empírica
    print(f"\nVerificación empírica (n=2, 3):")
    for n in [2, 3]:
        candidatos = generar_estructuras_n(n, optionx)
        discrepancias = 0
        coincidencias = 0
        for a in candidatos:
            b = cambio_de_signo(a.copy())
            if np.array_equal(a, b):
                continue
            if son_equivalentes_viejo(a, b, optionx):
                coincidencias += 1
            else:
                discrepancias += 1
        print(f"  n={n}: {coincidencias} equivalentes, {discrepancias} discrepancias")
    
    print(f"\n  Predicción: si sign ES simetría, esperamos discrepancias > 0")
    print(f"  Si sign NO ES simetría, esperamos discrepancias = 0")


if __name__ == "__main__":
    for optionx in [1, 2, 3, 4, 5, 6, 7, 8]:
        reporte_opcion(optionx)
