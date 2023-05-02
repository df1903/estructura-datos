# Estructura de Datos en Python

Repositorio con todo lo visto en la materia **Estructura de Datos**: ejercicios, talleres, parciales y proyectos, ordenados por tema, funcionales y con pruebas automáticas.

**Autor:** Daniel Felipe Franco Rincón

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen)

## Contenido

| # | Tema | Carpeta | Qué incluye |
|---|------|---------|-------------|
| 1 | Recursividad | [`recursividad/`](recursividad/) | Taller 2021-1 (ejercicios 1-14, básico / fácil / medio con backtracking) + clásicos (factorial, Fibonacci, Hanoi, MCD...) |
| 2 | Backtracking | [`backtracking/`](backtracking/) | Permutaciones, subconjuntos con suma, N-reinas, laberinto, coloreado de grafos |
| 3 | Árboles (ABB) | [`arboles/`](arboles/) | Taller ABB 2020-2 completo: recorridos, alturas, sumas, primos, hojas, repetidos, 3 tipos de eliminación, intercambio, árboles por regla, vehículos por placa |
| 4 | Búsqueda en anchura y profundidad | [`busquedas/`](busquedas/) | BFS y DFS (iterativo y recursivo) sobre grafos y árboles, caminos, componentes conexas |
| 5 | Grafos | [`grafos/`](grafos/) | Taller de grafos (11 puntos), Dijkstra, Prim, Kruskal, Borůvka, Floyd-Warshall, bloqueo de aristas, conexidad y ciclos |
| 6 | AVL | [`avl/`](avl/) | Árbol AVL con 4 tipos de rotación, inserción y eliminación balanceadas |
| 7 | Diccionarios | [`diccionarios/`](diccionarios/) | 9 ejercicios básicos, taller (fútbol, patinetas, competidores, zodiaco, nómina) y parcial de ADN |
| 8 | Proyectos | [`proyectos/`](proyectos/) | **Librerías** (grafos, ruta del mensajero) e **Isla El Paro** (árbol de cuevas, simulación) |
| - | Enunciados | [`docs/enunciados/`](docs/enunciados/) | Talleres, parciales y proyectos originales (docx / pdf) |
| - | Pruebas | [`tests/`](tests/) | 30 pruebas con `pytest` |

## Estructura

```
estructuras-de-datos-python/
├── main.py                  # menú para lanzar cada demo
├── helpers/keyboard.py      # lectura segura de entradas por consola
├── recursividad/ejercicios.py
├── backtracking/problemas.py
├── arboles/                 # nodo.py, arbol_abb.py, taller_abb.py
├── busquedas/anchura_profundidad.py
├── grafos/                  # vertice.py, arista.py, grafo.py, taller_grafos.py
├── avl/                     # arbol_avl.py, demo.py
├── diccionarios/            # ejercicios_basicos.py, taller.py, parcial_adn.py
├── proyectos/
│   ├── libreria_grafos/     # main.py + data/*.json
│   └── isla_cuevas/         # isla.py, main.py
├── docs/enunciados/         # enunciados originales
└── tests/
```

## Uso

Solo requiere Python 3.8+ (no hay dependencias externas; `pytest` solo para las pruebas).

```bash
git clone <url-del-repositorio>
cd estructuras-de-datos-python

python main.py                          # menú con todos los temas

# o cada tema por separado (desde la raíz del proyecto)
python -m recursividad.ejercicios
python -m backtracking.problemas
python -m arboles.taller_abb
python -m busquedas.anchura_profundidad
python -m grafos.taller_grafos
python -m avl.demo
python -m diccionarios.taller
python -m diccionarios.parcial_adn
python -m diccionarios.ejercicios_basicos
python -m proyectos.libreria_grafos.main --demo     # sin --demo: menú interactivo
python -m proyectos.isla_cuevas.main --segundos 600 --semilla 1

# pruebas
pip install pytest
python -m pytest
```

## Ejemplos

```python
from arboles.arbol_abb import Arbol
from arboles.nodo import Nodo

a = Arbol()
for n in (15, 9, 13, 2, 20, 7):
    a.ingresar(Nodo(n))
a.inOrden()          # [2, 7, 9, 13, 15, 20]
a.alturaArbol()      # 4
a.eliminar(9)        # hoja / un hijo / dos hijos, según el caso
```

```python
from avl.arbol_avl import ArbolAVL

t = ArbolAVL()
for n in range(1, 16):      # inserción ordenada: un ABB quedaría en lista (altura 15)
    t.insertar(n)
t.alturaArbol()             # 4
```

```python
from grafos.taller_grafos import grafo_no_dirigido
from grafos.grafo import Grafo

g = grafo_no_dirigido()
g.dijkstra("A", "F")                 # (distancia, camino)
Grafo.pesoTotal(g.kruskal())         # peso del árbol de expansión mínima
```

## Notas sobre el trabajo

Este repositorio parte de mis ejercicios y proyectos originales de la materia (Python). Se **conservaron los nombres de clases y métodos** (`ingresar`, `mostrarPreOrden`, `alturaArbol`, `ingresarVertice`, `mostrarPozos`...) y se hizo lo siguiente:

- **Organización:** una carpeta por tema; se eliminaron las copias repetidas del mismo proyecto (había hasta 6 versiones de "librerías"), entornos virtuales, instaladores, archivos de IDE y repositorios `.git` anidados.
- **Corrección de errores:** rutas absolutas del computador, `import` que no existían, métodos que quedaron a medias (Prim, `verticeAdyacente`), listas de clase que acumulaban resultados entre llamadas, eliminación de nodos sin retorno, entre otros.
- **Completado:** ejercicios 7-11 de recursividad, taller ABB completo (primos, hojas, repetidos, eliminar, intercambiar, árboles por regla, vehículos), búsquedas BFS/DFS, **AVL** (no existía), Borůvka, Floyd-Warshall, el taller y parcial de diccionarios, backtracking y pruebas.
- **Mejoras:** métodos que devuelven resultados (además de imprimir) para poder probarlos, simulación de la isla sin esperas reales (`time.sleep`) y con árbol siempre balanceado.

## Conceptos clave

| Tema | Idea | Complejidad típica |
|------|------|--------------------|
| Recursividad | Una función se llama a sí misma con un problema más pequeño y tiene un caso base | O(n) por llamadas |
| Backtracking | Probar, avanzar y deshacer cuando no hay solución | exponencial (con poda) |
| ABB | izq < raíz < der | O(log n) promedio, O(n) peor |
| AVL | ABB con factor de balance ∈ {-1, 0, 1} y rotaciones | O(log n) siempre |
| BFS / DFS | Cola / pila para recorrer | O(V + E) |
| Dijkstra | Camino mínimo con pesos no negativos | O((V + E) log V) |
| Kruskal / Prim / Borůvka | Árbol de expansión mínima | O(E log V) |
| Diccionario | Tabla hash clave → valor | O(1) promedio |
