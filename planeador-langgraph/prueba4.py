
import time
from grafo import grafo
from datos import RESERVAS, CUPOS

# ==========================================
# PRUEBA 4: RESERVA CONDICIONAL EN SUESCA
# ==========================================

consulta = (
    "Queremos ir a Suesca el sábado, somos 3 personas "
    "y tenemos un presupuesto de 250000 pesos. "
    "Si hay poca probabilidad de lluvia y el dinero "
    "alcanza, realiza una reserva a nombre de Laura."
)

estado_inicial = {
    "consulta": consulta,
    "resultados": [],
    "consultados": [],
    "siguiente": "",
    "respuesta_final": "",
}

# Estado inicial de las reservas
reservas_antes = len(RESERVAS)
cupos_antes = CUPOS[("suesca", "sabado")]

agentes_consultados = []
nodos_ejecutados = []
respuesta_final = ""
resultados_agentes = []

print("=" * 65)
print("PRUEBA 4: RESERVA CONDICIONAL EN SUESCA")
print("=" * 65)
print("Consulta:", consulta)
print("\nINICIO DE LA TRAZA")

inicio = time.perf_counter()

# ==========================================
# EJECUCIÓN DEL GRAFO
# ==========================================

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
            print("Agente:", agentes)

        if "resultados" in actualizacion:
            for resultado in actualizacion["resultados"]:
                resultados_agentes.append(resultado)
                print("Resultado:", resultado)

        if "respuesta_final" in actualizacion:
            respuesta_final = actualizacion["respuesta_final"]
            print("Respuesta final:")
            print(respuesta_final)

tiempo_total = time.perf_counter() - inicio

# ==========================================
# VERIFICACIÓN DE LA RESERVA
# ==========================================

reservas_despues = len(RESERVAS)
cupos_despues = CUPOS[("suesca", "sabado")]

nuevas_reservas = RESERVAS[reservas_antes:]

reserva_laura = next(
    (
        reserva
        for reserva in nuevas_reservas
        if reserva["destino"] == "suesca"
        and reserva["dia"] == "sabado"
        and reserva["personas"] == 3
        and reserva["nombre"].lower() == "laura"
    ),
    None
)

agentes_esperados = {
    "clima", "presupuesto", "reservas"
}

tres_agentes = (
    set(agentes_consultados) == agentes_esperados
    and len(agentes_consultados) == 3
)

reserva_correcta = (
    reserva_laura is not None
    and reservas_despues == reservas_antes + 1
    and cupos_despues == cupos_antes - 3
)

# ==========================================
# RESUMEN PARA LA BITÁCORA
# ==========================================

print("\n" + "=" * 65)
print("RESUMEN DE LA PRUEBA 4")
print("=" * 65)

print(f"Tiempo total: {tiempo_total:.2f} segundos")
print("Nodos ejecutados:", " -> ".join(nodos_ejecutados))
print("Agentes consultados:", agentes_consultados)
print("Cantidad de agentes:", len(agentes_consultados))

print("\nVerificación de reservas:")
print("Reservas antes:", reservas_antes)
print("Reservas después:", reservas_despues)
print("Cupos antes:", cupos_antes)
print("Cupos después:", cupos_despues)

if reserva_laura:
    print("Código de reserva:", reserva_laura["codigo"])
    print("Titular:", reserva_laura["nombre"])
else:
    print("No se encontró una reserva para Laura.")

print("\nValidaciones:")
print("¿Se ejecutaron los tres agentes?:", tres_agentes)
print("¿La reserva fue creada correctamente?:", reserva_correcta)

print("\n" + "=" * 65)

if tres_agentes and reserva_correcta:
    print("RESULTADO: PRUEBA 4 SUPERADA")
else:
    print("RESULTADO: PRUEBA 4 NO SUPERADA")
    print("Revisa la traza para identificar el problema.")

print(f"TIEMPO PARA LA BITÁCORA: {tiempo_total:.2f} s")
