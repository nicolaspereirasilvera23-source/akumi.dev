import csv
import random
from pathlib import Path

import pandas as pd

from database import (
    agregar_jugador_db,
    inicializar_db,
    listar_jugadores_db,
    registrar_asistencia_db,
)


def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Valor invalido. Debe ser un numero entero.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Valor invalido. Debe ser >= {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"Valor invalido. Debe ser <= {maximo}.")
            continue
        return numero


def alta_individual():
    print("\nAlta individual")
    nombre = input("Nombre: ").strip()
    edad = pedir_entero("Edad: ", 1, 120)
    tiempo = pedir_entero("Tiempo (meses): ", 0, 80)

    res = agregar_jugador_db(nombre, edad, tiempo)
    if res["exito"]:
        print(
            f"OK -> id={res.get('id')} codigo={res.get('codigo')} nombre={nombre}"
        )
    else:
        print(f"ERROR -> {res.get('mensaje', 'Error desconocido')}")


def alta_por_lote_manual():
    print("\nCarga por lote manual")
    print("Formato por linea: nombre,edad,tiempo")
    print("Ejemplo: Ana Perez,22,6")
    print("Linea vacia para terminar.")

    ok = 0
    fail = 0
    while True:
        linea = input("> ").strip()
        if not linea:
            break

        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 3:
            fail += 1
            print("ERROR -> formato invalido, usa: nombre,edad,tiempo")
            continue

        nombre, edad_txt, tiempo_txt = partes
        try:
            edad = int(edad_txt)
            tiempo = int(tiempo_txt)
        except ValueError:
            fail += 1
            print("ERROR -> edad y tiempo deben ser numeros enteros")
            continue

        res = agregar_jugador_db(nombre, edad, tiempo)
        if res["exito"]:
            ok += 1
            print(
                f"OK -> id={res.get('id')} codigo={res.get('codigo')} nombre={nombre}"
            )
        else:
            fail += 1
            print(f"ERROR -> {nombre}: {res.get('mensaje', 'Error desconocido')}")

    print(f"\nResumen lote manual -> OK: {ok} | ERROR: {fail}")


def alta_desde_csv():
    print("\nCarga desde CSV")
    print("El archivo debe tener cabeceras: nombre,edad,tiempo")
    ruta = input("Ruta del CSV: ").strip().strip('"')
    archivo = Path(ruta)
    if not archivo.exists():
        print("ERROR -> archivo no encontrado")
        return

    ok = 0
    fail = 0
    with archivo.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columnas = {c.strip().lower() for c in (reader.fieldnames or [])}
        requeridas = {"nombre", "edad", "tiempo"}
        if not requeridas.issubset(columnas):
            print("ERROR -> columnas requeridas: nombre,edad,tiempo")
            return

        for fila in reader:
            nombre = (fila.get("nombre") or "").strip()
            edad_txt = (fila.get("edad") or "").strip()
            tiempo_txt = (fila.get("tiempo") or "").strip()
            try:
                edad = int(edad_txt)
                tiempo = int(tiempo_txt)
            except ValueError:
                fail += 1
                print(f"ERROR -> fila invalida para nombre='{nombre}'")
                continue

            res = agregar_jugador_db(nombre, edad, tiempo)
            if res["exito"]:
                ok += 1
            else:
                fail += 1
                print(f"ERROR -> {nombre}: {res.get('mensaje', 'Error desconocido')}")

    print(f"\nResumen CSV -> OK: {ok} | ERROR: {fail}")


def _leer_excel(ruta_txt):
    ruta = ruta_txt.strip().strip('"')
    if not ruta:
        ruta = str(Path(__file__).resolve().parent / "Reporte_SVC.xlsx")
    archivo = Path(ruta)
    if not archivo.exists():
        print("ERROR -> archivo .xlsx no encontrado")
        return None
    return archivo


def _valor_fila(fila, columnas):
    for col in columnas:
        if col in fila and str(fila[col]).strip() != "":
            return fila[col]
    return None


