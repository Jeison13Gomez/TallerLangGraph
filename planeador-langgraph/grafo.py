
import operator
from typing import Annotated, TypedDict

from typing import Literal
from pydantic import BaseModel, Field

from agentes import (
    modelo,
    agente_clima,
    agente_presupuesto,
    agente_reservas,
    agente_actividades,
)

from config import MAX_PASOS

from langgraph.graph import StateGraph, START, END


from datos import buscar_destino, normalizar_dia, DESTINOS, PRONOSTICO


from herramientas import crear_reserva
from datos import CUPOS





class EstadoPlaneador(TypedDict):
    consulta: str
    resultados: Annotated[list[str], operator.add]
    consultados: Annotated[list[str], operator.add]
    siguiente: str
    respuesta_final: str
    plan: list[str]




class Decision(BaseModel):
    siguiente: Literal[
        "clima",
        "presupuesto",
        "reservas",
        "fin"
    ] = Field(
        description="Especialista que debe ejecutarse a continuación"
    )


class ClasificacionDominio(BaseModel):
    dentro_dominio: bool = Field(
        description=(
            "True si la consulta corresponde a la "
            "planeación de salidas de fin de semana. "
            "False si pertenece a otro tema."
        )
    )


def clasificar_dominio(consulta: str) -> bool:
    instrucciones = f"""
Eres un clasificador de dominio para un sistema
de planeación de salidas de fin de semana.

El sistema SOLO puede ayudar con:
- Consultar el clima de un destino.
- Calcular presupuestos y costos de viajes.
- Consultar disponibilidad de cupos.
- Recomendar actividades turísticas y lugares para visitar.
- Crear reservas para salidas de fin de semana.
- Combinar estas actividades para planear una salida.

La consulta puede mencionar destinos, fechas,
personas, dinero, transporte, alimentación o reservas.

FUERA DEL DOMINIO:
- Deportes y resultados deportivos.
- Programación y tecnología.
- Matemáticas.
- Historia y política.
- Cultura general.
- Cualquier pregunta que no esté relacionada
  con la planeación de una salida de fin de semana.

REGLAS:
1. Clasifica según la intención real del usuario.
2. No clasifiques como válida una pregunta solo
   porque mencione un lugar o una fecha.
3. No respondas la pregunta.
4. Ante una consulta ambigua que no permita
   identificar una intención de planificación,
   clasifica como fuera del dominio.

CONSULTA:
{consulta}
"""

    try:
        resultado = modelo.with_structured_output(
            ClasificacionDominio
        ).invoke(instrucciones)

        return resultado.dentro_dominio

    except Exception:
        # Si falla el clasificador, no ejecutar agentes.
        return False


class PlanEjecucion(BaseModel):
    agentes: list[Literal[
        "clima",
        "presupuesto",
        "reservas"
    ]] = Field(
        description=(
            "Agentes necesarios para resolver la solicitud, "
            "en orden de ejecución y sin repeticiones."
        )
    )





def crear_plan(consulta: str) -> list[str]:
    instrucciones = f"""
Eres un clasificador de intenciones para un sistema
de planeación de salidas de fin de semana.

Analiza la solicitud e identifica las necesidades
REALES del usuario.

INTENCIÓN CLIMA:
Verdadero si el usuario:
- Pregunta por el pronóstico o la lluvia.
- Solicita conocer las condiciones meteorológicas.
- Condiciona una reserva al clima.

INTENCIÓN PRESUPUESTO:
Verdadero si el usuario:
- Pregunta cuánto cuesta una salida.
- Solicita calcular gastos o saldo.
- Indica un presupuesto que debe verificarse.
- Condiciona una reserva al dinero disponible.

INTENCIÓN RESERVAS:
Verdadero si el usuario:
- Solicita reservar o confirmar una reserva.
- Pregunta por disponibilidad o cupos.
- Solicita gestionar una reserva.

INTENCIÓN ACTIVIDADES:
Verdadero si el usuario:
- Pregunta qué actividades puede realizar en un destino.
- Solicita recomendaciones de planes turísticos.
- Pregunta qué lugares puede visitar.
- Solicita opciones de senderismo, escalada,
  gastronomía, museos o recorridos turísticos.

REGLAS IMPORTANTES:
1. Clasifica cada intención de forma independiente.
2. No actives reservas solo porque se menciona
   un destino, una fecha o un número de personas.
3. No actives clima solo porque se menciona
   una salida, un sábado o un domingo.
4. No actives presupuesto solo porque se menciona
   un número de personas.
5. No actives actividades si el usuario solamente
   solicita clima, presupuesto o reservas.
6. Una consulta puede necesitar varios agentes.
7. No agregues tareas que el usuario no solicitó.
8. Si la pregunta está fuera del dominio,
   las cuatro intenciones deben ser false.

CONSULTA A CLASIFICAR:
{consulta}
"""

    try:
        respuesta = modelo.with_structured_output(
            IntencionesConsulta
        ).invoke(instrucciones)

        plan = []

        if respuesta.necesita_clima:
            plan.append("clima")

        if respuesta.necesita_presupuesto:
            plan.append("presupuesto")

        if respuesta.necesita_reservas:
            plan.append("reservas")

        if respuesta.necesita_actividades:
            plan.append("actividades")

        return plan[:MAX_PASOS]

    except Exception as error:
        print("Error al crear el plan:", error)
        return []


