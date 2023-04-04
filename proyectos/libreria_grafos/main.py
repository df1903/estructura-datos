"""
Proyecto "Librerías" (grafos).

Un mensajero recorre una ciudad con 10 librerías y su casita. Las rutas (con
distancia) están en data/rutas.json. El sistema permite:

  * Cargar el grafo desde JSON (si el grafo es dirigido lo convierte a no dirigido).
  * Bloquear un camino SOLO si existe una ruta alterna al destino.
  * Recorrido en anchura y en profundidad.
  * Ruta más corta desde la casita hasta una sucursal (Dijkstra).
  * Árbol de expansión mínima: Prim y Kruskal; y Borůvka.
  * Floyd-Warshall (todas las distancias).

Ejecutar desde la raíz del proyecto:
    python -m proyectos.libreria_grafos.main          # menú interactivo
    python -m proyectos.libreria_grafos.main --demo   # recorrido automático

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import sys
from pathlib import Path

from grafos.grafo import Grafo
from helpers.keyboard import Keyboard

DATA = Path(__file__).parent / "data"
CASA = "Casita"


def cargar_grafo():
    g = Grafo.desdeJSON(DATA / "librerias.json", DATA / "rutas.json")
    if g.esDirigido():
        g.convertirNoDirigido()
    return g


def _imprimir_aristas(aristas):
    for a in aristas:
        print(f"  {a.getOrigen()} ---- {a.getDestino()} ---> {a.getPeso()}")
    print("  Peso total:", Grafo.pesoTotal(aristas))


def ruta_mas_corta(g, destino="Libreria Celsius", origen=CASA):
    distancia, camino = g.dijkstra(origen, destino)
    print(f"Ruta más corta de {origen} a {destino} ({distancia}):")
    print("  " + " -> ".join(camino) if camino else "  No hay ruta")


def demo():
    g = cargar_grafo()
    print("Vértices:", len(g.getListaVertices()), "| Aristas:", len(g.getListaAristas()))
    print("\nAnchura desde Celsius :", g.recorridoAmplitud("Libreria Celsius"))
    print("Profundidad desde Celsius:", g.recorridoProfundidad("Libreria Celsius"))
    print()
    ruta_mas_corta(g)
    print("\nPrim desde la Casita:")
    _imprimir_aristas(g.prim(CASA))
    print("\nKruskal:")
    _imprimir_aristas(g.kruskal())
    print("\nBorůvka:")
    _imprimir_aristas(g.boruvka())
    print("\nRuta alterna Casita -> Libreria Euler con el camino directo bloqueado:")
    alterna = g.caminoBloqueado(CASA, "Libreria Euler")
    if alterna:
        _imprimir_aristas(alterna)
    else:
        print("  No hay ruta alterna (el camino no se puede bloquear)")


def _elegir_vertice(g, mensaje):
    nombres = g.nombresVertices()
    for i, n in enumerate(nombres, 1):
        print(f"  {i:2}. {n}")
    return nombres[Keyboard.readIntRange(mensaje, "Número inválido", 1, len(nombres)) - 1]


def menu():
    g = cargar_grafo()
    opciones = (
        "\n1 Mostrar grafo      2 Bloquear camino   3 Desbloquear todo\n"
        "4 Anchura            5 Profundidad       6 Ruta más corta (Dijkstra)\n"
        "7 Prim               8 Kruskal           9 Borůvka\n"
        "10 Floyd-Warshall    0 Salir"
    )
    while True:
        print(opciones)
        op = Keyboard.readIntRange("Opción: ", "Elija entre 0 y 10", 0, 10)
        if op == 0:
            break
        if op == 1:
            g.mostrarVertices()
            g.mostrarAristas()
        elif op == 2:
            a, b = _elegir_vertice(g, "Origen: "), _elegir_vertice(g, "Destino: ")
            print("Bloqueado." if g.bloquearArista(a, b) else "No se puede bloquear (no hay ruta alterna o no existe).")
        elif op == 3:
            g.desbloquearAristas()
            print("Caminos restaurados.")
        elif op == 4:
            print(g.recorridoAmplitud(_elegir_vertice(g, "Origen: ")))
        elif op == 5:
            print(g.recorridoProfundidad(_elegir_vertice(g, "Origen: ")))
        elif op == 6:
            ruta_mas_corta(g, _elegir_vertice(g, "Destino: "))
        elif op == 7:
            _imprimir_aristas(g.prim(_elegir_vertice(g, "Origen: ")))
        elif op == 8:
            _imprimir_aristas(g.kruskal())
        elif op == 9:
            _imprimir_aristas(g.boruvka())
        elif op == 10:
            tabla = g.floydWarshall()
            origen = _elegir_vertice(g, "Origen: ")
            for destino, d in tabla[origen].items():
                print(f"  {origen} -> {destino}: {d}")


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
