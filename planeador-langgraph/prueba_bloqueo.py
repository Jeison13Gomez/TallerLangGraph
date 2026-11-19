
from grafo import ejecutar_reserva_autorizada
from datos import RESERVAS, CUPOS

reservas_antes = len(RESERVAS)
cupos_antes = CUPOS[("suesca", "domingo")]

resultado = ejecutar_reserva_autorizada(
    destino="suesca",
    dia="domingo",
    personas=3,
    nombre="Laura",
    presupuesto=150000
)

reservas_despues = len(RESERVAS)
cupos_despues = CUPOS[("suesca", "domingo")]

print("RESULTADO:")
print(resultado)

print("\nVERIFICACIONES:")
print("Reservas antes:", reservas_antes)
print("Reservas después:", reservas_despues)
print("Cupos antes:", cupos_antes)
print("Cupos después:", cupos_despues)

assert reservas_antes == reservas_despues, (
    "ERROR: Se creó una reserva no autorizada."
)

assert cupos_antes == cupos_despues, (
    "ERROR: Se modificaron los cupos."
)

print("\nPRUEBA SUPERADA: no se creó ninguna reserva.")
