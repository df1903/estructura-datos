# Árbol AVL

ABB auto-balanceado: el factor de balance (`altura(izq) - altura(der)`) de cada nodo está en {-1, 0, 1}. Se corrige con rotaciones:

| Caso | Rotación |
|------|----------|
| Izq-Izq | derecha |
| Der-Der | izquierda |
| Izq-Der | izquierda + derecha |
| Der-Izq | derecha + izquierda |

`ArbolAVL`: `insertar`, `eliminar`, `buscar`, `minimo`, `maximo`, `inOrden`/`preOrden`/`postOrden`/`porNiveles`, `alturaArbol`, `esAVL`, `graficar` (muestra el factor de balance).

La demo compara un ABB y un AVL al insertar 1..15 en orden.

```bash
python -m avl.demo
```

*Autor: Daniel Felipe Franco Rincón*
