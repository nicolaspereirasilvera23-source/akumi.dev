"""
Tests unitarios para el backend de Suarez Voley Club.

Ejecuta con: pytest test_main.py -v
"""

import pytest
import sqlite3
import sys
from unittest.mock import patch

# --- Crear BD en memoria para tests ---

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


def agregar_jugador_test(conexion, nombre: str, edad: int, tiempo: int):
    """Agrega jugador directamente a la BD de test."""
    cursor = conexion.cursor()
    
    # Validaciones
    if not nombre or not nombre.strip():
        return {"exito": False, "mensaje": "El nombre no puede estar vacío"}
    
    if edad <= 0 or edad > 120:
        return {"exito": False, "mensaje": "Edad debe estar entre 1 y 120 años"}
    
    if tiempo < 0 or tiempo > 80:
        return {"exito": False, "mensaje": "Tiempo debe estar entre 0 y 80 años"}
    
    # Verificar si ya existe
    cursor.execute(
        "SELECT 1 FROM jugadores WHERE LOWER(nombre) = ?",
        (nombre.lower(),)
    )
    if cursor.fetchone():
        return {"exito": False, "mensaje": f"El jugador '{nombre}' ya existe"}

    # Guardar
    cursor.execute(
        "INSERT INTO jugadores (nombre, edad, tiempo) VALUES (?, ?, ?)",
        (nombre, edad, tiempo)
    )
    conexion.commit()
    return {"exito": True, "mensaje": f"✅ {nombre} guardado correctamente"}


def listar_jugadores_test(conexion):
    """Lista jugadores de la BD de test."""
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    return [{"id": j[0], "nombre": j[1], "edad": j[2], "tiempo": j[3]} for j in jugadores]


def borrar_jugador_test(conexion, nombre: str):
    """Borra jugador de la BD de test."""
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM jugadores WHERE LOWER(nombre) = ?",
        (nombre.lower(),)
    )
    
    if conexion.total_changes > 0:
        conexion.commit()
        return {"exito": True, "mensaje": f"🗑️ {nombre} eliminado"}
    else:
        return {"exito": False, "mensaje": f"No se encontró a '{nombre}'"}


def actualizar_jugador_test(conexion, nombre: str, edad: int = None, tiempo: int = None):
    """Actualiza jugador en la BD de test."""
    cursor = conexion.cursor()
    
    # Validaciones
    if edad is not None and (edad <= 0 or edad > 120):
        return {"exito": False, "mensaje": "Edad debe estar entre 1 y 120 años"}
    
    if tiempo is not None and (tiempo < 0 or tiempo > 80):
        return {"exito": False, "mensaje": "Tiempo debe estar entre 0 y 80 años"}
    
    # Verificar que el jugador existe
    cursor.execute(
        "SELECT id FROM jugadores WHERE LOWER(nombre) = ?",
        (nombre.lower(),)
    )
    resultado = cursor.fetchone()
    if not resultado:
        return {"exito": False, "mensaje": f"Jugador '{nombre}' no encontrado"}
    
    jugador_id = resultado[0]
    
    # Actualizar
    if edad is not None:
        cursor.execute("UPDATE jugadores SET edad = ? WHERE id = ?", (edad, jugador_id))
    if tiempo is not None:
        cursor.execute("UPDATE jugadores SET tiempo = ? WHERE id = ?", (tiempo, jugador_id))
    
    conexion.commit()
    return {"exito": True, "mensaje": f"✅ {nombre} actualizado correctamente"}


# --- FIXTURES ---

@pytest.fixture
def db():
    """Proporciona una BD en memoria para cada test."""
    return crear_db_test()


# --- TESTS para AGREGAR ---

def test_agregar_jugador_exitoso(db):
    """Verifica que se agrega un jugador correctamente."""
    resultado = agregar_jugador_test(db, "Juan", 25, 5)
    assert resultado["exito"] == True
    assert "guardado" in resultado["mensaje"]


