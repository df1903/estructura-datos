"""Pruebas de grafos, búsquedas, diccionarios y proyectos. Autor: Daniel Felipe Franco Rincón."""

from busquedas import anchura_profundidad as bp
from diccionarios import ejercicios_basicos as eb
from diccionarios import parcial_adn, taller
from grafos.grafo import Grafo
from grafos.taller_grafos import grafo_dirigido, grafo_no_dirigido
from proyectos.isla_cuevas.isla import Cueva, Isla, Simulacion
from proyectos.libreria_grafos.main import cargar_grafo


# ------------------------------- grafos --------------------------------- #
def test_taller_grafos():
    g = grafo_dirigido()
    assert g.minMaxAristas()[0].getPeso() == 1 and g.maxMinAristas()[0].getPeso() == 11
    assert g.gradoVertices() == {"A": 2, "B": 4, "C": 4, "D": 3, "E": 2, "F": 1}
    assert g.verticeMayorGrado()[1] == 4
    assert round(g.promedioListaAdyacencias(), 2) == 1.33
    assert g.pozos() == ["F"] and g.fuentes() == ["A"]
    assert g.promedioPesoAristas() == 5.0
    assert [a.getPeso() for a in g.aristaMayorPeso()] == [11]
    assert g.verticeAdyacente("C") == {"A": 1, "B": 1, "D": 0, "E": 0, "F": 0}
    assert len(g.listaAdyacencias()) == 8
    assert g.verticesNoContemplados() == ["A"]
    assert g.adyacenciaMasComun() == (["B", "C", "D"], 2)


def test_aristas_y_vertices():
    g = Grafo()
    assert g.ingresarVertice("A") and not g.ingresarVertice("A")
    g.ingresarVertice("B")
    assert g.ingresarArista("A", "B", 3)
    assert not g.ingresarArista("A", "B", 9) and not g.ingresarArista("A", "Z", 1)
    assert g.eliminarArista("A", "B") and not g.eliminarArista("A", "B")
    assert g.getListaAristas() == [] and g.obtenerVertice("A").getListaAdyacentes() == []


def test_recorridos_y_caminos():
    g = grafo_dirigido()
    assert g.recorridoAmplitud("A") == ["A", "B", "C", "D", "E", "F"]
    assert g.recorridoProfundidad("A") == ["A", "B", "C", "E", "D", "F"]
    assert g.recorridoAmplitud("Z") == []
    assert g.dijkstra("A", "F") == (20, ["A", "C", "E", "D", "F"])
    assert g.dijkstra("F", "A")[0] == float("inf")
    assert g.floydWarshall()["A"]["F"] == 20


def test_conexo_y_ciclos():
    g = grafo_dirigido()
    assert g.esDirigido() and g.esConexo() and g.tieneCiclos()
    h = Grafo()
    for v in "ABC":
        h.ingresarVertice(v)
    h.ingresarArista("A", "B", 1)
    assert not h.esConexo() and not h.tieneCiclos()
    h.ingresarArista("B", "C", 1)
    h.ingresarArista("A", "C", 1)
    assert h.esConexo() and not h.tieneCiclos()   # DAG
    h.convertirNoDirigido()
    assert not h.esDirigido() and h.tieneCiclos()  # triángulo no dirigido


def test_arboles_de_expansion_minima():
    n = grafo_no_dirigido()
    for arbol in (n.prim("A"), n.kruskal(), n.boruvka()):
        assert Grafo.pesoTotal(arbol) == 30 and len(arbol) == 5


def test_bloqueo_de_aristas():
    g = grafo_no_dirigido()
    assert g.bloquearArista("A", "B")           # hay ruta alterna A-D-B
    assert not g.existeArista("A", "B")
    g.desbloquearAristas()
    assert g.existeArista("A", "B") and g.existeArista("B", "A")
    solo = Grafo()
    solo.ingresarVertice("X")
    solo.ingresarVertice("Y")
    solo.ingresarArista("X", "Y", 1)
    solo.ingresarArista("Y", "X", 1)
    assert not solo.bloquearArista("X", "Y")    # sin alterna: no se bloquea
    assert solo.existeArista("X", "Y")


# ------------------------------ búsquedas ------------------------------- #
def test_bfs_dfs_grafo():
    g = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["F"], "F": []}
    assert bp.bfs(g, "A") == ["A", "B", "C", "D", "E", "F"]
    assert bp.dfs_iterativo(g, "A") == bp.dfs_recursivo(g, "A") == ["A", "B", "D", "E", "F", "C"]
    assert bp.camino_bfs(g, "A", "F") == ["A", "C", "F"]
    assert bp.camino_dfs(g, "A", "F")[-1] == "F"
    assert bp.camino_bfs(g, "D", "A") is None
    assert bp.componentes_conexas({"A": ["B"], "B": ["A"], "C": []}) == [["A", "B"], ["C"]]


