# hacemos una lista vacía para guardar los jugadores
suarezvoleyclub = []

while True:
    nombre = input("Agrega nombre de jugador: ")

    if nombre == "0":
        print("Sistema finalizado")
        break

    try:
        edad = int(input("Agrega edad del jugador: "))
    except ValueError:
        print("Solo agregue numeros")
        continue

    try:
        tiempo = int(input("Agrega tiempo jugado: "))
    except ValueError:
        print("Solo agregue numeros")
        continue

    # se agrega jugador (ESTO VA DENTRO DEL WHILE)
    jugador = {
        "nombre": nombre,
        "edad": edad,
        "tiempo": tiempo}

    suarezvoleyclub.append(jugador)
    print("Jugador agregado al sistema")

    print("Hola jugador", nombre)

    if edad >= 18:
        print("El jugador es mayor de edad")
    else:
        print("El jugador es menor de edad")

    print("El jugador tiene", tiempo, "años jugado en el equipo")

# fuera del while
print("\nLista de jugadores:")
for jugador in suarezvoleyclub:
    print(jugador["nombre"], "-", jugador["edad"], "años")