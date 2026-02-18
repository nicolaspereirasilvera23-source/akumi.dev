# akumi.dev - Suarez Voley Club (Registro de Asistencias)

Proyecto backend/fullstack junior con API REST en FastAPI, persistencia en SQLite y pruebas automatizadas.

## Stack
- Python 3.x
- FastAPI + Uvicorn
- SQLite
- Pandas + Openpyxl (exportacion de reporte Excel)
- Frontend HTML/CSS/JS
- Pytest + Playwright

## Funcionalidades
- CRUD de jugadores (crear, listar, obtener por id, actualizar, eliminar).
- Generacion automatica de codigo de 4 digitos por jugador.
- Check-in de asistencia por codigo.
- Endpoint de ultimos ingresos del dia.
- Exportacion automatica a `Reporte_SVC.xlsx` en cada alta/edicion/baja/asistencia.
- Interfaz web para check-in y CLI administrativa.

## Estructura
- `main.py`: API FastAPI.
- `database.py`: logica SQL y operaciones de datos.
- `console.py`: menu de administracion por consola.
- `static/index.html`: interfaz web.
- `tests/test_api.py`: pruebas API (rapidas).
- `tests/test_asistencia_db.py`: prueba E2E con navegador.

## Como ejecutar
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Abrir: `http://127.0.0.1:8000`

## Consola administrativa
```bash
python console.py
```

## Bot de carga rapida (pruebas)
Script con inputs para alta individual, lote manual, importacion CSV y generacion aleatoria.
```bash
python bot_prueba_jugadores.py
```
Incluye opciones para:
- Cargar jugadores desde `Reporte_SVC.xlsx` (hoja `Jugadores`).
- Registrar pruebas/asistencias desde `Reporte_SVC.xlsx` (hoja `Asistencias`, columna `Codigo`).

## Pruebas
Pruebas API/unitarias (recomendado para CI):
```bash
pytest -q -m "not e2e"
```

Prueba E2E (requiere servidor en ejecucion y navegador Playwright):
```bash
uvicorn main:app
pytest -q -m e2e tests/test_asistencia_db.py
```

## CI
Incluye pipeline base para GitLab en `.gitlab-ci.yml`, ejecutando `pytest -m "not e2e"`.
