"""Punto de entrada del gestor de tienda (menu interactivo en consola)."""

import almacen
import gestor
import reportes

ARCHIVO_DATOS = "datos_ejemplo.json"


def pedir_numero(mensaje):
    """Pide un numero al usuario hasta que escriba algo valido."""
    while True:
        respuesta = input(mensaje)
        try:
            return float(respuesta)
        except ValueError:
            print("Eso no es un numero, intenta de nuevo.")


def _mostrar_error():
    print("Error:", gestor.ultimo_error)


# ---------------------------------------------------------------
# Acciones del menu: cada una atiende una opcion.
# Regresan True solo cuando el programa debe terminar.
# ---------------------------------------------------------------
def opcion_agregar_producto():
    codigo = input("Codigo: ")
    nombre = input("Nombre: ")
    precio = pedir_numero("Precio: ")
    stock = int(pedir_numero("Stock inicial: "))
    if gestor.agregarProducto(codigo, nombre, precio, stock):
        print("Producto agregado.")
    else:
        _mostrar_error()


def opcion_registrar_venta():
    codigo = input("Codigo del producto: ")
    cantidad = int(pedir_numero("Cantidad: "))
    cliente = input("Codigo de cliente (enter si no tiene): ")
    venta = gestor.registrar_venta(codigo, cantidad, cliente)
    if venta is not None:
        print(venta["ticket"])
    else:
        _mostrar_error()


def opcion_cotizar():
    codigo = input("Codigo del producto: ")
    cantidad = int(pedir_numero("Cantidad: "))
    total = gestor.cotizar(codigo, cantidad)
    if total is not None:
        print("Total estimado (con IVA): $" + str(total))
    else:
        _mostrar_error()


def opcion_reporte_inventario():
    reportes.reporte_inventario()


def opcion_resumen_ventas():
    reportes.resumen_ventas()


def opcion_mas_vendidos():
    for codigo, unidades in reportes.mas_vendidos():
        print(codigo, "->", unidades, "unidades")


def opcion_stock_bajo():
    productos = reportes.productos_stock_bajo()
    if not productos:
        print("No hay productos con stock bajo.")
    for producto in productos:
        print("OJO:", producto["nombre"], "solo tiene", producto["stock"], "unidades")


def opcion_guardar_y_salir():
    almacen.guardar_datos(ARCHIVO_DATOS)
    print("Datos guardados. Hasta luego.")
    return True


# Opcion tecleada -> (texto que se muestra en el menu, accion que la atiende)
OPCIONES = {
    "1": ("Agregar producto", opcion_agregar_producto),
    "2": ("Registrar venta", opcion_registrar_venta),
    "3": ("Cotizar", opcion_cotizar),
    "4": ("Reporte de inventario", opcion_reporte_inventario),
    "5": ("Resumen de ventas", opcion_resumen_ventas),
    "6": ("Mas vendidos", opcion_mas_vendidos),
    "7": ("Alertas de stock bajo", opcion_stock_bajo),
    "8": ("Guardar y salir", opcion_guardar_y_salir),
}


def _cargar_datos_iniciales():
    if almacen.hay_archivo(ARCHIVO_DATOS):
        almacen.cargar_datos(ARCHIVO_DATOS)
        print("Datos cargados de", ARCHIVO_DATOS)


def _mostrar_menu():
    print("")
    for clave, (texto, _accion) in OPCIONES.items():
        print(clave + ") " + texto)


def menu():
    print("Bienvenido al gestor de la tienda La Esquina")
    _cargar_datos_iniciales()
    while True:
        _mostrar_menu()
        opcion = OPCIONES.get(input("Opcion: "))
        if opcion is None:
            print("Opcion no valida.")
            continue
        _texto, accion = opcion
        if accion():
            break


if __name__ == "__main__":
    menu()
