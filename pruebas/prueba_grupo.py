import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Operaciones básicas

def rot(a):
    """Rotación cíclica de columnas: 0→1, 1→2, 2→0."""
    return np.array(a[:, [1, 2, 0]])

def transp(a):
    """Intercambio de columnas 1 y 2."""
    return np.array(a[:, [0, 2, 1]])

def flip(a):
    """Inversión del orden de capas."""
    return np.flipud(a)

def sign(a):
    """
    Cambio de signo. Refleja cada capa respecto a su plano medio.
    - Tokens de 2 caracteres: +x ↔ -x (excepto +0 y *x)
    - Tokens de 6 caracteres: (+x-y) ↔ (-x+y) solo si x != y
    """
    y = np.copy(a)
    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            s = y[i, j]
            if len(s) == 2:
                letra = s[1]
                signo = s[0]
                if letra != '0' and signo != '*':
                    if signo == '+':
                        y[i, j] = '-' + letra
                    elif signo == '-':
                        y[i, j] = '+' + letra
            elif len(s) == 6:
                signo1, letra1 = s[1], s[2]
                signo2, letra2 = s[3], s[4]
                if letra1 != letra2:
                    if signo1 == '+':
                        y[i, j] = '(-' + letra1 + '+' + letra2 + ')'
                    elif signo1 == '-':
                        y[i, j] = '(+' + letra1 + '-' + letra2 + ')'
    return y


# Construcción del grupo

def elementos_S3():
    """Devuelve los 6 elementos de S_3 como funciones."""
    return [
        lambda a: a,
        lambda a: rot(a),
        lambda a: rot(rot(a)),
        lambda a: transp(a),
        lambda a: rot(transp(a)),
        lambda a: rot(rot(transp(a))),
    ]


def generar_grupo_std(optionx):
    """
    Genera la lista de operaciones del grupo G para la opción dada.

    Opciones 1-2 (planar): G ≅ S_3 × Z/2Z, 12 elementos.
    Opciones 3, 5, 6 (mismo elemento arriba/abajo): G ≅ S_3 × Z/2Z × Z/2Z, 24 elementos.
    Opciones 4, 7, 8 (elementos distintos arriba/abajo): G ≅ S_3 × Z/2Z, 12 elementos.

    La restricción de sign se justifica físicamente: el reflejo vertical
    solo es simetría cuando el mismo elemento está arriba y abajo en cada capa.
    """
    S3 = elementos_S3()
    Z2_flip = [lambda a: a, lambda a: flip(a)]

    # sign solo aplica si el mismo elemento está arriba y abajo
    if optionx in [3, 5, 6]:
        Z2_sign = [lambda a: a, lambda a: sign(a)]
    else:
        Z2_sign = [lambda a: a]

    operaciones = []
    for s in S3:
        for f in Z2_flip:
            for c in Z2_sign:
                def op(a, s=s, f=f, c=c):
                    x = s(a)
                    x = f(x)
                    x = c(x)
                    return x
                operaciones.append(op)
    return operaciones


# Clave canónica

def nparray2chain(a):
    """Convierte un array de tokens a su representación en cadena JAM."""
    lista = [''.join(j for j in a[:, i]) for i in range(3)]
    return '/'.join(lista)


def canonical_key_std(a, optionx):
    """Calcula la clave canónica de a bajo el grupo G de la opción dada."""
    operaciones = generar_grupo_std(optionx)
    cadenas = []
    for op in operaciones:
        x = op(a.copy())
        cadenas.append(nparray2chain(x))
    return min(cadenas)


def disc_equivalents_canonical_std(stackinglist, optionx):
    """Detecta duplicados usando claves canónicas."""
    dicc = {}
    for a in stackinglist:
        clave = canonical_key_std(a, optionx)
        if clave not in dicc:
            dicc[clave] = a
    return list(dicc.values())


# Pruebas

if __name__ == "__main__":
    print("=== Tamaño del grupo por opción ===")
    for opt in [1, 2, 3, 4, 5, 6, 7, 8]:
        n = len(generar_grupo_std(opt))
        print(f"  Opción {opt}: {n} operaciones")
    print()

    print("=== Sign con paréntesis ===")
    a = np.array([['*j', '(+k-l)', '+0']])
    print("a:")
    print(a)
    print("sign(a):")
    print(sign(a))
    print()

    print("=== Clave canónica: equivalentes dan misma clave ===")
    a = np.array([['+0', '+j', '-j'],
                  ['+j', '-j', '+0'],
                  ['-j', '+0', '+j']])
    b = rot(a)
    print(f"key(a) = {canonical_key_std(a, 3)}")
    print(f"key(b) = {canonical_key_std(b, 3)}")
    print(f"¿Iguales? {canonical_key_std(a, 3) == canonical_key_std(b, 3)}")
    print()

    print("=== Clave canónica: no equivalentes dan claves distintas ===")
    c = np.array([['+0', '+j', '+j'],
                  ['+0', '+j', '+j']])
    print(f"key(a) = {canonical_key_std(a, 3)}")
    print(f"key(c) = {canonical_key_std(c, 3)}")
    print(f"¿Iguales? {canonical_key_std(a, 3) == canonical_key_std(c, 3)}")
