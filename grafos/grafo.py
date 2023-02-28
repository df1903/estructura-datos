"""
Grafo ponderado (lista de vértices + lista de aristas + adyacencias).

Contiene:
  * Operaciones básicas (vértices, aristas, adyacencias).
  * Los 11 puntos del taller de grafos (grados, pozos, fuentes, promedios...).
  * Recorridos: anchura (BFS) y profundidad (DFS).
  * Caminos mínimos: Dijkstra y Floyd-Warshall.
  * Árboles de expansión mínima: Prim, Kruskal y Borůvka.
  * Bloqueo de aristas (solo si existe ruta alterna), conexidad y ciclos.

Los métodos `mostrar...` imprimen; los demás devuelven el resultado.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import heapq
import json
from collections import deque

from .arista import Arista
from .vertice import Vertice

INFINITO = float("inf")


class _ConjuntosDisjuntos:
    """Union-Find para Kruskal y Borůvka."""

    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}

    def buscar(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]
            x = self.padre[x]
        return x

    def unir(self, a, b):
        ra, rb = self.buscar(a), self.buscar(b)
        if ra == rb:
            return False
        self.padre[rb] = ra
        return True


class Grafo:

    def __init__(self):
        self.listaVertices = []
        self.listaAristas = []
        self.bloqueadas = []  # aristas retiradas temporalmente (ver bloquearArista)

    # ------------------------------------------------------------------ #
    # get / set
    # ------------------------------------------------------------------ #
    def getListaVertices(self):
        return self.listaVertices

    def setListaVertices(self, listaVertices):
        self.listaVertices = listaVertices

    def getListaAristas(self):
        return self.listaAristas

    def setListaAristas(self, listaAristas):
        self.listaAristas = listaAristas

    # ------------------------------------------------------------------ #
    # Vértices
    # ------------------------------------------------------------------ #
    def ingresarVertice(self, dato):
        """Agrega el vértice si no existe. Devuelve True si lo agregó."""
        if self.existeVertice(dato):
            return False
        self.listaVertices.append(Vertice(dato))
        return True

    def existeVertice(self, dato, listaVertices=None):
        lista = self.listaVertices if listaVertices is None else listaVertices
        return any(v.getDato() == dato for v in lista)

    def obtenerVertice(self, dato, lista=None):
        lista = self.listaVertices if lista is None else lista
        for v in lista:
            if v.getDato() == dato:
                return v
        return None

    def nombresVertices(self):
        return [v.getDato() for v in self.listaVertices]

    def mostrarVertices(self):
        print("                                    VERTICES")
        for i, v in enumerate(self.listaVertices, 1):
            print(i, "-", v.getDato())

    # ------------------------------------------------------------------ #
    # Aristas
    # ------------------------------------------------------------------ #
    def ingresarArista(self, origen, destino, peso=1):
        """Agrega origen -> destino. Falla (False) si ya existe o falta un vértice."""
        if self.existeArista(origen, destino):
            return False
        if not (self.existeVertice(origen) and self.existeVertice(destino)):
            return False
        self.listaAristas.append(Arista(origen, destino, peso))
        self.obtenerVertice(origen).getListaAdyacentes().append(destino)
        return True

    def existeArista(self, origen, destino, lista=None):
        lista = self.listaAristas if lista is None else lista
        return any(a.getOrigen() == origen and a.getDestino() == destino for a in lista)

    verificarListaAristas = existeArista  # nombre usado en el taller original

    def obtenerArista(self, origen, destino, lista=None):
        lista = self.listaAristas if lista is None else lista
        for a in lista:
            if a.getOrigen() == origen and a.getDestino() == destino:
                return a
        return None

    def eliminarArista(self, origen, destino):
        arista = self.obtenerArista(origen, destino)
        if arista is None:
            return False
        self.listaAristas.remove(arista)
        self.obtenerVertice(origen).getListaAdyacentes().remove(destino)
        return True

    def mostrarAristas(self):
        print("                                    ARISTAS")
        for a in self.listaAristas:
            print(f"| Origen: {a.getOrigen()}  →  Destino: {a.getDestino()}  |  Peso: {a.getPeso()} |")

    def mostrarAdyacencias(self):
        print("                                    ADYACENCIAS")
        for v in self.listaVertices:
            print(f"| vértice: {v.getDato()} |  Adyacencias: {v.getListaAdyacentes()} |")

    # ------------------------------------------------------------------ #
    # Carga desde JSON
    # ------------------------------------------------------------------ #
    @classmethod
    def desdeJSON(cls, rutaVertices, rutaAristas, claveVertice="nombre"):
        """Carga un grafo desde dos archivos JSON.
        vertices: [{"nombre": "A"}, ...]    aristas: [{"origen","destino","peso"}, ...]"""
        g = cls()
        with open(rutaVertices, "r", encoding="utf-8") as f:
            for v in json.load(f):
                g.ingresarVertice(v[claveVertice])
        with open(rutaAristas, "r", encoding="utf-8") as f:
            for a in json.load(f):
                g.ingresarArista(a["origen"], a["destino"], a.get("peso", 1))
        return g

    # ------------------------------------------------------------------ #
    # Dirigido / no dirigido
    # ------------------------------------------------------------------ #
    def esDirigido(self):
        """True si alguna arista no tiene su arista de regreso."""
        return any(not self.existeArista(a.getDestino(), a.getOrigen()) for a in self.listaAristas)

    def convertirNoDirigido(self):
        """Agrega la arista inversa (mismo peso) a toda arista dirigida."""
        for a in list(self.listaAristas):
            self.ingresarArista(a.getDestino(), a.getOrigen(), a.getPeso())

    # ------------------------------------------------------------------ #
    # TALLER DE GRAFOS (puntos 1 al 11)
    # ------------------------------------------------------------------ #
    # 1) ordenar aristas por peso (recursivo, como en el taller)
    def minMaxAristas(self, entorno=0):
        """Ordena las aristas de menor a mayor peso."""
        if entorno >= len(self.listaAristas):
            return self.listaAristas
        self._ordenar(entorno, entorno + 1, mayorAMenor=False)
        return self.minMaxAristas(entorno + 1)

    def maxMinAristas(self, entorno=0):
        """Ordena las aristas de mayor a menor peso."""
        if entorno >= len(self.listaAristas):
            return self.listaAristas
        self._ordenar(entorno, entorno + 1, mayorAMenor=True)
        return self.maxMinAristas(entorno + 1)

    def _ordenar(self, entorno, iter, mayorAMenor):
        if iter == len(self.listaAristas):
            return
        a, b = self.listaAristas[entorno], self.listaAristas[iter]
        if (a.getPeso() < b.getPeso()) if mayorAMenor else (a.getPeso() > b.getPeso()):
            self.listaAristas[entorno], self.listaAristas[iter] = b, a
        self._ordenar(entorno, iter + 1, mayorAMenor)

    # 2) grado de los vértices (aristas que entran + aristas que salen)
    def gradoVertices(self):
        """Dict {vértice: grado}."""
        grados = {v.getDato(): 0 for v in self.listaVertices}
        for a in self.listaAristas:
            grados[a.getOrigen()] += 1
            grados[a.getDestino()] += 1
        return grados

    def mostrarGradoVertices(self):
        print("                                 GRADOS DE LOS VERTICES")
        for v, g in self.gradoVertices().items():
            print(f"{v} Grado({g})")

    # 3) vértice con mayor grado
    def verticeMayorGrado(self):
        """Devuelve (vértice, grado) del vértice con mayor grado (None si no hay)."""
        grados = self.gradoVertices()
        if not grados:
            return None
        v = max(grados, key=grados.get)
        return v, grados[v]

    # 4) promedio de la lista de adyacencias
    def promedioListaAdyacencias(self):
        """Promedio del tamaño de las listas de adyacencia de todos los vértices."""
        if not self.listaVertices:
            return 0
        return sum(len(v.getListaAdyacentes()) for v in self.listaVertices) / len(self.listaVertices)

    # 5) pozos: vértices a los que llegan aristas pero de los que no sale ninguna
    def pozos(self):
        return [v.getDato() for v in self.listaVertices if not v.getListaAdyacentes()]

    def mostrarPozos(self):
        print("                                    POZOS")
        for p in self.pozos():
            print(p)

    # 6) fuentes: vértices de los que salen aristas pero a los que no llega ninguna
    def fuentes(self):
        destinos = {a.getDestino() for a in self.listaAristas}
        return [v.getDato() for v in self.listaVertices if v.getDato() not in destinos]

    def mostrarFuentes(self):
        print("                                   FUENTES")
        for f in self.fuentes():
            print(f)

    # 7) promedio de pesos
    def promedioPesoAristas(self):
        if not self.listaAristas:
            return 0
        return sum(a.getPeso() for a in self.listaAristas) / len(self.listaAristas)

    # 8) y 9) aristas de mayor y menor peso (puede haber empates)
    def aristaMayorPeso(self):
        if not self.listaAristas:
            return []
        mayor = max(a.getPeso() for a in self.listaAristas)
        return [a for a in self.listaAristas if a.getPeso() == mayor]

    def aristaMenorPeso(self):
        if not self.listaAristas:
            return []
        menor = min(a.getPeso() for a in self.listaAristas)
        return [a for a in self.listaAristas if a.getPeso() == menor]

    # 10) dado un vértice, en cuántas listas de adyacencia de los otros aparece
    def verticeAdyacente(self, dato):
        """Dict {otro vértice: veces que `dato` aparece en su lista de adyacencias}."""
        return {v.getDato(): v.getListaAdyacentes().count(dato)
                for v in self.listaVertices if v.getDato() != dato}

    # 11) lista del grafo con todas las adyacencias
    def listaAdyacencias(self):
        lista = []
        for v in self.listaVertices:
            lista.extend(v.getListaAdyacentes())
        return lista

    def mostrarListaAdyacentes(self):
        print("                                  LISTA ADYACENTES")
        for a in self.listaAdyacencias():
            print(a)

    # 11-a) vértices que no se contemplan en la lista de adyacencias
    def verticesNoContemplados(self):
        contemplados = set(self.listaAdyacencias())
        return [v.getDato() for v in self.listaVertices if v.getDato() not in contemplados]

    def mostrarVerticesNoContemplados(self):
        print("                                  VERTICES NO CONTEMPLADOS")
        for v in self.verticesNoContemplados():
            print(v)

    # 11-b) adyacencia más común
    def adyacenciaMasComun(self):
        """Devuelve ([vértices más comunes], veces). Lista vacía si no hay aristas."""
        conteo = {}
        for dato in self.listaAdyacencias():
            conteo[dato] = conteo.get(dato, 0) + 1
        if not conteo:
            return [], 0
        mayor = max(conteo.values())
        return [v for v, c in conteo.items() if c == mayor], mayor

    def mostarAdyacenciaMasComun(self):
        vertices, veces = self.adyacenciaMasComun()
        print(f"La adyacencia más común es {vertices} con {veces}")

    # ------------------------------------------------------------------ #
    # RECORRIDOS
    # ------------------------------------------------------------------ #
    def recorridoAmplitud(self, origen):
        """BFS: visita por niveles usando una cola. Devuelve la lista de vértices."""
        if not self.existeVertice(origen):
            return []
        visitados, cola, recorrido = {origen}, deque([origen]), []
        while cola:
            actual = cola.popleft()
            recorrido.append(actual)
            for vecino in self.obtenerVertice(actual).getListaAdyacentes():
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        return recorrido

    def recorridoProfundidad(self, origen):
        """DFS: avanza lo más hondo posible y retrocede. Devuelve la lista de vértices."""
        recorrido, visitados = [], set()

        def _dfs(actual):
            visitados.add(actual)
            recorrido.append(actual)
            for vecino in self.obtenerVertice(actual).getListaAdyacentes():
                if vecino not in visitados:
                    _dfs(vecino)

        if self.existeVertice(origen):
            _dfs(origen)
        return recorrido

    # ------------------------------------------------------------------ #
    # CONEXIDAD Y CICLOS
    # ------------------------------------------------------------------ #
    def esConexo(self):
        """Conexo en sentido débil: ignorando la dirección de las aristas."""
        if not self.listaVertices:
            return True
        vecinos = {v: set() for v in self.nombresVertices()}
        for a in self.listaAristas:
            vecinos[a.getOrigen()].add(a.getDestino())
            vecinos[a.getDestino()].add(a.getOrigen())
        inicio = self.listaVertices[0].getDato()
        visitados, pila = {inicio}, [inicio]
        while pila:
            for n in vecinos[pila.pop()]:
                if n not in visitados:
                    visitados.add(n)
                    pila.append(n)
        return len(visitados) == len(self.listaVertices)

    def tieneCiclos(self):
        """Grafo dirigido: ciclo dirigido (DFS con colores).
        Grafo no dirigido (todas las aristas con regreso): ciclo no trivial."""
        if self.esDirigido():
            estado = {v: 0 for v in self.nombresVertices()}  # 0 blanco, 1 gris, 2 negro

            def _dfs(u):
                estado[u] = 1
                for w in self.obtenerVertice(u).getListaAdyacentes():
                    if estado[w] == 1 or (estado[w] == 0 and _dfs(w)):
                        return True
                estado[u] = 2
                return False

            return any(estado[v] == 0 and _dfs(v) for v in list(estado))

        visitados = set()

        def _dfs_nd(u, padre):
            visitados.add(u)
            for w in self.obtenerVertice(u).getListaAdyacentes():
                if w not in visitados:
                    if _dfs_nd(w, u):
                        return True
                elif w != padre:
                    return True
            return False

        return any(v not in visitados and _dfs_nd(v, None) for v in self.nombresVertices())

    # ------------------------------------------------------------------ #
    # CAMINOS MÍNIMOS
    # ------------------------------------------------------------------ #
    def dijkstraTodos(self, origen):
        """Dijkstra desde `origen`. Devuelve (distancias, previos)."""
        distancias = {v: INFINITO for v in self.nombresVertices()}
        previos = {v: None for v in self.nombresVertices()}
        if origen not in distancias:
            return distancias, previos
        distancias[origen] = 0
        cola = [(0, origen)]
        while cola:
            d, u = heapq.heappop(cola)
            if d > distancias[u]:
                continue
            for w in self.obtenerVertice(u).getListaAdyacentes():
                nueva = d + self.obtenerArista(u, w).getPeso()
                if nueva < distancias[w]:
                    distancias[w] = nueva
                    previos[w] = u
                    heapq.heappush(cola, (nueva, w))
        return distancias, previos

    def dijkstra(self, origen, destino):
        """Camino más corto origen -> destino. Devuelve (distancia, [vértices]);
        (inf, []) si no hay camino."""
        distancias, previos = self.dijkstraTodos(origen)
        if destino not in distancias or distancias[destino] == INFINITO:
            return INFINITO, []
        camino, actual = [], destino
        while actual is not None:
            camino.insert(0, actual)
            actual = previos[actual]
        return distancias[destino], camino

    def caminoMasCorto(self, origen, destino):
        """Igual que dijkstra pero devolviendo el camino como lista de aristas."""
        distancia, camino = self.dijkstra(origen, destino)
        return [self.obtenerArista(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]

    def floydWarshall(self):
        """Distancias mínimas entre todos los pares. Devuelve dict de dicts."""
        nombres = self.nombresVertices()
        dist = {u: {v: (0 if u == v else INFINITO) for v in nombres} for u in nombres}
        for a in self.listaAristas:
            dist[a.getOrigen()][a.getDestino()] = min(dist[a.getOrigen()][a.getDestino()], a.getPeso())
        for k in nombres:
            for i in nombres:
                for j in nombres:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    # ------------------------------------------------------------------ #
    # ÁRBOLES DE EXPANSIÓN MÍNIMA (se tratan como grafo no dirigido)
    # ------------------------------------------------------------------ #
    def _aristasUnicas(self):
        """Una sola arista por pareja de vértices (la de menor peso)."""
        mejor = {}
        for a in self.listaAristas:
            clave = frozenset((a.getOrigen(), a.getDestino()))
            if len(clave) == 2 and (clave not in mejor or a.getPeso() < mejor[clave].getPeso()):
                mejor[clave] = a
        return list(mejor.values())

    def kruskal(self):
        """Árbol (o bosque) de expansión mínima. Devuelve la lista de aristas."""
        conjuntos = _ConjuntosDisjuntos(self.nombresVertices())
        arbol = []
        for a in sorted(self._aristasUnicas(), key=lambda x: x.getPeso()):
            if conjuntos.unir(a.getOrigen(), a.getDestino()):
                arbol.append(a)
        return arbol

    def prim(self, origen=None):
        """Árbol de expansión mínima partiendo de `origen` (el primer vértice si
        no se indica). Devuelve la lista de aristas en el orden en que se eligen."""
        if not self.listaVertices:
            return []
        origen = self.listaVertices[0].getDato() if origen is None else origen
        vecinos = {v: [] for v in self.nombresVertices()}
        for a in self._aristasUnicas():
            vecinos[a.getOrigen()].append(a)
            vecinos[a.getDestino()].append(a)

        visitados, arbol, cola, contador = {origen}, [], [], 0
        for a in vecinos[origen]:
            heapq.heappush(cola, (a.getPeso(), contador, a))
            contador += 1
        while cola and len(visitados) < len(self.listaVertices):
            _, _, a = heapq.heappop(cola)
            nuevo = a.getDestino() if a.getOrigen() in visitados else a.getOrigen()
            if nuevo in visitados:
                continue
            visitados.add(nuevo)
            arbol.append(a)
            for b in vecinos[nuevo]:
                if (b.getOrigen() if b.getDestino() == nuevo else b.getDestino()) not in visitados:
                    heapq.heappush(cola, (b.getPeso(), contador, b))
                    contador += 1
        return arbol

    def boruvka(self):
        """Árbol de expansión mínima por Borůvka: en cada ronda cada componente
        elige su arista de salida más barata."""
        conjuntos = _ConjuntosDisjuntos(self.nombresVertices())
        aristas = sorted(self._aristasUnicas(), key=lambda x: (x.getPeso(), x.getOrigen(), x.getDestino()))
        arbol, componentes = [], len(self.listaVertices)
        while componentes > 1:
            mejores = {}
            for a in aristas:
                ra, rb = conjuntos.buscar(a.getOrigen()), conjuntos.buscar(a.getDestino())
                if ra == rb:
                    continue
                for r in (ra, rb):
                    if r not in mejores:
                        mejores[r] = a
            if not mejores:
                break  # grafo no conexo
            for a in mejores.values():
                if conjuntos.unir(a.getOrigen(), a.getDestino()):
                    arbol.append(a)
                    componentes -= 1
        return arbol

    @staticmethod
    def pesoTotal(aristas):
        return sum(a.getPeso() for a in aristas)

    # ------------------------------------------------------------------ #
    # BLOQUEO DE ARISTAS
    # ------------------------------------------------------------------ #
    def hayRuta(self, origen, destino):
        return destino in self.recorridoAmplitud(origen)

    def bloquearArista(self, origen, destino):
        """Bloquea el camino origen <-> destino SOLO si sigue existiendo una
        ruta alterna entre ambos. Devuelve True si quedó bloqueado."""
        directa = self.obtenerArista(origen, destino)
        inversa = self.obtenerArista(destino, origen)
        if directa is None and inversa is None:
            return False
        quitadas = [a for a in (directa, inversa) if a is not None]
        for a in quitadas:
            self.eliminarArista(a.getOrigen(), a.getDestino())
        if self.hayRuta(origen, destino):
            self.bloqueadas.extend(quitadas)
            return True
        for a in quitadas:  # no había alterna: se restaura
            self.ingresarArista(a.getOrigen(), a.getDestino(), a.getPeso())
        return False

    def desbloquearAristas(self):
        for a in self.bloqueadas:
            self.ingresarArista(a.getOrigen(), a.getDestino(), a.getPeso())
        self.bloqueadas.clear()

    def caminoBloqueado(self, origen, destino):
        """Ruta mínima origen -> destino con el camino directo bloqueado
        (ruta alterna). Devuelve la lista de aristas ([] si no hay alterna)."""
        if not self.bloquearArista(origen, destino):
            return []
        try:
            return self.caminoMasCorto(origen, destino)
        finally:
            self.desbloquearAristas()
