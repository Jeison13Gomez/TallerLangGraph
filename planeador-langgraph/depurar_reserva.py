
from grafo import extraer_solicitud_reserva

consulta = (
    "Queremos ir a Suesca el sábado, somos 3 personas "
    "y tenemos un presupuesto de 250000 pesos. "
    "Si hay poca probabilidad de lluvia y el dinero "
    "alcanza, realiza una reserva a nombre de Laura."
)

print("=" * 60)
print("DEPURACIÓN DE EXTRACCIÓN DE RESERVAS")
print("=" * 60)

solicitud = extraer_solicitud_reserva(consulta)

print("\nDatos extraídos por Qwen:")
print(solicitud.model_dump_json(indent=2))

print("\nVerificación individual:")
print("¿Quiere reservar?:", solicitud.quiere_reservar)
print("Destino:", solicitud.destino)
print("Día:", solicitud.dia)
print("Personas:", solicitud.personas)
print("Nombre:", solicitud.nombre)
print("Presupuesto:", solicitud.presupuesto)

faltantes = [
    campo
    for campo in [
        "destino",
        "dia",
        "personas",
        "nombre",
        "presupuesto",
    ]
    if getattr(solicitud, campo) is None
]

print("\nCampos faltantes:", faltantes)

if faltantes:
    print("RESULTADO: extracción incompleta.")
else:
    print("RESULTADO: extracción completa.")
