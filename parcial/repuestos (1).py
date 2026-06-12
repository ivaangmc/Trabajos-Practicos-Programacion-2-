import json
import csv
import uuid
from datetime import datetime

# ─── Archivos de datos ───────────────────────────────────────────────────────
ARCHIVO_JSON = "repuestos.json"
ARCHIVO_CSV  = "repuestos.csv"

# Categorías disponibles
CATEGORIAS = ["motor", "frenos", "suspension", "electrico", "carroceria", "transmision", "otro"]


# ─── Persistencia ────────────────────────────────────────────────────────────

def cargar_inventario():
    """Lee repuestos.json y devuelve la lista. Si no existe, devuelve lista vacía."""
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_inventario(inventario):
    """Guarda la lista de repuestos en repuestos.json."""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def ahora():
    """Devuelve la fecha y hora actual en formato ISO 8601."""
    return datetime.now().isoformat(timespec="seconds")

def pedir_float_positivo(mensaje):
    """Pide un número flotante mayor a 0, repite hasta que sea válido."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = float(valor)
            if numero > 0:
                return numero
            print("  ✗ El precio debe ser mayor a 0.")
        except ValueError:
            print("  ✗ Ingresá un número válido.")

def pedir_int_no_negativo(mensaje):
    """Pide un entero mayor o igual a 0, repite hasta que sea válido."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero >= 0:
                return numero
            print("  ✗ El stock no puede ser negativo.")
        except ValueError:
            print("  ✗ Ingresá un número entero válido.")

def pedir_categoria():
    """Muestra las categorías y pide que el usuario elija una."""
    print("  Categorías:", ", ".join(CATEGORIAS))
    while True:
        cat = input("  Categoría: ").strip().lower()
        if cat in CATEGORIAS:
            return cat
        print("  ✗ Categoría inválida. Elegí una de la lista.")

def mostrar_repuesto(r):
    """Imprime un repuesto de forma legible."""
    print(f"""
  ID        : {r['id']}
  Nombre    : {r['nombre']}
  Marca     : {r['marca']}
  Modelo    : {r['modelo_auto']}
  Categoría : {r['categoria']}
  Precio    : ${r['precio']:.2f}
  Stock     : {r['stock']} unidades
  Ingreso   : {r['fecha_ingreso']}
  Modificado: {r['fecha_modificado']}
  {"─" * 40}""")


# ─── Operaciones del menú ─────────────────────────────────────────────────────

def agregar_repuesto(inventario):
    """Solicita los datos al usuario y agrega un nuevo repuesto."""
    print("\n── Agregar repuesto ──")
    repuesto = {
        "id"               : str(uuid.uuid4()),
        "nombre"           : input("  Nombre: ").strip(),
        "marca"            : input("  Marca: ").strip(),
        "modelo_auto"      : input("  Modelo de auto: ").strip(),
        "categoria"        : pedir_categoria(),
        "precio"           : pedir_float_positivo("  Precio: $"),
        "stock"            : pedir_int_no_negativo("  Stock: "),
        "fecha_ingreso"    : ahora(),
        "fecha_modificado" : ahora(),
    }
    inventario.append(repuesto)
    guardar_inventario(inventario)
    print("  ✓ Repuesto agregado correctamente.")

def listar_repuestos(inventario):
    """Muestra todos los repuestos o avisa si el inventario está vacío."""
    print("\n── Listado de repuestos ──")
    if not inventario:
        print("  El inventario está vacío.")
        return
    for r in inventario:
        mostrar_repuesto(r)

def buscar_repuesto(inventario):
    """Busca repuestos por nombre o marca (parcial, sin distinguir mayúsculas)."""
    print("\n── Buscar repuesto ──")
    termino = input("  Ingresá nombre o marca a buscar: ").strip().lower()
    resultados = [
        r for r in inventario
        if termino in r["nombre"].lower() or termino in r["marca"].lower()
    ]
    if not resultados:
        print("  No se encontraron repuestos.")
    else:
        print(f"  Se encontraron {len(resultados)} resultado(s):")
        for r in resultados:
            mostrar_repuesto(r)

