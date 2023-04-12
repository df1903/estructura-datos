"""
Ejecuta la simulación de la isla "El Paro".

    python -m proyectos.isla_cuevas.main                      # 5 minutos simulados
    python -m proyectos.isla_cuevas.main --segundos 600 --camiones 10 --cuevas 7 --semilla 1

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

import argparse

from .isla import Simulacion


def main():
    ap = argparse.ArgumentParser(description="Simulación de la isla El Paro")
    ap.add_argument("--segundos", type=int, default=300, help="tiempo a simular")
    ap.add_argument("--camiones", type=int, default=10)
    ap.add_argument("--cuevas", type=int, default=7)
    ap.add_argument("--semilla", type=int, default=None, help="semilla aleatoria (reproducible)")
    args = ap.parse_args()

    sim = Simulacion(args.camiones, args.cuevas, args.semilla)
    print("Isla inicial (pre-orden):")
    sim.isla.mostrar("pre")
    sim.avanzar(args.segundos)
    print("\nEventos:")
    print("\n".join(sim.registro) or "  (sin eventos todavía; los camiones salen cada 30 s)")
    print("\nIsla final (pre-orden):")
    sim.isla.mostrar("pre")
    print("\n" + str(sim.almacen))


if __name__ == "__main__":
    main()
