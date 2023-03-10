"""Pruebas de ABB, AVL y búsquedas en árboles. Autor: Daniel Felipe Franco Rincón."""

import random

from arboles.arbol_abb import (Arbol, Vehiculo, arbolDePares, arbolDeVehiculos,
                               arbolParesIzquierdaImparesDerecha,
                               arbolPrimosDerechaRestoIzquierda, paresYPrimos)
from arboles.nodo import Nodo
from avl.arbol_avl import ArbolAVL
from busquedas.anchura_profundidad import bfs_arbol, dfs_arbol

DATOS = [15, 9, 13, 14, 2, 7, 6, 8, 5, 3, 4, 1, 10, 11, 12, 20]


def construir():
    a = Arbol()
    for n in DATOS:
        a.ingresar(Nodo(n))
    return a


def test_recorridos_y_listas():
    a = construir()
    assert a.inOrden() == sorted(DATOS)
    assert a.preOrden()[0] == 15 and a.postOrden()[-1] == 15
    # llamar dos veces no acumula (en el taller original sí acumulaba)
    assert a.inOrden() == a.inOrden()


def test_alturas_y_sumas():
    a = construir()
    assert a.numNodos() == 16
    assert a.sumaArbol() == sum(DATOS)
    assert a.alturaRaiz(a.getRaiz(), 0, 15) == 1
    assert a.alturaRaiz(a.getRaiz(), 0, 99) is None
    assert a.sumaNivel(a.getRaiz(), 1) == sum(DATOS)
    assert a.sumaNivel(a.getRaiz(), 2) == sum(DATOS) - 15
    assert a.alturaArbol() == a.alturaMayor()
    assert Arbol().alturaArbol() == 0


def test_menor_mayor_primos_hojas():
    a = construir()
    assert (a.devolvermenor(), a.devolvermayor()) == (1, 20)
    assert a.primos() == [2, 3, 5, 7, 11, 13]
    assert a.hojas() == [1, 4, 8, 12, 14, 20]
    assert paresYPrimos(a) == [2]
    assert Arbol().devolvermenor() is None


def test_repetidos():
    a = construir()
    a.ingresar(Nodo(7))
    a.ingresar(Nodo(7))
    assert a.cuantasVeces(7) == 3 and a.cuantasVeces(999) == 0
    assert a.numNodos() == 16  # no se crean nodos nuevos


def test_eliminar_tres_casos():
    a = construir()
    assert a.eliminar(4)           # hoja
    assert a.eliminar(14)          # un hijo? (13 -> 14 hoja)  y luego:
    assert a.eliminar(9)           # dos hijos
    assert a.eliminar(15)          # raíz con dos hijos
    assert not a.eliminar(1000)
    esperado = sorted(set(DATOS) - {4, 14, 9, 15})
    assert a.inOrden() == esperado
    b = construir()
    b.eliminar(15, modo="predecesor")
    assert b.inOrden() == sorted(set(DATOS) - {15})
    vacio = Arbol()
    vacio.ingresar(1)
    vacio.eliminar(1)
    assert vacio.getRaiz() is None


def test_intercambiar_y_gemelos():
    a = construir()
    assert a.intercambiar(1, 20)
    assert a.buscarPreOrden(a.getRaiz(), 20) is not None
    x, y = Arbol(), Arbol()
    for n in (5, 3, 8):
        x.ingresar(n)
    for n in (5, 3, 8):
        y.ingresarInvertido(n)  # espejo de x
    assert x.sonGemelos(x.getRaiz(), y.getRaiz())
    y.ingresar(1)
    assert not x.sonGemelos(x.getRaiz(), y.getRaiz())


def test_arboles_por_regla():
    pi = arbolParesIzquierdaImparesDerecha()
    pp = arbolPrimosDerechaRestoIzquierda()
    for n in range(1, 11):
        pi.ingresar(n)
        pp.ingresar(n)
    assert sorted(pi.inOrden()) == list(range(1, 11))
    assert pi.getRaiz().getIzq().getDato() == 2 and pi.getRaiz().getDer().getDato() == 3
    assert pp.getRaiz().getDer().getDato() == 2
    pares, arbol = arbolDePares(construir())
    assert pares == [2, 4, 6, 8, 10, 12, 14, 20]
    assert arbol.inOrden() == pares


def test_vehiculos_por_placa():
    v = arbolDeVehiculos()
    for p in ("KLM123", "ABC987", "XYZ555"):
        v.ingresar(Vehiculo(p))
    assert [x.placa for x in v.inOrden()] == ["ABC987", "KLM123", "XYZ555"]
    assert v.buscar("XYZ555").getDato().placa == "XYZ555"
    assert v.eliminar("KLM123") and v.numNodos() == 2


# ------------------------------- AVL ------------------------------------ #
def test_avl_rotaciones_basicas():
    for secuencia in ([3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]):
        t = ArbolAVL()
        for n in secuencia:
            t.insertar(n)
        assert t.getRaiz().dato == 2 and t.esAVL()


def test_avl_orden_creciente_y_aleatorio():
    t = ArbolAVL()
    for n in range(1, 1024):
        t.insertar(n)
    assert t.alturaArbol() == 10 and t.esAVL()
    datos = random.Random(7).sample(range(10_000), 500)
    t2 = ArbolAVL()
    for n in datos:
        t2.insertar(n)
    assert t2.inOrden() == sorted(datos) and t2.esAVL()
    for n in datos[:250]:
        assert t2.eliminar(n)
        assert t2.esAVL()
    assert t2.inOrden() == sorted(datos[250:])


def test_avl_repetidos_y_consultas():
    t = ArbolAVL()
    assert t.insertar(5) and not t.insertar(5)
    assert t.eliminar(5) and not t.eliminar(5)
    assert t.getRaiz() is None and t.minimo() is None
    for n in (10, 5, 20):
        t.ingresar(n)
    assert (t.minimo(), t.maximo()) == (5, 20)
    assert t.porNiveles() == [[10], [5, 20]]


# --------------------------- búsquedas en árbol -------------------------- #
def test_busquedas_en_arbol():
    a = construir()
    niveles = bfs_arbol(a.getRaiz())
    assert niveles[0] == [15] and sum(len(n) for n in niveles) == 16
    assert dfs_arbol(a.getRaiz(), "pre") == a.preOrden()
    assert dfs_arbol(a.getRaiz(), "in") == a.inOrden()
    assert dfs_arbol(a.getRaiz(), "post") == a.postOrden()
    assert bfs_arbol(None) == [] and dfs_arbol(None, "in") == []
