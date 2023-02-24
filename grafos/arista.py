"""
Arista de un grafo.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""


class Arista:
    """Arista dirigida origen -> destino con un peso."""

    def __init__(self, origen, destino, peso=1):
        self.origen = origen
        self.destino = destino
        self.peso = peso

    def getOrigen(self):
        return self.origen

    def setOrigen(self, origen):
        self.origen = origen

    def getDestino(self):
        return self.destino

    def setDestino(self, destino):
        self.destino = destino

    def getPeso(self):
        return self.peso

    def setPeso(self, peso):
        self.peso = peso

    def __repr__(self):
        return f"Arista({self.origen!r} -> {self.destino!r}, peso={self.peso})"
