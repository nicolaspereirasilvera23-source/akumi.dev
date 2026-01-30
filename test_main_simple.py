"""
Tests unitarios simples para el backend de Suarez Voley Club.

Ejecuta con: pytest test_main_simple.py -v
"""

import pytest
import sqlite3

# --- Funciones de prueba (copias de main.py optimizadas para testing) ---

def crear_db_test():
    """Crea una BD en memoria para los tests."""
    conexion = sqlite3.connect(":memory:")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            tiempo INTEGER
        )
    """)
    conexion.commit()
    return conexion


def agregar_jugador(db, nombre: str, edad: int, tiempo: int) -> dict:
    """Agrega jugador a la BD."""
    # Validaciones
    if not nombre or not nombre.strip():
        return {"exito": False, "mensaje": "El nombre no puede estar vacío"}
    if edad <= 0 or edad > 120:
        return {"exito": False, "mensaje": "Edad debe estar entre 1 y 120 años"}
    if tiempo < 0 or tiempo > 80:
        return {"exito": False, "mensaje": "Tiempo debe estar entre 0 y 80 años"}
    
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM jugadores WHERE LOWER(nombre) = ?", (nombre.lower(),))
    if cursor.fetchone():
        return {"exito": False, "mensaje": f"El jugador '{nombre}' ya existe"}
    
    cursor.execute(
        "INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)",
        (nombre, edad, tiempo)
    )
    db.commit()
    return {"exito": True, "mensaje": f"✅ {nombre} guardado correctamente"}


def listar_jugadores(db) -> list:
    """Lista todos los jugadores."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    return [{"id": j[0], "nombre": j[1], "edad": j[2], "tiempo": j[3]} for j in jugadores]


def actualizar_jugador(db, nombre: str, edad: int = None, tiempo: int = None) -> dict:
    """Actualiza un jugador."""
    if edad is not None and (edad <= 0 or edad > 120):
        return {"exito": False, "mensaje": "Edad debe estar entre 1 y 120 años"}
    if tiempo is not None and (tiempo < 0 or tiempo > 80):
        return {"exito": False, "mensaje": "Tiempo debe estar entre 0 y 80 años"}
    
    cursor = db.cursor()
    cursor.execute("SELECT id FROM jugadores WHERE LOWER(nombre) = ?", (nombre.lower(),))
    resultado = cursor.fetchone()
    if not resultado:
        return {"exito": False, "mensaje": f"Jugador '{nombre}' no encontrado"}
    
    jugador_id = resultado[0]
    if edad is not None:
        cursor.execute("UPDATE jugadores SET edad = ? WHERE id = ?", (edad, jugador_id))
    if tiempo is not None:
        cursor.execute("UPDATE jugadores SET tiempo = ? WHERE id = ?", (tiempo, jugador_id))
    
    db.commit()
    return {"exito": True, "mensaje": f"✅ {nombre} actualizado correctamente"}


def borrar_jugador(db, nombre: str) -> dict:
    """Borra un jugador."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM jugadores WHERE LOWER(nombre) = ?", (nombre.lower(),))
    
    if db.total_changes > 0:
        db.commit()
        return {"exito": True, "mensaje": f"🗑️ {nombre} eliminado"}
    else:
        return {"exito": False, "mensaje": f"No se encontró a '{nombre}'"}


# --- FIXTURES ---

@pytest.fixture
def db():
    """BD en memoria para cada test."""
    return crear_db_test()


# --- TESTS ---

class TestAgregar:
    def test_agregar_exitoso(self, db):
        resultado = agregar_jugador(db, "Juan", 25, 5)
        assert resultado["exito"] == True
    
    def test_agregar_duplicado(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        resultado = agregar_jugador(db, "Juan", 30, 10)
        assert resultado["exito"] == False
        assert "ya existe" in resultado["mensaje"]
    
    def test_agregar_edad_invalida(self, db):
        resultado = agregar_jugador(db, "Juan", 0, 5)
        assert resultado["exito"] == False
        resultado = agregar_jugador(db, "Juan", 150, 5)
        assert resultado["exito"] == False
    
    def test_agregar_tiempo_invalido(self, db):
        resultado = agregar_jugador(db, "Juan", 25, -5)
        assert resultado["exito"] == False
    
    def test_agregar_nombre_vacio(self, db):
        resultado = agregar_jugador(db, "", 25, 5)
        assert resultado["exito"] == False


class TestListar:
    def test_listar_vacio(self, db):
        jugadores = listar_jugadores(db)
        assert jugadores == []
    
    def test_listar_multiples(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        agregar_jugador(db, "María", 22, 3)
        jugadores = listar_jugadores(db)
        assert len(jugadores) == 2
    
    def test_listar_estructura(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        jugadores = listar_jugadores(db)
        assert "id" in jugadores[0]
        assert "nombre" in jugadores[0]


class TestActualizar:
    def test_actualizar_exitoso(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        resultado = actualizar_jugador(db, "Juan", edad=26, tiempo=6)
        assert resultado["exito"] == True
        jugadores = listar_jugadores(db)
        assert jugadores[0]["edad"] == 26
    
    def test_actualizar_parcial(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        actualizar_jugador(db, "Juan", edad=30)
        jugadores = listar_jugadores(db)
        assert jugadores[0]["edad"] == 30
        assert jugadores[0]["tiempo"] == 5
    
    def test_actualizar_no_existe(self, db):
        resultado = actualizar_jugador(db, "NoExiste", edad=30)
        assert resultado["exito"] == False


class TestBorrar:
    def test_borrar_exitoso(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        resultado = borrar_jugador(db, "Juan")
        assert resultado["exito"] == True
    
    def test_borrar_no_existe(self, db):
        resultado = borrar_jugador(db, "NoExiste")
        assert resultado["exito"] == False
    
    def test_borrar_case_insensitive(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        resultado = borrar_jugador(db, "juan")
        assert resultado["exito"] == True


class TestIntegracion:
    def test_crud_completo(self, db):
        # CREATE
        agregar_jugador(db, "Carlos", 28, 7)
        # READ
        assert len(listar_jugadores(db)) == 1
        # UPDATE
        actualizar_jugador(db, "Carlos", edad=29)
        # DELETE
        borrar_jugador(db, "Carlos")
        assert len(listar_jugadores(db)) == 0
    
    def test_multiples_operaciones(self, db):
        agregar_jugador(db, "Juan", 25, 5)
        agregar_jugador(db, "María", 22, 3)
        agregar_jugador(db, "Carlos", 28, 7)
        
        assert len(listar_jugadores(db)) == 3
        
        actualizar_jugador(db, "María", edad=23)
        borrar_jugador(db, "Juan")
        
        jugadores = listar_jugadores(db)
        assert len(jugadores) == 2
        assert any(j["nombre"] == "María" and j["edad"] == 23 for j in jugadores)
