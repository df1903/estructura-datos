"""
Demostración del taller de árboles ABB (2020-2).
Ejecutar desde la raíz del proyecto:  python -m arboles.taller_abb

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from .arbol_abb import (Arbol, Vehiculo, arbolDePares, arbolDeVehiculos,
                        arbolParesIzquierdaImparesDerecha,
                        arbolPrimosDerechaRestoIzquierda, paresYPrimos)
from .nodo import Nodo


def construir_arbol():
    A = Arbol()
    for n in (15, 9, 13, 14, 2, 7, 6, 8, 5, 3, 4, 1, 10, 11, 12, 20, 16, 17, 19, 18, 2):
        A.ingresar(Nodo(n))  # el último 2 es repetido
    return A


def main():
    A = construir_arbol()
    print("Árbol:\n" + A.graficar())
    print("1-2) Recorridos:")
    print("   pre-orden :", A.preOrden())
    print("   in-orden  :", A.inOrden())
    print("   post-orden:", A.postOrden())
    print("4) Altura del árbol:", A.alturaArbol())
    print("   Altura hasta el 12:", A.alturaRaiz(A.getRaiz(), 0, 12))
    print("   Altura del subárbol del 9:", A.alturaElemento(A.getRaiz(), 9))
    print("5) Suma de elementos:", A.sumaArbol())
    print("6) Suma desde el nivel 4:", A.sumaNivel(A.getRaiz(), 4))
    print("7) Primos:", A.primos())
    print("8-9) Menor / mayor:", A.devolvermenor(), "/", A.devolvermayor())
    print("10-11) Hojas:", A.hojas())
    print("12) Veces que está el 2:", A.cuantasVeces(2))
    print("13) Cantidad de nodos:", A.numNodos())
    print("15) Eliminar hoja 4, nodo con un hijo 14 y nodo con dos hijos 9")
    for dato in (4, 14, 9):
        A.eliminar(dato)
    print("   in-orden:", A.inOrden())
    print("18) Pares y primos:", paresYPrimos(A))
    pares, arbolPares = arbolDePares(A)
    print("19) Pares:", pares, "-> árbol in-orden:", arbolPares.inOrden())

    pi = arbolParesIzquierdaImparesDerecha()
    pp = arbolPrimosDerechaRestoIzquierda()
    for n in range(1, 11):
        pi.ingresar(n)
        pp.ingresar(n)
    print("21) Pares izq / impares der:\n" + pi.graficar())
    print("22) Primos der / resto izq:\n" + pp.graficar())

    v = arbolDeVehiculos()
    for placa in ("KLM123", "ABC987", "XYZ555", "DEF321"):
        v.ingresar(Vehiculo(placa))
    print("23) Vehículos por placa (in-orden):", v.inOrden())


if __name__ == "__main__":
    main()