def actualizar_repuesto(inventario):
    """Busca un repuesto por ID y permite modificar precio y/o stock."""
    print("\n── Actualizar repuesto ──")
    id_buscado = input("  Ingresá el ID del repuesto: ").strip()

    # Buscar el repuesto en la lista
    repuesto = next((r for r in inventario if r["id"] == id_buscado), None)

    if not repuesto:
        print("  ✗ No se encontró un repuesto con ese ID.")
        return

    mostrar_repuesto(repuesto)

    # Precio (Enter para no cambiar)
    nuevo_precio = input(f"  Nuevo precio (actual: ${repuesto['precio']:.2f}) [Enter para no cambiar]: ").strip()
    if nuevo_precio:
        try:
            precio = float(nuevo_precio)
            if precio > 0:
                repuesto["precio"] = precio
            else:
                print("  ✗ Precio inválido, no se modificó.")
        except ValueError:
            print("  ✗ Valor inválido, no se modificó el precio.")

    # Stock (Enter para no cambiar)
    nuevo_stock = input(f"  Nuevo stock (actual: {repuesto['stock']}) [Enter para no cambiar]: ").strip()
    if nuevo_stock:
        try:
            stock = int(nuevo_stock)
            if stock >= 0:
                repuesto["stock"] = stock
            else:
                print("  ✗ Stock inválido, no se modificó.")
        except ValueError:
            print("  ✗ Valor inválido, no se modificó el stock.")

    repuesto["fecha_modificado"] = ahora()
    guardar_inventario(inventario)
    print("  ✓ Repuesto actualizado correctamente.")

def eliminar_repuesto(inventario):
    """Busca por ID y elimina el repuesto tras confirmación del usuario."""
    print("\n── Eliminar repuesto ──")
    id_buscado = input("  Ingresá el ID del repuesto a eliminar: ").strip()

    repuesto = next((r for r in inventario if r["id"] == id_buscado), None)

    if not repuesto:
        print("  ✗ No se encontró un repuesto con ese ID.")
        return

    mostrar_repuesto(repuesto)
    confirmacion = input("  ¿Confirmar eliminación? (s/n): ").strip().lower()

    if confirmacion == "s":
        inventario.remove(repuesto)
        guardar_inventario(inventario)
        print("  ✓ Repuesto eliminado.")
    else:
        print("  Operación cancelada.")

def exportar_csv(inventario):
    """Exporta todos los repuestos a repuestos.csv con encabezados."""
    print("\n── Exportar a CSV ──")
    if not inventario:
        print("  El inventario está vacío, no hay nada para exportar.")
        return

    campos = ["id", "nombre", "marca", "modelo_auto", "categoria", "precio", "stock", "fecha_ingreso", "fecha_modificado"]

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()         # Fila de encabezados
        writer.writerows(inventario) # Todas las filas

    print(f"  ✓ Archivo '{ARCHIVO_CSV}' generado con {len(inventario)} repuesto(s).")


# ─── Menú principal ───────────────────────────────────────────────────────────

def mostrar_menu():
    print("""

   INVENTARIO DE REPUESTOS        

  1. Agregar repuesto                 
  2. Listar repuestos                 
  3. Buscar repuesto                  
  4. Actualizar repuesto              
  5. Eliminar repuesto                
  6. Exportar a CSV                   
  0. Salir                            """)

def main():
    # Cargar datos al iniciar
    inventario = cargar_inventario()
    print(f"  Sistema iniciado. {len(inventario)} repuesto(s) cargados.")

    while True:
        mostrar_menu()
        opcion = input("  Elegí una opción: ").strip()

        if opcion == "1":
            agregar_repuesto(inventario)
        elif opcion == "2":
            listar_repuestos(inventario)
        elif opcion == "3":
            buscar_repuesto(inventario)
        elif opcion == "4":
            actualizar_repuesto(inventario)
        elif opcion == "5":
            eliminar_repuesto(inventario)
        elif opcion == "6":
            exportar_csv(inventario)
        elif opcion == "0":
            guardar_inventario(inventario)
            print("  Datos guardados. ¡Hasta luego!")
            break
        else:
            # Entrada inválida: el programa no se rompe, solo avisa
            print("  ✗ Opción inválida. Ingresá un número del 0 al 6.")


# Punto de entrada
if __name__ == "__main__":
    main()
