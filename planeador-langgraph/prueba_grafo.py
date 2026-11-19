
from grafo import grafo


estado_inicial = {
    "consulta": (
        "Somos 4 personas y tenemos un presupuesto de "
        "350000 pesos para ir a Zipaquirá. "
        "¿Nos alcanza el dinero?"
    ),
    "resultados": [],
    "consultados": [],
    "siguiente": "",
    "respuesta_final": "",
}


resultado = grafo.invoke(estado_inicial)

print("\nAGENTES CONSULTADOS:")
print(resultado["consultados"])

print("\nRESULTADOS DE LOS ESPECIALISTAS:")
for item in resultado["resultados"]:
    print(item)

print("\nRESPUESTA FINAL:")
print(resultado["respuesta_final"])
