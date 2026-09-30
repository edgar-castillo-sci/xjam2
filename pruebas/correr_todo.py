"""
Corre todos los scripts de validación en orden y reporta el estado.
"""
import subprocess
import sys
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def correr(script):
    print(f"\n{'='*70}")
    print(f"  {script}")
    print(f"{'='*70}\n")
    result = subprocess.run(
        [sys.executable, os.path.join(_SCRIPT_DIR, script)],
        cwd=_SCRIPT_DIR,
    )
    return result.returncode


if __name__ == "__main__":
    scripts = [
        "prueba_grupo.py",
        "validacion.py",
        "reporte_completo.py",
    ]

    resultados = []
    for s in scripts:
        rc = correr(s)
        resultados.append((s, rc))

    print(f"\n{'='*70}")
    print("  RESUMEN FINAL")
    print(f"{'='*70}\n")

    todos_ok = True
    for s, rc in resultados:
        marca = "✓" if rc == 0 else "✗"
        print(f"  {marca}  {s}")
        if rc != 0:
            todos_ok = False

    print()
    if todos_ok:
        print("✓ Todos los scripts corrieron sin errores.")
    else:
        print("✗ Algunos scripts fallaron.")

    sys.exit(0 if todos_ok else 1)
