
import time
from grafo import grafo
from datos import RESERVAS, CUPOS

# ==========================================
# PRUEBA 5: SUESCA - DOMINGO
# ==========================================

consulta = (
    "Somos 3 personas y tenemos un presupuesto de "
    "150000 pesos. Queremos reservar Suesca el domingo "
    "a nombre de Laura, solo si alcanza el dinero."
)

estado_inicial = {
    "consulta": consulta,
    "resultados": [],
    "consultados": [],
    "siguiente": "",
    "respuesta_final": "",
}

# Guardar el estado antes de ejecutar
reservas_antes = len(RESERVAS)
cupos_antes = CUPOS[("suesca", "domingo")]

agentes_consultados = []
respuesta_final = ""

print("=" * 60)
print("PRUEBA 5: SUESCA - DOMINGO")
print("=" * 60)
print("Consulta:", consulta)
print("\nINICIO DE LA TRAZA")

# Iniciar cronómetro
inicio = time.perf_counter()

# Ejecutar el grafo y registrar sus pasos
for numero, evento in enumerate(
    grafo.stream(estado_inicial, stream_mode="updates"),
    start=1
):
    for nodo, actualizacion in evento.items():
        print(f"\nPASO {numero}: {nodo}")

        if "siguiente" in actualizacion:
            print("Decisión:", actualizacion["siguiente"])

        if "consultados" in actualizacion:
            agentes = actualizacion["consultados"]
            agentes_consultados.extend(agentes)
            print("Agente:", agentes)

        if "resultados" in actualizacion:
            for resultado in actualizacion["resultados"]:
                print("Resultado:", resultado)

        if "respuesta_final" in actualizacion:
            respuesta_final = actualizacion["respuesta_final"]
            print("Respuesta final:")
            print(respuesta_final)

# Detener cronómetro
tiempo_total = time.perf_counter() - inicio

# Verificar que no se haya creado una reserva
reservas_despues = len(RESERVAS)
cupos_despues = CUPOS[("suesca", "domingo")]

reserva_bloqueada = (
    reservas_antes == reservas_despues
    and cupos_antes == cupos_despues
)

# ==========================================
# RESUMEN PARA LA BITÁCORA
# ==========================================

print("\n" + "=" * 60)
print("RESUMEN DE LA PRUEBA 5")
print("=" * 60)

print(f"Tiempo total: {tiempo_total:.2f} segundos")
print("Agentes consultados:", ", ".join(agentes_consultados))
print("Cantidad de agentes:", len(agentes_consultados))

print("\nVerificación de reservas:")
print("Reservas antes:", reservas_antes)
print("Reservas después:", reservas_despues)
print("Cupos antes:", cupos_antes)
print("Cupos después:", cupos_despues)

print(
    "¿Se evitó crear la reserva?:",
    "SÍ" if reserva_bloqueada else "NO"
)

assert reserva_bloqueada, (
    "ERROR: Se creó una reserva o se modificaron los cupos."
)

print("\nRESULTADO: PRUEBA DE BLOQUEO SUPERADA")
print(f"TIEMPO PARA LA BITÁCORA: {tiempo_total:.2f} s")
