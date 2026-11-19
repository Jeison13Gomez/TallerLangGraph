
import time
from grafo import grafo
from datos import RESERVAS, CUPOS

# ==========================================
# PRUEBA 6: PREGUNTA FUERA DE CONTEXTO
# ==========================================

consulta = "¿Quién ganó el Mundial de fútbol de 2022?"

estado_inicial = {
    "consulta": consulta,
    "resultados": [],
    "consultados": [],
    "siguiente": "",
    "respuesta_final": "",
}

reservas_antes = len(RESERVAS)
cupos_antes = CUPOS.copy()

agentes_consultados = []
respuesta_final = ""
nodos_ejecutados = []

print("=" * 60)
print("PRUEBA 6: PREGUNTA FUERA DE CONTEXTO")
print("=" * 60)
print("Consulta:", consulta)
print("\nINICIO DE LA TRAZA")

inicio = time.perf_counter()

for numero, evento in enumerate(
    grafo.stream(estado_inicial, stream_mode="updates"),
    start=1
):
    for nodo, actualizacion in evento.items():
        nodos_ejecutados.append(nodo)

        print(f"\nPASO {numero}: {nodo}")

        if "siguiente" in actualizacion:
            print("Decisión:", actualizacion["siguiente"])

        if "consultados" in actualizacion:
            agentes = actualizacion["consultados"]
            agentes_consultados.extend(agentes)
            print("Agentes:", agentes)

        if "resultados" in actualizacion:
            for resultado in actualizacion["resultados"]:
                print("Resultado:", resultado)

        if "respuesta_final" in actualizacion:
            respuesta_final = actualizacion["respuesta_final"]
            print("Respuesta final:")
            print(respuesta_final)

tiempo_total = time.perf_counter() - inicio

reservas_despues = len(RESERVAS)
cupos_despues = CUPOS.copy()

# ==========================================
# VALIDACIONES
# ==========================================

sin_especialistas = len(agentes_consultados) == 0
sin_reservas_nuevas = reservas_antes == reservas_despues
cupos_sin_cambios = cupos_antes == cupos_despues

respuesta_correcta = (
    "fin de semana" in respuesta_final.lower()
    or "salidas" in respuesta_final.lower()
    or "viajes" in respuesta_final.lower()
)

print("\n" + "=" * 60)
print("RESUMEN DE LA PRUEBA 6")
print("=" * 60)

print(f"Tiempo total: {tiempo_total:.2f} segundos")
print("Nodos ejecutados:", " -> ".join(nodos_ejecutados))
print("Agentes consultados:", agentes_consultados)
print("Cantidad de agentes:", len(agentes_consultados))

print("\nVerificaciones:")
print("¿Se evitaron agentes especialistas?:", sin_especialistas)
print("¿Se evitaron nuevas reservas?:", sin_reservas_nuevas)
print("¿Los cupos permanecieron iguales?:", cupos_sin_cambios)
print("¿La respuesta corresponde al dominio?:", respuesta_correcta)

assert sin_especialistas, (
    "ERROR: Se ejecutaron agentes para una pregunta fuera de contexto."
)

assert sin_reservas_nuevas, (
    "ERROR: Se creó una reserva inesperadamente."
)

assert cupos_sin_cambios, (
    "ERROR: Se modificaron los cupos."
)

assert respuesta_correcta, (
    "ERROR: La respuesta no parece corresponder al dominio."
)

print("\nRESULTADO: PRUEBA 6 SUPERADA")
print(f"TIEMPO PARA LA BITÁCORA: {tiempo_total:.2f} s")
