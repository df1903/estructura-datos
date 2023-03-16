"""
Validación de entradas por consola.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import sys

PREFIJO = "▌▓▒░    "


class Keyboard:
    """Lecturas seguras: repiten la pregunta hasta recibir un valor válido."""

    @staticmethod
    def readInt(inputMessage, errorMessage="Ingrese un valor correcto"):
        while True:
            try:
                return int(input(PREFIJO + inputMessage))
            except ValueError:
                print(PREFIJO + errorMessage)

    @staticmethod
    def readIntDefaultErrorMessage(inputMessage):
        return Keyboard.readInt(inputMessage)

    @staticmethod
    def readIntRange(inputMessage, errorMessage, minValue, maxValue):
        while True:
            valor = Keyboard.readInt(inputMessage, errorMessage)
            if minValue <= valor <= maxValue:
                return valor
            print(PREFIJO + errorMessage)

    @staticmethod
    def readIntRangeDefaultErrorMessage(inputMessage, minValue=0, maxValue=sys.maxsize):
        return Keyboard.readIntRange(
            inputMessage, "Ingrese un valor correcto", minValue, maxValue
        )

    @staticmethod
    def readBoolean(inputMessage, errorMessage="Ingrese si o no"):
        while True:
            valor = input(PREFIJO + inputMessage).strip().lower()
            if valor.startswith(("s", "y")):
                return True
            if valor.startswith("n"):
                return False
            print(PREFIJO + errorMessage)
