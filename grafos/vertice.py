"""
Vértice de un grafo.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""


class Vertice:
    """Vértice con un dato (nombre) y la lista de vértices adyacentes (destinos)."""

    def __init__(self, dato):
        self.dato = dato
        self.listaAdyacentes = []

    def getDato(self):
        return self.dato

    def setDato(self, dato):
        self.dato = dato

    def getListaAdyacentes(self):
        return self.listaAdyacentes

    def setListaAdyacentes(self, listaAdyacentes):
        self.listaAdyacentes = listaAdyacentes

    def __repr__(self):
        return f"Vertice({self.dato!r})"
