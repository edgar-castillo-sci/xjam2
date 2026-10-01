"""
Benchmark: método actual (pairwise) vs método canónico.

Mide solo la etapa de filtrado (detección de duplicados).

Para poder alcanzar niveles altos con el método canónico, la generación
de candidatos usa el método canónico en los pasos intermedios. Eso
permite generar candidatos para n grandes sin depender del método viejo,
que es el cuello de botella.
"""
import numpy as np
import sys
import os
from itertools import permutations
from time import perf_counter

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_XJAM2_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _XJAM2_DIR)

from xjam.libjamstd import (
    disc_equivalents as disc_old_std,
    conv2pseudocanonic as conv_std,
)
from xjam.libjamtdm import (
    disc_equivalents as disc_old_tdm,
    conv2pseudocanonic as conv_tdm,
)

from prueba_grupo import (
    disc_equivalents_canonical_std,
)


def get_funcs(optionx):
    if optionx in [1, 2, 3, 4]:
        return disc_old_std, conv_std
    return disc_old_tdm, conv_tdm


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


def generar_candidatos(num_layers, optionx, verbose=False):
    """
    Genera candidatos para n capas usando el método canónico en los
    pasos intermedios. Esto permite alcanzar n grandes sin que el
    método viejo sea cuello de botella.
    """
    _, conv = get_funcs(optionx)
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

        canonic = [conv(ai) for ai in nparraylist]
        arraynorep = disc_equivalents_canonical_std(canonic, optionx)

        if verbose:
            print(f"    n={case}: {len(nparraylist)} candidatos, {len(arraynorep)} únicas")

    return nparraylist


def medir_viejo(candidatos, optionx):
    disc_old, conv = get_funcs(optionx)
    candidatos_canonicos = [conv(c.copy()) for c in candidatos]
    t0 = perf_counter()
    viejas = disc_old(candidatos_canonicos, optionx, 1)
    viejas = disc_old(viejas, optionx, 2)
    t1 = perf_counter()
    return t1 - t0, len(viejas)


def medir_nuevo(candidatos, optionx):
    t0 = perf_counter()
    nuevas = disc_equivalents_canonical_std(candidatos, optionx)
    t1 = perf_counter()
    return t1 - t0, len(nuevas)


def benchmark_opcion(optionx, niveles_viejo, niveles_nuevo):
    print(f"\n{'='*72}")
    print(f"OPCIÓN {optionx}")
    print(f"{'='*72}\n")
    print(f"{'n':>3} {'Cand.':>9} {'Viejo (s)':>14} {'Nuevo (s)':>14} {'Speedup':>11}")
    print("-" * 56)

    for n in niveles_viejo:
        print(f"  Generando n={n}...", end=" ", flush=True)
        candidatos = generar_candidatos(n, optionx)
        print(f"{len(candidatos)}")

        t_viejo, n_viejas = medir_viejo(candidatos, optionx)
        t_nuevo, n_nuevas = medir_nuevo(candidatos, optionx)
        speedup = t_viejo / t_nuevo if t_nuevo > 0 else float('inf')

        print(f"{n:>3} {len(candidatos):>9} {t_viejo:>14.3f} {t_nuevo:>14.3f} {speedup:>10.1f}x")

    for n in niveles_nuevo:
        print(f"  Generando n={n}...", end=" ", flush=True)
        candidatos = generar_candidatos(n, optionx)
        print(f"{len(candidatos)}")

        t_nuevo, n_nuevas = medir_nuevo(candidatos, optionx)
        print(f"{n:>3} {len(candidatos):>9} {'—':>14} {t_nuevo:>14.3f} {'—':>11}")

    print()


if __name__ == "__main__":
    print("=" * 72)
    print("BENCHMARK: método actual (pairwise) vs método canónico")
    print("=" * 72)
    print()
    print("Mide solo la etapa de filtrado (detección de duplicados).")
    print("La generación usa el método canónico en pasos intermedios.")
    print()

    # Opción 1 (planar, la más simple)
    benchmark_opcion(
        optionx=1,
        niveles_viejo=[2, 3, 4, 5, 6, 7, 8],
        niveles_nuevo=[9, 10, 11, 12],
    )

    # Opción 5 (buckled 1H: MoS₂, WS₂)
    benchmark_opcion(
        optionx=5,
        niveles_viejo=[2, 3, 4, 5],
        niveles_nuevo=[6, 7, 8, 9],
    )

    # Opción 7 (ternaria, la más costosa)
    benchmark_opcion(
        optionx=7,
        niveles_viejo=[2, 3, 4],
        niveles_nuevo=[5, 6, 7],
    )
