

import sys

from grafo import grafo


def main():
    if "--grafo" in sys.argv[1:]:
        print(grafo.get_graph().draw_mermaid())
        return

    print("=== PLANEADOR MULTIAGENTE ===")
    print("Escribe 'salir' para finalizar.\n")

    while True:
        consulta = input("Tu consulta: ").strip()

        if consulta.lower() in ("salir", "exit"):
            print("Programa finalizado.")
            break

        if not consulta:
            continue

        estado_inicial = {
            "consulta": consulta,
            "resultados": [],
            "consultados": []
        }

        try:
            resultado = grafo.invoke(estado_inicial)

            print("\nAgentes consultados:")
            print(resultado.get("consultados", []))

            print("\nRespuesta:")
            print(resultado.get("respuesta_final", ""))

        except Exception as error:
            print(f"\nError al procesar la consulta: {error}")

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
