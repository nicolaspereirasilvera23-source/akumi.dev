from database import (
    agregar_jugador_db,
    exportar_asistencias_excel,
    inicializar_db,
    listar_jugadores_db,
)


def menu_consola():
    while True:
        print("\nSUAREZ VOLEY CLUB")
        print("1. Agregar jugador")
        print("2. Listar jugadores")
        print("3. Generar reporte Excel")
        print("4. Salir")
        op = input("Opcion: ")

        if op == "1":
            try:
                nombre = input("Nombre: ")
                edad = int(input("Edad: "))
                tiempo = int(input("Tiempo: "))
                res = agregar_jugador_db(nombre, edad, tiempo)
                if res["exito"]:
                    print(f"Jugador agregado con exito. Codigo: {res.get('codigo', '----')}")
                else:
                    print(f"Error: {res.get('mensaje', 'Error desconocido')}")
            except ValueError:
                print("Error: Edad y tiempo deben ser numeros.")
        elif op == "2":
            jugadores = listar_jugadores_db()
            print("\nLISTADO DE JUGADORES:")
            for j in jugadores:
                print(
                    f"- {j['nombre']} (Edad: {j['edad']}, Tiempo: {j['tiempo']} meses, Codigo: {j['codigo']})"
                )
        elif op == "3":
            ruta = exportar_asistencias_excel()
            print(f"Reporte '{ruta}' generado con exito.")
        elif op == "4":
            print("Saliendo...")
            break


if __name__ == "__main__":
    inicializar_db()
    menu_consola()
