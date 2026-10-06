# CLAUDE.md

Guía para Claude Code en este repositorio.

## Qué es este proyecto

Aplicación de consola en Python para la tienda "La Esquina": alta de productos,
ventas con descuentos e IVA, cotizaciones, alertas de stock bajo, reporte de
más vendidos y persistencia en JSON.

El objetivo del reto es **refactorizar `src/` sin cambiar el comportamiento**.
El programa ya funciona; no se agregan funcionalidades nuevas.

## Estructura

- `src/gestor.py`: lógica de productos y ventas, más el estado global
  (`INVENTARIO`, `VENTAS`, contador de folios, `ultimo_error`).
- `src/almacen.py`: carga y guardado del estado en JSON.
- `src/reportes.py`: reportes e indicadores.
- `src/main.py`: menú interactivo de consola.
- `tests/`: pruebas pytest de caja negra (20 pruebas).
- `pyproject.toml`: configuración de ruff y pytest.
- `BITACORA.md`: registro de cada refactorización.

## Comandos (Windows, desde la raíz del repo)

```bash
.venv/Scripts/python.exe -m pytest           # deben pasar las 20 pruebas
.venv/Scripts/python.exe -m ruff check src   # meta final: 0 errores
cd src && ../.venv/Scripts/python.exe main.py  # app interactiva (opcional)
```

## Reglas obligatorias

1. **No modificar `tests/` ni `pyproject.toml`.** Si un test falla, el error
   está en la refactorización, nunca en el test. Tampoco se desactivan reglas
   de ruff con `# noqa`.
2. **El comportamiento observable debe quedar idéntico**: valores de retorno,
   mensajes de `ultimo_error`, textos impresos y del ticket, formato de los
   montos y orden de los resultados.
3. **Conservar la API que usan los tests**: `agregarProducto` y
   `buscarProducto` mantienen su nombre; `gestor.INVENTARIO` (dict) y
   `gestor.VENTAS` (list) siguen siendo atributos del módulo, y
   `gestor.reiniciar_sistema()` los vacía.
4. **Una refactorización a la vez.** Después de cada una: correr `pytest` y
   `ruff check src`, revisar el diff, registrar la fila en `BITACORA.md` y
   hacer un commit atómico.
5. **No hacer commits ni push sin autorización explícita del usuario.**

## Trampas conocidas

- **Precisión flotante**: los tests comparan totales exactos (23.2, 661.2,
  2088.0, 647.28). Al extraer el cálculo de precios hay que conservar el orden
  de las operaciones y los puntos de redondeo.
- **`cotizar` y `registrar_venta` no son idénticas**: `cotizar` no aplica el
  descuento VIP, no valida stock, valida existencia antes que cantidad y no
  produce el error "codigo vacio". Solo se comparte el cálculo común
  (descuento por volumen + IVA).
- **Regla VIP**: el 2% extra se calcula sobre el subtotal y solo aplica si
  `subtotal - descuento > 200`.
- **Formato de montos**: se usa `str(round(v, 2))` (imprime `185.0`, no
  `185.00`). No cambiar a f-strings con `:.2f`.
- **Tipos de los montos**: sin descuento, `venta["descuento"]` es el entero
  `0` (no `0.0`), y el total de un día sin ventas se imprime `$0`. Inicializar
  acumuladores y descuentos con `0`, no con `0.0`.
- **No usar `sum()` para acumular montos**: desde Python 3.12 usa suma
  compensada y puede diferir del bucle original en el último decimal
  (10 × 0.1 → `0.9999999999999999` con bucle, `1.0` con `sum()`).
- **`mas_vendidos`**: el orden de los empates debe conservarse
  (`sorted(..., reverse=True)` es estable).
- **Contador de folios**: `almacen.py` lee y escribe `gestor.contador_ventas`;
  si se renombra, hay que actualizar ambos archivos en el mismo cambio.
- **Ruta de datos**: `main.py` abre `datos_ejemplo.json` relativo al
  directorio actual. Desde `src/` no encuentra el archivo de la raíz. Es
  comportamiento existente: no se corrige sin aprobación del usuario.

## Estilo

- PEP 8 y snake_case (salvo las dos excepciones de arriba), según ruff.
- Nombres descriptivos en español, igual que el código existente.
- Constantes en MAYÚSCULAS en lugar de números mágicos.
