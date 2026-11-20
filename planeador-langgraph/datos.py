
import unicodedata

# Costos ficticios por persona en pesos colombianos
DESTINOS = {
    "guatavita": {
        "nombre": "Laguna de Guatavita",
        "transporte": 30000,
        "entrada": 25000,
        "alimentacion": 35000
    },
    "zipaquira": {
        "nombre": "Catedral de Sal de Zipaquirá",
        "transporte": 20000,
        "entrada": 50000,
        "alimentacion": 30000
    },
    "villa de leyva": {
        "nombre": "Villa de Leyva",
        "transporte": 70000,
        "entrada": 0,
        "alimentacion": 45000
    },
    "suesca": {
        "nombre": "Rocas de Suesca",
        "transporte": 25000,
        "entrada": 15000,
        "alimentacion": 30000
    },
    "chicaque": {
        "nombre": "Parque Natural Chicaque",
        "transporte": 20000,
        "entrada": 35000,
        "alimentacion": 35000
    }
}


# Otras formas en que un usuario podría nombrar un destino
ALIAS = {
    "laguna": "guatavita",
    "catedral": "zipaquira",
    "zipa": "zipaquira",
    "leiva": "villa de leyva",
    "leyva": "villa de leyva",
    "rocas": "suesca",
}


# Pronóstico ficticio: (destino, día) -> datos
PRONOSTICO = {
    ("guatavita", "sabado"): {"cielo": "parcialmente nublado", "min": 8, "max": 18, "lluvia": 30},
    ("guatavita", "domingo"): {"cielo": "lluvioso", "min": 7, "max": 15, "lluvia": 80},

    ("zipaquira", "sabado"): {"cielo": "nublado", "min": 9, "max": 19, "lluvia": 40},
    ("zipaquira", "domingo"): {"cielo": "soleado", "min": 8, "max": 20, "lluvia": 10},

    ("villa de leyva", "sabado"): {"cielo": "soleado", "min": 12, "max": 25, "lluvia": 5},
    ("villa de leyva", "domingo"): {"cielo": "soleado", "min": 11, "max": 24, "lluvia": 10},

    ("suesca", "sabado"): {"cielo": "soleado", "min": 7, "max": 21, "lluvia": 15},
    ("suesca", "domingo"): {"cielo": "tormentas en la tarde", "min": 8, "max": 17, "lluvia": 70},

    ("chicaque", "sabado"): {"cielo": "neblina en la mañana", "min": 10, "max": 19, "lluvia": 50},
    ("chicaque", "domingo"): {"cielo": "parcialmente nublado", "min": 10, "max": 20, "lluvia": 35},
}


# Cupos disponibles: (destino, día) -> cantidad
CUPOS = {
    ("guatavita", "sabado"): 12,
    ("guatavita", "domingo"): 4,
    ("zipaquira", "sabado"): 30,
    ("zipaquira", "domingo"): 25,
    ("villa de leyva", "sabado"): 2,
    ("villa de leyva", "domingo"): 10,
    ("suesca", "sabado"): 8,
    ("suesca", "domingo"): 6,
    ("chicaque", "sabado"): 0,
    ("chicaque", "domingo"): 15,
}

# Reservas creadas durante la ejecución
RESERVAS: list[dict] = []




# Actividades turísticas simuladas por destino.
# Información ficticia utilizada exclusivamente en el taller.

ACTIVIDADES = {
    "guatavita": [
        "Senderismo por los alrededores de la laguna",
        "Recorridos culturales e históricos",
        "Fotografía de paisajes naturales"
    ],
    "zipaquira": [
        "Visita turística a la Catedral de Sal",
        "Recorrido por el centro histórico",
        "Degustación de gastronomía típica"
    ],
    "villa de leyva": [
        "Recorrido por la Plaza Mayor",
        "Visita a museos y sitios históricos",
        "Senderismo por paisajes naturales"
    ],
    "suesca": [
        "Escalada en roca",
        "Senderismo por los alrededores",
        "Fotografía de paisajes y formaciones rocosas"
    ],
    "chicaque": [
        "Senderismo por senderos ecológicos",
        "Observación de aves",
        "Fotografía de flora y fauna"
    ]
}



def normalizar(texto: str) -> str:
    """Convierte texto a minúsculas, sin tildes ni espacios sobrantes."""
    sin_tildes = unicodedata.normalize("NFD", texto or "")
    sin_tildes = "".join(
        c for c in sin_tildes
        if unicodedata.category(c) != "Mn"
    )
    return " ".join(sin_tildes.lower().split())


def buscar_destino(texto: str) -> str | None:
    """Devuelve la clave del destino o None si no existe."""
    t = normalizar(texto)

    if not t:
        return None

    for clave in DESTINOS:
        if clave in t or (len(t) >= 4 and t in clave):
            return clave

    for alias, clave in ALIAS.items():
        if alias in t:
            return clave

    return None


def normalizar_dia(texto: str) -> str | None:
    """Reconoce sábado y domingo, incluso con abreviaturas."""
    t = normalizar(texto)

    if t.startswith("sab"):
        return "sabado"

    if t.startswith("dom"):
        return "domingo"

    return None


def pesos(valor: int) -> str:
    """Formatea números como pesos colombianos."""
    return "$" + f"{valor:,}".replace(",", ".")



