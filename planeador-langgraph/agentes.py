
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from config import MODELO, OLLAMA_URL

from herramientas import (
    listar_destinos,
    consultar_pronostico,
    estimar_costo,
    calcular_saldo,
    consultar_disponibilidad,
    crear_reserva,
    recomendar_actividades,
)


modelo = ChatOllama(
    model=MODELO,
    base_url=OLLAMA_URL,
    temperature=0,
)





agente_clima = create_agent(
    model=modelo,
    tools=[
        listar_destinos,
        consultar_pronostico,
    ],
    system_prompt=(
        "Eres un agente especializado exclusivamente en clima.\n"
        "Tu responsabilidad es consultar pronósticos para "
        "salidas de fin de semana cerca de Bogotá.\n\n"

        "REGLAS:\n"
        "1. Si el usuario indica destino y día, utiliza "
        "consultar_pronostico.\n"
        "2. Responde únicamente sobre condiciones meteorológicas.\n"
        "3. No hables de precios, presupuestos ni reservas.\n"
        "4. No recomiendes consultar agencias de viajes "
        "ni buscar información en internet.\n"
        "5. Utiliza exclusivamente los datos de las herramientas.\n"
        "6. Responde en español de forma breve."
    ),
)





agente_presupuesto = create_agent(
    model=modelo,
    tools=[
        estimar_costo,
        calcular_saldo,
    ],
    system_prompt=(
        "Eres un agente especializado exclusivamente en presupuestos.\n\n"

        "REGLAS:\n"
        "1. Si el usuario indica destino y número de personas, "
        "utiliza estimar_costo.\n"
        "2. Si también proporciona un presupuesto, utiliza "
        "calcular_saldo después de estimar_costo.\n"
        "3. Si el usuario solo pregunta cuánto cuesta, "
        "responde el costo sin pedir un presupuesto.\n"
        "4. No hables de clima ni de reservas.\n"
        "5. No recomiendes agencias de viajes ni búsquedas en internet.\n"
        "6. No inventes precios ni realices cálculos manualmente.\n"
        "7. Responde en español de manera breve."
    ),
)





agente_reservas = create_agent(
    model=modelo,
    tools=[consultar_disponibilidad],
    system_prompt=(
        "Eres un agente especializado en reservas de salidas "
        "de fin de semana.\n"
        "Tu función es consultar la disponibilidad de cupos.\n"
        "REGLAS:\n"
        "1. Utiliza consultar_disponibilidad para verificar cupos.\n"
        "2. No afirmes que una reserva fue creada.\n"
        "3. No inventes códigos de reserva.\n"
        "4. La creación de reservas es responsabilidad del grafo.\n"
        "5. Responde brevemente en español."
    ),
)


# --------------------------------------------------
# AGENTE DE ACTIVIDADES
# --------------------------------------------------

agente_actividades = create_agent(
    model=modelo,
    tools=[recomendar_actividades],
    system_prompt=(
        "Eres un agente especializado en recomendar "
        "actividades turísticas para salidas de fin de semana "
        "cerca de Bogotá. "

        "Tu responsabilidad es identificar el destino "
        "mencionado por el usuario y consultar la herramienta "
        "recomendar_actividades para obtener las opciones. "

        "REGLAS: "
        "1. Utiliza siempre la herramienta recomendar_actividades. "
        "2. Recomienda únicamente las actividades devueltas "
        "por la herramienta. "
        "3. No inventes actividades, horarios ni precios. "
        "4. Si el destino no está disponible, informa al usuario. "
        "5. Responde en español de forma clara y breve. "
        "6. No realices reservas ni calcules presupuestos."
    )
)
