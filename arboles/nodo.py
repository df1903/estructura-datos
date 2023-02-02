"""
Nodo de un árbol binario.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""


class Nodo:
    """Nodo con dato, hijo izquierdo, hijo derecho y contador de repetidos."""

    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None
        self.repetidos = 0  # veces extra que se intentó ingresar el mismo dato

    # dato
    def getDato(self):
        return self.dato

    def setDato(self, dato):
        self.dato = dato

    # izquierda
    def getIzq(self):
        return self.izq

    def setIzq(self, izq):
        self.izq = izq

    # derecha
    def getDer(self):
        return self.der

    def setDer(self, der):
        self.der = der

    # repetidos
    def getRepetidos(self):
        return self.repetidos

    def setRepetidos(self, repetidos):
        self.repetidos = repetidos

    def esHoja(self):
        return self.izq is None and self.der is None

    def __repr__(self):
        return f"Nodo({self.dato!r})"
