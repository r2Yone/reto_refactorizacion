"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

# Un producto con menos unidades que este minimo se reporta como stock bajo
STOCK_MINIMO = 5


def formatear_dinero(monto):
    """Da formato de dinero a un monto, p. ej. 185.0 -> "$185.0"."""
    return "$" + str(round(monto, 2))


def productos_stock_bajo():
    """Regresa la lista de productos con stock por debajo del minimo."""
    return [
        producto
        for producto in gestor.INVENTARIO.values()
        if producto["stock"] < STOCK_MINIMO
    ]


def reporte_inventario():
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    reporte = "===== INVENTARIO =====\n"
    valor_total = 0
    for producto in gestor.INVENTARIO.values():
        linea = (
            producto["codigo"] + " | " + producto["nombre"] + " | "
            + formatear_dinero(producto["precio"])
            + " | stock: " + str(producto["stock"])
        )
        if producto["stock"] < STOCK_MINIMO:
            linea = linea + "  <-- STOCK BAJO"
        reporte = reporte + linea + "\n"
        valor_total = valor_total + producto["precio"] * producto["stock"]
    reporte = reporte + "Valor total del inventario: "
    reporte = reporte + formatear_dinero(valor_total) + "\n"
    print(reporte)
    return reporte


def total_vendido():
    """Suma el total (con IVA) de todas las ventas registradas."""
    # Bucle explicito a proposito: sum() usa suma compensada desde
    # Python 3.12 y podria diferir en el ultimo decimal.
    total = 0
    for venta in gestor.VENTAS:
        total = total + venta["total"]
    return round(total, 2)


def mas_vendidos(n=3):
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    unidades_por_codigo = {}
    for venta in gestor.VENTAS:
        codigo = venta["codigo"]
        unidades_por_codigo[codigo] = (
            unidades_por_codigo.get(codigo, 0) + venta["cantidad"]
        )
    # sorted es estable: en empates se conserva el orden de la primera venta
    ranking = sorted(
        unidades_por_codigo.items(), key=lambda par: par[1], reverse=True
    )
    return ranking[:n]


def resumen_ventas():
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    reporte = "===== RESUMEN DE VENTAS =====\n"
    total_dia = 0
    for venta in gestor.VENTAS:
        reporte = reporte + "Folio " + str(venta["folio"]) + ": " + venta["nombre"]
        reporte = reporte + " x" + str(venta["cantidad"]) + " = "
        reporte = reporte + formatear_dinero(venta["total"]) + "\n"
        total_dia = total_dia + venta["total"]
    reporte = reporte + "Numero de ventas: " + str(len(gestor.VENTAS)) + "\n"
    reporte = reporte + "Total del dia: " + formatear_dinero(total_dia) + "\n"
    print(reporte)
    return reporte
