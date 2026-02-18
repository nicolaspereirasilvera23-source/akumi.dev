import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_NAME = "suarez_voley.db"

def inicializar_db():
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                edad INTEGER NOT NULL CHECK(edad > 0 AND edad <= 120),
                tiempo INTEGER NOT NULL CHECK(tiempo >= 0 AND tiempo <= 80)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                presente INTEGER DEFAULT 1,
                FOREIGN KEY (jugador_id) REFERENCES jugadores(id)
            )
        """)
        conexion.commit()

def _normalizar_nombre(nombre):
    return nombre.strip()

def agregar_jugador_db(nombre, edad, tiempo):
    nombre_limpio = _normalizar_nombre(nombre)
    if not nombre_limpio:
        return {"exito": False, "mensaje": "Nombre invalido"}

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id FROM jugadores WHERE LOWER(nombre) = ?",
                (nombre_limpio.lower(),)
            )
            if cur.fetchone():
                return {"exito": False, "mensaje": "Jugador ya existe"}

            cur.execute(
                "INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)",
                (nombre_limpio, edad, tiempo)
            )
            conn.commit()
            return {"exito": True, "id": cur.lastrowid}
        except sqlite3.IntegrityError as err:
            return {"exito": False, "mensaje": f"Error de integridad: {err}"}

def listar_jugadores_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, edad, tiempo FROM jugadores ORDER BY id ASC")
        filas = cur.fetchall()
        return [
            {"id": f[0], "nombre": f[1], "edad": f[2], "tiempo": f[3]}
            for f in filas
        ]

def obtener_jugador_db(jugador_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre, edad, tiempo FROM jugadores WHERE id = ?",
            (jugador_id,)
        )
        fila = cur.fetchone()
        if not fila:
            return None
        return {"id": fila[0], "nombre": fila[1], "edad": fila[2], "tiempo": fila[3]}

def actualizar_jugador_db(jugador_id, nombre, edad, tiempo):
    nombre_limpio = _normalizar_nombre(nombre)
    if not nombre_limpio:
        return {"exito": False, "mensaje": "Nombre invalido"}

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM jugadores WHERE id = ?", (jugador_id,))
        if not cur.fetchone():
            return {"exito": False, "mensaje": "Jugador no encontrado"}

        cur.execute(
            "SELECT id FROM jugadores WHERE LOWER(nombre) = ? AND id != ?",
            (nombre_limpio.lower(), jugador_id)
        )
        if cur.fetchone():
            return {"exito": False, "mensaje": "Ya existe otro jugador con ese nombre"}

        cur.execute(
            "UPDATE jugadores SET nombre = ?, edad = ?, tiempo = ? WHERE id = ?",
            (nombre_limpio, edad, tiempo, jugador_id)
        )
        conn.commit()
        return {"exito": True}

def eliminar_jugador_db(jugador_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM jugadores WHERE id = ?", (jugador_id,))
        if not cur.fetchone():
            return {"exito": False, "mensaje": "Jugador no encontrado"}

        cur.execute("DELETE FROM asistencias WHERE jugador_id = ?", (jugador_id,))
        cur.execute("DELETE FROM jugadores WHERE id = ?", (jugador_id,))
        conn.commit()
        return {"exito": True}

def registrar_asistencia_db(nombre):
    nombre_limpio = _normalizar_nombre(nombre)
    if not nombre_limpio:
        return {"exito": False}

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre FROM jugadores WHERE LOWER(nombre)=?",
            (nombre_limpio.lower(),)
        )
        jugador = cur.fetchone()

        if not jugador:
            return {"exito": False}

        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M")

        cur.execute(
            "INSERT INTO asistencias (jugador_id, fecha, hora) VALUES (?, ?, ?)",
            (jugador[0], fecha, hora)
        )
        conn.commit()
        return {"exito": True, "nombre": jugador[1], "hora": hora}

def verificar_jugador_db(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM jugadores WHERE LOWER(nombre)=?", (nombre.strip().lower(),))
        jugador = cur.fetchone()
        if jugador:
            return {"existe": True, "nombre": jugador[1]}
        else:
            return {"existe": False, "nombre": nombre}

def exportar_asistencias_excel():
    # Ruta absoluta basada en la ubicación de este script
    ruta_excel = Path(__file__).resolve().parent / "Reporte_SVC.xlsx"
    with sqlite3.connect(DB_NAME) as conn:
        query = """
            SELECT j.nombre AS Jugador, a.fecha AS Fecha, a.hora AS Hora
            FROM asistencias a
            JOIN jugadores j ON a.jugador_id = j.id
            ORDER BY a.fecha DESC, a.hora DESC
        """
        df = pd.read_sql_query(query, conn)
        df.to_excel(ruta_excel, index=False)
        return ruta_excel

def obtener_ultimos_asistentes(limite=5):
    limite = max(1, int(limite))
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        query = """
            SELECT j.nombre, a.hora 
            FROM asistencias a
            JOIN jugadores j ON a.jugador_id = j.id
            WHERE a.fecha = ?
            ORDER BY a.id DESC
            LIMIT ?
        """
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        cur.execute(query, (fecha_hoy, limite))
        filas = cur.fetchall()
        return [{"nombre": f[0], "hora": f[1]} for f in filas]
