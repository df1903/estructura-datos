"""
Demostración del taller de grafos y de los algoritmos Dijkstra, Prim, Kruskal
y Borůvka sobre un grafo de ejemplo.
Ejecutar desde la raíz del proyecto:  python -m grafos.taller_grafos

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from .grafo import Grafo


def grafo_dirigido():
    """Grafo dirigido de ejemplo para el taller (puntos 1 al 11)."""
    g = Grafo()
    for v in "ABCDEF":
        g.ingresarVertice(v)
    for o, d, p in [("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10),
                    ("C", "E", 3), ("E", "D", 4), ("D", "F", 11), ("C", "B", 1)]:
        g.ingresarArista(o, d, p)
    return g


def grafo_no_dirigido():
    """Grafo no dirigido de ejemplo para los árboles de expansión mínima."""
    g = Grafo()
    for v in "ABCDEF":
        g.ingresarVertice(v)
    for o, d, p in [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7),
                    ("C", "E", 5), ("D", "E", 15), ("D", "F", 6), ("E", "F", 8)]:
        g.ingresarArista(o, d, p)
    g.convertirNoDirigido()
    return g


def main():
    g = grafo_dirigido()
    g.mostrarVertices()
    g.mostrarAristas()
    g.mostrarAdyacencias()
    print("\n1) Aristas de menor a mayor:", [(a.origen, a.destino, a.peso) for a in g.minMaxAristas()])
    print("2) Grados:", g.gradoVertices())
    print("3) Mayor grado:", g.verticeMayorGrado())
    print("4) Promedio lista de adyacencias:", round(g.promedioListaAdyacencias(), 2))
    print("5) Pozos:", g.pozos())
    print("6) Fuentes:", g.fuentes())
    print("7) Promedio de pesos:", round(g.promedioPesoAristas(), 2))
    print("8) Arista mayor peso:", g.aristaMayorPeso())
    print("9) Arista menor peso:", g.aristaMenorPeso())
    print("10) ¿Cuántas veces es adyacente C en los otros?:", g.verticeAdyacente("C"))
    print("11) Lista de adyacencias:", g.listaAdyacencias())
    print("11-a) No contemplados:", g.verticesNoContemplados())
    print("11-b) Adyacencia más común:", g.adyacenciaMasComun())
    print("\nAnchura desde A:", g.recorridoAmplitud("A"))
    print("Profundidad desde A:", g.recorridoProfundidad("A"))
    print("¿Conexo?:", g.esConexo(), "| ¿Ciclos?:", g.tieneCiclos())
    print("Dijkstra A->F:", g.dijkstra("A", "F"))

    n = grafo_no_dirigido()
    print("\n--- Árboles de expansión mínima (no dirigido) ---")
    for nombre, arbol in (("Prim", n.prim("A")), ("Kruskal", n.kruskal()), ("Borůvka", n.boruvka())):
        print(f"{nombre}: peso {Grafo.pesoTotal(arbol)} ->",
              [(a.origen, a.destino, a.peso) for a in arbol])
    print("Floyd-Warshall A->F:", n.floydWarshall()["A"]["F"])


if __name__ == "__main__":
    main()
