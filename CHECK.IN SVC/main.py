from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import sqlite3
from datetime import datetime
import pandas as pd 

app = FastAPI()

# ----------------------------
# ARCHIVOS ESTÁTICOS
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# BASE DE DATOS
# ----------------------------
DB_NAME = "suarez_voley.db"

def inicializar_db():
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                edad INTEGER,
                tiempo INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                presente INTEGER DEFAULT 1
            )
        """)
        conexion.commit()

@app.on_event("startup")
def startup_event():
    inicializar_db()

# ----------------------------
# MODELOS
# ----------------------------
class Jugador(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., gt=0, le=120)
    tiempo: int = Field(..., ge=0, le=80)

# ----------------------------
# LÓGICA DB
# ----------------------------
def agregar_jugador_db(nombre, edad, tiempo):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)",
                (nombre, edad, tiempo)
            )
            conn.commit()
            return {"exito": True}
        except sqlite3.IntegrityError:
            return {"exito": False, "mensaje": "Jugador ya existe"}

def listar_jugadores_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, edad, tiempo FROM jugadores")
        filas = cur.fetchall()
        return [
            {"id": f[0], "nombre": f[1], "edad": f[2], "tiempo": f[3]}
            for f in filas
        ]

def registrar_asistencia_db(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM jugadores WHERE LOWER(nombre)=?", (nombre.lower(),))
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
        return {"exito": True}

def exportar_asistencias_excel():
    with sqlite3.connect(DB_NAME) as conn:
        query = """
            SELECT j.nombre AS Jugador, a.fecha AS Fecha, a.hora AS Hora
            FROM asistencias a
            JOIN jugadores j ON a.jugador_id = j.id
            ORDER BY a.fecha DESC, a.hora DESC
        """
        df = pd.read_sql_query(query, conn)
        df.to_excel("Reporte_SVC.xlsx", index=False)
        print("✅ Reporte 'Reporte_SVC.xlsx' generado con éxito.")

# ----------------------------
# ENDPOINTS API
# ----------------------------
@app.get("/verificar/{nombre}")
def verificar_jugador(nombre: str):
    resultado = registrar_asistencia_db(nombre)
    if resultado["exito"]:
        ahora = datetime.now().strftime("%H:%M")
        return {"existe": True, "nombre": nombre, "hora": ahora}
    else:
        return {"existe": False, "nombre": nombre, "hora": None}

@app.post("/check-in/{nombre}")
def check_in(nombre: str):
    resultado = registrar_asistencia_db(nombre)
    if not resultado["exito"]:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"mensaje": "Asistencia registrada"}

@app.post("/jugadores/", status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador: Jugador):
    res = agregar_jugador_db(jugador.nombre, jugador.edad, jugador.tiempo)
    if not res["exito"]:
        raise HTTPException(status_code=400, detail=res["mensaje"])
    return {"mensaje": "Jugador creado"}

@app.get("/jugadores/")
def listar():
    return listar_jugadores_db()

# ----------------------------
# CONSOLA
# ----------------------------
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
                print(agregar_jugador_db(nombre, edad, tiempo))
            except ValueError:
                print("Error: Edad y Tiempo deben ser números.")
        elif op == "2":
            print(listar_jugadores_db())
        elif op == "3":
            exportar_asistencias_excel()
        elif op == "4":
            print("Saliendo...")
            break

if __name__ == "__main__":
    inicializar_db()
    menu_consola()