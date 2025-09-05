# gestor_notas.py
# -------------------------------------------------------------
# Gestor de Notas Académicas - Fase 3
# Autor: Kleyver
# Descripción:
#   Programa de consola para registrar cursos con notas y
#   realizar operaciones básicas: mostrar, promedio, contadores,
#   búsqueda lineal y actualización de notas.
#
#   Este código sigue la lógica del pseudocódigo trabajado en
#   las fases anteriores: validación de entradas numéricas (0-100)
#   y flujo controlado por un menú repetitivo.
# -------------------------------------------------------------

# Estructura de datos principal:
#   - 'cursos' es una lista de diccionarios con forma:
#       {"nombre": <str>, "nota": <float>}

cursos = []  # lista global de cursos


# --------------------------- Utilidades ---------------------------
def leer_nota():
    """
    Lee una nota desde teclado con validación.
    Regresa un float entre 0 y 100.
    (Versión en Python del pseudocódigo de Fase 2: validar numérico y rango)
    """
    while True:
        entrada = input("Ingrese una nota entre 0 y 100: ").strip()
        try:
            nota = float(entrada)
            if 0 <= nota <= 100:
                return nota
            else:
                print("Error: la nota debe estar entre 0 y 100.")
        except ValueError:
            print("Error: debe ingresar un número válido.")


def normalizar(texto):
    """Devuelve el texto en minúsculas y sin espacios extremos para comparar nombres."""
    return texto.strip().lower()


def pausar():
    input("\nPresione Enter para continuar...")


# --------------------------- Funcionalidades ---------------------------
def registrar_curso():
    """Opción 1: Registrar un curso con su nota (valida nombre y nota)."""
    nombre = input("Ingrese el nombre del curso: ").strip()
    if not nombre:
        print("El nombre del curso no puede estar vacío.")
        return

    # Si ya existe un curso con el mismo nombre (ignorando mayúsculas), avisamos.
    for curso in cursos:
        if normalizar(curso["nombre"]) == normalizar(nombre):
            print("Aviso: ya existe un curso con ese nombre. Use 'Actualizar' si desea cambiar la nota.")
            break

    nota = leer_nota()
    cursos.append({"nombre": nombre, "nota": nota})
    print("Curso registrado con éxito.")


def mostrar_cursos():
    """Opción 2: Mostrar todos los cursos y notas."""
    if not cursos:
        print("No hay cursos registrados.")
        return

    print("\nCursos registrados:")
    for i, curso in enumerate(cursos, start=1):
        print(f"{i}. {curso['nombre']} - Nota: {curso['nota']}")


def calcular_promedio():
    """Opción 3: Calcular el promedio general de las notas."""
    if not cursos:
        print("No hay cursos para calcular el promedio.")
        return

    suma = sum(c["nota"] for c in cursos)
    promedio = suma / len(cursos)
    print(f"Promedio general: {promedio:.2f}")


def contar_aprobados_reprobados():
    """Opción 4: Contar cuántos cursos están aprobados (>=60) y reprobados (<60)."""
    if not cursos:
        print("No hay cursos registrados.")
        return

    aprobados = sum(1 for c in cursos if c["nota"] >= 60)
    reprobados = len(cursos) - aprobados
    print(f"Cursos aprobados: {aprobados}")
    print(f"Cursos reprobados: {reprobados}")


def buscar_curso_lineal():
    """
    Opción 5: Búsqueda lineal por nombre.
    - Ignora mayúsculas/minúsculas.
    - Permite coincidencia parcial (muestra todas las coincidencias).
    """
    if not cursos:
        print("No hay cursos registrados.")
        return

    termino = input("Ingrese el nombre del curso a buscar: ").strip()
    if not termino:
        print("Debe ingresar un texto de búsqueda.")
        return

    termino_norm = normalizar(termino)
    encontrados = [c for c in cursos if termino_norm in normalizar(c["nombre"])]

    if encontrados:
        print("Coincidencias encontradas:")
        for i, c in enumerate(encontrados, start=1):
            print(f"{i}. {c['nombre']} - Nota: {c['nota']}")
    else:
        print("No se encontraron cursos que coincidan con la búsqueda.")


def actualizar_nota():
    """
    Opción 6: Actualizar la nota de un curso.
    - Búsqueda lineal por coincidencia parcial (case-insensitive).
    - Si hay múltiples coincidencias, el usuario elige cuál actualizar.
    """
    if not cursos:
        print("No hay cursos registrados.")
        return

    termino = input("Ingrese el nombre del curso a actualizar: ").strip()
    if not termino:
        print("Debe ingresar un nombre.")
        return

    termino_norm = normalizar(termino)
    coincidencias = [ (idx, c) for idx, c in enumerate(cursos) if termino_norm in normalizar(c["nombre"]) ]

    if not coincidencias:
        print("No se encontró ningún curso con ese nombre.")
        return

    if len(coincidencias) == 1:
        idx, curso = coincidencias[0]
        print(f"Curso encontrado: {curso['nombre']} - Nota actual: {curso['nota']}")
    else:
        print("Se encontraron varios cursos:")
        for i, (idx, c) in enumerate(coincidencias, start=1):
            print(f"{i}. {c['nombre']} - Nota: {c['nota']}")
        # Elegir uno
        while True:
            elec = input("Seleccione el número del curso a actualizar: ").strip()
            if elec.isdigit() and 1 <= int(elec) <= len(coincidencias):
                idx, curso = coincidencias[int(elec) - 1]
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    nueva_nota = leer_nota()
    cursos[idx]["nota"] = nueva_nota
    print(f"Nota actualizada correctamente: {cursos[idx]['nombre']} → {nueva_nota}")


# --------------------------- Menú principal ---------------------------
def mostrar_menu():
    print("\n====== GESTOR DE NOTAS ACADÉMICAS ======")
    print("1. Registrar nuevo curso")
    print("2. Mostrar todos los cursos y notas")
    print("3. Calcular promedio general")
    print("4. Contar cursos aprobados y reprobados")
    print("5. Buscar curso por nombre (búsqueda lineal)")
    print("6. Actualizar nota de un curso")
    print("7. Salir")


def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_curso()
            pausar()
        elif opcion == "2":
            mostrar_cursos()
            pausar()
        elif opcion == "3":
            calcular_promedio()
            pausar()
        elif opcion == "4":
            contar_aprobados_reprobados()
            pausar()
        elif opcion == "5":
            buscar_curso_lineal()
            pausar()
        elif opcion == "6":
            actualizar_nota()
            pausar()
        elif opcion == "7":
            print("Gracias por usar el Gestor de Notas Académicas. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            pausar()


# Punto de entrada
if __name__ == "__main__":
    ejecutar_menu()
