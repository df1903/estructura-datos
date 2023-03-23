"""
Taller de diccionarios: jugadores, patinetas, competidores, zodiaco y nómina.
Ejecutar:  python -m diccionarios.taller

Autor: Daniel Felipe Franco Rincón
Materia: Estructura de Datos
"""

from collections import Counter

# --------------------------------------------------------------------------- #
# 1) Equipo de fútbol (6 jugadores)
# --------------------------------------------------------------------------- #
EQUIPO = [
    {"cedula": "001", "nombre": "jugador1", "apellido": "uno", "velocidad": 70, "aceleración": 10, "potencia": 70},
    {"cedula": "002", "nombre": "daniel", "apellido": "franco", "velocidad": 60, "aceleración": 9, "potencia": 90},
    {"cedula": "003", "nombre": "jugador3", "apellido": "tres", "velocidad": 50, "aceleración": 8, "potencia": 6},
    {"cedula": "004", "nombre": "jugador4", "apellido": "cuatro", "velocidad": 60, "aceleración": 9, "potencia": 6},
    {"cedula": "005", "nombre": "jugador5", "apellido": "cinco", "velocidad": 80, "aceleración": 18, "potencia": 10},
    {"cedula": "006", "nombre": "felipe", "apellido": "rincon", "velocidad": 70, "aceleración": 9, "potencia": 90},
]


def estadisticas_equipo(equipo):
    """Jugador más rápido, con más aceleración, con más potencia y promedio de velocidad."""
    return {
        "mas_rapido": max(equipo, key=lambda j: j["velocidad"]),
        "mas_aceleracion": max(equipo, key=lambda j: j["aceleración"]),
        "mas_potente": max(equipo, key=lambda j: j["potencia"]),
        "promedio_velocidad": sum(j["velocidad"] for j in equipo) / len(equipo),
    }


# --------------------------------------------------------------------------- #
# 2) Almacén de patinetas (15)
# --------------------------------------------------------------------------- #
PATINETAS = [
    {"tipo material": "a", "velocidad": 70, "ancho": 7, "alto": 9, "color": "amarillo", "precio": 400},
    {"tipo material": "b", "velocidad": 80, "ancho": 6, "alto": 9, "color": "verde", "precio": 300},
    {"tipo material": "c", "velocidad": 90, "ancho": 6, "alto": 8, "color": "rojo", "precio": 200},
    {"tipo material": "d", "velocidad": 60, "ancho": 5, "alto": 8, "color": "gris", "precio": 403},
    {"tipo material": "e", "velocidad": 50, "ancho": 4, "alto": 7, "color": "cafe", "precio": 100},
    {"tipo material": "a", "velocidad": 75, "ancho": 7, "alto": 9, "color": "azul", "precio": 350},
    {"tipo material": "b", "velocidad": 85, "ancho": 6, "alto": 9, "color": "negro", "precio": 320},
    {"tipo material": "c", "velocidad": 65, "ancho": 6, "alto": 8, "color": "blanco", "precio": 210},
    {"tipo material": "d", "velocidad": 55, "ancho": 5, "alto": 8, "color": "rosado", "precio": 390},
    {"tipo material": "e", "velocidad": 95, "ancho": 4, "alto": 7, "color": "naranja", "precio": 150},
    {"tipo material": "a", "velocidad": 72, "ancho": 7, "alto": 9, "color": "morado", "precio": 410},
    {"tipo material": "b", "velocidad": 82, "ancho": 6, "alto": 9, "color": "cafe", "precio": 310},
    {"tipo material": "c", "velocidad": 92, "ancho": 6, "alto": 8, "color": "verde", "precio": 220},
    {"tipo material": "d", "velocidad": 62, "ancho": 5, "alto": 8, "color": "gris", "precio": 395},
    {"tipo material": "e", "velocidad": 52, "ancho": 4, "alto": 7, "color": "rojo", "precio": 120},
]


def costo_total(patinetas):
    return sum(p["precio"] for p in patinetas)


def segunda_mejor_velocidad(patinetas):
    """Segunda patineta con mejor velocidad (sin ordenar toda la lista)."""
    primera = segunda = None
    for p in patinetas:
        if primera is None or p["velocidad"] > primera["velocidad"]:
            primera, segunda = p, primera
        elif segunda is None or p["velocidad"] > segunda["velocidad"]:
            segunda = p
    return segunda


# --------------------------------------------------------------------------- #
# 3) Competidores 100 m (d = v * t)
# --------------------------------------------------------------------------- #
class Competidor:
    def __init__(self, cedula, nombre, apellido, direccion, telefono, velocidad):
        self.datos = {"cedula": cedula, "nombre": nombre, "apellido": apellido,
                      "dirección": direccion, "teléfono": telefono, "velocidad": velocidad}

    def tiempo(self, distancia=100):
        """De d = v*t  ->  t = d / v  (velocidad en m/s)."""
        return distancia / self.datos["velocidad"]


def ultimo_en_llegar(competidores, distancia=100):
    """Competidor que llegó de último (el de mayor tiempo)."""
    return max(competidores, key=lambda c: c.tiempo(distancia))


def primero_en_llegar(competidores, distancia=100):
    return min(competidores, key=lambda c: c.tiempo(distancia))


