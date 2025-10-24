# Estructuras principales
cursos = []            # Lista de cursos: {"nombre": str, "nota": float}
historial = []         # Pila: registros de acciones (append = push, mostrar en LIFO)
cola_revisiones = []   # Cola: nombres de cursos pendientes de revisión (append = enqueue, pop(0) = dequeue)


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


# --------------------------- Historial (Pila) ---------------------------
def push_historial(mensaje):
    """Agrega un mensaje a la pila de historial."""
    historial.append(mensaje)


def ver_historial():
    """Muestra el historial en orden inverso (último cambio primero)."""
    if not historial:
        print("No hay historial de cambios.")
        return
    print("\nHistorial de cambios (más reciente primero):")
    for i, msg in enumerate(reversed(historial), start=1):
        print(f"{i}. {msg}")


# --------------------------- Cola de revisiones (FIFO) ---------------------------
def encolar_revision(nombre_curso):
    """Agrega el nombre del curso a la cola de revisiones si no está ya en ella."""
    nombre_norm = normalizar(nombre_curso)
    if any(normalizar(x) == nombre_norm for x in cola_revisiones):
        print(f"'{nombre_curso}' ya está en la cola de revisiones.")
        return
    cola_revisiones.append(nombre_curso)
    print(f"'{nombre_curso}' agregado a la cola de revisiones.")
    push_historial(f"Se encoló a revisión: {nombre_curso}")


def procesar_cola_revisiones():
    """Procesa y vacía la cola mostrando cada curso en orden FIFO."""
    if not cola_revisiones:
        print("La cola de revisiones está vacía.")
        return
    print("\nProcesando solicitudes de revisión:")
    while cola_revisiones:
        curso = cola_revisiones.pop(0)  # dequeue
        print(f"Revisando: {curso}")
    print("Cola de revisiones procesada.")


# --------------------------- Operaciones sobre la lista 'cursos' ---------------------------
def existe_curso(nombre):
    """Retorna el índice del curso con nombre exacto (case-insensitive) o None si no existe."""
    nombre_norm = normalizar(nombre)
    for idx, c in enumerate(cursos):
        if normalizar(c["nombre"]) == nombre_norm:
            return idx
    return None


def registrar_curso():
    """Registrar un curso nuevo; si la nota es baja lo encola para revisión."""
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
    push_historial(f"Se registró: {nombre} - Nota: {nota}")

    # Regla adicional: si la nota es menor a 60, sugerimos encolarlo para revisión
    if nota < 60:
        encolar_revision(nombre)


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

    nota_anterior = cursos[idx]["nota"]
    nueva_nota = leer_nota()
    cursos[idx]["nota"] = nueva_nota
    print(f"Nota actualizada correctamente: {cursos[idx]['nombre']} → {nueva_nota}")
    push_historial(f"Se actualizó: {cursos[idx]['nombre']} - Nota anterior: {nota_anterior} → Nueva nota: {nueva_nota}")

    # Si la nueva nota es baja, encolar para revisión
    if nueva_nota < 60:
        encolar_revision(cursos[idx]["nombre"])


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
        push_historial(f"Se eliminó: {eliminado['nombre']} - Nota: {eliminado['nota']}")
        # Si estaba en la cola de revisiones, eliminarlo de la cola
        nombre_norm = normalizar(eliminado['nombre'])
        cola_revisiones[:] = [x for x in cola_revisiones if normalizar(x) != nombre_norm]
    else:
        print("Eliminación cancelada.")


