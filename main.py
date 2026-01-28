from fastapi import FastAPI
app=FastAPI()

import sqlite3

# --- Configuración de Base de Datos ---
DB_NAME = "suarez_voley.db"

def inicializar_db():
    """Crea el archivo de base de datos y la tabla si no existen."""
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        # id: número único para cada jugador (se pone solo)
        # nombre: texto, edad: número, tiempo: número
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER,
                tiempo INTEGER
            )
        ''')
        conexion.commit()

# --- Funciones de Validación ---
def pedir_entero(mensaje):
    """Asegura que el usuario ingrese un número válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("❌ Error: Solo se permiten números.")

# --- Acciones del Sistema ---

def agregar_jugador():
    nombre = input("Nombre del jugador (0 para cancelar): ").strip()
    if nombre == "0": return

    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        
        # 1. Verificar si ya existe (para no duplicar)
        cursor.execute("SELECT * FROM jugadores WHERE LOWER(nombre) = ?", (nombre.lower(),))
        if cursor.fetchone():
            print(f"⚠️ El jugador '{nombre}' ya está en la base de datos.\n")
            return

        # 2. Pedir el resto de los datos
        edad = pedir_entero("Edad: ")
        tiempo = pedir_entero("Tiempo jugado (años): ")

        # 3. Guardar en SQL
        cursor.execute("INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)", 
                       (nombre, edad, tiempo))
        conexion.commit()
        print(f"✅ {nombre} guardado correctamente.")

def listar_jugadores():
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugadores")
        jugadores = cursor.fetchall() # Trae todos los datos como una lista de tuplas
        
        if not jugadores:
            print("\n📭 No hay jugadores registrados en la base de datos.")
            return

        print("\n--- LISTA DE SOCIOS (DB) ---")
        for j in jugadores:
            # j[1] es nombre, j[2] es edad, j[3] es tiempo
            print(f"ID: {j[0]} | 👤 {j[1]} | {j[2]} años | Exp: {j[3]} años")
        print("----------------------------\n")

def borrar_jugador():
    nombre_borrar = input("Nombre del jugador a eliminar: ").strip()
    
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM jugadores WHERE LOWER(nombre) = ?", (nombre_borrar.lower(),))
        
        # total_changes nos dice si SQL realmente borró algo o no
        if conexion.total_changes > 0:
            conexion.commit()
            print(f"🗑️ El jugador '{nombre_borrar}' ha sido eliminado.")
        else:
            print(f"❌ No se encontró a nadie con el nombre '{nombre_borrar}'.")

# --- Menú Principal ---
def main():
    # Paso 1: Asegurarnos de que la DB exista al arrancar
    inicializar_db()
    
    while True:
        print("\n🏐 SUAREZ VOLEY CLUB - GESTIÓN BACKEND")
        print("1. Agregar jugador")
        print("2. Listar jugadores")
        print("3. Borrar jugador")
        print("4. Salir")
        
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            agregar_jugador()
        elif opcion == "2":
            listar_jugadores()
        elif opcion == "3":
            borrar_jugador()
        elif opcion == "4":
            print("Cerrando conexión... ¡Nos vemos en la cancha! 👋")
            break
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")

# Punto de entrada del script
if __name__ == "__main__":
    main()

    # TODO: eliminar menú por consola
# TODO: convertir estas funciones en lógica reutilizable
# TODO: exponer endpoints con FastAPI
