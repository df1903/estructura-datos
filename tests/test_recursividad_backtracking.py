"""Pruebas de recursividad y backtracking. Autor: Daniel Felipe Franco Rincón."""

from backtracking import problemas as bt
from recursividad import ejercicios as r


def test_basicos(capsys):
    r.saludar(3)
    assert capsys.readouterr().out.count("hola mundo") == 3
    assert r.invertir([1, 2, 3], [0, 0, 0]) == [3, 2, 1]
    assert r.ordenar([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert r.ordenar([]) == []
    r.listaInvertida([1, 2, 3])
    assert capsys.readouterr().out.split() == ["3", "2", "1"]
    r.listaDirecta([1, 2, 3])
    assert capsys.readouterr().out.split() == ["1", "2", "3"]
    r.productos(2, 3)
    assert "2 * 3 = 6" in capsys.readouterr().out


def test_con_backtracking():
    assert r.sumaParesHastaDos(10)[0] == 30
    assert r.sumaParesHastaDos(4) == (6, ["error: 3 es impar"])
    suma, errores = r.sumaParesHastaDos(9)
    assert suma == 20 and len(errores) == 4
    assert r.sumaArreglo([1, 2, 3, 4]) == 10
    assert r.invertirLista([1, 2, 3]) == [3, 2, 1]
    assert r.invertirNumero(1234) == 4321 and r.invertirNumero(-120) == -21
    assert r.sumaLista([1, 2, 3]) == 6
    assert r.menor([-2, 23, 5, 2, 3, -4]) == -4
    assert r.menor([7]) == 7
    assert r.sumaVector([1, 1, 1, 1, 1, -4]) == 1


def test_primos():
    assert [n for n in range(1, 30) if r.esPrimo(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert r.esPrimo(5353627) is False
    assert r.esPrimo(104729) is True


def test_clasicos():
    assert r.factorial(5) == 120
    assert r.fibonacci(30) == 832040
    assert r.potencia(2, 10) == 1024 and r.potencia(3, 0) == 1
    assert r.mcd(48, 18) == 6
    assert r.sumaDigitos(1234) == 10
    assert r.esPalindromo("Anita lava la tina") and not r.esPalindromo("hola")
    assert r.aBinario(10) == "1010"
    assert len(r.hanoi(4)) == 15


def test_backtracking():
    assert len(bt.permutaciones([1, 2, 3, 4])) == 24
    assert sorted(map(sorted, bt.subconjuntos_suma([3, 34, 4, 12, 5, 2], 9))) == [[2, 3, 4], [4, 5]]
    assert len(bt.n_reinas(6)) == 4 and len(bt.n_reinas(8)) == 92
    lab = [[0, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1], [1, 1, 0, 0]]
    assert bt.laberinto(lab)[-1] == (3, 3)
    assert bt.laberinto([[0, 1], [1, 0]]) is None
    ady = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}
    color = bt.colorear_grafo(ady, ["r", "g", "b"])
    assert len(set(color.values())) == 3
    assert bt.colorear_grafo(ady, ["r", "g"]) is None
