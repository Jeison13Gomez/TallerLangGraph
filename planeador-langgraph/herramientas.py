
from langchain_core.tools import tool


from datos import (
    DESTINOS,
    PRONOSTICO,
    CUPOS,
    RESERVAS,
    buscar_destino,
    normalizar_dia,
    pesos,
    ACTIVIDADES
)


@tool
def listar_destinos() -> str:
    """Lista los destinos disponibles para las salidas de fin de semana."""
    nombres = [
        destino["nombre"]
        for destino in DESTINOS.values()
    ]

    return "Destinos disponibles: " + ", ".join(nombres)


@tool
def consultar_pronostico(destino: str, dia: str) -> str:
    """Consulta el pronóstico del clima para un destino el sábado o domingo."""
    clave = buscar_destino(destino)
    dia_normalizado = normalizar_dia(dia)

    if clave is None:
        return f"Destino no reconocido: {destino}"

    if dia_normalizado is None:
        return "Día no válido. Debe ser sábado o domingo."

    pronostico = PRONOSTICO.get((clave, dia_normalizado))

    if pronostico is None:
        return "No hay pronóstico disponible para esa consulta."

    nombre = DESTINOS[clave]["nombre"]

    return (
        f"Pronóstico para {nombre} el {dia_normalizado}: "
        f"{pronostico['cielo']}, "
        f"temperatura entre {pronostico['min']}°C y "
        f"{pronostico['max']}°C, "
        f"probabilidad de lluvia del {pronostico['lluvia']}%."
    )


@tool
def estimar_costo(destino: str, personas: int) -> str:
    """Estima el costo total de una salida según el destino y el número de personas."""
    clave = buscar_destino(destino)

    if clave is None:
        return f"Destino no reconocido: {destino}"

    if personas <= 0:
        return "El número de personas debe ser mayor que cero."

    datos = DESTINOS[clave]

    costo_persona = (
        datos["transporte"]
        + datos["entrada"]
        + datos["alimentacion"]
    )

    costo_total = costo_persona * personas

    return (
        f"Destino: {datos['nombre']}. "
        f"Personas: {personas}. "
        f"Costo por persona: {pesos(costo_persona)}. "
        f"Costo total: {pesos(costo_total)}."
    )


@tool
def calcular_saldo(presupuesto: int, costo_total: int) -> str:
    """Calcula el dinero restante o faltante después de cubrir el costo de una salida."""
    if presupuesto < 0 or costo_total < 0:
        return "El presupuesto y el costo deben ser valores no negativos."

    saldo = presupuesto - costo_total

    if saldo >= 0:
        return (
            f"Presupuesto: {pesos(presupuesto)}. "
            f"Costo total: {pesos(costo_total)}. "
            f"Saldo disponible: {pesos(saldo)}. "
            "El presupuesto es suficiente."
        )

    return (
        f"Presupuesto: {pesos(presupuesto)}. "
        f"Costo total: {pesos(costo_total)}. "
        f"Faltan {pesos(abs(saldo))}. "
        "El presupuesto es insuficiente."
    )


@tool
def consultar_disponibilidad(destino: str, dia: str, personas: int) -> str:
    """Consulta si hay cupos suficientes para un grupo en un destino y día."""
    clave = buscar_destino(destino)
    dia_normalizado = normalizar_dia(dia)

    if clave is None:
        return f"Destino no reconocido: {destino}"

    if dia_normalizado is None:
        return "Día no válido. Debe ser sábado o domingo."

    if personas <= 0:
        return "El número de personas debe ser mayor que cero."

    disponibles = CUPOS.get((clave, dia_normalizado), 0)
    nombre = DESTINOS[clave]["nombre"]

    if disponibles >= personas:
        return (
            f"Hay disponibilidad para {personas} personas "
            f"en {nombre} el {dia_normalizado}. "
            f"Cupos disponibles: {disponibles}."
        )

    return (
        f"No hay cupos suficientes en {nombre} el {dia_normalizado}. "
        f"Cupos solicitados: {personas}. "
        f"Cupos disponibles: {disponibles}."
    )


@tool
def crear_reserva(
    destino: str,
    dia: str,
    personas: int,
    nombre: str
) -> str:
    """Crea una reserva ficticia si hay cupos suficientes."""
    clave = buscar_destino(destino)
    dia_normalizado = normalizar_dia(dia)

    if clave is None:
        return f"Destino no reconocido: {destino}"

    if dia_normalizado is None:
        return "Día no válido. Debe ser sábado o domingo."

    if personas <= 0:
        return "El número de personas debe ser mayor que cero."

    if not nombre.strip():
        return "Debes proporcionar un nombre para la reserva."

    llave = (clave, dia_normalizado)
    disponibles = CUPOS.get(llave, 0)

    if disponibles < personas:
        return (
            f"No se pudo crear la reserva. "
            f"Solo hay {disponibles} cupos disponibles."
        )

    codigo = f"RES-{len(RESERVAS) + 1:04d}"

    reserva = {
        "codigo": codigo,
        "destino": clave,
        "dia": dia_normalizado,
        "personas": personas,
        "nombre": nombre,
    }

    RESERVAS.append(reserva)
    CUPOS[llave] -= personas

    return (
        f"Reserva confirmada. Código: {codigo}. "
        f"Destino: {DESTINOS[clave]['nombre']}. "
        f"Día: {dia_normalizado}. "
        f"Personas: {personas}. "
        f"Nombre: {nombre}. "
        f"Cupos restantes: {CUPOS[llave]}."
    )


@tool
def recomendar_actividades(destino: str) -> str:
    """
    Recomienda actividades turísticas simuladas
    para un destino cercano a Bogotá.

    Args:
        destino: Nombre del destino turístico.

    Returns:
        Lista de actividades disponibles para el destino.
    """

    destino_id = buscar_destino(destino)

    if destino_id is None:
        return (
            f"No se encontraron actividades para '{destino}'. "
            "Consulta los destinos disponibles."
        )

    actividades = ACTIVIDADES.get(destino_id, [])

    if not actividades:
        return (
            f"No hay actividades registradas para {destino}."
        )

    nombre = DESTINOS[destino_id]["nombre"]

    lista = "\n".join(
        f"- {actividad}" for actividad in actividades
    )

    return (
        f"Actividades recomendadas en {nombre}:\n"
        f"{lista}"
    )
