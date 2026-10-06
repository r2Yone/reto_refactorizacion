"""Modulo principal del gestor de inventario y ventas de "La Esquina".

Aqui vive casi toda la logica del negocio. Historicamente este archivo
lo fueron parchando varias personas, asi que hay de todo un poco.
"""

from datetime import datetime

# ---------------------------------------------------------------
# Reglas de negocio: descuentos, impuestos y formato
# ---------------------------------------------------------------
TASA_IVA = 0.16

# Descuento por volumen: se aplica segun el subtotal de la compra
UMBRAL_DESCUENTO_ALTO = 1000
TASA_DESCUENTO_ALTO = 0.10
UMBRAL_DESCUENTO_MEDIO = 500
TASA_DESCUENTO_MEDIO = 0.05

# Clientes VIP: descuento extra si la compra ya con descuento supera el minimo
PREFIJO_VIP = "VIP"
TASA_DESCUENTO_VIP = 0.02
MONTO_MINIMO_VIP = 200

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

# ---------------------------------------------------------------
# Estado global de la aplicacion (inventario, ventas y contadores)
# ---------------------------------------------------------------
INVENTARIO = {}
VENTAS = []
contadorVentas = 0
ultimo_error = ""


def reiniciar_sistema():
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contadorVentas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contadorVentas = 0
    ultimo_error = ""


def agregarProducto(codigo, nombre, precio, stock):
    # valida los datos y da de alta un producto en el inventario
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return False
    if codigo in INVENTARIO:
        ultimo_error = "el producto ya existe"
        return False
    if precio <= 0:
        ultimo_error = "precio invalido"
        return False
    if stock < 0:
        ultimo_error = "stock invalido"
        return False
    x = {}
    x["codigo"] = codigo
    x["nombre"] = nombre
    x["precio"] = precio
    x["stock"] = stock
    INVENTARIO[codigo] = x
    return True


def eliminar_producto(codigo):
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = "producto no existe"
    return False


def actualizar_stock(codigo, cantidad):
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    aux = INVENTARIO[codigo]["stock"] + cantidad
    if aux < 0:
        ultimo_error = "el stock no puede quedar negativo"
        return False
    INVENTARIO[codigo]["stock"] = aux
    return True


def buscarProducto(texto):
    # busca productos cuyo nombre contenga el texto (sin importar mayusculas)
    temp2 = []
    for k in INVENTARIO:
        if texto.lower() in INVENTARIO[k]["nombre"].lower():
            temp2.append(INVENTARIO[k])
    return temp2


def _descuento_por_volumen(subtotal):
    """Descuento que corresponde al subtotal de una compra (0 si no aplica)."""
    if subtotal >= UMBRAL_DESCUENTO_ALTO:
        return subtotal * TASA_DESCUENTO_ALTO
    if subtotal >= UMBRAL_DESCUENTO_MEDIO:
        return subtotal * TASA_DESCUENTO_MEDIO
    return 0


def _calcular_iva(base):
    """IVA que se cobra sobre el monto ya descontado."""
    return base * TASA_IVA


def _calcular_descuento(subtotal, cliente):
    """Descuento total de una venta: por volumen mas el extra VIP.

    Los clientes cuyo codigo empieza con VIP reciben un extra, pero solo si
    su compra (ya con el descuento por volumen) pasa del monto minimo.
    """
    descuento = _descuento_por_volumen(subtotal)
    es_vip = bool(cliente) and cliente.startswith(PREFIJO_VIP)
    if es_vip and subtotal - descuento > MONTO_MINIMO_VIP:
        descuento = descuento + subtotal * TASA_DESCUENTO_VIP
    return descuento


def _validar_venta(codigo, cantidad):
    """Regresa el motivo por el que la venta no procede, o None si es valida."""
    if codigo is None or codigo == "":
        return "codigo vacio"
    if codigo not in INVENTARIO:
        return "producto no existe"
    if cantidad is None or cantidad <= 0:
        return "cantidad invalida"
    if INVENTARIO[codigo]["stock"] < cantidad:
        return "stock insuficiente"
    return None


def _generar_ticket(venta):
    """Arma el ticket en texto plano a partir del registro de la venta."""
    lineas = [
        "TIENDA LA ESQUINA",
        "----------------------------",
        "Folio: " + str(venta["folio"]),
        venta["nombre"] + " x" + str(venta["cantidad"]),
        "Subtotal: $" + str(venta["subtotal"]),
    ]
    if venta["descuento"] > 0:
        lineas.append("Descuento: -$" + str(venta["descuento"]))
    lineas.append("IVA: $" + str(venta["impuesto"]))
    lineas.append("TOTAL: $" + str(venta["total"]))
    return "\n".join(lineas) + "\n"


def registrar_venta(codigo, cantidad, cliente=""):
    """Registra una venta: valida, calcula importes, descuenta el stock,
    asigna folio y genera el ticket.

    Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contadorVentas, ultimo_error
    error = _validar_venta(codigo, cantidad)
    if error is not None:
        ultimo_error = error
        return None

    producto = INVENTARIO[codigo]
    subtotal = producto["precio"] * cantidad
    descuento = _calcular_descuento(subtotal, cliente)
    base = subtotal - descuento
    impuesto = _calcular_iva(base)

    producto["stock"] = producto["stock"] - cantidad
    contadorVentas = contadorVentas + 1
    venta = {
        "folio": contadorVentas,
        "codigo": codigo,
        "nombre": producto["nombre"],
        "cantidad": cantidad,
        "subtotal": round(subtotal, 2),
        "descuento": round(descuento, 2),
        "impuesto": round(impuesto, 2),
        "total": round(base + impuesto, 2),
        "cliente": cliente,
        "fecha": datetime.now().strftime(FORMATO_FECHA),
    }
    venta["ticket"] = _generar_ticket(venta)
    VENTAS.append(venta)
    return venta


def cotizar(codigo, cantidad):
    """Calcula cuanto costaria una compra sin registrar la venta."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return None
    subtotal = INVENTARIO[codigo]["precio"] * cantidad
    base = subtotal - _descuento_por_volumen(subtotal)
    return round(base + _calcular_iva(base), 2)
