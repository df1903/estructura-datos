"""
Ejercicios básicos de diccionarios (1 al 9).

La lógica está en funciones puras (fáciles de probar); la interacción por
consola está en las funciones `interactivo_N` y en el menú del final.
Ejecutar:  python -m diccionarios.ejercicios_basicos

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import sys

from helpers.keyboard import Keyboard

# --------------------------------------------------------------------------- #
# 1) Divisas
# --------------------------------------------------------------------------- #
DIVISAS = {"Euro": "€", "Dollar": "$", "Yen": "¥"}


def simbolo_divisa(divisa, divisas=DIVISAS):
    """Símbolo de la divisa o None si no está en el diccionario."""
    return divisas.get(divisa.strip().title())


# --------------------------------------------------------------------------- #
# 2) Datos de una persona
# --------------------------------------------------------------------------- #
def frase_persona(persona):
    return (f"{persona['nombre']} tiene {persona['edad']} años, vive en "
            f"{persona['dirección']} y su número de teléfono es {persona['teléfono']}")


# --------------------------------------------------------------------------- #
# 3) Precio de frutas
# --------------------------------------------------------------------------- #
FRUTAS = {"platano": 1.35, "manzana": 0.80, "pera": 0.85, "naranja": 0.70}


def precio_fruta(fruta, kilos, frutas=FRUTAS):
    """Precio de `kilos` de `fruta`, o None si no hay esa fruta."""
    if fruta not in frutas:
        return None
    return round(frutas[fruta] * kilos, 2)


# --------------------------------------------------------------------------- #
# 4) Fecha con nombre del mes
# --------------------------------------------------------------------------- #
MESES = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
         7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre",
         12: "diciembre"}


def fecha_en_texto(fecha):
    """'25/12/2022' -> '25 de diciembre de 2022'."""
    dia, mes, anio = fecha.split("/")
    return f"{int(dia)} de {MESES[int(mes)]} de {anio}"


# --------------------------------------------------------------------------- #
# 5) Créditos de un curso
# --------------------------------------------------------------------------- #
CURSO = {"Matemáticas": 6, "Física": 4, "Química": 5}


def resumen_creditos(curso):
    """Devuelve (líneas de texto, total de créditos)."""
    lineas = [f"{asignatura} tiene {creditos} créditos" for asignatura, creditos in curso.items()]
    return lineas, sum(curso.values())


# --------------------------------------------------------------------------- #
# 6) Diccionario que se llena dinámicamente -> ver interactivo_6
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# 7) Cesta de la compra
# --------------------------------------------------------------------------- #
def total_compra(compra):
    """Suma de los precios de la cesta."""
    return sum(compra.values())


# --------------------------------------------------------------------------- #
# 8) Traductor español-inglés
# --------------------------------------------------------------------------- #
def crear_diccionario(texto):
    """'casa:house,perro:dog' -> {'casa': 'house', 'perro': 'dog'}"""
    diccionario = {}
    for par in texto.split(","):
        if ":" in par:
            palabra, traduccion = par.split(":", 1)
            diccionario[palabra.strip().lower()] = traduccion.strip()
    return diccionario


def traducir(frase, diccionario):
    """Traduce palabra a palabra; las que no están se dejan igual."""
    return " ".join(diccionario.get(p.lower(), p) for p in frase.split())


# --------------------------------------------------------------------------- #
# 9) Facturas pendientes de cobro
# --------------------------------------------------------------------------- #
class Facturas:
    """Número de factura -> costo. Lleva lo cobrado y lo pendiente."""

    def __init__(self):
        self.facturas = {}
        self.cobrado = 0

    @property
    def pendiente(self):
        return sum(self.facturas.values())

    def agregar(self, numero, costo):
        self.facturas[numero] = costo

    def pagar(self, numero):
        """Paga (elimina) la factura. Devuelve su valor o None si no existe."""
        valor = self.facturas.pop(numero, None)
        if valor is not None:
            self.cobrado += valor
        return valor


# --------------------------------------------------------------------------- #
# Versiones interactivas
# --------------------------------------------------------------------------- #
def interactivo_1():
    simbolo = simbolo_divisa(input("Ingrese la divisa: "))
    print("El símbolo de la divisa es", simbolo) if simbolo else print("La divisa no está en el diccionario")


def interactivo_2():
    persona = {k: input(f"Ingrese su {k}: ") for k in ("nombre", "edad", "dirección", "teléfono")}
    print(frase_persona(persona))


def interactivo_3():
    for fruta, precio in FRUTAS.items():
        print(f"{fruta} : {precio}")
    fruta = input("Ingrese la fruta que desea llevar: ")
    if fruta in FRUTAS:
        kilos = Keyboard.readIntRangeDefaultErrorMessage("Cantidad de kilos: ", 0, sys.maxsize)
        print(f"Usted llevó {kilos} kg de {fruta} a un precio de {precio_fruta(fruta, kilos)}")
    else:
        print(f"No tenemos {fruta} en nuestro inventario")


def interactivo_4():
    print(fecha_en_texto(input("Introduce una fecha en formato dd/mm/aaaa: ")))


def interactivo_5():
    lineas, total = resumen_creditos(CURSO)
    print("\n".join(lineas))
    print(f"El curso tiene un total de {total} créditos")


def interactivo_6():
    datos = {}
    while True:
        datos[input("Tipo de dato que desea almacenar: ")] = input("Valor correspondiente: ")
        print(datos)
        if not Keyboard.readBoolean("¿Desea continuar? (si/no): "):
            break


def interactivo_7():
    compra = {}
    while True:
        articulo = input("Nombre del artículo: ")
        compra[articulo] = Keyboard.readIntDefaultErrorMessage("Valor del artículo: ")
        if not Keyboard.readBoolean("¿Desea continuar? (si/no): "):
            break
    for articulo, precio in compra.items():
        print(f"{articulo} --- {precio}")
    print("Compra total:", total_compra(compra))


def interactivo_8():
    diccionario = crear_diccionario(input("Pares palabra:traducción separados por comas: "))
    print(traducir(input("Frase a traducir: "), diccionario))


def interactivo_9():
    f = Facturas()
    opcion = 0
    while opcion != 3:
        opcion = Keyboard.readIntRange("1 - Añadir factura | 2 - Pagar factura | 3 - Terminar: ",
                                       "Ingrese 1, 2 o 3", 1, 3)
        if opcion == 1:
            f.agregar(input("Número de la factura: "), Keyboard.readIntDefaultErrorMessage("Costo: "))
        elif opcion == 2:
            for numero, valor in f.facturas.items():
                print(f"{numero} --- {valor}")
            if f.pagar(input("Número de la factura a pagar: ")) is None:
                print("Esa factura no existe")
        print(f"Cobrado: {f.cobrado} | Pendiente: {f.pendiente}")


def main():
    ejercicios = {1: interactivo_1, 2: interactivo_2, 3: interactivo_3, 4: interactivo_4,
                  5: interactivo_5, 6: interactivo_6, 7: interactivo_7, 8: interactivo_8,
                  9: interactivo_9}
    while True:
        n = Keyboard.readIntRange("Ejercicio (1-9, 0 para salir): ", "Elija entre 0 y 9", 0, 9)
        if n == 0:
            break
        ejercicios[n]()


if __name__ == "__main__":
    main()
