from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from database import (
    agregar_jugador_db,
    actualizar_jugador_db,
    eliminar_jugador_db,
    inicializar_db,
    listar_jugadores_db,
    obtener_jugador_db,
    obtener_ultimos_asistentes,
    registrar_asistencia_db,
    verificar_jugador_db,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_db()
    yield


app = FastAPI(lifespan=lifespan)

# ----------------------------
# ARCHIVOS ESTATICOS
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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# MODELOS
# ----------------------------
class Jugador(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., gt=0, le=120)
    tiempo: int = Field(..., ge=0, le=80)


class CheckInRequest(BaseModel):
    codigo: str = Field(..., pattern=r"^\d{4}$")


# ----------------------------
# ENDPOINTS API
# ----------------------------
@app.get("/verificar/{codigo}")
def verificar_jugador(codigo: str):
    """Verifica si un jugador existe por codigo de 4 digitos."""
    try:
        return verificar_jugador_db(codigo)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {err}")


@app.get("/asistencias/recientes")
def obtener_recientes():
    """Devuelve los ultimos asistentes del dia."""
    try:
        return obtener_ultimos_asistentes()
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recientes: {err}")


@app.post("/check-in")
def check_in(request: CheckInRequest):
    """Registra la asistencia de un jugador usando su codigo."""
    try:
        resultado = registrar_asistencia_db(request.codigo)
        if not resultado["exito"]:
            raise HTTPException(status_code=404, detail="Codigo no encontrado")
        return {
            "mensaje": "Asistencia registrada",
            "nombre": resultado["nombre"],
            "hora": resultado["hora"],
            "codigo": resultado["codigo"],
        }
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=f"Error interno al registrar asistencia: {err}")


@app.post("/jugadores/", status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador: Jugador):
    try:
        res = agregar_jugador_db(jugador.nombre, jugador.edad, jugador.tiempo)
        if not res["exito"]:
            raise HTTPException(status_code=400, detail=res["mensaje"])
        return {
            "mensaje": "Jugador creado",
            "id": res.get("id"),
            "codigo": res.get("codigo"),
        }
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=f"Error al crear jugador: {err}")


@app.get("/jugadores/")
def listar_jugadores():
    try:
        return listar_jugadores_db()
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al listar jugadores: {err}")


@app.get("/jugadores/{jugador_id}")
def obtener_jugador(jugador_id: int):
    try:
        jugador = obtener_jugador_db(jugador_id)
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return jugador
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=f"Error al obtener jugador: {err}")


@app.put("/jugadores/{jugador_id}")
def actualizar_jugador(jugador_id: int, jugador: Jugador):
    try:
        res = actualizar_jugador_db(jugador_id, jugador.nombre, jugador.edad, jugador.tiempo)
        if not res["exito"]:
            if res["mensaje"] == "Jugador no encontrado":
                raise HTTPException(status_code=404, detail=res["mensaje"])
            raise HTTPException(status_code=400, detail=res["mensaje"])
        return {"mensaje": "Jugador actualizado"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=f"Error al actualizar jugador: {err}")


@app.delete("/jugadores/{jugador_id}")
def eliminar_jugador(jugador_id: int):
    try:
        res = eliminar_jugador_db(jugador_id)
        if not res["exito"]:
            raise HTTPException(status_code=404, detail=res["mensaje"])
        return {"mensaje": "Jugador eliminado"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=f"Error al eliminar jugador: {err}")
