"""
Reporte completo: todas las claves canónicas producidas por ambos métodos,
para las 8 opciones y n = 2, 3. Marca coincidencias al nivel de cadena.
"""
import numpy as np
import sys
from itertools import permutations
import os

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
    canonical_key_std,
    disc_equivalents_canonical_std,
    generar_grupo_std,
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
        canonic = [conv(ai) for ai in nparraylist]
        arraynorep = disc_old(canonic, optionx, 1)
        arraynorep = disc_old(arraynorep, optionx, 2)
    return nparraylist


def reporte_opcion(optionx, num_layers, out):
    disc_old, conv = get_funcs(optionx)

    candidatos = generar_candidatos(num_layers, optionx)

    candidatos_canonicos = [conv(c.copy()) for c in candidatos]
    viejas = disc_old(candidatos_canonicos, optionx, 1)
    viejas = disc_old(viejas, optionx, 2)

    nuevas = disc_equivalents_canonical_std(candidatos, optionx)

    keys_viejas = set(canonical_key_std(v, optionx) for v in viejas)
    keys_nuevas = set(canonical_key_std(v, optionx) for v in nuevas)

    identicas = keys_viejas == keys_nuevas

    out.write(f"\n{'='*70}\n")
    out.write(f"Opción {optionx}, n = {num_layers}\n")
    out.write(f"{'='*70}\n")
    out.write(f"Grupo: {len(generar_grupo_std(optionx))} operaciones\n")
    out.write(f"Candidatos: {len(candidatos)}\n")
    out.write(f"Viejo: {len(viejas)} estructuras, {len(keys_viejas)} claves únicas\n")
    out.write(f"Nuevo: {len(nuevas)} estructuras, {len(keys_nuevas)} claves únicas\n")
    out.write(f"¿Conjuntos idénticos? {'SÍ' if identicas else 'NO'}\n\n")

    if identicas:
        out.write(f"Claves canónicas ({len(keys_viejas)}):\n")
        for k in sorted(keys_viejas):
            out.write(f"  {k}\n")
    else:
        solo_viejo = sorted(keys_viejas - keys_nuevas)
        solo_nuevo = sorted(keys_nuevas - keys_viejas)
        comun = sorted(keys_viejas & keys_nuevas)

        out.write(f"Claves en común ({len(comun)}):\n")
        for k in comun:
            out.write(f"  {k}\n")
        out.write(f"\nClaves solo en viejo ({len(solo_viejo)}):\n")
        for k in solo_viejo:
            out.write(f"  {k}\n")
        out.write(f"\nClaves solo en nuevo ({len(solo_nuevo)}):\n")
        for k in solo_nuevo:
            out.write(f"  {k}\n")

    return identicas


if __name__ == "__main__":
    niveles = [2, 3]
    todos = True

    out = open("reporte_completo_salida.txt", "w")
    out.write("REPORTE COMPLETO DE VALIDACIÓN\n")
    out.write("Método actual vs método canónico\n")
    out.write(f"Opciones: 1-8. Niveles: {niveles}\n")

    # Resumen primero
    out.write(f"\n{'='*70}\n")
    out.write("RESUMEN\n")
    out.write(f"{'='*70}\n")
    out.write(f"{'Opción':>6} {'n':>3} {'Viejo':>8} {'Nuevo':>8} {'¿Iguales?':>12}\n")
    out.write("-" * 45 + "\n")

    resultados = []
    for optionx in range(1, 9):
        for n in niveles:
            disc_old, conv = get_funcs(optionx)
            candidatos = generar_candidatos(n, optionx)
            candidatos_canonicos = [conv(c.copy()) for c in candidatos]
            viejas = disc_old(candidatos_canonicos, optionx, 1)
            viejas = disc_old(viejas, optionx, 2)
            nuevas = disc_equivalents_canonical_std(candidatos, optionx)
            kv = set(canonical_key_std(v, optionx) for v in viejas)
            kn = set(canonical_key_std(v, optionx) for v in nuevas)
            marca = "✓" if kv == kn else "✗"
            out.write(f"{optionx:>6} {n:>3} {len(kv):>8} {len(kn):>8} {marca:>12}\n")
            resultados.append((optionx, n, kv == kn))

    out.write("\n")
    if all(r[2] for r in resultados):
        out.write("✓ Todas las opciones producen exactamente las mismas clases.\n")
    else:
        out.write("✗ Algunas opciones difieren.\n")
        todos = False

    # Detalle completo
    out.write(f"\n{'='*70}\n")
    out.write("DETALLE POR OPCIÓN\n")
    out.write(f"{'='*70}\n")

    for optionx in range(1, 9):
        for n in niveles:
            if not reporte_opcion(optionx, n, out):
                todos = False

    out.close()

    # Imprimir resumen por pantalla
    with open("reporte_completo_salida.txt") as f:
        for i, line in enumerate(f):
            if i < 40:
                print(line, end="")

    print(f"\n... ver reporte_completo_salida.txt para detalle completo")
    sys.exit(0 if todos else 1)
