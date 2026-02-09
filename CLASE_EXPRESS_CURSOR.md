# Clase Express: Cómo usar Cursor

Guía rápida para sacar partido a Cursor, el editor con IA.

---

## 1. Abrir Cursor y el chat

- **Chat con IA**: `Ctrl + L` (o clic en el icono de chat) para abrir el panel de chat.
- **Chat en línea**: Selecciona código y usa `Ctrl + L` para preguntar solo sobre lo seleccionado.
- **Composer (multiedición)**: `Ctrl + I` para modo que puede editar varios archivos a la vez.

---

## 2. Comandos básicos en el chat

| Quieres que... | Escribe algo como... |
|----------------|----------------------|
| Explique código | "Explica qué hace esta función" |
| Refactorice | "Refactoriza esto para que sea más legible" |
| Arregle errores | "Corrige los errores de este archivo" |
| Escriba código nuevo | "Crea una función que haga X" |
| Traduzca/coma documentación | "Documenta esta clase" o "Añade comentarios" |

**Tip**: Usa **@** para dar contexto:
- `@archivo.py` — incluir un archivo en la conversación.
- `@carpeta/` — incluir una carpeta.
- `@docs` — usar la documentación que Cursor conozca.

---

## 3. Editar con la IA (inline)

- Selecciona el código que quieres cambiar.
- Pulsa `Ctrl + K` (o clic derecho → "Edit with AI").
- Describe el cambio en lenguaje natural (ej: "convierte esto a async" o "añade manejo de errores").
- Acepta o rechaza los cambios que te proponga.

---

## 4. Composer (Ctrl + I) — Varios archivos

- Abre Composer con `Ctrl + I`.
- Describe la tarea (ej: "Añade un endpoint de login en el backend y un botón en el frontend").
- Cursor puede crear o modificar varios archivos en un solo paso.
- Revisa el diff y acepta los cambios que quieras.

---

## 5. Atajos útiles

| Atajo | Acción |
|-------|--------|
| `Ctrl + L` | Abrir chat |
| `Ctrl + I` | Abrir Composer |
| `Ctrl + K` | Editar selección con IA |
| `Ctrl + Shift + P` | Paleta de comandos |

---

## 6. Buenas prácticas

1. **Sé concreto**: "Añade validación de email en el formulario de registro" mejor que "arregla el formulario".
2. **Usa @**: Menciona archivos o carpetas con @ para que la IA tenga contexto.
3. **Itera**: Si no queda bien, pide "cambia X por Y" o "usa otro enfoque".
4. **Revisa el código**: Siempre revisa y prueba lo que la IA genera.

---

## 7. Reglas del proyecto (.cursor/rules)

Puedes definir reglas que Cursor siga en tu proyecto:

- Crea `.cursor/rules` en la raíz del proyecto.
- Añade archivos `.mdc` o escribe en "Rules for AI" en ajustes.
- Ejemplo: "Siempre responde en español", "Usa type hints en Python", "No usar var en JavaScript".

---

**Resumen**: Usa **Ctrl + L** para preguntar, **Ctrl + K** para editar un trozo de código y **Ctrl + I** para tareas que toquen varios archivos. Usa **@** para dar contexto y revisa siempre los cambios.