class SolicitudReserva(BaseModel):
    quiere_reservar: bool = Field(
        description="Indica si el usuario solicita crear una reserva"
    )
    destino: str | None = Field(
        default=None,
        description="Destino solicitado"
    )
    dia: str | None = Field(
        default=None,
        description="Sábado o domingo"
    )
    personas: int | None = Field(
        default=None,
        description="Número de personas"
    )
    nombre: str | None = Field(
        default=None,
        description="Nombre del titular de la reserva"
    )
    presupuesto: int | None = Field(
        default=None,
        description="Presupuesto disponible en pesos colombianos"
    )



def extraer_solicitud_reserva(consulta: str):
    instrucciones = f"""
Eres un extractor de información.

Tu única tarea es identificar datos que aparecen
explícitamente en una solicitud de reserva.

CAMPOS:
- quiere_reservar: true si solicita crear una reserva.
- destino: nombre del destino mencionado.
- dia: dia de la semana mencionado.
- personas: cantidad de personas.
- nombre: persona a cuyo nombre se hará la reserva.
- presupuesto: cantidad de dinero disponible en COP.

REGLAS OBLIGATORIAS:
1. No inventes información.
2. No hagas cálculos.
3. No cambies las cantidades numéricas.
4. Conserva exactamente el valor numérico del presupuesto.
5. Si dice "250000 pesos", presupuesto debe ser 250000.
6. Si dice "150000 pesos", presupuesto debe ser 150000.
7. Si dice "a nombre de Pedro", nombre debe ser "Pedro".
8. Si dice "el sábado", dia debe ser "sabado".
9. Si dice "el domingo", dia debe ser "domingo".
10. Si falta un dato, utiliza null.
11. No confundas el presupuesto con el costo del viaje.
12. No crees reservas ni respondas al usuario.

EJEMPLO 1:
Solicitud:
Quiero reservar Guatavita el domingo
para 2 personas a nombre de Ana.
Tengo 180000 pesos.

Extracción:
quiere_reservar=true
destino="Guatavita"
dia="domingo"
personas=2
nombre="Ana"
presupuesto=180000

SOLICITUD REAL:
{consulta}
"""

    return modelo.with_structured_output(
        SolicitudReserva
    ).invoke(instrucciones)




def supervisor(estado):
    consulta = estado["consulta"]
    consultados = estado.get("consultados", [])

    # Crear el plan únicamente en la primera visita.
    if "plan" not in estado:
        if not clasificar_dominio(consulta):
            return {
                "plan": [],
                "siguiente": "fin"
            }

        plan = crear_plan(consulta)

        if not plan:
            return {
                "plan": [],
                "siguiente": "fin"
            }

        return {
            "plan": plan,
            "siguiente": plan[0]
        }

    # Recuperar el plan original.
    plan = estado["plan"]

    # Evitar superar el límite de especialistas.
    if len(consultados) >= MAX_PASOS:
        return {"siguiente": "fin"}

    # Identificar el siguiente agente pendiente.
    pendientes = [
        agente
        for agente in plan
        if agente not in consultados
    ]

    if not pendientes:
        return {"siguiente": "fin"}

    return {"siguiente": pendientes[0]}






def ejecutar_especialista(estado: EstadoPlaneador, nombre: str, agente) -> dict:
    """Ejecuta un especialista y devuelve sus resultados al grafo."""

    consulta = estado["consulta"]

    # Compartir resultados previos con el especialista
    contexto = "\n".join(estado.get("resultados", []))

    mensaje = (
        f"Solicitud original del usuario:\n{consulta}\n\n"
        f"Resultados de otros especialistas:\n{contexto}\n\n"
        "Resuelve únicamente la parte de la solicitud "
        "que corresponde a tu especialidad. "
        "No inventes información."
    )

    respuesta = agente.invoke({
        "messages": [
            {"role": "user", "content": mensaje}
        ]
    })

    contenido = respuesta["messages"][-1].content

    return {
        "resultados": [f"{nombre}: {contenido}"],
        "consultados": [nombre],
    }


