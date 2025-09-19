# gestor_notas.py
# -------------------------------------------------------------
# Gestor de Notas Académicas - Fase 4
# Autor: Kleyver Josué Lapoyeu Martínez
# Descripción:
#   Versión del programa con eliminación de cursos, uso claro de listas,
#   y modularización por funciones. Mantiene registro y operación por menú.
# -------------------------------------------------------------

cursos = []  # Lista principal: cada elemento es {"nombre": str, "nota": float}


# --------------------------- Utilidades ---------------------------
def leer_nota():
    """Lee una nota desde teclado con validación (0-100)."""
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


# --------------------------- Operaciones sobre la lista 'cursos' ---------------------------
def existe_curso(nombre):
    """
    Verifica si existe un curso por nombre (case-insensitive).
    Retorna el índice del primer curso encontrado o None si no existe.
    """
    nombre_norm = normalizar(nombre)
    for idx, c in enumerate(cursos):
        if normalizar(c["nombre"]) == nombre_norm:
            return idx
    return None


def registrar_curso():
    """Registrar un curso nuevo (no bloquea si ya existe; avisa si existe)."""
    nombre = input("Ingrese el nombre del curso: ").strip()
    if not nombre:
        print("El nombre del curso no puede estar vacío.")
        return

    idx = existe_curso(nombre)
    if idx is not None:
        print("Aviso: ya existe un curso con ese nombre. Use 'Actualizar' si desea cambiar la nota.")
        return

    nota = leer_nota()
    cursos.append({"nombre": nombre, "nota": nota})
    print("Curso registrado con éxito.")


def mostrar_cursos():
    """Muestra todos los cursos registrados en la lista."""
    if not cursos:
        print("No hay cursos registrados.")
        return

    print("\nCursos registrados:")
    for i, curso in enumerate(cursos, start=1):
        print(f"{i}. {curso['nombre']} - Nota: {curso['nota']}")


def calcular_promedio():
    """Calcula y muestra el promedio de las notas si hay cursos."""
    if not cursos:
        print("No hay cursos para calcular el promedio.")
        return
    suma = sum(c["nota"] for c in cursos)
    promedio = suma / len(cursos)
    print(f"Promedio general: {promedio:.2f}")


def contar_aprobados_reprobados():
    """Cuenta y muestra aprobados (>=60) y reprobados (<60)."""
    if not cursos:
        print("No hay cursos registrados.")
        return
    aprobados = sum(1 for c in cursos if c["nota"] >= 60)
    reprobados = len(cursos) - aprobados
    print(f"Cursos aprobados: {aprobados}")
    print(f"Cursos reprobados: {reprobados}")


def buscar_curso_lineal():
    """Búsqueda lineal por coincidencia parcial (case-insensitive). Muestra todas las coincidencias."""
    if not cursos:
        print("No hay cursos registrados.")
        return

    termino = input("Ingrese el nombre del curso a buscar: ").strip()
    if not termino:
        print("Debe ingresar un texto de búsqueda.")
        return

    termino_norm = normalizar(termino)
    encontrados = [ (i, c) for i, c in enumerate(cursos) if termino_norm in normalizar(c["nombre"]) ]

    if encontrados:
        print("Coincidencias encontradas:")
        for num, (idx, c) in enumerate(encontrados, start=1):
            print(f"{num}. {c['nombre']} - Nota: {c['nota']} (índice interno: {idx})")
    else:
        print("No se encontraron cursos que coincidan con la búsqueda.")


def actualizar_nota():
    """Actualiza la nota de un curso. Si hay múltiples coincidencias, el usuario elige cuál."""
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


def eliminar_curso():
    """
    Elimina un curso identificado por nombre (coincidencia parcial permitida).
    - Si hay varias coincidencias, el usuario elige cuál eliminar.
    - Pide confirmación antes de borrar.
    """
    if not cursos:
        print("No hay cursos registrados.")
        return

    termino = input("Ingrese el nombre del curso a eliminar: ").strip()
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
    else:
        print("Se encontraron varios cursos:")
        for i, (idx, c) in enumerate(coincidencias, start=1):
            print(f"{i}. {c['nombre']} - Nota: {c['nota']}")
        while True:
            elec = input("Seleccione el número del curso a eliminar: ").strip()
            if elec.isdigit() and 1 <= int(elec) <= len(coincidencias):
                idx, curso = coincidencias[int(elec) - 1]
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    confirm = input(f"¿Está seguro que desea eliminar '{curso['nombre']}'? (s/n): ").strip().lower()
    if confirm == "s":
        eliminado = cursos.pop(idx)
        print(f"Curso eliminado correctamente: {eliminado['nombre']} - Nota: {eliminado['nota']}")
    else:
        print("Eliminación cancelada.")


# --------------------------- Menú principal ---------------------------
def mostrar_menu():
    print("\n====== GESTOR DE NOTAS ACADÉMICAS (Fase 4) ======")
    print("1. Registrar nuevo curso")
    print("2. Mostrar todos los cursos y notas")
    print("3. Calcular promedio general")
    print("4. Contar cursos aprobados y reprobados")
    print("5. Buscar curso por nombre (búsqueda lineal)")
    print("6. Actualizar nota de un curso")
    print("7. Eliminar un curso")
    print("8. Salir")


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
            eliminar_curso()
            pausar()
        elif opcion == "8":
            print("Gracias por usar el Gestor de Notas Académicas. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            pausar()


if __name__ == "__main__":
    ejecutar_menu()
