from database import (
    inicializar_db,
    agregar_jugador_db,
    listar_jugadores_db,
    exportar_asistencias_excel
)

def menu_consola():
    while True:
        print("\n🏐 SUAREZ VOLEY CLUB")
        print("1. Agregar jugador")
        print("2. Listar jugadores")
        print("3. Generar Reporte Excel")
        print("4. Salir")
        op = input("Opción: ")

        if op == "1":
            try:
                nombre = input("Nombre: ")
                edad = int(input("Edad: "))
                tiempo = int(input("Tiempo: "))
                res = agregar_jugador_db(nombre, edad, tiempo)
                if res["exito"]:
                    print("✅ Jugador agregado con éxito.")
                else:
                    print(f"❌ Error: {res.get('mensaje', 'Error desconocido')}")
            except ValueError:
                print("Error: Edad y Tiempo deben ser números.")
        elif op == "2":
            jugadores = listar_jugadores_db()
            print("\n📋 LISTADO DE JUGADORES:")
            for j in jugadores:
                print(f"- {j['nombre']} (Edad: {j['edad']}, Tiempo: {j['tiempo']} meses)")
        elif op == "3":
            ruta = exportar_asistencias_excel()
            print(f"✅ Reporte '{ruta}' generado con éxito.")
        elif op == "4":
            print("Saliendo...")
            break

if __name__ == "__main__":
    inicializar_db()
    menu_consola()
