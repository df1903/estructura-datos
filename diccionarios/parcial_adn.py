"""
Parcial de diccionarios: secuenciación de ADN.

Cada individuo es un diccionario {cade1: base, cade2: base, ...} con bases
A, C, G o T. Restricción del enunciado: NO se puede usar ningún método de
ordenamiento (ni sorted, ni sort).

  1) Individuo con la base 'A' que más se repite.
  2) Promedio de bases 'G' de todos los individuos.

Ejecutar:  python -m diccionarios.parcial_adn

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

SECUENCIAS = [
    {"cade1": "A", "cade2": "A", "cade3": "A", "cade4": "T"},
    {"cade1": "G", "cade2": "G", "cade3": "G", "cade4": "A"},
    {"cade1": "C", "cade2": "A", "cade3": "A", "cade4": "C"},
]


def contar_base(individuo, base):
    """Cuántas veces aparece `base` en las cadenas del individuo."""
    return sum(1 for b in individuo.values() if b == base)


def individuo_con_mas_bases(secuencias, base="A"):
    """Devuelve (posición, individuo, cantidad) del individuo con más `base`.
    Recorrido lineal: se guarda el mayor visto hasta el momento (sin ordenar)."""
    mejor_pos, mejor_cant = None, -1
    for i, individuo in enumerate(secuencias):
        cantidad = contar_base(individuo, base)
        if cantidad > mejor_cant:
            mejor_pos, mejor_cant = i, cantidad
    if mejor_pos is None:
        return None
    return mejor_pos, secuencias[mejor_pos], mejor_cant


def promedio_base(secuencias, base="G"):
    """Promedio de apariciones de `base` por individuo."""
    if not secuencias:
        return 0
    return sum(contar_base(i, base) for i in secuencias) / len(secuencias)


def main():
    pos, individuo, cantidad = individuo_con_mas_bases(SECUENCIAS, "A")
    print(f"Individuo con más 'A': #{pos + 1} {individuo} ({cantidad} veces)")
    print("Promedio de 'G' por individuo:", round(promedio_base(SECUENCIAS, "G"), 2))


if __name__ == "__main__":
    main()
