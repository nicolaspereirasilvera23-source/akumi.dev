import sqlite3
import pytest
from playwright.sync_api import Page, expect

DB_NAME = "../suarez_voley.db" # Ruta relativa desde la carpeta 'tests'

def test_flujo_asistencia_real(page: Page):
    nombre_test = "Akumi de Prueba"
    
    # --- PREPARACIÓN: Asegurar que el jugador existe en la DB ---
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Lo borramos si ya existe para que el test sea limpio
        cur.execute("DELETE FROM jugadores WHERE nombre = ?", (nombre_test,))
        # Lo creamos
        cur.execute("INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)", (nombre_test, 25, 10))
        conn.commit()

    # --- ACCIÓN: El Robot marca asistencia ---
    page.goto("http://127.0.0.1:8000")
    
    # Escribimos el nombre en el input
    page.get_by_placeholder("Escribí tu nombre aquí...").fill(nombre_test)
    
    # Hacemos click en CONFIRMAR
    page.get_by_role("button", name="CONFIRMAR").click()
    
    # Esperamos un segundo a que el backend guarde
    page.wait_for_timeout(1000)

    # --- VERIFICACIÓN: Consultamos la tabla 'asistencias' con un JOIN ---
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        query = """
            SELECT a.id 
            FROM asistencias a
            JOIN jugadores j ON a.jugador_id = j.id
            WHERE j.nombre = ?
        """
        cur.execute(query, (nombre_test,))
        asistencia = cur.fetchone()

    # Si asistencia no es None, ¡el test pasó!
    assert asistencia is not None, f"No se encontró registro de asistencia para {nombre_test}"
    print(f"\n✅ Golazo: {nombre_test} marcó presente y se guardó en la DB.")