"""
Búsqueda en anchura (BFS) y en profundidad (DFS).

  * BFS: explora por niveles. Usa una COLA (FIFO). Encuentra el camino con
         menos aristas en grafos sin peso.
  * DFS: explora una rama hasta el fondo y retrocede. Usa una PILA (LIFO) o la
         pila de llamadas (recursión).

Se implementan sobre:
  1) Grafos como diccionario de adyacencias {vertice: [vecinos]}.
  2) Árboles binarios (cualquier objeto con atributos `dato`, `izq`, `der`).

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from collections import deque

# --------------------------------------------------------------------------- #
# Grafos (diccionario de adyacencias)
# --------------------------------------------------------------------------- #


def bfs(grafo, inicio):
    """Recorrido en anchura. Devuelve la lista de vértices en orden de visita."""
    visitados, cola, orden = {inicio}, deque([inicio]), []
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return orden


def dfs_iterativo(grafo, inicio):
    """Recorrido en profundidad con pila explícita."""
    visitados, pila, orden = set(), [inicio], []
    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        orden.append(actual)
        # se apilan al revés para visitar los vecinos en el orden dado
        for vecino in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                pila.append(vecino)
    return orden


def dfs_recursivo(grafo, inicio, visitados=None, orden=None):
    """Recorrido en profundidad recursivo."""
    visitados = set() if visitados is None else visitados
    orden = [] if orden is None else orden
    visitados.add(inicio)
    orden.append(inicio)
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            dfs_recursivo(grafo, vecino, visitados, orden)
    return orden


def camino_bfs(grafo, inicio, fin):
    """Camino con MENOS aristas entre dos vértices (BFS). None si no existe."""
    previo, cola = {inicio: None}, deque([inicio])
    while cola:
        actual = cola.popleft()
        if actual == fin:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = previo[actual]
            return camino[::-1]
        for vecino in grafo.get(actual, []):
            if vecino not in previo:
                previo[vecino] = actual
                cola.append(vecino)
    return None


def camino_dfs(grafo, inicio, fin, visitados=None):
    """Algún camino entre dos vértices (DFS). No es necesariamente el más corto."""
    visitados = set() if visitados is None else visitados
    visitados.add(inicio)
    if inicio == fin:
        return [inicio]
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            resto = camino_dfs(grafo, vecino, fin, visitados)
            if resto:
                return [inicio] + resto
    return None


def componentes_conexas(grafo):
    """Lista de componentes conexas de un grafo no dirigido (usa BFS)."""
    vistos, componentes = set(), []
    for v in grafo:
        if v not in vistos:
            comp = bfs(grafo, v)
            vistos.update(comp)
            componentes.append(comp)
    return componentes


# --------------------------------------------------------------------------- #
# Árboles binarios
# --------------------------------------------------------------------------- #


def bfs_arbol(raiz):
    """Recorrido por niveles. Devuelve lista de listas (un nivel por lista)."""
    if raiz is None:
        return []
    niveles, cola = [], deque([raiz])
    while cola:
        nivel = []
        for _ in range(len(cola)):
            nodo = cola.popleft()
            nivel.append(nodo.dato)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        niveles.append(nivel)
    return niveles


def dfs_arbol(raiz, orden="pre"):
    """Recorrido en profundidad ('pre', 'in' o 'post') con pila explícita."""
    resultado, pila = [], []
    if orden == "pre":
        if raiz:
            pila.append(raiz)
        while pila:
            nodo = pila.pop()
            resultado.append(nodo.dato)
            if nodo.der:
                pila.append(nodo.der)
            if nodo.izq:
                pila.append(nodo.izq)
    elif orden == "in":
        actual = raiz
        while pila or actual:
            while actual:
                pila.append(actual)
                actual = actual.izq
            actual = pila.pop()
            resultado.append(actual.dato)
            actual = actual.der
    elif orden == "post":
        if raiz:
            pila.append(raiz)
        while pila:
            nodo = pila.pop()
            resultado.append(nodo.dato)
            if nodo.izq:
                pila.append(nodo.izq)
            if nodo.der:
                pila.append(nodo.der)
        resultado.reverse()
    else:
        raise ValueError("orden debe ser 'pre', 'in' o 'post'")
    return resultado


def _demo():
    grafo = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["F"], "F": []}
    print("BFS            :", bfs(grafo, "A"))
    print("DFS iterativo  :", dfs_iterativo(grafo, "A"))
    print("DFS recursivo  :", dfs_recursivo(grafo, "A"))
    print("Camino BFS A->F:", camino_bfs(grafo, "A", "F"))
    print("Camino DFS A->F:", camino_dfs(grafo, "A", "F"))


if __name__ == "__main__":
    _demo()
