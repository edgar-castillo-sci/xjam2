# Canonicalización de cadenas JAM

*[Read in English](README.md)*

Desarrollo y validación de un método alternativo para detección de
duplicados en las estructuras generadas por JAM 2.0.

## Contexto

JAM genera todas las combinaciones de apilamiento para un sistema de n
capas. Muchas son equivalentes bajo las simetrías del problema: rotación
de columnas, intercambio de columnas, inversión del orden de capas,
reflexión global del sistema. El programa actual detecta equivalencias
por comparación pairwise.

El método propuesto reemplaza esa comparación por un diccionario de
claves canónicas. La clave de una estructura se calcula aplicando todas
las operaciones del grupo de simetría y tomando el mínimo
lexicográfico. Dos estructuras equivalentes producen la misma clave.

## Formulación

    κ(a) = argmin_{x ∈ Orb(a)} σ(x)

σ codifica un array a cadena JAM. Orb(a) es la órbita de a bajo G.

El grupo de simetría:

    Opciones planas (1, 2):    G = S3 × {e, flip}              (12)
    Opciones con buckling (3-8): G = S3 × {e, sign·flip}        (12)

La simetría vertical es la composición **sign·flip** (reflexión global
del sistema). No se usa sign ni flip por separado.

Documento completo en `Sobre_la_canonicalizacion_de_cadenas_JAM.pdf`:
definición del conjunto, construcción del grupo, definición de κ,
demostración de que distingue clases de equivalencia, pseudocódigo,
complejidad O(|S|² · k) → O(|S| · |G| · k).

## Scripts

### Principales

**`prueba_grupo.py`**
Implementa las tres funciones centrales:

- `generar_grupo_std(optionx)`: construye las operaciones del grupo.
- `canonical_key_std(a, optionx)`: calcula la clave canónica.
- `disc_equivalents_canonical_std(stackinglist, optionx)`: detecta
  duplicados por diccionario.

Define además `rot`, `transp`, `flip`, `sign`, `elementos_S3`.

**`validacion.py`**
Compara `disc_equivalents` (método actual) contra
`disc_equivalents_canonical_std` para las 8 opciones, n = 2, 3.
Verifica igual número de estructuras y equivalencia de clases mediante
conjuntos de claves canónicas.

**`reporte_completo.py`**
Genera `reporte_completo_salida.txt` con todas las claves canónicas
producidas por cada método, lado a lado, para las 8 opciones y n = 2, 3.
Marca coincidencias al nivel de cadena.

**`correr_todo.py`**
Ejecuta los tres scripts anteriores en orden y reporta el estado final.

### Legacy

Ver `legacy/README.md`. Scripts de exploración que llevaron a la
formulación final. No forman parte del flujo de validación actual.

## Simetrías por opción

Regla: la simetría vertical es la composición sign·flip. Para opciones
planas, sign no aplica (no hay desplazamientos verticales), por lo que
la simetría es flip.

| Opción | Tipo | Fila | Grupo |
|--------|------|------|-------|
| 1 | Planar | `+0 +j +j` | S3 × {e, flip} |
| 2 | Planar binaria | `+0 +j +k` | S3 × {e, flip} |
| 3 | Buckled | `+0 +j -j` | S3 × {e, sign·flip} |
| 4 | Buckled binaria | `+0 +j -k` | S3 × {e, sign·flip} |
| 5 | Buckled 1H | `+0 *j (+k-k)` | S3 × {e, sign·flip} |
| 6 | Buckled 1T | `*j +k -k` | S3 × {e, sign·flip} |
| 7 | Ternaria 1H | `+0 *j (+k-l)` | S3 × {e, sign·flip} |
| 8 | Ternaria 1T | `*j +k -l` | S3 × {e, sign·flip} |

En todos los casos el grupo tiene 12 elementos.

Nota sobre opciones con buckling: la operación sign·flip actúa como una
sola transformación, no como dos operaciones independientes. Para
opciones planas, sign es un no-op y sign·flip ≡ flip.

## Validación

Ambos métodos (pairwise y canónico) producen **exactamente las mismas
clases de equivalencia** para las 8 opciones y n = 2, 3. La verificación
compara conjuntos de claves canónicas, no solo conteos.

El reporte completo está en `reporte_completo_salida.txt`, generado por
`reporte_completo.py`.

## Estado

- [x] Implementación del método canónico.
- [x] Validación contra el método actual, 8 opciones, n = 2, 3.
- [x] Verificación de que las clases coinciden (mismas claves).
- [x] Corrección del grupo según indicación de la Dra. Arcudia.
- [ ] Benchmark de rendimiento (n=3, 4, 5, 6).
- [ ] Propuesta de integración al repositorio principal.

## Ejecución

    cd pruebas
    python3 correr_todo.py

O individualmente:

    python3 prueba_grupo.py         # verifica grupo y claves
    python3 validacion.py           # comparación resumida
    python3 reporte_completo.py     # evidencia completa

## Dependencias

Python 3.x, NumPy, JAM 2.0 instalado.

## Referencia

Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
Merino, G. (2023). "Joining and arrangement of multilayers: A string
representation for honeycomb layered materials." Matter, 6(5),
1503–1513. doi: 10.1016/j.matt.2023.02.014
