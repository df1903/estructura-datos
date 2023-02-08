# Árboles binarios de búsqueda (ABB)

`Nodo` (dato, izq, der, repetidos) y `Arbol` con todo el taller 2020-2 ([enunciado](../docs/enunciados/taller_arboles_abb_2020-2.docx)). La raíz está en el nivel 1; los métodos de recorrido aceptan opcionalmente el nodo de partida.

| Punto | Método |
|-------|--------|
| 1 | `ingresar`, `ingresarInvertido` |
| 2-3 | `mostrarPreOrden/InOrden/PostOrden`, `preOrden/inOrden/postOrden` (devuelven lista) |
| 4 | `alturaArbol`, `alturaRaiz`, `alturaElemento`, `alturaMayor` |
| 5-6 | `sumaArbol`, `sumaNivel` |
| 7-11 | `primos`, `devolvermenor`, `devolvermayor`, `hojas`, `mostrarHojas` |
| 12, 20 | repetidos (`Nodo.repetidos`), `cuantasVeces` |
| 13 | `numNodos` |
| 15 | `eliminar` (hoja, un hijo, dos hijos por sucesor o predecesor) |
| 17 | `intercambiar` |
| 18-19 | `paresYPrimos`, `arbolDePares` |
| 21-22 | `arbolParesIzquierdaImparesDerecha`, `arbolPrimosDerechaRestoIzquierda` |
| 23 | `arbolDeVehiculos` (ordenado por placa) |
| extra | `sonGemelos` (espejo), `buscar`, `graficar` |

```bash
python -m arboles.taller_abb
```

*Autor: Daniel Felipe Franco Rincón*
