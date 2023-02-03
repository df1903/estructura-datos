"""
Árbol Binario de Búsqueda (ABB) con todos los ejercicios del taller de árboles.

Los nombres de los métodos son los del taller original (ingresar,
mostrarInOrden, alturaArbol, sumaNivel, ...). Todos los métodos de recorrido
reciben opcionalmente el nodo desde donde empezar; si no se indica, parten de
la raíz.

Niveles: la raíz está en el nivel 1.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from .nodo import Nodo


def esPrimo(n):
    """True si n es primo."""
    if not isinstance(n, int) or n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


RAIZ = object()  # valor por defecto: "empezar desde la raíz del árbol"


class Arbol:
    """ABB. Los datos menores van a la izquierda y los mayores a la derecha.

    `clave` permite ordenar objetos por un atributo (ej. la placa de un
    vehículo): clave=lambda v: v.placa. Por defecto el dato se ordena a sí mismo.
    """

    def __init__(self, clave=None):
        self.raiz = None
        self.lista = []
        self.suma = 0
        self.clave = clave or (lambda dato: dato)

    # ------------------------------------------------------------------ #
    # get / set
    # ------------------------------------------------------------------ #
    def getRaiz(self):
        return self.raiz

    def setRaiz(self, raiz):
        self.raiz = raiz

    def getLista(self):
        return self.lista

    def _inicio(self, padre):
        return self.raiz if padre is RAIZ else padre

    # ------------------------------------------------------------------ #
    # 1) Ingreso
    # ------------------------------------------------------------------ #
    def ingresar(self, nodo):
        """Ingresa un nodo. Si el dato ya existe NO se duplica: se incrementa
        `repetidos` del nodo existente (ejercicios 12 y 20 del taller)."""
        if not isinstance(nodo, Nodo):
            nodo = Nodo(nodo)
        if self.raiz is None:
            self.raiz = nodo
            return
        actual = self.raiz
        while True:
            k, ka = self.clave(nodo.getDato()), self.clave(actual.getDato())
            if k == ka:
                actual.setRepetidos(actual.getRepetidos() + 1)
                return
            if k < ka:
                if actual.getIzq() is None:
                    actual.setIzq(nodo)
                    return
                actual = actual.getIzq()
            else:
                if actual.getDer() is None:
                    actual.setDer(nodo)
                    return
                actual = actual.getDer()

    def ingresarInvertido(self, nodo):
        """Ingreso con orden invertido: los mayores van a la izquierda."""
        if not isinstance(nodo, Nodo):
            nodo = Nodo(nodo)
        if self.raiz is None:
            self.raiz = nodo
            return
        actual = self.raiz
        while True:
            k, ka = self.clave(nodo.getDato()), self.clave(actual.getDato())
            if k == ka:
                actual.setRepetidos(actual.getRepetidos() + 1)
                return
            if k > ka:
                if actual.getIzq() is None:
                    actual.setIzq(nodo)
                    return
                actual = actual.getIzq()
            else:
                if actual.getDer() is None:
                    actual.setDer(nodo)
                    return
                actual = actual.getDer()

    # ------------------------------------------------------------------ #
    # 2) Recorridos que muestran
    # ------------------------------------------------------------------ #
    def mostrarInOrden(self, padre=RAIZ):
        padre = self._inicio(padre)
        if padre is None:
            return
        self.mostrarInOrden(padre.getIzq())
        print(padre.getDato())
        self.mostrarInOrden(padre.getDer())

    def mostrarPreOrden(self, padre=RAIZ):
        padre = self._inicio(padre)
        if padre is None:
            return
        print(padre.getDato())
        self.mostrarPreOrden(padre.getIzq())
        self.mostrarPreOrden(padre.getDer())

    def mostrarPostOrden(self, padre=RAIZ):
        padre = self._inicio(padre)
        if padre is None:
            return
        self.mostrarPostOrden(padre.getIzq())
        self.mostrarPostOrden(padre.getDer())
        print(padre.getDato())

    # ------------------------------------------------------------------ #
    # 3) Recorridos que retornan lista
    # ------------------------------------------------------------------ #
    def inOrden(self, padre=RAIZ):
        """Devuelve (y guarda en self.lista) los datos en in-orden."""
        self.lista = self._recorrer(self._inicio(padre), "in")
        return self.lista

    def preOrden(self, padre=RAIZ):
        self.lista = self._recorrer(self._inicio(padre), "pre")
        return self.lista

    def postOrden(self, padre=RAIZ):
        self.lista = self._recorrer(self._inicio(padre), "post")
        return self.lista

    def _recorrer(self, padre, tipo):
        if padre is None:
            return []
        izq = self._recorrer(padre.getIzq(), tipo)
        der = self._recorrer(padre.getDer(), tipo)
        if tipo == "pre":
            return [padre.getDato()] + izq + der
        if tipo == "in":
            return izq + [padre.getDato()] + der
        return izq + der + [padre.getDato()]

    # ------------------------------------------------------------------ #
    # 4) Alturas
    # ------------------------------------------------------------------ #
    def alturaArbol(self, raiz=RAIZ):
        """Altura (en niveles) del árbol o subárbol. Árbol vacío = 0."""
        raiz = self._inicio(raiz)
        if raiz is None:
            return 0
        return 1 + max(self.alturaArbol(raiz.getIzq()), self.alturaArbol(raiz.getDer()))

    def alturaMayor(self):
        """Retorna la altura mayor del árbol."""
        return self.alturaArbol()

    def alturaRaiz(self, padre, alt, num):
        """Nivel al que se encuentra `num` (altura desde la raíz hasta él).
        Se llama como alturaRaiz(raiz, 0, num). Devuelve None si no existe."""
        if padre is None:
            return None
        if padre.getDato() == num:
            return alt + 1
        siguiente = padre.getIzq() if num < padre.getDato() else padre.getDer()
        return self.alturaRaiz(siguiente, alt + 1, num)

    def alturaElemento(self, padre, num):
        """Altura del subárbol que cuelga de `num` (None si no está)."""
        if padre is None:
            return None
        if padre.getDato() == num:
            return self.alturaArbol(padre)
        siguiente = padre.getIzq() if num < padre.getDato() else padre.getDer()
        return self.alturaElemento(siguiente, num)

    # ------------------------------------------------------------------ #
    # 5) Sumas
    # ------------------------------------------------------------------ #
    def sumaArbol(self, padre=RAIZ, suma=0):
        """Suma de todos los elementos del árbol."""
        padre = self._inicio(padre)
        if padre is None:
            return suma
        suma += padre.getDato()
        suma = self.sumaArbol(padre.getIzq(), suma)
        return self.sumaArbol(padre.getDer(), suma)

    def sumaNivel(self, padre, nivel, actual=1):
        """6) Suma de los datos desde `nivel` en adelante (raíz = nivel 1)."""
        if padre is None:
            return 0
        propio = padre.getDato() if actual >= nivel else 0
        total = propio + self.sumaNivel(padre.getIzq(), nivel, actual + 1) \
            + self.sumaNivel(padre.getDer(), nivel, actual + 1)
        if actual == 1:
            self.suma = total
        return total

    # ------------------------------------------------------------------ #
    # 7-11) Primos, menor, mayor, hojas, conteo
    # ------------------------------------------------------------------ #
    def primos(self):
        """Lista con todos los números primos del árbol."""
        return [d for d in self.inOrden() if esPrimo(d)]

    def devolvermenor(self, padre=RAIZ):
        padre = self._inicio(padre)
        if padre is None:
            return None
        return padre.getDato() if not padre.getIzq() else self.devolvermenor(padre.getIzq())

    def devolvermayor(self, padre=RAIZ):
        padre = self._inicio(padre)
        if padre is None:
            return None
        return padre.getDato() if not padre.getDer() else self.devolvermayor(padre.getDer())

    def mostrarHojas(self, padre=RAIZ):
        for hoja in self.hojas(padre):
            print(hoja)

    def hojas(self, padre=RAIZ):
        """Lista con las hojas (nodos sin hijos) del árbol."""
        padre = self._inicio(padre)
        if padre is None:
            return []
        if padre.esHoja():
            return [padre.getDato()]
        return self.hojas(padre.getIzq()) + self.hojas(padre.getDer())

    def numNodos(self, padre=RAIZ):
        """Cantidad de nodos del árbol."""
        padre = self._inicio(padre)
        if padre is None:
            return 0
        return 1 + self.numNodos(padre.getIzq()) + self.numNodos(padre.getDer())


    # ------------------------------------------------------------------ #
    # Búsqueda
    # ------------------------------------------------------------------ #
    def buscar(self, dato):
        """Devuelve el nodo cuyo dato (o clave) coincide, o None."""
        k = dato if not hasattr(dato, "__dict__") else self.clave(dato)
        actual = self.raiz
        while actual is not None:
            ka = self.clave(actual.getDato())
            if k == ka:
                return actual
            actual = actual.getIzq() if k < ka else actual.getDer()
        return None

    def existe(self, dato):
        return self.buscar(dato) is not None

    def buscarPreOrden(self, padre, num):
        """Busca recorriendo pre-orden (sirve aunque el árbol no sea ABB)."""
        if padre is None:
            return None
        if padre.getDato() == num:
            return padre
        return self.buscarPreOrden(padre.getIzq(), num) or self.buscarPreOrden(padre.getDer(), num)

    def cuantasVeces(self, dato):
        """Cuántas veces se ha ingresado un dato (1 + repetidos), 0 si no está."""
        nodo = self.buscar(dato)
        return 0 if nodo is None else 1 + nodo.getRepetidos()

    # ------------------------------------------------------------------ #
    # 15) Los 3 tipos de eliminación
    # ------------------------------------------------------------------ #
    def eliminar(self, dato, modo="sucesor"):
        """Elimina `dato` (o la clave) del árbol. Devuelve True si lo eliminó.

        Casos:
          1. nodo hoja            -> se quita.
          2. nodo con un hijo     -> el hijo ocupa su lugar.
          3. nodo con dos hijos   -> se reemplaza por su sucesor in-orden
                                     (menor del subárbol derecho) o, con
                                     modo="predecesor", por el mayor del izquierdo.
        """
        k = dato if not hasattr(dato, "__dict__") else self.clave(dato)
        existia = self.buscar(k) is not None
        self.raiz = self._eliminar(self.raiz, k, modo)
        return existia

    def _eliminar(self, nodo, k, modo):
        if nodo is None:
            return None
        kn = self.clave(nodo.getDato())
        if k < kn:
            nodo.setIzq(self._eliminar(nodo.getIzq(), k, modo))
        elif k > kn:
            nodo.setDer(self._eliminar(nodo.getDer(), k, modo))
        else:
            if nodo.getIzq() is None:      # hoja o solo hijo derecho
                return nodo.getDer()
            if nodo.getDer() is None:      # solo hijo izquierdo
                return nodo.getIzq()
            if modo == "predecesor":
                reemplazo = nodo.getIzq()
                while reemplazo.getDer():
                    reemplazo = reemplazo.getDer()
                nodo.setDato(reemplazo.getDato())
                nodo.setRepetidos(reemplazo.getRepetidos())
                nodo.setIzq(self._eliminar(nodo.getIzq(), self.clave(reemplazo.getDato()), modo))
            else:
                reemplazo = nodo.getDer()
                while reemplazo.getIzq():
                    reemplazo = reemplazo.getIzq()
                nodo.setDato(reemplazo.getDato())
                nodo.setRepetidos(reemplazo.getRepetidos())
                nodo.setDer(self._eliminar(nodo.getDer(), self.clave(reemplazo.getDato()), modo))
        return nodo

    def eliminarNodo(self, nodo):
        """Compatibilidad con el taller: elimina el nodo dado."""
        return self.eliminar(nodo.getDato())

    # ------------------------------------------------------------------ #
    # 17) Intercambiar datos de dos nodos
    # ------------------------------------------------------------------ #
    def intercambiar(self, datoA, datoB):
        """Intercambia los datos de dos nodos cualesquiera. OJO: puede romper
        la propiedad de ABB (es lo que pide el ejercicio)."""
        a, b = self.buscarPreOrden(self.raiz, datoA), self.buscarPreOrden(self.raiz, datoB)
        if a is None or b is None:
            return False
        a.dato, b.dato = b.dato, a.dato
        return True

    # ------------------------------------------------------------------ #
    # Árboles espejo / gemelos
    # ------------------------------------------------------------------ #
    def sonGemelos(self, raizA, raizB):
        """True si A y B son espejo uno del otro (mismos datos, lados cruzados)."""
        if raizA is None and raizB is None:
            return True
        if raizA is None or raizB is None:
            return False
        return (raizA.getDato() == raizB.getDato()
                and self.sonGemelos(raizA.getIzq(), raizB.getDer())
                and self.sonGemelos(raizA.getDer(), raizB.getIzq()))

    # ------------------------------------------------------------------ #
    # Dibujo
    # ------------------------------------------------------------------ #
    def graficar(self, padre=RAIZ, prefijo="", lado=""):
        """Devuelve el árbol dibujado como texto (raíz arriba, izq/der indentados)."""
        padre = self._inicio(padre)
        if padre is None:
            return "(vacío)"
        extra = f" x{1 + padre.getRepetidos()}" if padre.getRepetidos() else ""
        txt = f"{prefijo}{lado}{padre.getDato()}{extra}\n"
        for etiqueta, hijo in (("I: ", padre.getIzq()), ("D: ", padre.getDer())):
            if hijo:
                txt += self.graficar(hijo, prefijo + "    ", etiqueta)
        return txt


# ---------------------------------------------------------------------- #
# Ejercicios 18-23: árboles construidos a partir de una regla
# ---------------------------------------------------------------------- #
def paresYPrimos(arbol):
    """18) Vector con los números que son pares y primos a la vez (solo el 2)."""
    return [d for d in arbol.inOrden() if d % 2 == 0 and esPrimo(d)]


def arbolDePares(arbol):
    """19) Guarda los pares de `arbol` en una lista y crea con ellos un árbol."""
    pares = [d for d in arbol.inOrden() if d % 2 == 0]
    nuevo = Arbol()
    for p in pares:
        nuevo.ingresar(Nodo(p))
    return pares, nuevo


class ArbolPorRegla(Arbol):
    """Árbol donde una regla decide si el dato baja por la izquierda o la derecha.

    `vaALaIzquierda(dato) -> bool`. El dato se ubica en el primer hueco libre
    siguiendo la regla desde la raíz.
    """

    def __init__(self, vaALaIzquierda):
        super().__init__()
        self.vaALaIzquierda = vaALaIzquierda

    def ingresar(self, nodo):
        if not isinstance(nodo, Nodo):
            nodo = Nodo(nodo)
        if self.raiz is None:
            self.raiz = nodo
            return
        actual = self.raiz
        while True:
            if self.vaALaIzquierda(nodo.getDato()):
                if actual.getIzq() is None:
                    actual.setIzq(nodo)
                    return
                actual = actual.getIzq()
            else:
                if actual.getDer() is None:
                    actual.setDer(nodo)
                    return
                actual = actual.getDer()


def arbolParesIzquierdaImparesDerecha():
    """21) Pares a la izquierda, impares a la derecha."""
    return ArbolPorRegla(lambda d: d % 2 == 0)


def arbolPrimosDerechaRestoIzquierda():
    """22) Primos a la derecha, el resto a la izquierda."""
    return ArbolPorRegla(lambda d: not esPrimo(d))


class Vehiculo:
    """Vehículo identificado por su placa."""

    def __init__(self, placa, marca="", modelo=""):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo

    def __repr__(self):
        detalle = f", {self.marca} {self.modelo}".rstrip() if self.marca or self.modelo else ""
        return f"Vehiculo({self.placa}{detalle})"


def arbolDeVehiculos():
    """23) Árbol de vehículos: según la placa van por izquierda (menor) o derecha (mayor)."""
    return Arbol(clave=lambda v: v.placa)
