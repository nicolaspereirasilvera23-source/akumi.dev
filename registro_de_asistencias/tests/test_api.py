import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_path = tmp_path / "test_svc.db"
    monkeypatch.setattr(database, "DB_NAME", str(db_path))
    database.inicializar_db()

    with TestClient(main.app) as test_client:
        yield test_client


def test_crud_jugador(client: TestClient):
    crear = client.post(
        "/jugadores/",
        json={"nombre": "Lucia", "edad": 22, "tiempo": 6},
    )
    assert crear.status_code == 201

    crear_data = crear.json()
    jugador_id = crear_data["id"]
    codigo = crear_data["codigo"]
    assert re.fullmatch(r"\d{4}", codigo)

    listar = client.get("/jugadores/")
    assert listar.status_code == 200
    assert len(listar.json()) == 1
    assert listar.json()[0]["codigo"] == codigo

    detalle = client.get(f"/jugadores/{jugador_id}")
    assert detalle.status_code == 200
    assert detalle.json()["nombre"] == "Lucia"
    assert detalle.json()["codigo"] == codigo

    actualizar = client.put(
        f"/jugadores/{jugador_id}",
        json={"nombre": "Lucia Gomez", "edad": 23, "tiempo": 7},
    )
    assert actualizar.status_code == 200

    detalle_actualizado = client.get(f"/jugadores/{jugador_id}")
    assert detalle_actualizado.status_code == 200
    assert detalle_actualizado.json()["nombre"] == "Lucia Gomez"

    eliminar = client.delete(f"/jugadores/{jugador_id}")
    assert eliminar.status_code == 200

    detalle_eliminado = client.get(f"/jugadores/{jugador_id}")
    assert detalle_eliminado.status_code == 404


def test_jugador_duplicado(client: TestClient):
    payload = {"nombre": "Mateo", "edad": 21, "tiempo": 4}

    r1 = client.post("/jugadores/", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/jugadores/", json=payload)
    assert r2.status_code == 400


def test_verificar_y_checkin_por_codigo(client: TestClient):
    crear = client.post(
        "/jugadores/",
        json={"nombre": "Nicolas", "edad": 24, "tiempo": 10},
    )
    assert crear.status_code == 201
    codigo = crear.json()["codigo"]

    verificar = client.get(f"/verificar/{codigo}")
    assert verificar.status_code == 200
    assert verificar.json()["existe"] is True
    assert verificar.json()["nombre"] == "Nicolas"

    checkin = client.post("/check-in", json={"codigo": codigo})
    assert checkin.status_code == 200
    assert checkin.json()["nombre"] == "Nicolas"


def test_check_in_codigo_inexistente(client: TestClient):
    r = client.post("/check-in", json={"codigo": "9999"})
    assert r.status_code == 404
