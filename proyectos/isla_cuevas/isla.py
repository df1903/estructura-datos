"""
Modelo del proyecto "La isla El Paro" (árboles).

La empresa Acme explota un sistema de cuevas (árbol binario) con 5 materiales:
oro, plata, bronce, piedra y madera.

Reglas del enunciado:
  * Cada 10 s cada cueva produce 2 unidades de su material.
  * Cada 30 s se despacha un camión (si hay) que recorre el sistema (pre, in o
    post-orden al azar), recoge el 20 % de cada cueva y lo deja en el almacén.
  * Cuando el almacén supera otras 100 unidades se crea una cueva nueva. La
    creación debe mantener el árbol balanceado: se inserta en el primer hueco
    por niveles (recorrido en anchura), así el árbol siempre es completo.
  * Una cueva con menos de 10 unidades puede eliminarse; al eliminarla el árbol
    también se mantiene completo (se reemplaza por la última cueva del último nivel).

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import random
from collections import deque

MATERIALES = ["oro", "plata", "bronce", "piedra", "madera"]
PORCENTAJE_EXTRACCION = 0.2
INCREMENTO = 2
MINIMO_ELIMINAR = 10


class Cueva:
    """Nodo del árbol."""

    def __init__(self, material=None, cantidad=None, rng=random):
        self.material = material or rng.choice(MATERIALES)
        self.cantidad = cantidad if cantidad is not None else rng.randint(10, 50)
        self.izquierda = None
        self.derecha = None

    # get / set
    def getMaterial(self):
        return self.material

    def setMaterial(self, material):
        self.material = material

    def getCantidad(self):
        return round(self.cantidad, 2)

    def setCantidad(self, cantidad):
        self.cantidad = cantidad

    def getIzquierda(self):
        return self.izquierda

    def setIzquierda(self, cueva):
        self.izquierda = cueva

    def getDerecha(self):
        return self.derecha

    def setDerecha(self, cueva):
        self.derecha = cueva

    def puedeEliminarse(self):
        return self.cantidad < MINIMO_ELIMINAR

    def __repr__(self):
        return f"Cueva({self.material}, {self.getCantidad()})"


class Almacen:
    def __init__(self, nombre="ACME"):
        self.nombre = nombre
        self.recursos = {m: 0 for m in MATERIALES}

    def ingresarRecursos(self, camion):
        for m in MATERIALES:
            self.recursos[m] += camion.carga[m]

    def getTotal(self):
        return round(sum(self.recursos.values()), 2)

    def __str__(self):
        detalle = " | ".join(f"{m.capitalize()}: {round(v, 2)}" for m, v in self.recursos.items())
        return f"Almacén {self.nombre} | {detalle} | Total: {self.getTotal()}"


class Camion:
    def __init__(self, id):
        self.id = id
        self.carga = {m: 0 for m in MATERIALES}

    def obtenerRecurso(self, cueva):
        """Se lleva el 20 % de la cueva y se lo suma a su carga."""
        extraido = cueva.cantidad * PORCENTAJE_EXTRACCION
        self.carga[cueva.material] += extraido
        cueva.cantidad -= extraido

    def vaciar(self):
        self.carga = {m: 0 for m in MATERIALES}

    def __str__(self):
        detalle = " | ".join(f"{m.capitalize()}: {round(v, 2)}" for m, v in self.carga.items())
        return f"Camión {self.id} | {detalle}"


class Isla:
    """Árbol binario completo de cuevas."""

    def __init__(self, nombre="El Paro"):
        self.nombre = nombre
        self.raiz = None

    def getRaiz(self):
        return self.raiz

    # ------------------------------------------------------------------ #
    # Inserción / eliminación balanceadas
    # ------------------------------------------------------------------ #
    def ingresar(self, cueva):
        """Inserta en el primer hueco por niveles (mantiene el árbol completo)."""
        if self.raiz is None:
            self.raiz = cueva
            return
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            if actual.izquierda is None:
                actual.izquierda = cueva
                return
            if actual.derecha is None:
                actual.derecha = cueva
                return
            cola.append(actual.izquierda)
            cola.append(actual.derecha)

    def _ultimaConPadre(self):
        """(última cueva por niveles, su padre)."""
        cola, ultimo, padre = deque([(self.raiz, None)]), None, None
        while cola:
            ultimo, padre = cola.popleft()
            for hijo in (ultimo.izquierda, ultimo.derecha):
                if hijo:
                    cola.append((hijo, ultimo))
        return ultimo, padre

    def eliminar(self, cueva):
        """Elimina la cueva dada manteniendo el árbol completo."""
        if self.raiz is None:
            return False
        ultima, padreUltima = self._ultimaConPadre()
        if ultima is cueva:
            if padreUltima is None:
                self.raiz = None
            elif padreUltima.derecha is ultima:
                padreUltima.derecha = None
            else:
                padreUltima.izquierda = None
            return True
        if cueva not in self.preOrden():
            return False
        # la cueva toma el contenido de la última y la última se desprende
        cueva.material, cueva.cantidad = ultima.material, ultima.cantidad
        if padreUltima.derecha is ultima:
            padreUltima.derecha = None
        else:
            padreUltima.izquierda = None
        return True

    # ------------------------------------------------------------------ #
    # Recorridos (devuelven la lista de cuevas)
    # ------------------------------------------------------------------ #
    def preOrden(self, padre="raiz"):
        padre = self.raiz if padre == "raiz" else padre
        return [] if padre is None else [padre] + self.preOrden(padre.izquierda) + self.preOrden(padre.derecha)

    def inOrden(self, padre="raiz"):
        padre = self.raiz if padre == "raiz" else padre
        return [] if padre is None else self.inOrden(padre.izquierda) + [padre] + self.inOrden(padre.derecha)

    def postOrden(self, padre="raiz"):
        padre = self.raiz if padre == "raiz" else padre
        return [] if padre is None else self.postOrden(padre.izquierda) + self.postOrden(padre.derecha) + [padre]

    def numNodos(self):
        return len(self.preOrden())

    def altura(self, padre="raiz"):
        padre = self.raiz if padre == "raiz" else padre
        return 0 if padre is None else 1 + max(self.altura(padre.izquierda), self.altura(padre.derecha))

    def incremento(self):
        """Cada cueva produce INCREMENTO unidades."""
        for cueva in self.preOrden():
            cueva.cantidad += INCREMENTO

    def cuevasEliminables(self):
        return [c for c in self.preOrden() if c.puedeEliminarse()]

    def mostrar(self, orden="pre"):
        cuevas = {"pre": self.preOrden, "in": self.inOrden, "post": self.postOrden}[orden]()
        for c in cuevas:
            print(f"▌▓▒░    Cueva con {c.material}, tiene {c.getCantidad()} materiales.")


class Simulacion:
    """Simulación por pasos de tiempo (sin esperas reales, fácil de probar)."""

    def __init__(self, numCamiones=10, numCuevas=7, semilla=None):
        self.rng = random.Random(semilla)
        self.isla = Isla()
        self.almacen = Almacen()
        self.camiones = [Camion(i + 1) for i in range(numCamiones)]
        self.tiempo = 0
        self.cuevasNuevas = 0   # cuántas veces se ha superado otra centena
        self.registro = []      # eventos ocurridos
        for _ in range(numCuevas):
            self.isla.ingresar(Cueva(rng=self.rng))

    def _log(self, mensaje):
        self.registro.append(f"[{self.tiempo:>4}s] {mensaje}")

    def recorridoAleatorio(self, camion):
        """El camión recorre la isla en pre, in o post-orden (al azar)."""
        orden = self.rng.choice(["pre", "in", "post"])
        cuevas = {"pre": self.isla.preOrden, "in": self.isla.inOrden, "post": self.isla.postOrden}[orden]()
        for cueva in cuevas:
            camion.obtenerRecurso(cueva)
        return orden

    def despachar(self):
        """Envía un camión: recorre, deposita en el almacén y se vacía."""
        if not self.camiones or self.isla.getRaiz() is None:
            return None
        camion = self.camiones.pop(0)
        orden = self.recorridoAleatorio(camion)
        self._log(f"Camión {camion.id} recorre en {orden}-orden: {camion}")
        self.almacen.ingresarRecursos(camion)
        camion.vaciar()
        self.camiones.append(camion)  # regresa a la base
        # nueva cueva por cada 100 unidades acumuladas en el almacén
        while int(self.almacen.getTotal() // 100) > self.cuevasNuevas:
            self.cuevasNuevas += 1
            nueva = Cueva(rng=self.rng)
            self.isla.ingresar(nueva)
            self._log(f"El almacén superó {self.cuevasNuevas * 100}: nueva cueva {nueva}")
        return camion

    def eliminarCuevasMenores(self, decidir=lambda cueva: True):
        """Elimina las cuevas con < 10 unidades que `decidir` apruebe."""
        eliminadas = []
        for cueva in self.isla.cuevasEliminables():
            if decidir(cueva) and self.isla.eliminar(cueva):
                eliminadas.append(cueva)
                self._log(f"Cueva eliminada: {cueva}")
        return eliminadas

    def avanzar(self, segundos=1, decidirEliminar=lambda cueva: True):
        """Avanza el reloj segundo a segundo aplicando las reglas del enunciado."""
        for _ in range(segundos):
            self.tiempo += 1
            if self.tiempo % 10 == 0:
                self.isla.incremento()
            if self.tiempo % 30 == 0:
                self.despachar()
                self.eliminarCuevasMenores(decidirEliminar)
