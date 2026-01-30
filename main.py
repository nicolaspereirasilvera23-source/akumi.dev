from fastapi import FastAPI
import sqlite3

app = FastAPI()

# --- Configuración de Base de Datos ---
DB_NAME = "suarez_voley.db"

def inicializar_db():
    """Crea el archivo de base de datos y la tabla si no existen."""
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER,
                tiempo INTEGER
            )
        """)
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
    if nombre == "0":
        return

    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()

        # Verificar si ya existe
        cursor.execute(
            "SELECT 1 FROM jugadores WHERE LOWER(nombre) = ?",
            (nombre.lower(),)
        )
        if cursor.fetchone():
            print(f"⚠️ El jugador '{nombre}' ya está en la base de datos.\n")
            return

        edad = pedir_entero("Edad: ")
        tiempo = pedir_entero("Tiempo jugado (años): ")

        cursor.execute(
            "INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)",
            (nombre, edad, tiempo)
        )
        conexion.commit()
        print(f"✅ {nombre} guardado correctamente.")

def listar_jugadores():
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugadores")
        jugadores = cursor.fetchall()

        if not jugadores:
            print("\n📭 No hay jugadores registrados en la base de datos.")
            return

        print("\n--- LISTA DE SOCIOS (DB) ---")
        for j in jugadores:
            print(f"ID: {j[0]} | 👤 {j[1]} | {j[2]} años | Exp: {j[3]} años")
        print("----------------------------\n")

def borrar_jugador():
    nombre_borrar = input("Nombre del jugador a eliminar: ").strip()

    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM jugadores WHERE LOWER(nombre) = ?",
            (nombre_borrar.lower(),)
        )

        if conexion.total_changes > 0:
            conexion.commit()
            print(f"🗑️ El jugador '{nombre_borrar}' ha sido eliminado.")
        else:
            print(f"❌ No se encontró a nadie con el nombre '{nombre_borrar}'.")

# --- Menú Principal ---
def main():
    inicializar_db()

    running = True  # controla el ciclo del programa

    while running:
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
            running = False
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")

# Punto de entrada del script
if __name__ == "__main__":
    main()
