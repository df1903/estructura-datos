"""
Demostración del árbol AVL: compara con un ABB normal y muestra las rotaciones.
Ejecutar desde la raíz del proyecto:  python -m avl.demo

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from arboles.arbol_abb import Arbol

from .arbol_avl import ArbolAVL


def main():
    avl, abb = ArbolAVL(), Arbol()
    for n in range(1, 16):  # inserción ordenada: el peor caso de un ABB
        avl.insertar(n)
        abb.ingresar(n)

    print("Insertando 1..15 en orden:")
    print(f"  ABB normal -> altura {abb.alturaArbol()} (degenerado en lista)")
    print(f"  AVL        -> altura {avl.alturaArbol()}  | rotaciones: {avl.rotaciones}")
    print("\nAVL resultante:\n" + avl.graficar())
    print("Por niveles:", avl.porNiveles())
    print("¿Es AVL válido?:", avl.esAVL())

    for n in (8, 4, 12, 1):
        avl.eliminar(n)
    print("\nTras eliminar 8, 4, 12 y 1:")
    print(avl.graficar())
    print("in-orden:", avl.inOrden(), "| ¿Es AVL válido?:", avl.esAVL())


if __name__ == "__main__":
    main()
