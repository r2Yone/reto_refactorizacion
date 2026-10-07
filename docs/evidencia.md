# Evidencia de pruebas y linter

Salida de los comandos de validación sobre el código final de `src/`.

| Dato | Valor |
|------|-------|
| Fecha | 2026-10-06 |
| Último commit que modifica `src/` | `f8fee3b`: refactor: Fase 2. R9 separar impresión de los reportes |
| Python | 3.14.8 (Windows) |
| pytest | 9.1.1 |
| ruff | 0.16.10 |

## Resumen

| Validación | Línea base (antes) | Final |
|------------|--------------------|-------|
| `pytest` | 20 passed | **20 passed** |
| `ruff check src` | 20 errores | **0 errores** |
| Cambios en `tests/` y `pyproject.toml` | — | **Ninguno** (`git diff c93b297 -- tests pyproject.toml` vacío) |

Las pruebas también pasaron después de **cada** refactorización (ver la columna
"Tests OK" en [`bitacora.md`](bitacora.md)).

## `pytest -v`

Las rutas absolutas se abreviaron y se omitió el tiempo de ejecución.

```text
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.6.0 -- .venv\Scripts\python.exe
rootdir: reto-refactorizacion
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================= 20 passed ==============================
```

## `ruff check src`

```text
All checks passed!
```

Línea base, antes de refactorizar (`ruff check src` sobre el commit inicial
`c93b297`): **20 errores**: UP009 ×4, SIM115 ×3, SIM102 ×3, N802 ×2, C901 ×2
(`registrar_venta` 12, `menu` 17), N816, SIM108, SIM103, UP015, I001, F401.

## Validación adicional de equivalencia

Además de pytest, después de cada refactorización se ejecutó una traza de
~1 500 casos (ventas con distintos precios, cantidades y clientes,
cotizaciones, errores, reportes, guardado/carga y una sesión completa del menú)
sobre el código original y sobre el refactorizado, comparando las salidas. El
resultado fue idéntico en todos los pasos, salvo en R9, donde aparecieron
exactamente las 3 diferencias esperadas (los reportes ya no imprimen al
llamarse directamente). El menú siguió siendo idéntico.
