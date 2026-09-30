# Canonicalización de cadenas JAM

Desarrollo y validación de un método alternativo para detección de
duplicados en las estructuras generadas por JAM 2.0.

## Contexto

JAM genera todas las combinaciones de apilamiento para un sistema de n
capas. Muchas son equivalentes bajo las simetrías del problema:
rotación de columnas, intercambio de columnas, inversión del orden de
capas, cambio de signo. El programa actual detecta equivalencias por
comparación pairwise.

El método propuesto reemplaza esa comparación por un diccionario de
claves canónicas. La clave de una estructura se calcula aplicando todas
las operaciones del grupo de simetría y tomando el mínimo
lexicográfico. Dos estructuras equivalentes producen la misma clave.

## Formulación

    G ≅ S_3 × Z/2Z × Z/2Z     (opciones con buckling, 24 elementos)
    G ≅ S_3 × Z/2Z            (opciones planas, 12 elementos)

    κ(a) = argmin_{x ∈ Orb(a)} σ(x)

σ codifica un array a cadena JAM. Orb(a) es la órbita de a bajo G.

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

**`debug_validacion.py`**
Diagnóstico detallado para opción 4, n=2.

**`experimento_flip_sign.py`**
Compara 5 grupos candidatos contra el método actual:

- S3 (6 operaciones)
- S3 × flip (12)
- S3 × sign (12)
- S3 × flip × sign (24)
- S3 × (flip·sign) (12)

### Históricos

**`diagnostico.py`**
Primer caso de discrepancia (opción 3).

**`experimento_sign_v2.py`**
Análisis por pares (elemento_arriba, elemento_abajo) por capa.

**`experimento_sign.py`**
Versión inicial del análisis por conjuntos. Resultado descartado por
tratar opciones multi-elemento como si tuvieran un solo tipo de par.

## Simetrías por opción

Regla: el cambio de signo es simetría válida si y solo si en cada capa
el elemento superior y el inferior son el mismo.

| Opción | Tipo | Fila | Arriba | Abajo | sign | Grupo |
|--------|------|------|--------|-------|------|-------|
| 1 | Planar | `+0 +j +j` | j | — | n/a | S3 × flip |
| 2 | Planar binaria | `+0 +j +k` | j,k | — | n/a | S3 × flip |
| 3 | Buckled | `+0 +j -j` | j | j | sí | S3 × flip × sign |
| 4 | Buckled binaria | `+0 +j -k` | j | k | no | S3 × flip |
| 5 | Buckled 1H | `+0 *j (+k-k)` | k | k | sí (nulo) | S3 × flip |
| 6 | Buckled 1T | `*j +k -k` | k | k | sí | S3 × flip × sign |
| 7 | Ternaria 1H | `+0 *j (+k-l)` | k | l | no | S3 × flip |
| 8 | Ternaria 1T | `*j +k -l` | k | l | no | S3 × flip |

Opción 5: sign es válido pero nulo, porque `(+k-k)` es invariante bajo
sign.

## Hallazgos

### Discrepancia

Coincidencia entre métodos para opciones 1, 2, 5. Discrepancia para
3, 4, 6, 7, 8.

### Causa

El método actual aplica sign solo después de flip, nunca solo. La
relación de equivalencia resultante no es transitiva: si flip y
sign·flip son simetrías, entonces sign = flip · (sign·flip) también
debería serlo. El código no verifica esa cadena.

### Evidencia

Opción 4, n=2:

    Candidatos generados:            144
    Estructuras devueltas (viejo):   16
    Estructuras devueltas (nuevo):   16
    Claves únicas en viejo:          11
    Claves únicas en nuevo:          16

El método actual devuelve 16 estructuras, de las cuales solo 11 son
clases distintas. Las otras 5 son duplicados no detectados.

### Alcance

El bug no se manifiesta en opciones 1, 2, 5 (las más usadas: grafeno,
h-BN, MoS₂). Se manifiesta en opciones con buckling específico y
ternarias.

## Estado

- [x] Implementación del método canónico.
- [x] Validación contra el método actual, 8 opciones.
- [x] Diagnóstico del caso concreto.
- [x] Identificación de la causa raíz.
- [x] Determinación de la regla de simetría por opción.
- [ ] Confirmación de la interpretación física (Dra. Arcudia).
- [ ] Ajuste final del grupo por opción.
- [ ] Pull request al repositorio principal.
- [ ] Benchmark de rendimiento (n=3,4,5,6).

## Ejecución

    cd pruebas
    python3 prueba_grupo.py
    python3 validacion.py
    python3 debug_validacion.py
    python3 experimento_flip_sign.py

## Dependencias

Python 3.x, NumPy, JAM 2.0 instalado.

## Referencia

Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
Merino, G. (2023). "Joining and arrangement of multilayers: A string
representation for honeycomb layered materials." Matter, 6(5),
1503–1513. doi: 10.1016/j.matt.2023.02.014
