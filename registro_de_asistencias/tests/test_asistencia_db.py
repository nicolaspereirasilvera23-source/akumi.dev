import sqlite3
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from database import inicializar_db

DB_NAME = str(Path(__file__).resolve().parent.parent / "suarez_voley.db")


@pytest.mark.e2e
def test_flujo_asistencia_real(page: Page):
    inicializar_db()
    nombre_test = "Akumi de Prueba"
    codigo_test = "2468"
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # --- PREPARACION: Asegurar que el jugador existe en la DB ---
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM asistencias WHERE jugador_id IN (SELECT id FROM jugadores WHERE codigo = ?)",
            (codigo_test,),
        )
        cur.execute("DELETE FROM jugadores WHERE codigo = ?", (codigo_test,))
        cur.execute("DELETE FROM jugadores WHERE LOWER(nombre) = ?", (nombre_test.lower(),))
        cur.execute(
            "INSERT INTO jugadores (nombre, edad, tiempo, codigo) VALUES (?, ?, ?, ?)",
            (nombre_test, 25, 10, codigo_test),
        )
        conn.commit()

    # --- ACCION: El usuario marca asistencia ---
    page.goto("http://127.0.0.1:8000")
    page.get_by_test_id("codigo-input").fill(codigo_test)
    page.get_by_test_id("confirmar-btn").click()

    # Confirmamos feedback visual de exito
    expect(page.get_by_test_id("toast-success")).to_be_visible(timeout=5000)

    # --- VERIFICACION: Se guarda en DB ---
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        query = """
            SELECT COUNT(*)
            FROM asistencias a
            JOIN jugadores j ON a.jugador_id = j.id
            WHERE j.codigo = ? AND a.fecha = ?
        """
        cur.execute(query, (codigo_test, fecha_hoy))
        total = cur.fetchone()[0]

    assert total >= 1, f"No se encontro registro de asistencia para codigo {codigo_test}"