def nodo_clima(estado: EstadoPlaneador) -> dict:
    return ejecutar_especialista(
        estado, "clima", agente_clima
    )


def nodo_presupuesto(estado: EstadoPlaneador) -> dict:
    return ejecutar_especialista(
        estado, "presupuesto", agente_presupuesto
    )




def validar_reserva_condicional(
    destino, dia, personas, presupuesto, max_lluvia=30
):
    destino_normalizado = buscar_destino(destino)
    dia_normalizado = normalizar_dia(dia)

    if not destino_normalizado:
        return False, "Destino no encontrado."

    if not dia_normalizado:
        return False, "Día no válido."

    if not isinstance(personas, int) or personas <= 0:
        return False, "Número de personas no válido."

    if presupuesto is None or presupuesto < 0:
        return False, "Presupuesto no válido."

    pronostico = PRONOSTICO.get(
        (destino_normalizado, dia_normalizado)
    )

    if not pronostico:
        return False, "No hay pronóstico disponible."

    datos_destino = DESTINOS[destino_normalizado]

    costo_persona = (
        datos_destino["transporte"]
        + datos_destino["entrada"]
        + datos_destino["alimentacion"]
    )

    costo_total = costo_persona * personas
    probabilidad_lluvia = pronostico["lluvia"]

    if costo_total > presupuesto:
        return False, (
            f"Presupuesto insuficiente. "
            f"Costo total: ${costo_total:,}. "
            f"Presupuesto disponible: ${presupuesto:,}. "
            f"Faltan ${costo_total - presupuesto:,}."
        )

    if probabilidad_lluvia > max_lluvia:
        return False, (
            f"Probabilidad de lluvia demasiado alta: "
            f"{probabilidad_lluvia}%. "
            f"Máximo permitido: {max_lluvia}%."
        )

    return True, (
        f"Condiciones cumplidas. "
        f"Costo total: ${costo_total:,}. "
        f"Saldo restante: ${presupuesto - costo_total:,}. "
        f"Probabilidad de lluvia: {probabilidad_lluvia}%."
    )




def ejecutar_reserva_autorizada(
    destino, dia, personas, nombre, presupuesto
):
    permitido, motivo = validar_reserva_condicional(
        destino=destino,
        dia=dia,
        personas=personas,
        presupuesto=presupuesto
    )

    if not permitido:
        return f"No se realizó ninguna reserva. {motivo}"

    clave = buscar_destino(destino)
    dia_normalizado = normalizar_dia(dia)

    disponibles = CUPOS.get(
        (clave, dia_normalizado), 0
    )

    if disponibles < personas:
        return (
            "No se realizó ninguna reserva. "
            f"Solo hay {disponibles} cupos disponibles."
        )

    resultado = crear_reserva.invoke({
        "destino": destino,
        "dia": dia,
        "personas": personas,
        "nombre": nombre
    })

    return f"{motivo} {resultado}"




def nodo_reservas(estado):
    consulta = estado["consulta"]

    # Extraer los datos de la solicitud con Qwen
    try:
        solicitud = extraer_solicitud_reserva(consulta)
    except Exception:
        return {
            "resultados": [
                "reservas: No se realizó ninguna reserva. "
                "No fue posible interpretar la solicitud."
            ],
            "consultados": ["reservas"],
        }

    # Si solo pregunta por disponibilidad,
    # consultar sin crear una reserva.
    if not solicitud.quiere_reservar:
        return ejecutar_especialista(
            estado, "reservas", agente_reservas
        )

    # Verificar que estén todos los datos obligatorios.
    datos = [
        solicitud.destino,
        solicitud.dia,
        solicitud.personas,
        solicitud.nombre,
        solicitud.presupuesto,
    ]

    if any(dato is None for dato in datos):
        return {
            "resultados": [
                "reservas: No se realizó ninguna reserva. "
                "Faltan datos obligatorios: destino, día, "
                "personas, nombre o presupuesto."
            ],
            "consultados": ["reservas"],
        }

    # Validar tipos y valores antes de crear la reserva.
    if (
        not isinstance(solicitud.personas, int)
        or isinstance(solicitud.personas, bool)
        or solicitud.personas <= 0
        or not isinstance(solicitud.presupuesto, int)
        or isinstance(solicitud.presupuesto, bool)
        or solicitud.presupuesto < 0
        or not solicitud.nombre.strip()
    ):
        return {
            "resultados": [
                "reservas: No se realizó ninguna reserva. "
                "Los datos de la solicitud no son válidos."
            ],
            "consultados": ["reservas"],
        }

    # Crear la reserva mediante la función protegida.
    resultado = ejecutar_reserva_autorizada(
        destino=solicitud.destino,
        dia=solicitud.dia,
        personas=solicitud.personas,
        nombre=solicitud.nombre,
        presupuesto=solicitud.presupuesto,
    )

    return {
        "resultados": [f"reservas: {resultado}"],
        "consultados": ["reservas"],
    }


