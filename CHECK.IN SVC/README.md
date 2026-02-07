# akumi.dev🏐 Suarez Voley Club – Sistema de Gestión de Ingresos
Junior Back-end Developer | akumi.dev – Beta Repository

Este proyecto es un sistema de gestión integral para un club de voley, diseñado para automatizar el registro de asistencia y la generación de reportes administrativos. Desarrollado con un enfoque en la eficiencia del backend y la integridad de los datos.

# 🚀 Tecnologías y Herramientas
Lenguaje: Python 3.x

Framework Web: FastAPI (API REST de alta performance)

Base de Datos: SQLite3 (Persistencia de datos estructurada)

Procesamiento de Datos: Pandas & Openpyxl (Generación de reportes automáticos en Excel)

Frontend: Vanilla HTML5, CSS3 (Custom properties) y JavaScript Asíncrono (Fetch API)

# 🛠️ Funcionalidades Implementadas
Gestión de Jugadores: CRUD completo para administración de socios.

Registro Automático de Asistencia: Sistema de check-in con validación en tiempo real y registro de timestamps.

Reportes Administrativos: Módulo de exportación de datos a Excel mediante análisis con Pandas.

Interfaz de Consola & Web: Dualidad de interfaz para administración interna (CLI) y uso de usuarios (Web).

Validación de Datos: Uso de Pydantic para garantizar la integridad de la información entrante.

# 📂 Arquitectura del Proyecto
El proyecto sigue una estructura clara de separación de responsabilidades:

main.py: Punto de entrada, rutas de FastAPI y menú de administración.

/static: Interfaz de usuario y activos estáticos.

suarez_voley.db: Base de datos relacional.

test_main.py: Pruebas de lógica y validación.

# 🎯 Próximos Pasos (Roadmap)

[ ] Implementar autenticación para el panel administrativo.

[ ] Automatizar el envío de reportes semanales por email.

[ ] Integrar un sistema de estadísticas visuales de asistencia.