# PedidoListo Project

API backend para gestión simple de pedidos desarrollada con **FastAPI** y **SQLite**.
El objetivo del proyecto es simular un sistema básico de pedidos donde un cliente puede consultar productos y crear pedidos.

Este proyecto fue desarrollado como práctica de arquitectura backend, testing y flujo de trabajo con IA (Copilot / Codex).

---

# Tecnologías

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy**
* **SQLite**
* **Playwright (tests E2E)**
* **Pytest**
* **Git / GitHub**

---

# Arquitectura del Proyecto

```
PedidoListo/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── pedidos.py
│   └── models.py
│
├── tests/
│   └── test_playwright.py
│
├── app.js
├── pedidos.db
├── requirements.txt
└── README.md
```

### Descripción de componentes

**backend/main.py**
Inicializa la aplicación FastAPI y registra las rutas.

**backend/database.py**
Configura la conexión con SQLite y la sesión de SQLAlchemy.

**backend/pedidos.py**
Contiene la lógica de negocio y endpoints relacionados con pedidos.

**backend/models.py**
Define los modelos de base de datos.

**tests/test_playwright.py**
Pruebas End-to-End que verifican el flujo completo de creación de pedidos.

**app.js**
Script simple para interactuar con la API.

---

# Instalación

Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/pedidolisto.git
cd pedidolisto
```

Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno

Linux / Mac

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar el servidor

```bash
uvicorn backend.main:app --reload
```

Servidor disponible en

```
http://127.0.0.1:8000
```

Documentación automática

```
http://127.0.0.1:8000/docs
```

---

# Endpoints principales

## Obtener productos

```
GET /productos
```

Respuesta

```json
[
  {
    "id": 1,
    "nombre": "Hamburguesa",
    "precio": 10
  }
]
```

---

## Crear pedido

```
POST /pedidos
```

Body

```json
{
  "producto_id": 1,
  "cantidad": 2
}
```

Respuesta esperada

```json
{
  "pedido_id": 10,
  "estado": "creado"
}
```

---

# Testing

Ejecutar tests

```bash
pytest
```

Tests incluidos

* Validación de endpoints
* Flujo completo de creación de pedidos
* Validación de errores HTTP

---

# Problemas conocidos (Tech Notes)

Durante el análisis automático del código se detectaron algunos puntos a mejorar:

### Bug crítico

`POST /pedidos` puede generar **error 500** si se abre una transacción después de realizar una consulta previa en la misma sesión.

Causa probable:

```
InvalidRequestError: transaction already begun
```

Archivo afectado:

```
backend/pedidos.py
```

---

### Test E2E puede dar falso positivo

`app.js` imprime mensaje de éxito incluso si el backend responde con error.

Archivo afectado

```
tests/test_playwright.py
```

---

### Riesgo de múltiples bases SQLite

Uso de ruta relativa:

```
sqlite:///./pedidos.db
```

Esto puede crear bases en carpetas distintas dependiendo del directorio desde donde se ejecute el servidor.

---

# Mejoras futuras

* Manejo de errores más específico
* Logging estructurado
* Validación avanzada con Pydantic
* Migraciones con Alembic
* Dockerización del proyecto
* CI/CD pipeline

---

# Objetivo del proyecto

Este proyecto busca practicar:

* diseño de APIs
* debugging backend
* arquitectura simple
* testing automatizado
* uso de IA para asistencia en desarrollo

---

# Autor

Desarrollado por **Akumi**
Backend Developer en formación.


1. Iniciar servidor:
   uvicorn main:app --reload

2. Abrir en navegador: http://localhost:8000

## Tests

Ejecutar tests con Playwright:
python tests/test_playwright.py