def nodo_actividades(estado: EstadoPlaneador):
    """
    Ejecuta el agente de actividades turísticas
    y registra su resultado en el estado del grafo.
    """

    return ejecutar_especialista(
        estado,
        "actividades",
        agente_actividades
    )


def sintetizador(estado: EstadoPlaneador) -> dict:
    """Construye la respuesta final usando los resultados obtenidos."""

    resultados = estado.get("resultados", [])

    if not resultados:
        return {
            "respuesta_final": (
                "Solo puedo ayudarte a planear salidas de fin "
                "de semana, incluyendo clima, presupuesto, "
                "reservas y actividades turísticas."
            )
        }

    contexto = "\n".join(resultados)

    instrucciones = f"""
    Eres un asistente que presenta los resultados de un
    planeador de fin de semana.

    Pregunta del usuario:
    {estado['consulta']}

    Información verificada:
    {contexto}

    TAREA:
    Redacta una respuesta final en español utilizando
    exclusivamente la información verificada.

    REGLAS:
    - Responde directamente la pregunta del usuario.
    - No repitas estas instrucciones.
    - No agregues información que no fue solicitada.
    - No inventes datos, costos ni reservas.
    - Si existe una reserva confirmada, informa su código.
    - Si no hay resultados de reservas, no hables de reservas.
    - Mantén la respuesta breve y natural.

    RESPUESTA FINAL:
    """

    respuesta = modelo.invoke(instrucciones)

    return {
        "respuesta_final": respuesta.content
    }


def seleccionar_ruta(estado: EstadoPlaneador) -> str:
    """Devuelve el siguiente nodo seleccionado por el supervisor."""
    return estado["siguiente"]


constructor = StateGraph(EstadoPlaneador)

# Registrar nodos
constructor.add_node("supervisor", supervisor)
constructor.add_node("clima", nodo_clima)
constructor.add_node("presupuesto", nodo_presupuesto)
constructor.add_node("reservas", nodo_reservas)
constructor.add_node("sintetizador", sintetizador)
constructor.add_node("actividades", nodo_actividades)

# Iniciar por el supervisor
constructor.add_edge(START, "supervisor")

# Enrutamiento según la decisión del supervisor
constructor.add_conditional_edges(
    "supervisor",
    seleccionar_ruta,
    {
        "clima": "clima",
        "presupuesto": "presupuesto",
        "reservas": "reservas",
        "actividades": "actividades",
        "fin": "sintetizador",
    },
)

# Cada especialista regresa al supervisor
constructor.add_edge("clima", "supervisor")
constructor.add_edge("presupuesto", "supervisor")
constructor.add_edge("reservas", "supervisor")
constructor.add_edge("actividades", "supervisor")

# Finalizar después del sintetizador
constructor.add_edge("sintetizador", END)


# Compilar el grafo
grafo = constructor.compile()



class IntencionesConsulta(BaseModel):
    necesita_clima: bool = Field(
        description=(
            "True únicamente si el usuario solicita "
            "información meteorológica o condiciona "
            "una decisión al clima."
        )
    )

    necesita_presupuesto: bool = Field(
        description=(
            "True únicamente si el usuario solicita "
            "costos, saldos o condiciona una decisión "
            "al dinero disponible."
        )
    )

    necesita_reservas: bool = Field(
        description=(
            "True únicamente si el usuario solicita "
            "consultar disponibilidad o crear una reserva."
        )
    )

    necesita_actividades: bool = Field(
        description=(
            "True únicamente si el usuario solicita "
            "recomendaciones de actividades turísticas, "
            "lugares para visitar o planes para realizar "
            "en un destino, como senderismo, gastronomía, "
            "museos, escalada o recorridos culturales. "
            "False si solamente pregunta por clima, "
            "presupuesto o reservas."
        )
    )

    
