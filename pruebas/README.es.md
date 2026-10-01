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

    Opciones planas (1, 2):      G = S3 × {e, flip}              (12)
    Opciones con buckling (3-8): G = S3 × {e, sign·flip}         (12)

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

**`benchmark.py`**
Mide el tiempo de filtrado (detección de duplicados) para ambos métodos.
Genera `benchmark_salida.txt` con los resultados.

**`correr_todo.py`**
Ejecuta los scripts principales en orden y reporta el estado final.

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

## Benchmark

Mide solo la etapa de filtrado (detección de duplicados). La generación
de candidatos usa el método canónico en los pasos intermedios, para
permitir alcanzar niveles altos sin que el método viejo sea cuello de
botella.

### Opción 1 (planar)

| n | Candidatos | Viejo (s) | Nuevo (s) | Speedup |
|---|------------|-----------|-----------|---------|
| 8 | 1,176 | 7.777 | 0.212 | 36.6x |
| 9 | 3,444 | — | 0.654 | — |
| 10 | 10,086 | — | 1.962 | — |
| 11 | 30,012 | — | 6.197 | — |
| 12 | 89,304 | — | 18.824 | — |

### Opción 5 (buckled 1H: MoS₂, WS₂)

| n | Candidatos | Viejo (s) | Nuevo (s) | Speedup |
|---|------------|-----------|-----------|---------|
| 5 | 1,440 | 18.092 | 0.311 | 58.2x |
| 6 | 7,992 | — | 1.836 | — |
| 7 | 47,520 | — | 11.804 | — |
| 8 | 281,232 | — | 74.268 | — |
| 9 | 1,684,800 | — | 475.549 | — |

### Opción 7 (ternaria, la más costosa)

| n | Candidatos | Viejo (s) | Nuevo (s) | Speedup |
|---|------------|-----------|-----------|---------|
| 4 | 3,456 | 103.650 | 0.711 | 145.7x |
| 5 | 42,624 | — | 9.591 | — |
| 6 | 497,664 | — | 122.115 | — |
| 7 | 5,985,792 | — | 1,628.460 | — |

Los niveles con `—` en la columna del método viejo no se midieron
porque su tiempo estimado excede varias horas. Ver la sección
"Estimación" más abajo.

### Estimación del método viejo en niveles no medidos

El método viejo es O(m²). A partir del último nivel medido, se puede
estimar su tiempo en niveles superiores:

| Opción | n | Candidatos | Nuevo (s) | Viejo estimado |
|--------|---|------------|-----------|----------------|
| 1 | 12 | 89,304 | 18.824 | ~44,850 s (12.5 h) |
| 5 | 9 | 1,684,800 | 475.549 | ~24,760,000 s (287 días) |
| 7 | 7 | 5,985,792 | 1,628.460 | ~310,000,000 s (10 años) |

El estimado se calcula como:

    t_viejo(n) ≈ t_viejo(n₀) × (candidatos(n) / candidatos(n₀))²

donde n₀ es el último nivel medido del método viejo.

### Complejidad empírica

El método canónico crece linealmente con el número de candidatos:

| Opción | Δ candidatos | Δ tiempo | Ratio |
|--------|--------------|----------|-------|
| 1 (11→12) | ×2.98 | ×3.04 | 1.02 |
| 5 (8→9) | ×5.99 | ×6.40 | 1.07 |
| 7 (6→7) | ×12.03 | ×13.34 | 1.11 |

El ratio tiempo/candidatos se mantiene cercano a 1. Confirma
empíricamente O(m).

### Para n pequeño

Para n = 2, 3, el método viejo es más rápido, porque el método canónico
tiene un costo fijo por estructura (aplicar 12 operaciones y convertir
a cadena). El punto de cruce está entre n=2 y n=3. Para n ≥ 4, el
método canónico gana consistentemente, y la ganancia crece con n.

## Estado

- [x] Implementación del método canónico.
- [x] Validación contra el método actual, 8 opciones, n = 2, 3.
- [x] Verificación de que las clases coinciden (mismas claves).
- [x] Corrección del grupo según indicación de la Dra. Arcudia.
- [x] Benchmark de rendimiento (opciones 1, 5, 7; n hasta 12).
- [ ] Propuesta de integración al repositorio principal.

## Ejecución

    cd pruebas
    python3 correr_todo.py

O individualmente:

    python3 prueba_grupo.py         # verifica grupo y claves
    python3 validacion.py           # comparación resumida
    python3 reporte_completo.py     # evidencia completa de clases
    python3 benchmark.py            # tiempos de filtrado

## Dependencias

Python 3.x, NumPy, JAM 2.0 instalado.

## Referencia

Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
Merino, G. (2023). "Joining and arrangement of multilayers: A string
representation for honeycomb layered materials." Matter, 6(5),
1503–1513. doi: 10.1016/j.matt.2023.02.014
