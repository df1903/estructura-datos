"""
Árbol AVL (Adelson-Velsky y Landis): árbol binario de búsqueda AUTO-BALANCEADO.

Invariante: en cada nodo, la diferencia de alturas entre sus subárboles
(factor de balance = altura(izq) - altura(der)) está en {-1, 0, 1}.
Si una inserción o eliminación lo rompe, se corrige con rotaciones:

    Caso Izq-Izq  (balance > 1  y  dato < izq.dato)   -> rotación simple a la derecha
    Caso Der-Der  (balance < -1 y  dato > der.dato)   -> rotación simple a la izquierda
    Caso Izq-Der  (balance > 1  y  dato > izq.dato)   -> rotación izquierda-derecha
    Caso Der-Izq  (balance < -1 y  dato < der.dato)   -> rotación derecha-izquierda

Insertar, buscar y eliminar son O(log n) en el peor caso.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""


class NodoAVL:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None
        self.altura = 1  # una hoja tiene altura 1

    def getDato(self):
        return self.dato

    def getIzq(self):
        return self.izq

    def getDer(self):
        return self.der

    def __repr__(self):
        return f"NodoAVL({self.dato!r})"


class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self.rotaciones = 0  # contador, útil para ver cuántas correcciones hizo

    def getRaiz(self):
        return self.raiz

    # ------------------------------------------------------------------ #
    # Utilidades de altura y balance
    # ------------------------------------------------------------------ #
    @staticmethod
    def altura(nodo):
        return nodo.altura if nodo else 0

    @staticmethod
    def _actualizarAltura(nodo):
        nodo.altura = 1 + max(ArbolAVL.altura(nodo.izq), ArbolAVL.altura(nodo.der))

    @staticmethod
    def factorBalance(nodo):
        """altura(izq) - altura(der). Positivo: cargado a la izquierda."""
        return ArbolAVL.altura(nodo.izq) - ArbolAVL.altura(nodo.der) if nodo else 0

    # ------------------------------------------------------------------ #
    # Rotaciones
    # ------------------------------------------------------------------ #
    def rotarDerecha(self, y):
        """      y            x
                / \\          / \\
               x   C   ->   A   y
              / \\              / \\
             A   B            B   C"""
        x = y.izq
        y.izq, x.der = x.der, y
        self._actualizarAltura(y)
        self._actualizarAltura(x)
        self.rotaciones += 1
        return x

    def rotarIzquierda(self, x):
        """    x                y
              / \\              / \\
             A   y     ->     x   C
                / \\          / \\
               B   C        A   B"""
        y = x.der
        x.der, y.izq = y.izq, x
        self._actualizarAltura(x)
        self._actualizarAltura(y)
        self.rotaciones += 1
        return y

    def _balancear(self, nodo):
        """Actualiza la altura de `nodo` y lo rebalancea si hace falta."""
        self._actualizarAltura(nodo)
        balance = self.factorBalance(nodo)
        if balance > 1:                                   # cargado a la izquierda
            if self.factorBalance(nodo.izq) < 0:          # caso Izq-Der
                nodo.izq = self.rotarIzquierda(nodo.izq)
            return self.rotarDerecha(nodo)                # caso Izq-Izq
        if balance < -1:                                  # cargado a la derecha
            if self.factorBalance(nodo.der) > 0:          # caso Der-Izq
                nodo.der = self.rotarDerecha(nodo.der)
            return self.rotarIzquierda(nodo)              # caso Der-Der
        return nodo

    # ------------------------------------------------------------------ #
    # Inserción
    # ------------------------------------------------------------------ #
    def insertar(self, dato):
        """Inserta `dato`. Devuelve False si ya existía (no se permiten repetidos)."""
        if self.buscar(dato):
            return False
        self.raiz = self._insertar(self.raiz, dato)
        return True

    ingresar = insertar

    def _insertar(self, nodo, dato):
        if nodo is None:
            return NodoAVL(dato)
        if dato < nodo.dato:
            nodo.izq = self._insertar(nodo.izq, dato)
        else:
            nodo.der = self._insertar(nodo.der, dato)
        return self._balancear(nodo)

    # ------------------------------------------------------------------ #
    # Eliminación
    # ------------------------------------------------------------------ #
    def eliminar(self, dato):
        """Elimina `dato`. Devuelve True si estaba en el árbol."""
        if not self.buscar(dato):
            return False
        self.raiz = self._eliminar(self.raiz, dato)
        return True

    def _eliminar(self, nodo, dato):
        if nodo is None:
            return None
        if dato < nodo.dato:
            nodo.izq = self._eliminar(nodo.izq, dato)
        elif dato > nodo.dato:
            nodo.der = self._eliminar(nodo.der, dato)
        else:
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            sucesor = self._minimo(nodo.der)      # dos hijos: sucesor in-orden
            nodo.dato = sucesor.dato
            nodo.der = self._eliminar(nodo.der, sucesor.dato)
        return self._balancear(nodo)

    # ------------------------------------------------------------------ #
    # Consultas
    # ------------------------------------------------------------------ #
    def buscar(self, dato):
        actual = self.raiz
        while actual:
            if dato == actual.dato:
                return actual
            actual = actual.izq if dato < actual.dato else actual.der
        return None

    @staticmethod
    def _minimo(nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def minimo(self):
        return self._minimo(self.raiz).dato if self.raiz else None

    def maximo(self):
        actual = self.raiz
        while actual and actual.der:
            actual = actual.der
        return actual.dato if actual else None

    def alturaArbol(self):
        return self.altura(self.raiz)

    def numNodos(self, nodo="raiz"):
        nodo = self.raiz if nodo == "raiz" else nodo
        return 0 if nodo is None else 1 + self.numNodos(nodo.izq) + self.numNodos(nodo.der)

    def esAVL(self, nodo="raiz"):
        """Verifica la propiedad AVL (y la de ABB) en todo el árbol."""
        nodo = self.raiz if nodo == "raiz" else nodo
        if nodo is None:
            return True
        if abs(self.factorBalance(nodo)) > 1:
            return False
        if nodo.izq and nodo.izq.dato >= nodo.dato:
            return False
        if nodo.der and nodo.der.dato <= nodo.dato:
            return False
        return self.esAVL(nodo.izq) and self.esAVL(nodo.der)

    # ------------------------------------------------------------------ #
    # Recorridos
    # ------------------------------------------------------------------ #
    def inOrden(self, nodo="raiz"):
        nodo = self.raiz if nodo == "raiz" else nodo
        return [] if nodo is None else self.inOrden(nodo.izq) + [nodo.dato] + self.inOrden(nodo.der)

    def preOrden(self, nodo="raiz"):
        nodo = self.raiz if nodo == "raiz" else nodo
        return [] if nodo is None else [nodo.dato] + self.preOrden(nodo.izq) + self.preOrden(nodo.der)

    def postOrden(self, nodo="raiz"):
        nodo = self.raiz if nodo == "raiz" else nodo
        return [] if nodo is None else self.postOrden(nodo.izq) + self.postOrden(nodo.der) + [nodo.dato]

    def porNiveles(self):
        """Recorrido en anchura: lista de niveles."""
        niveles, actual = [], [self.raiz] if self.raiz else []
        while actual:
            niveles.append([n.dato for n in actual])
            actual = [h for n in actual for h in (n.izq, n.der) if h]
        return niveles

    # ------------------------------------------------------------------ #
    # Dibujo
    # ------------------------------------------------------------------ #
    def graficar(self, nodo="raiz", prefijo="", lado=""):
        """Árbol como texto. Entre paréntesis: factor de balance."""
        nodo = self.raiz if nodo == "raiz" else nodo
        if nodo is None:
            return "(vacío)\n"
        texto = f"{prefijo}{lado}{nodo.dato} (fb={self.factorBalance(nodo)})\n"
        for etiqueta, hijo in (("I: ", nodo.izq), ("D: ", nodo.der)):
            if hijo:
                texto += self.graficar(hijo, prefijo + "    ", etiqueta)
        return texto
