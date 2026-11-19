
import time
from grafo import grafo

PRUEBAS = [
    {
        "numero": 1,
        "pregunta": "¿Cómo estará el clima en Guatavita el domingo?",
        "esperados": ["clima"],
    },
    {
        "numero": 2,
        "pregunta": (
            "Somos 4 personas y tenemos un presupuesto de "
            "350000 pesos para ir a Zipaquirá. "
            "¿Nos alcanza el dinero?"
        ),
        "esperados": ["presupuesto"],
    },
    {
        "numero": 3,
        "pregunta": (
            "¿Cómo estará el clima en Villa de Leyva el sábado "
            "y cuánto cuesta ir para 2 personas?"
        ),
        "esperados": ["clima", "presupuesto"],
    },
]


def ejecutar_prueba(prueba):
    estado_inicial = {
        "consulta": prueba["pregunta"],
        "resultados": [],
        "consultados": [],
        "siguiente": "",
        "respuesta_final": "",
    }

    inicio = time.perf_counter()

    try:
        resultado = grafo.invoke(estado_inicial)
        tiempo = time.perf_counter() - inicio

        consultados = resultado["consultados"]

        print(f"\n{'=' * 55}")
        print(f"PRUEBA {prueba['numero']}")
        print(f"{'=' * 55}")

        print(f"Pregunta: {prueba['pregunta']}")
        print(f"Agentes esperados: {prueba['esperados']}")
        print(f"Agentes consultados: {consultados}")
        print(f"Tiempo total: {tiempo:.2f} segundos")

        print("\nRESULTADOS:")
        for item in resultado["resultados"]:
            print(f"- {item}")

        print("\nRESPUESTA FINAL:")
        print(resultado["respuesta_final"])

        if set(consultados) == set(prueba["esperados"]):
            print("\nEnrutamiento: CORRECTO")
        else:
            print("\nEnrutamiento: REVISAR")

    except Exception as error:
        tiempo = time.perf_counter() - inicio
        print(f"\nError en prueba {prueba['numero']}: {error}")
        print(f"Tiempo hasta el error: {tiempo:.2f} segundos")


if __name__ == "__main__":
    for prueba in PRUEBAS:
        ejecutar_prueba(prueba)