def test_agregar_jugador_duplicado(db):
    """Verifica que no permite agregar jugador duplicado."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = agregar_jugador_test(db, "Juan", 30, 10)
    assert resultado["exito"] == False
    assert "ya existe" in resultado["mensaje"]


def test_agregar_jugador_edad_invalida(db):
    """Verifica que no permite edades inválidas."""
    resultado = agregar_jugador_test(db, "Juan", 0, 5)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]
    
    resultado = agregar_jugador_test(db, "Juan", 150, 5)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]


def test_agregar_jugador_tiempo_invalido(db):
    """Verifica que no permite tiempo inválido."""
    resultado = agregar_jugador_test(db, "Juan", 25, -5)
    assert resultado["exito"] == False
    assert "Tiempo" in resultado["mensaje"]
    
    resultado = agregar_jugador_test(db, "Juan", 25, 100)
    assert resultado["exito"] == False
    assert "Tiempo" in resultado["mensaje"]


def test_agregar_jugador_nombre_vacio(db):
    """Verifica que no permite nombres vacíos."""
    resultado = agregar_jugador_test(db, "", 25, 5)
    assert resultado["exito"] == False
    assert "nombre" in resultado["mensaje"].lower()


# --- TESTS para LISTAR ---

def test_listar_jugadores_vacio(db):
    """Verifica que lista está vacía al inicio."""
    jugadores = listar_jugadores_test(db)
    assert jugadores == []


def test_listar_jugadores_multiples(db):
    """Verifica que lista múltiples jugadores."""
    agregar_jugador_test(db, "Juan", 25, 5)
    agregar_jugador_test(db, "María", 22, 3)
    
    jugadores = listar_jugadores_test(db)
    assert len(jugadores) == 2
    assert jugadores[0]["nombre"] == "Juan"
    assert jugadores[1]["nombre"] == "María"


def test_listar_estructura_datos(db):
    """Verifica que los datos tienen la estructura correcta."""
    agregar_jugador_test(db, "Juan", 25, 5)
    jugadores = listar_jugadores_test(db)
    
    assert "id" in jugadores[0]
    assert "nombre" in jugadores[0]
    assert "edad" in jugadores[0]
    assert "tiempo" in jugadores[0]


# --- TESTS para ACTUALIZAR ---

def test_actualizar_jugador_exitoso(db):
    """Verifica que actualiza un jugador correctamente."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = actualizar_jugador_test(db, "Juan", edad=26, tiempo=6)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_test(db)
    assert jugadores[0]["edad"] == 26
    assert jugadores[0]["tiempo"] == 6


def test_actualizar_jugador_parcial(db):
    """Verifica que actualiza solo campos especificados."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = actualizar_jugador_test(db, "Juan", edad=30)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_test(db)
    assert jugadores[0]["edad"] == 30
    assert jugadores[0]["tiempo"] == 5  # No cambió


def test_actualizar_jugador_no_existe(db):
    """Verifica que no puede actualizar jugador inexistente."""
    resultado = actualizar_jugador_test(db, "NoExiste", edad=30)
    assert resultado["exito"] == False
    assert "no encontrado" in resultado["mensaje"].lower()


def test_actualizar_edad_invalida(db):
    """Verifica que no permite edades inválidas en actualización."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = actualizar_jugador_test(db, "Juan", edad=150)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]


# --- TESTS para BORRAR ---

def test_borrar_jugador_exitoso(db):
    """Verifica que borra un jugador correctamente."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = borrar_jugador_test(db, "Juan")
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_test(db)
    assert len(jugadores) == 0


def test_borrar_jugador_no_existe(db):
    """Verifica que no puede borrar jugador inexistente."""
    resultado = borrar_jugador_test(db, "NoExiste")
    assert resultado["exito"] == False
    assert "no se encontró" in resultado["mensaje"].lower()


def test_borrar_case_insensitive(db):
    """Verifica que borrar es insensible a mayúsculas."""
    agregar_jugador_test(db, "Juan", 25, 5)
    resultado = borrar_jugador_test(db, "juan")  # minúsculas
    assert resultado["exito"] == True


# --- TESTS INTEGRACIÓN ---

def test_flujo_completo_crud(db):
    """Test que verifica el flujo completo CRUD."""
    # CREATE
    resultado = agregar_jugador_test(db, "Carlos", 28, 7)
    assert resultado["exito"] == True
    
    # READ
    jugadores = listar_jugadores_test(db)
    assert len(jugadores) == 1
    assert jugadores[0]["nombre"] == "Carlos"
    
    # UPDATE
    resultado = actualizar_jugador_test(db, "Carlos", edad=29, tiempo=8)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_test(db)
    assert jugadores[0]["edad"] == 29
    
    # DELETE
    resultado = borrar_jugador_test(db, "Carlos")
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_test(db)
    assert len(jugadores) == 0


def test_multiples_jugadores_operaciones(db):
    """Test con múltiples jugadores."""
    # Agregar 3
    agregar_jugador_test(db, "Juan", 25, 5)
    agregar_jugador_test(db, "María", 22, 3)
    agregar_jugador_test(db, "Carlos", 28, 7)
    
    assert len(listar_jugadores_test(db)) == 3
    
    # Actualizar 1
    actualizar_jugador_test(db, "María", edad=23)
    
    # Borrar 1
    borrar_jugador_test(db, "Juan")
    
    jugadores = listar_jugadores_test(db)
    assert len(jugadores) == 2
    assert any(j["nombre"] == "María" and j["edad"] == 23 for j in jugadores)
    assert not any(j["nombre"] == "Juan" for j in jugadores)



# --- TESTS para AGREGAR ---

def test_agregar_jugador_exitoso():
    """Verifica que se agrega un jugador correctamente."""
    resultado = agregar_jugador_db("Juan", 25, 5)
    assert resultado["exito"] == True
    assert "guardado" in resultado["mensaje"]


def test_agregar_jugador_duplicado():
    """Verifica que no permite agregar jugador duplicado."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = agregar_jugador_db("Juan", 30, 10)
    assert resultado["exito"] == False
    assert "ya existe" in resultado["mensaje"]