def cargar_jugadores_desde_excel():
    print("\nCarga desde XLSX (hoja Jugadores)")
    print("Enter para usar el archivo por defecto: Reporte_SVC.xlsx")
    archivo = _leer_excel(input("Ruta del XLSX: "))
    if not archivo:
        return

    try:
        df = pd.read_excel(archivo, sheet_name="Jugadores")
    except Exception as err:
        print(f"ERROR -> no se pudo leer la hoja 'Jugadores': {err}")
        return

    df.columns = [str(c).strip().lower() for c in df.columns]
    ok = 0
    fail = 0

    for _, fila in df.iterrows():
        nombre = _valor_fila(fila, ["nombre", "jugador"])
        edad = _valor_fila(fila, ["edad"])
        tiempo = _valor_fila(fila, ["tiempo"])

        if nombre is None or edad is None or tiempo is None:
            fail += 1
            continue

        try:
            edad = int(edad)
            tiempo = int(tiempo)
        except (TypeError, ValueError):
            fail += 1
            continue

        res = agregar_jugador_db(str(nombre).strip(), edad, tiempo)
        if res["exito"]:
            ok += 1
        else:
            fail += 1

    print(f"\nResumen XLSX jugadores -> OK: {ok} | ERROR: {fail}")


def registrar_pruebas_desde_excel():
    print("\nRegistrar pruebas desde XLSX (hoja Asistencias)")
    print("Enter para usar el archivo por defecto: Reporte_SVC.xlsx")
    archivo = _leer_excel(input("Ruta del XLSX: "))
    if not archivo:
        return

    try:
        df = pd.read_excel(archivo, sheet_name="Asistencias")
    except Exception as err:
        print(f"ERROR -> no se pudo leer la hoja 'Asistencias': {err}")
        return

    df.columns = [str(c).strip().lower() for c in df.columns]
    ok = 0
    fail = 0

    for _, fila in df.iterrows():
        codigo = _valor_fila(fila, ["codigo"])
        if codigo is None:
            fail += 1
            continue

        codigo_txt = str(codigo).strip()
        if codigo_txt.endswith(".0"):
            codigo_txt = codigo_txt[:-2]
        codigo_txt = codigo_txt.zfill(4)

        res = registrar_asistencia_db(codigo_txt)
        if res["exito"]:
            ok += 1
        else:
            fail += 1

    print(f"\nResumen XLSX pruebas -> OK: {ok} | ERROR: {fail}")


def generar_prueba_aleatoria():
    print("\nGenerar usuarios de prueba")
    cantidad = pedir_entero("Cantidad a generar: ", 1, 300)

    nombres = [
        "Ana",
        "Luis",
        "Carla",
        "Diego",
        "Valen",
        "Sofia",
        "Mateo",
        "Mia",
        "Luca",
        "Tomas",
    ]
    apellidos = [
        "Perez",
        "Gomez",
        "Diaz",
        "Lopez",
        "Suarez",
        "Torres",
        "Vera",
        "Silva",
        "Ruiz",
        "Sosa",
    ]

    ok = 0
    fail = 0
    for i in range(cantidad):
        nombre = f"{random.choice(nombres)} {random.choice(apellidos)} {i + 1}"
        edad = random.randint(16, 45)
        tiempo = random.randint(0, 36)
        res = agregar_jugador_db(nombre, edad, tiempo)
        if res["exito"]:
            ok += 1
        else:
            fail += 1

    print(f"\nResumen generacion -> OK: {ok} | ERROR: {fail}")


def listar_ultimos():
    print("\nUltimos jugadores cargados")
    limite = pedir_entero("Cuantos quieres ver?: ", 1, 100)
    jugadores = listar_jugadores_db()
    for j in jugadores[-limite:]:
        print(
            f"id={j['id']} | codigo={j['codigo']} | nombre={j['nombre']} | edad={j['edad']} | tiempo={j['tiempo']}"
        )


def menu():
    while True:
        print("\n=== BOT DE PRUEBA - CARGA DE JUGADORES ===")
        print("1) Alta individual")
        print("2) Carga por lote manual")
        print("3) Carga desde CSV")
        print("4) Cargar jugadores desde XLSX")
        print("5) Registrar pruebas desde XLSX")
        print("6) Generar usuarios aleatorios")
        print("7) Ver ultimos cargados")
        print("8) Salir")

        opcion = input("Opcion: ").strip()
        if opcion == "1":
            alta_individual()
        elif opcion == "2":
            alta_por_lote_manual()
        elif opcion == "3":
            alta_desde_csv()
        elif opcion == "4":
            cargar_jugadores_desde_excel()
        elif opcion == "5":
            registrar_pruebas_desde_excel()
        elif opcion == "6":
            generar_prueba_aleatoria()
        elif opcion == "7":
            listar_ultimos()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    inicializar_db()
    menu()
