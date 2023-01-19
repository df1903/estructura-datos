"""
Backtracking (vuelta atrás): probar una decisión, avanzar, y si no lleva a una
solución deshacerla (retroceder) y probar la siguiente.

Plantilla general:
    1. Si la solución parcial está completa -> guardarla.
    2. Para cada opción posible:
         a. si es válida -> elegirla
         b. llamar recursivamente
         c. deshacer la elección (retroceder)

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""


def permutaciones(elementos):
    """Todas las permutaciones de una lista."""
    soluciones = []

    def _bt(actual, usados):
        if len(actual) == len(elementos):
            soluciones.append(actual[:])
            return
        for i, e in enumerate(elementos):
            if usados[i]:
                continue
            usados[i] = True
            actual.append(e)
            _bt(actual, usados)
            actual.pop()  # retroceder
            usados[i] = False

    _bt([], [False] * len(elementos))
    return soluciones


def subconjuntos_suma(numeros, objetivo):
    """Todos los subconjuntos de `numeros` (positivos) cuya suma es `objetivo`."""
    soluciones = []

    def _bt(inicio, actual, suma):
        if suma == objetivo:
            soluciones.append(actual[:])
            return
        if suma > objetivo:
            return  # poda: ya nos pasamos
        for i in range(inicio, len(numeros)):
            actual.append(numeros[i])
            _bt(i + 1, actual, suma + numeros[i])
            actual.pop()  # retroceder

    _bt(0, [], 0)
    return soluciones


def n_reinas(n):
    """Todas las formas de ubicar n reinas sin que se ataquen.
    Cada solución es una lista donde el índice es la fila y el valor la columna."""
    soluciones = []
    columnas, diag1, diag2 = set(), set(), set()

    def _bt(fila, tablero):
        if fila == n:
            soluciones.append(tablero[:])
            return
        for col in range(n):
            if col in columnas or (fila - col) in diag1 or (fila + col) in diag2:
                continue
            columnas.add(col)
            diag1.add(fila - col)
            diag2.add(fila + col)
            tablero.append(col)
            _bt(fila + 1, tablero)
            tablero.pop()  # retroceder
            columnas.remove(col)
            diag1.remove(fila - col)
            diag2.remove(fila + col)

    _bt(0, [])
    return soluciones


def laberinto(matriz, inicio=(0, 0), fin=None):
    """Busca un camino en un laberinto. 0 = libre, 1 = pared.
    Devuelve la lista de casillas del camino o None si no existe."""
    filas, cols = len(matriz), len(matriz[0])
    fin = fin or (filas - 1, cols - 1)
    camino, visitado = [], set()

    def _bt(f, c):
        if not (0 <= f < filas and 0 <= c < cols):
            return False
        if matriz[f][c] == 1 or (f, c) in visitado:
            return False
        visitado.add((f, c))
        camino.append((f, c))
        if (f, c) == fin:
            return True
        for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if _bt(f + df, c + dc):
                return True
        camino.pop()  # retroceder: esta casilla no sirve
        return False

    return camino if _bt(*inicio) else None


def colorear_grafo(adyacencias, colores):
    """Asigna uno de `colores` (lista) a cada vértice sin repetir color entre vecinos.
    `adyacencias` es un dict {vertice: [vecinos]}. Devuelve dict o None."""
    vertices = list(adyacencias)
    asignacion = {}

    def _bt(i):
        if i == len(vertices):
            return True
        v = vertices[i]
        for color in colores:
            if all(asignacion.get(vecino) != color for vecino in adyacencias[v]):
                asignacion[v] = color
                if _bt(i + 1):
                    return True
                del asignacion[v]  # retroceder
        return False

    return asignacion if _bt(0) else None


def _mostrar_tablero(solucion):
    n = len(solucion)
    for col in solucion:
        print(" ".join("R" if c == col else "." for c in range(n)))


if __name__ == "__main__":
    print("Permutaciones de [1,2,3]:", permutaciones([1, 2, 3]))
    print("Subconjuntos de [3,34,4,12,5,2] que suman 9:", subconjuntos_suma([3, 34, 4, 12, 5, 2], 9))
    sols = n_reinas(6)
    print(f"6 reinas: {len(sols)} soluciones. Primera:")
    _mostrar_tablero(sols[0])
    lab = [[0, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1], [1, 1, 0, 0]]
    print("Laberinto:", laberinto(lab))
    print("Colorear:", colorear_grafo({"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B", "D"], "D": ["C"]}, ["rojo", "verde", "azul"]))
