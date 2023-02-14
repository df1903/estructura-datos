# Búsqueda en anchura y profundidad

- **BFS** usa una **cola**: explora por niveles y halla el camino con menos aristas.
- **DFS** usa una **pila** (o la recursión): baja por una rama hasta el fondo y retrocede.

Funciones en `anchura_profundidad.py`: `bfs`, `dfs_iterativo`, `dfs_recursivo`, `camino_bfs`, `camino_dfs`, `componentes_conexas` (grafos como diccionario de adyacencias) y `bfs_arbol`, `dfs_arbol` (árboles). La clase `Grafo` de [`grafos/`](../grafos/) también expone `recorridoAmplitud` y `recorridoProfundidad`.

```bash
python -m busquedas.anchura_profundidad
```

*Autor: Daniel Felipe Franco Rincón*
