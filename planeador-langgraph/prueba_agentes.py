
from agentes import agente_reservas

respuesta = agente_reservas.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Quiero reservar 3 cupos en Suesca para"
                 "el sábado a nombre de Laura. Primero consulta"
                  "la disponibilidad y, si hay cupos suficientes,"
                   "crea la reserva."

            )
        }
    ]
})

print("\nRESPUESTA DEL AGENTE:")
print(respuesta["messages"][-1].content)

print("\nHERRAMIENTAS UTILIZADAS:")
for mensaje in respuesta["messages"]:
    if getattr(mensaje, "tool_calls", None):
        for llamada in mensaje.tool_calls:
            print(llamada["name"], llamada["args"])