# ----------------------------- diccionarios ----------------------------- #
def test_ejercicios_basicos():
    assert eb.simbolo_divisa("euro") == "€" and eb.simbolo_divisa("peso") is None
    assert eb.precio_fruta("manzana", 10) == 8.0 and eb.precio_fruta("kiwi", 1) is None
    assert eb.fecha_en_texto("05/03/2021") == "5 de marzo de 2021"
    assert eb.resumen_creditos(eb.CURSO)[1] == 15
    assert eb.total_compra({"a": 2, "b": 3}) == 5
    d = eb.crear_diccionario("casa:house, perro:dog")
    assert eb.traducir("mi casa y mi perro", d) == "mi house y mi dog"
    f = eb.Facturas()
    f.agregar("1", 100)
    f.agregar("2", 50)
    assert f.pagar("1") == 100 and f.pagar("9") is None
    assert (f.cobrado, f.pendiente) == (100, 50)


def test_taller_diccionarios():
    e = taller.estadisticas_equipo(taller.EQUIPO)
    assert e["mas_rapido"]["velocidad"] == 80 and e["promedio_velocidad"] == 65
    assert taller.costo_total(taller.PATINETAS) == 4278
    assert taller.segunda_mejor_velocidad(taller.PATINETAS)["velocidad"] == 92
    comp = [taller.Competidor(str(i), "n", "a", "d", "t", v) for i, v in enumerate((5, 10, 2))]
    assert taller.ultimo_en_llegar(comp).datos["velocidad"] == 2
    assert taller.primero_en_llegar(comp).datos["velocidad"] == 10
    assert taller.signo_zodiacal(3, 21) == "Aries" and taller.signo_zodiacal(12, 25) == "Capricornio"
    assert taller.signo_zodiacal(1, 5) == "Capricornio" and taller.signo_zodiacal(2, 1) == "Acuario"
    assert taller.signo_mas_comun({"a": (3, 25), "b": (4, 2), "c": (8, 1)}) == ("Aries", 2)
    assert taller.descuento(taller.SALARIO_MINIMO) == 0.10
    assert taller.descuento(5 * taller.SALARIO_MINIMO) == 0.15
    assert taller.descuento(7 * taller.SALARIO_MINIMO) == 0.20
    r = taller.nomina([dict(t) for t in taller.TRABAJADORES])
    assert r["mayor_salario"]["nombre"] == "Tomás" and r["mas_ocupaciones"]["nombre"] == "Juan"


def test_parcial_adn():
    pos, individuo, cant = parcial_adn.individuo_con_mas_bases(parcial_adn.SECUENCIAS, "A")
    assert pos == 0 and cant == 3
    assert parcial_adn.promedio_base(parcial_adn.SECUENCIAS, "G") == 1.0
    assert parcial_adn.individuo_con_mas_bases([], "A") is None


# ------------------------------- proyectos ------------------------------- #
def test_proyecto_libreria():
    g = cargar_grafo()
    assert len(g.getListaVertices()) == 11 and not g.esDirigido()
    distancia, camino = g.dijkstra("Casita", "Libreria Celsius")
    assert camino[0] == "Casita" and camino[-1] == "Libreria Celsius" and distancia == 435
    assert Grafo.pesoTotal(g.kruskal()) == Grafo.pesoTotal(g.prim("Casita")) == Grafo.pesoTotal(g.boruvka())
    assert g.esConexo()


def test_isla_balanceada():
    isla = Isla()
    for _ in range(15):
        isla.ingresar(Cueva())
    assert isla.altura() == 4 and isla.numNodos() == 15
    for _ in range(7):
        assert isla.eliminar(isla.preOrden()[0])
    assert isla.numNodos() == 8 and isla.altura() == 4
    assert not isla.eliminar(Cueva())
    while isla.getRaiz():
        isla.eliminar(isla.getRaiz())
    assert isla.numNodos() == 0


def test_simulacion():
    sim = Simulacion(numCamiones=10, numCuevas=7, semilla=1)
    total_inicial = sum(c.cantidad for c in sim.isla.preOrden())
    sim.avanzar(10)
    assert round(sum(c.cantidad for c in sim.isla.preOrden()), 2) == total_inicial + 14  # 7 cuevas x 2
    sim.avanzar(590)
    assert sim.almacen.getTotal() > 0 and sim.registro
    assert sim.isla.altura() <= 4 + 2  # sigue balanceada (árbol completo)