# --------------------------------------------------------------------------- #
# 4) Signo zodiacal
# --------------------------------------------------------------------------- #
# (mes, día) de inicio de cada signo, en orden dentro del año
_SIGNOS = [((1, 20), "Acuario"), ((2, 19), "Piscis"), ((3, 21), "Aries"), ((4, 20), "Tauro"),
           ((5, 21), "Géminis"), ((6, 21), "Cáncer"), ((7, 23), "Leo"), ((8, 23), "Virgo"),
           ((9, 23), "Libra"), ((10, 23), "Escorpio"), ((11, 22), "Sagitario"),
           ((12, 22), "Capricornio")]


def signo_zodiacal(mes, dia):
    """Signo zodiacal para una fecha de nacimiento."""
    signo = "Capricornio"
    for inicio, nombre in _SIGNOS:
        if (mes, dia) >= inicio:
            signo = nombre
    return signo


def signo_mas_comun(personas):
    """`personas`: dict {nombre: (mes, día)}. Devuelve (signo, veces)."""
    conteo = {}
    for mes, dia in personas.values():
        s = signo_zodiacal(mes, dia)
        conteo[s] = conteo.get(s, 0) + 1
    signo = max(conteo, key=conteo.get)
    return signo, conteo[signo]


# --------------------------------------------------------------------------- #
# 5) Nómina de 6 trabajadores
# --------------------------------------------------------------------------- #
SALARIO_MINIMO = 1_300_000  # ajustar al valor vigente
OCUPACIONES = ["Reuniones", "Exposiciones", "Tomar café", "Imprimir copias",
               "Enviar informes", "Firmar certificados"]


def descuento(salario, minimo=SALARIO_MINIMO):
    """Porcentaje de descuento según cuántos mínimos gana:
    <= 3 mínimos: 10 % | > 3 y <= 6: 15 % | > 6: 20 %."""
    if salario <= 3 * minimo:
        return 0.10
    if salario <= 6 * minimo:
        return 0.15
    return 0.20


def nomina(trabajadores, minimo=SALARIO_MINIMO):
    """Calcula el descuento y salario neto de cada trabajador y devuelve el resumen."""
    for t in trabajadores:
        t["descuento"] = round(t["salario"] * descuento(t["salario"], minimo), 2)
        t["neto"] = t["salario"] - t["descuento"]
    todas = Counter(o for t in trabajadores for o in t["ocupaciones"])
    return {
        "mayor_salario": max(trabajadores, key=lambda t: t["salario"]),
        "ocupacion_mas_comun": todas.most_common(1)[0],
        "mas_ocupaciones": max(trabajadores, key=lambda t: len(t["ocupaciones"])),
    }


TRABAJADORES = [
    {"cedula": "101", "nombre": "Ana", "apellido": "Gómez", "salario": 1_300_000, "ocupaciones": OCUPACIONES[:2]},
    {"cedula": "102", "nombre": "Luis", "apellido": "Pérez", "salario": 3_900_000, "ocupaciones": OCUPACIONES[:4]},
    {"cedula": "103", "nombre": "Marta", "apellido": "Ríos", "salario": 5_200_000, "ocupaciones": OCUPACIONES[1:3]},
    {"cedula": "104", "nombre": "Juan", "apellido": "Soto", "salario": 7_800_000, "ocupaciones": OCUPACIONES[1:]},
    {"cedula": "105", "nombre": "Sara", "apellido": "León", "salario": 2_600_000, "ocupaciones": OCUPACIONES[2:4]},
    {"cedula": "106", "nombre": "Tomás", "apellido": "Vega", "salario": 9_100_000, "ocupaciones": OCUPACIONES[:1]},
]


def main():
    e = estadisticas_equipo(EQUIPO)
    print("== 1) Equipo de fútbol ==")
    print("Más rápido     :", e["mas_rapido"]["nombre"], e["mas_rapido"]["apellido"], e["mas_rapido"]["velocidad"], "km/h")
    print("Más aceleración:", e["mas_aceleracion"]["nombre"], e["mas_aceleracion"]["aceleración"])
    print("Más potencia   :", e["mas_potente"]["nombre"], e["mas_potente"]["potencia"])
    print("Promedio veloc.:", round(e["promedio_velocidad"], 2))

    print("\n== 2) Patinetas ==")
    print("Costo total:", costo_total(PATINETAS))
    print("Segunda con mejor velocidad:", segunda_mejor_velocidad(PATINETAS))

    print("\n== 3) Competidores 100 m ==")
    comp = [Competidor(str(i), f"corredor{i}", "X", "calle", "300", 5 + i * 0.5) for i in range(1, 11)]
    u = ultimo_en_llegar(comp)
    print(f"Llegó de último {u.datos['nombre']} en {u.tiempo():.2f} s")

    print("\n== 4) Zodiaco ==")
    personas = {"p1": (1, 5), "p2": (3, 25), "p3": (4, 2), "p4": (3, 30), "p5": (8, 10),
                "p6": (12, 25), "p7": (3, 22), "p8": (7, 1), "p9": (11, 3), "p10": (5, 5)}
    print("Signo de p2:", signo_zodiacal(*personas["p2"]))
    print("Signo más común:", signo_mas_comun(personas))

    print("\n== 5) Nómina ==")
    r = nomina(TRABAJADORES)
    for t in TRABAJADORES:
        print(f"{t['nombre']:6} salario {t['salario']:>10,} desc {t['descuento']:>12,.0f} neto {t['neto']:>12,.0f}")
    print("Mayor salario:", r["mayor_salario"]["nombre"])
    print("Ocupación más común:", r["ocupacion_mas_comun"])
    print("Más ocupaciones:", r["mas_ocupaciones"]["nombre"])


if __name__ == "__main__":
    main()