def test_agregar_jugador_edad_invalida():
    """Verifica que no permite edades inválidas."""
    resultado = agregar_jugador_db("Juan", 0, 5)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]
    
    resultado = agregar_jugador_db("Juan", 150, 5)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]


def test_agregar_jugador_tiempo_invalido():
    """Verifica que no permite tiempo inválido."""
    resultado = agregar_jugador_db("Juan", 25, -5)
    assert resultado["exito"] == False
    assert "Tiempo" in resultado["mensaje"]
    
    resultado = agregar_jugador_db("Juan", 25, 100)
    assert resultado["exito"] == False
    assert "Tiempo" in resultado["mensaje"]


def test_agregar_jugador_nombre_vacio():
    """Verifica que no permite nombres vacíos."""
    resultado = agregar_jugador_db("", 25, 5)
    assert resultado["exito"] == False
    assert "nombre" in resultado["mensaje"].lower()


# --- TESTS para LISTAR ---

def test_listar_jugadores_vacio():
    """Verifica que lista está vacía al inicio."""
    jugadores = listar_jugadores_db()
    assert jugadores == []


def test_listar_jugadores_multiples():
    """Verifica que lista múltiples jugadores."""
    agregar_jugador_db("Juan", 25, 5)
    agregar_jugador_db("María", 22, 3)
    
    jugadores = listar_jugadores_db()
    assert len(jugadores) == 2
    assert jugadores[0]["nombre"] == "Juan"
    assert jugadores[1]["nombre"] == "María"


def test_listar_estructura_datos():
    """Verifica que los datos tienen la estructura correcta."""
    agregar_jugador_db("Juan", 25, 5)
    jugadores = listar_jugadores_db()
    
    assert "id" in jugadores[0]
    assert "nombre" in jugadores[0]
    assert "edad" in jugadores[0]
    assert "tiempo" in jugadores[0]


# --- TESTS para ACTUALIZAR ---

def test_actualizar_jugador_exitoso():
    """Verifica que actualiza un jugador correctamente."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = actualizar_jugador_db("Juan", edad=26, tiempo=6)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_db()
    assert jugadores[0]["edad"] == 26
    assert jugadores[0]["tiempo"] == 6


def test_actualizar_jugador_parcial():
    """Verifica que actualiza solo campos especificados."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = actualizar_jugador_db("Juan", edad=30)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_db()
    assert jugadores[0]["edad"] == 30
    assert jugadores[0]["tiempo"] == 5  # No cambió


def test_actualizar_jugador_no_existe():
    """Verifica que no puede actualizar jugador inexistente."""
    resultado = actualizar_jugador_db("NoExiste", edad=30)
    assert resultado["exito"] == False
    assert "no encontrado" in resultado["mensaje"].lower()


def test_actualizar_edad_invalida():
    """Verifica que no permite edades inválidas en actualización."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = actualizar_jugador_db("Juan", edad=150)
    assert resultado["exito"] == False
    assert "Edad" in resultado["mensaje"]


# --- TESTS para BORRAR ---

def test_borrar_jugador_exitoso():
    """Verifica que borra un jugador correctamente."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = borrar_jugador_db("Juan")
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_db()
    assert len(jugadores) == 0


def test_borrar_jugador_no_existe():
    """Verifica que no puede borrar jugador inexistente."""
    resultado = borrar_jugador_db("NoExiste")
    assert resultado["exito"] == False
    assert "no encontrado" in resultado["mensaje"].lower()


def test_borrar_case_insensitive():
    """Verifica que borrar es insensible a mayúsculas."""
    agregar_jugador_db("Juan", 25, 5)
    resultado = borrar_jugador_db("juan")  # minúsculas
    assert resultado["exito"] == True


# --- TESTS INTEGRACIÓN ---

def test_flujo_completo_crud():
    """Test que verifica el flujo completo CRUD."""
    # CREATE
    resultado = agregar_jugador_db("Carlos", 28, 7)
    assert resultado["exito"] == True
    
    # READ
    jugadores = listar_jugadores_db()
    assert len(jugadores) == 1
    assert jugadores[0]["nombre"] == "Carlos"
    
    # UPDATE
    resultado = actualizar_jugador_db("Carlos", edad=29, tiempo=8)
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_db()
    assert jugadores[0]["edad"] == 29
    
    # DELETE
    resultado = borrar_jugador_db("Carlos")
    assert resultado["exito"] == True
    
    jugadores = listar_jugadores_db()
    assert len(jugadores) == 0


def test_multiples_jugadores_operaciones():
    """Test con múltiples jugadores."""
    # Agregar 3
    agregar_jugador_db("Juan", 25, 5)
    agregar_jugador_db("María", 22, 3)
    agregar_jugador_db("Carlos", 28, 7)
    
    assert len(listar_jugadores_db()) == 3
    
    # Actualizar 1
    actualizar_jugador_db("María", edad=23)
    
    # Borrar 1
    borrar_jugador_db("Juan")
    
    jugadores = listar_jugadores_db()
    assert len(jugadores) == 2
    assert any(j["nombre"] == "María" and j["edad"] == 23 for j in jugadores)
    assert not any(j["nombre"] == "Juan" for j in jugadores)
