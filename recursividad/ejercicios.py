"""
Taller de recursividad.

Ejercicios 1-6  : nivel básico   (sin backtracking, el trabajo se hace "de ida").
Ejercicios 7-14 : nivel fácil / medio (con backtracking: el resultado se arma
                  "de regreso", cuando los ambientes se van cerrando).
Ejercicios 15+  : clásicos de recursividad (complemento).

Cada función es recursiva (sin bucles para recorrer) y devuelve su resultado
para poder probarla; las que en el taller pedían "imprimir" siguen imprimiendo.

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

# --------------------------------------------------------------------------- #
# NIVEL BÁSICO (sin backtracking)
# --------------------------------------------------------------------------- #


def saludar(x):
    """1) Saluda x veces. Crea x ambientes."""
    if x <= 0:
        return
    print("hola mundo")
    saludar(x - 1)


def productos(num, numProductos, count=1):
    """2) Tabla de multiplicar de `num` hasta `numProductos`."""
    if count > numProductos:
        return
    print(num, "*", count, "=", num * count)
    productos(num, numProductos, count + 1)


def invertir(ordenada, invertida, count=0):
    """3) Copia `ordenada` invertida dentro de `invertida` (misma longitud).
    Crea len(ordenada) ambientes. Devuelve la lista invertida."""
    if count == len(ordenada):
        return invertida
    invertida[count] = ordenada[len(ordenada) - (count + 1)]
    return invertir(ordenada, invertida, count + 1)


def ordenar(lista, entorno=0):
    """4) Ordena de menor a mayor (selección recursiva). Modifica y devuelve la lista."""
    if entorno >= len(lista) - 1:
        return lista
    return ordenar(ciclar(lista, entorno, entorno + 1), entorno + 1)


def ciclar(vec, ent, iter):
    """Paso interno de `ordenar`: deja en `ent` el menor de vec[ent:]."""
    if iter == len(vec):
        return vec
    if vec[ent] > vec[iter]:
        vec[ent], vec[iter] = vec[iter], vec[ent]
    return ciclar(vec, ent, iter + 1)


def listaInvertida(lista, count=None):
    """5) Imprime los datos de la lista de atrás hacia adelante."""
    if count is None:
        count = len(lista) - 1
    if count < 0:
        return
    print(lista[count])
    listaInvertida(lista, count - 1)


def listaDirecta(lista, count=0):
    """6) Imprime los datos de la lista de adelante hacia atrás."""
    if count >= len(lista):
        return
    print(lista[count])
    listaDirecta(lista, count + 1)


# --------------------------------------------------------------------------- #
# NIVEL FÁCIL (con backtracking)
# --------------------------------------------------------------------------- #


def sumaParesHastaDos(N, errores=None):
    """7) Suma de los enteros positivos pares desde N hasta 2.
    Por cada impar encontrado se guarda un mensaje de error en `errores`.
    Devuelve (suma, errores)."""
    if errores is None:
        errores = []
    if N < 2:
        return 0, errores
    if N % 2 != 0:
        errores.append(f"error: {N} es impar")
        return sumaParesHastaDos(N - 1, errores)
    suma, errores = sumaParesHastaDos(N - 1, errores)
    return suma + N, errores


def sumaArreglo(arreglo, i=0):
    """8) Suma los enteros de un arreglo."""
    if i == len(arreglo):
        return 0
    return arreglo[i] + sumaArreglo(arreglo, i + 1)


# --------------------------------------------------------------------------- #
# NIVEL MEDIO (recursividad con backtracking)
# --------------------------------------------------------------------------- #


def invertirLista(lista):
    """9) Devuelve una lista nueva con los enteros invertidos."""
    if not lista:
        return []
    return invertirLista(lista[1:]) + [lista[0]]


def invertirNumero(n):
    """10) Invierte un número entero: 1234 -> 4321 (conserva el signo)."""
    if n < 0:
        return -invertirNumero(-n)

    def _inv(resto, acumulado):
        if resto == 0:
            return acumulado
        return _inv(resto // 10, acumulado * 10 + resto % 10)

    return _inv(n, 0)


def sumaLista(lista, count=None):
    """11) Suma los elementos de una lista (de atrás hacia adelante)."""
    if count is None:
        count = len(lista) - 1
    if count < 0:
        return 0
    return lista[count] + sumaLista(lista, count - 1)


def menor(lista, count=None, variable=None):
    """12) Retorna el número menor del vector.
    Cada ambiente compara su elemento con el menor que le devuelve el anterior."""
    if count is None:
        count = len(lista) - 1
        variable = lista[count]
    if count == 0:
        return lista[0]
    count -= 1
    minimo = menor(lista, count, lista[count])
    return variable if variable < minimo else minimo


def sumaVector(lista, count=None, variable=None):
    """13) Suma de los elementos del vector acumulando al regreso."""
    if count is None:
        count = len(lista) - 1
        variable = lista[count]
    if count == 0:
        return lista[0]
    count -= 1
    return sumaVector(lista, count, lista[count]) + variable


def esPrimo(num, n=2):
    """14) Indica si `num` es primo (prueba divisores hasta la raíz cuadrada)."""
    if num < 2:
        return False
    if n * n > num:
        return True
    if num % n == 0:
        return False
    return esPrimo(num, n + 1 if n == 2 else n + 2)


# --------------------------------------------------------------------------- #
# CLÁSICOS (complemento)
# --------------------------------------------------------------------------- #


def factorial(n):
    """15) n!"""
    return 1 if n <= 1 else n * factorial(n - 1)


def fibonacci(n, memo=None):
    """16) n-ésimo Fibonacci (con memoria para evitar recálculo exponencial)."""
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


def potencia(base, exp):
    """17) base**exp por exponenciación rápida (exp >= 0)."""
    if exp == 0:
        return 1
    mitad = potencia(base, exp // 2)
    return mitad * mitad if exp % 2 == 0 else mitad * mitad * base


def mcd(a, b):
    """18) Máximo común divisor (Euclides)."""
    return a if b == 0 else mcd(b, a % b)


def sumaDigitos(n):
    """19) Suma de los dígitos de n."""
    n = abs(n)
    return n if n < 10 else n % 10 + sumaDigitos(n // 10)


def esPalindromo(texto):
    """20) True si el texto se lee igual al derecho y al revés (ignora espacios y mayúsculas)."""
    t = "".join(c.lower() for c in texto if c.isalnum())
    if len(t) < 2:
        return True
    return t[0] == t[-1] and esPalindromo(t[1:-1])


def aBinario(n):
    """21) Representación binaria de un entero no negativo."""
    return str(n) if n < 2 else aBinario(n // 2) + str(n % 2)


def hanoi(n, origen="A", destino="C", auxiliar="B", movimientos=None):
    """22) Torres de Hanoi. Devuelve la lista de movimientos (origen, destino)."""
    if movimientos is None:
        movimientos = []
    if n == 0:
        return movimientos
    hanoi(n - 1, origen, auxiliar, destino, movimientos)
    movimientos.append((origen, destino))
    hanoi(n - 1, auxiliar, destino, origen, movimientos)
    return movimientos


if __name__ == "__main__":
    print("-- 1) saludar(3)")
    saludar(3)
    print("-- 2) productos(4, 5)")
    productos(4, 5)
    print("-- 3) invertir:", invertir([1, 2, 3, 4], [0] * 4))
    print("-- 4) ordenar:", ordenar([5, 4, 3, 2, 1]))
    print("-- 5) listaInvertida([1, 22, 34])")
    listaInvertida([1, 22, 34])
    print("-- 6) listaDirecta([1, 22, 34])")
    listaDirecta([1, 22, 34])
    print("-- 7) suma pares hasta 2 desde 9:", sumaParesHastaDos(9))
    print("-- 8) suma arreglo:", sumaArreglo([1, 2, 3, 4]))
    print("-- 9) invertir lista:", invertirLista([1, 2, 3]))
    print("-- 10) invertir número:", invertirNumero(12345))
    print("-- 11) suma lista:", sumaLista([1, 2, 3, 4]))
    print("-- 12) menor:", menor([-2, 23, 5, 2, 3, -4]))
    print("-- 13) suma vector:", sumaVector([1, 1, 1, 1, 1, -4]))
    print("-- 14) ¿5353627 es primo?:", esPrimo(5353627))
    print("-- 22) hanoi(3):", hanoi(3))
