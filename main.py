"""
Menú principal: lanza la demostración de cada tema del curso.

    python main.py

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import runpy

TEMAS = {
    1: ("Recursividad", "recursividad.ejercicios"),
    2: ("Backtracking", "backtracking.problemas"),
    3: ("Árboles (ABB)", "arboles.taller_abb"),
    4: ("Búsqueda en anchura y profundidad", "busquedas.anchura_profundidad"),
    5: ("Grafos (taller + Dijkstra, Prim, Kruskal, Borůvka)", "grafos.taller_grafos"),
    6: ("Árbol AVL", "avl.demo"),
    7: ("Diccionarios: taller", "diccionarios.taller"),
    8: ("Diccionarios: parcial de ADN", "diccionarios.parcial_adn"),
    9: ("Diccionarios: ejercicios básicos (interactivo)", "diccionarios.ejercicios_basicos"),
    10: ("Proyecto Librerías (grafos) - demo", "proyectos.libreria_grafos.main"),
    11: ("Proyecto Isla El Paro (árboles) - simulación", "proyectos.isla_cuevas.main"),
}

CABECERA = """
╔══════════════════════════════════════════════════════════╗
║                 ESTRUCTURA DE DATOS (Python)             ║
║              Daniel Felipe Franco Rincón                 ║
╚══════════════════════════════════════════════════════════╝"""


def main():
    import sys

    while True:
        print(CABECERA)
        for n, (nombre, _) in TEMAS.items():
            print(f"  {n:2}. {nombre}")
        print("   0. Salir")
        try:
            opcion = int(input("\nElija una opción: "))
        except ValueError:
            continue
        if opcion == 0:
            break
        if opcion in TEMAS:
            print()
            # el proyecto de librerías corre su demo; el resto, su main normal
            sys.argv = [TEMAS[opcion][1]] + (["--demo"] if opcion == 10 else [])
            runpy.run_module(TEMAS[opcion][1], run_name="__main__")
            input("\n[Enter para volver al menú]")


if __name__ == "__main__":
    main()
