import json

# ------------------------------
# Función para pedir números
# ------------------------------
def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Solo se permiten números")

# ------------------------------
# Cargar jugadores desde JSON
# ------------------------------
try:
    with open("jugadores.json", "r") as archivo:
        suarezvoleyclub = json.load(archivo)
except FileNotFoundError:
    suarezvoleyclub = []

# ------------------------------
# Función para agregar jugador
# ------------------------------
def agregar_jugador():
    nombre = input("Agrega nombre de jugador (0 para cancelar): ").strip()
    if nombre == "0":
        return

    # Verificar duplicado
    for j in suarezvoleyclub:
        if j["nombre"].lower() == nombre.lower():
            print(f"El jugador {nombre} ya está registrado.\n")
            return

    edad = pedir_entero("Agrega edad del jugador: ")
    tiempo = pedir_entero("Agrega tiempo jugado: ")

    jugador = {"nombre": nombre, "edad": edad, "tiempo": tiempo}
    suarezvoleyclub.append(jugador)

    print(f"\nJugador agregado: {nombre}")
    print("Mayor de edad" if edad >= 18 else "Menor de edad")
    print(f"Años jugados: {tiempo}\n")

# ------------------------------
# Función para listar jugadores
# ------------------------------
def listar_jugadores():
    if not suarezvoleyclub:
        print("No hay jugadores registrados.\n")
        return
    print("\nLista de jugadores:")
    for jugador in suarezvoleyclub:
        print(f"{jugador['nombre']} - {jugador['edad']} años")
    print("")

# ------------------------------
# Función para borrar jugador
# ------------------------------
def borrar_jugador():
    nombre_borrar = input("Ingresa el nombre del jugador a borrar: ").strip()
    for jugador in suarezvoleyclub:
        if jugador["nombre"].lower() == nombre_borrar.lower():
            suarezvoleyclub.remove(jugador)
            print(f"Jugador {nombre_borrar} eliminado del sistema.\n")
            return
    print(f"No se encontró un jugador llamado {nombre_borrar}.\n")

# ------------------------------
# Menú principal
# ------------------------------
while True:
    print("===== SUAREZ VOLEY CLUB =====")
    print("1. Agregar jugador")
    print("2. Listar jugadores")
    print("3. Borrar jugador")
    print("4. Salir")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        agregar_jugador()
    elif opcion == "2":
        listar_jugadores()
    elif opcion == "3":
        borrar_jugador()
    elif opcion == "4":
        # Guardar cambios antes de salir
        with open("jugadores.json", "w") as archivo:
            json.dump(suarezvoleyclub, archivo, indent=4)
        print("Sistema cerrado. ¡Hasta luego!")
        break
    else:
        print("Opción inválida. Intenta de nuevo.\n")


    # Guardar siempre en JSON
    with open("jugadores.json", "w") as archivo:
        json.dump(suarezvoleyclub, archivo, indent=4)

# ------------------------------
# Mostrar lista final de jugadores
# ------------------------------
print("\nLista de jugadores:")
for jugador in suarezvoleyclub:
    print(f"{jugador['nombre']} - {jugador['edad']} años, {jugador['tiempo']} años jugados")