# --------------------------- Ordenamientos (no modifican 'cursos') ---------------------------
def bubble_sort_by_note_desc(lista_cursos):
    """Burbuja: ordena por nota de mayor a menor y devuelve una copia ordenada."""
    arr = [dict(c) for c in lista_cursos]  # copia por valor
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j]["nota"] < arr[j + 1]["nota"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort_by_name_asc(lista_cursos):
    """Inserción: ordena por nombre A-Z y devuelve una copia ordenada."""
    arr = [dict(c) for c in lista_cursos]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and normalizar(arr[j]["nombre"]) > normalizar(key["nombre"]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def mostrar_ordenamientos():
    """Muestra los resultados de ambos ordenamientos sin modificar la lista original."""
    if not cursos:
        print("No hay cursos registrados para ordenar.")
        return

    print("\n--- Ordenamiento (Burbuja) por nota (descendente) ---")
    orden_burbuja = bubble_sort_by_note_desc(cursos)
    for i, c in enumerate(orden_burbuja, start=1):
        print(f"{i}. {c['nombre']} - Nota: {c['nota']}")

    print("\n--- Ordenamiento (Inserción) por nombre (A-Z) ---")
    orden_insercion = insertion_sort_by_name_asc(cursos)
    for i, c in enumerate(orden_insercion, start=1):
        print(f"{i}. {c['nombre']} - Nota: {c['nota']}")


# --------------------------- Funciones puente para menú ---------------------------
def ordenar_por_nota_burbuja():
    """Muestra la lista de cursos ordenada por nota (descendente)."""
    print("\n--- Ordenamiento por nota (Burbuja) ---")
    orden_burbuja = bubble_sort_by_note_desc(cursos)
    for i, c in enumerate(orden_burbuja, start=1):
        print(f"{i}. {c['nombre']} - Nota: {c['nota']}")


def ordenar_por_nombre_insercion():
    """Muestra la lista de cursos ordenada por nombre (ascendente)."""
    print("\n--- Ordenamiento por nombre (Inserción) ---")
    orden_insercion = insertion_sort_by_name_asc(cursos)
    for i, c in enumerate(orden_insercion, start=1):
        print(f"{i}. {c['nombre']} - Nota: {c['nota']}")


def buscar_curso_binaria():
    """Búsqueda binaria por nombre (requiere lista ordenada por nombre)."""
    if not cursos:
        print("No hay cursos registrados.")
        return

    # Crear copia ordenada por nombre para búsqueda binaria
    lista_ordenada = insertion_sort_by_name_asc(cursos)
    termino = input("Ingrese el nombre del curso a buscar (búsqueda binaria): ").strip()
    if not termino:
        print("Debe ingresar un nombre.")
        return

    termino_norm = normalizar(termino)
    izquierda, derecha = 0, len(lista_ordenada) - 1
    encontrado = None

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_medio = normalizar(lista_ordenada[medio]["nombre"])
        if nombre_medio == termino_norm:
            encontrado = lista_ordenada[medio]
            break
        elif nombre_medio < termino_norm:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    if encontrado:
        print(f"Curso encontrado: {encontrado['nombre']} - Nota: {encontrado['nota']}")
    else:
        print("No se encontró ningún curso con ese nombre.")


def simular_cola_revisiones():
    """Simula el procesamiento de la cola de revisiones."""
    if not cola_revisiones:
        print("La cola de revisiones está vacía.")
        return

    print("\n--- Cola de revisiones ---")
    print("Cursos en cola:", ", ".join(cola_revisiones))
    procesar_cola_revisiones()


# --------------------------- Menú principal --------------------------- 
def mostrar_menu():
    print("\n====== GESTOR DE NOTAS ACADÉMICAS ======")
    print("1. Registrar nuevo curso")
    print("2. Mostrar todos los cursos y notas")
    print("3. Calcular promedio general")
    print("4. Contar cursos aprobados y reprobados")
    print("5. Buscar curso por nombre (búsqueda lineal)")
    print("6. Actualizar nota de un curso")
    print("7. Eliminar un curso")
    print("8. Ordenar cursos por nota (ordenamiento burbuja)")
    print("9. Ordenar cursos por nombre (ordenamiento inserción)")
    print("10. Buscar curso por nombre (búsqueda binaria)")
    print("11. Simular cola de solicitudes de revisión")
    print("12. Mostrar historial de cambios (pila)")
    print("13. Salir")


def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_curso()
        elif opcion == "2":
            mostrar_cursos()
        elif opcion == "3":
            calcular_promedio()
        elif opcion == "4":
            contar_aprobados_reprobados()
        elif opcion == "5":
            buscar_curso_lineal()
        elif opcion == "6":
            actualizar_nota()
        elif opcion == "7":
            eliminar_curso()
        elif opcion == "8":
            ordenar_por_nota_burbuja()
        elif opcion == "9":
            ordenar_por_nombre_insercion()
        elif opcion == "10":
            buscar_curso_binaria()
        elif opcion == "11":
            simular_cola_revisiones()
        elif opcion == "12":
            ver_historial()
        elif opcion == "13":
            print("Gracias por usar el Gestor de Notas Académicas. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar_menu()
