
from grafo import crear_plan

pruebas = [
    (
        "Prueba 1",
        "¿Cómo estará el clima en Guatavita el domingo?",
        {"clima"}
    ),
    (
        "Prueba 2",
        "¿Cuánto cuesta ir a Zipaquirá con 4 personas "
        "si tenemos 350000 pesos?",
        {"presupuesto"}
    ),
    (
        "Prueba 3",
        "Queremos ir a Villa de Leyva el sábado, "
        "somos 2 personas. Consulta el clima y el costo.",
        {"clima", "presupuesto"}
    ),
    (
        "Prueba 4",
        "Queremos ir a Suesca el sábado, somos 3 personas "
        "y tenemos un presupuesto de 250000 pesos. "
        "Si hay poca probabilidad de lluvia y el dinero "
        "alcanza, realiza una reserva a nombre de Laura.",
        {"clima", "presupuesto", "reservas"}
    ),
    (
        "Prueba 5",
        "Somos 3 personas y tenemos un presupuesto de "
        "150000 pesos. Queremos reservar Suesca el domingo "
        "a nombre de Laura, solo si alcanza el dinero.",
        {"presupuesto", "reservas"}
    ),
    (
        "Prueba 6",
        "¿Quién ganó el Mundial de fútbol de 2022?",
        set()
    ),
]

print("=" * 60)
print("VALIDACIÓN DEL PLANIFICADOR")
print("=" * 60)

aprobadas = 0

for nombre, consulta, esperados in pruebas:
    plan = crear_plan(consulta)

    agentes_correctos = set(plan) == esperados
    sin_repeticiones = len(plan) == len(set(plan))
    reservas_al_final = (
        "reservas" not in plan
        or plan[-1] == "reservas"
    )

    correcta = (
        agentes_correctos
        and sin_repeticiones
        and reservas_al_final
    )

    print(f"\n{nombre}")
    print("Plan generado:", plan)
    print("Agentes esperados:", sorted(esperados))
    print("Resultado:", "CORRECTO" if correcta else "REVISAR")

    if correcta:
        aprobadas += 1

print("\n" + "=" * 60)
print(f"PLANES CORRECTOS: {aprobadas}/6")
print("=" * 60)
