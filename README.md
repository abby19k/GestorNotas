# Gestor de Notas Académicas

## Descripción del problema

El "Gestor de Notas Académicas" es un sistema desarrollado para ayudar a los estudiantes a organizar, registrar y analizar sus notas de forma sencilla. En muchas ocasiones, los estudiantes llevan el control de sus calificaciones en papel o de forma desordenada, lo que puede causar errores o confusiones.

Este programa busca proporcionar una herramienta práctica y accesible desde la consola, donde el estudiante pueda ingresar sus cursos, registrar sus notas, actualizar información, y visualizar su rendimiento académico con estadísticas claras. Está enfocado en estudiantes que deseen mejorar su organización personal sin necesidad de herramientas complejas.

## Requisitos del sistema

### Requisitos funcionales

El sistema permitirá realizar las siguientes acciones:

1. Registrar un nuevo curso con su respectiva nota.
2. Mostrar todos los cursos registrados y sus notas.
3. Calcular el promedio general de todas las notas ingresadas.
4. Contar cuántos cursos están aprobados y cuántos reprobados.

### Requisitos no funcionales

- El sistema se ejecutará exclusivamente desde la consola.
- Estará desarrollado en Python, sin usar librerías externas.
- Utilizará estructuras de control básicas como condicionales (`if`, `else`) y bucles (`while`).
- El menú estará controlado por un bucle que repetirá las opciones hasta que el usuario decida salir.

## Avance de Proyecto 04 - Eliminación de cursos, uso de listas, funciones y modularización

**Resumen de lo implementado en esta fase:**

- Se implementó la función `eliminar_curso()` para borrar un curso registrado.
  - La búsqueda permite coincidencia parcial y no distingue mayúsculas/minúsculas.
  - Si hay varias coincidencias, el usuario puede seleccionar cuál eliminar.
  - Antes de eliminar se pide confirmación (s/n).
- Se evidencia un uso claro de **listas**: `cursos` es la estructura principal (lista de diccionarios).
- El código está **modularizado** en funciones: utilidades, operaciones sobre la lista y menú.
- Se mantienen validaciones: nombre no vacío, nota numérica en rango 0–100.
- Mensajes al usuario y pausas para facilitar la interacción en consola.

**Cómo probar localmente**
1. Ejecutar `python gestor_notas.py`.
2. Registrar algunos cursos (opción 1).
3. Usar la opción 7 para eliminar un curso y verificar con la opción 2 que desapareció.

