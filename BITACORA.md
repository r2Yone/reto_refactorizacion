# Bitácora de refactorización

**Nombre:** Arturo Guzmán Yonemoto

**Matrícula:** Pendiente

**Fecha:** 06 Octubre 2026

Registra aquí **cada refactorización** que realices con Claude Code. Copia el
prompt tal cual lo escribiste (o un resumen fiel si fue una conversación larga),
describe el cambio que se aplicó al código y justifica por qué mejora la calidad.
Después de cada cambio ejecuta `pytest` y anota el resultado.

## Línea base (antes de refactorizar)

- `pytest`: **20 passed**.
- `ruff check src`: **20 errores**: UP009 ×4, SIM115 ×3, SIM102 ×3, N802 ×2,
  C901 ×2 (`registrar_venta` 12, `menu` 17), N816, SIM108, SIM103, UP015,
  I001, F401.

## Refactorizaciones

| #  | Prompt usado | Cambio realizado | Justificación | Tests OK |
|----|--------------|------------------|---------------|----------|
| 1  | "Elimina el código muerto" (tras aprobar el plan de refactorización generado a partir de `prompt_base.md`) | Se eliminaron `calcular_descuento_viejo` y el bloque comentado `exportar_txt` (gestor), la constante sin uso `MODO_DEBUG`, `reporteViejoCSV` e `import os` (reportes), y la declaración `# -*- coding: utf-8 -*-` de los 4 módulos. Antes de borrar se verificó con búsqueda que nada en `src/` ni `tests/` los usara. | El código que nadie llama confunde al lector y hay que mantenerlo sin que aporte nada; Git ya conserva la historia "por si acaso". El encabezado de codificación sobra en Python 3, donde UTF-8 es el default. Ruff: 20 → 13 (se resolvieron F401, N802, SIM115 y UP009 ×4). | ✅ 20/20 |
| 2  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R2, constantes para números mágicos) | Se crearon constantes con nombre para las reglas de negocio: `TASA_IVA`, `UMBRAL_DESCUENTO_ALTO/MEDIO`, `TASA_DESCUENTO_ALTO/MEDIO`, `PREFIJO_VIP`, `TASA_DESCUENTO_VIP`, `MONTO_MINIMO_VIP` y `FORMATO_FECHA` (gestor), y `STOCK_MINIMO` (reportes). Se reemplazaron los literales en `registrar_venta`, `cotizar`, `productos_stock_bajo` y `reporte_inventario`. | `0.16` o `200` no dicen qué significan, y los mismos valores estaban repetidos en dos funciones: cambiar el IVA obligaba a buscar cada aparición. Ahora cada regla tiene un nombre y un solo lugar. Además de pytest, se validó con una traza de 1502 casos comparada contra el código original: idéntica. Ruff sigue en 13 (no hay regla de ruff para números mágicos). | ✅ 20/20 |
| 3  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R3, extraer el cálculo de precios duplicado) | Se extrajeron `_descuento_por_volumen(subtotal)` y `_calcular_iva(base)` en gestor. `registrar_venta` y `cotizar` ahora las usan en lugar de repetir los `if` de descuento y la multiplicación por el IVA; `cotizar` quedó en 3 líneas de cálculo. Se respetó el orden exacto de las operaciones y que el descuento sin rebaja siga siendo el entero `0`. | La regla de descuento por volumen estaba copiada en dos funciones: si cambiaba, había que acordarse de editar ambas o la cotización dejaría de coincidir con la venta. Ahora hay una sola fuente de verdad. Con guard clauses (`return` temprano) desaparece el `else: if` anidado. Ruff: 13 → 11 (se resolvieron SIM108 y C901 de `registrar_venta`, que bajó de 12 a ≤10). Traza de equivalencia: idéntica. | ✅ 20/20 |
| 4  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R4, dividir `registrar_venta`) | `registrar_venta` se dividió en funciones con una sola responsabilidad: `_validar_venta` (guard clauses en lugar de 4 `if` anidados; regresa el motivo del error), `_calcular_descuento` (volumen + VIP en una sola condición con `startswith`), `_generar_ticket` (lista de líneas unidas con `join` en lugar de concatenar `t = t + ...`). El registro de la venta se arma con un literal de diccionario. Se renombraron `temp2`/`aux`/`desc` → `producto`/`subtotal`/`descuento`. | La función hacía 6 cosas distintas en 70 líneas con 8 niveles de anidamiento; ahora `registrar_venta` se lee como una receta y cada paso se puede entender por separado. Se conservaron el orden de las validaciones, los mensajes de error y el orden de las claves del registro (se guarda en JSON). La línea "Descuento" del ticket ahora depende del valor redondeado, lo cual es equivalente porque el descuento es 0 o ≥ $4. Ruff: 11 → 8 (SIM102 ×3). Traza de equivalencia: idéntica. | ✅ 20/20 |
| 5  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R5, persistencia segura y nombres PEP 8 en `almacen`) | En `almacen.py`, los archivos se abren con `with open(...)` en lugar de `open()`/`close()` manuales; se quitó el modo `"r"` redundante; los bucles de copia se reemplazaron por `dict.update` y `list.extend`; `d`/`f` → `datos`/`archivo`; `hayArchivo` → `hay_archivo`, que ahora regresa directamente `os.path.exists(ruta)` en lugar del `if/else` con `True`/`False`. Se actualizó la llamada en `main.py`. | Con `open()`/`close()` manual, si `json.dump` o `json.load` fallan el archivo puede quedar abierto (el original incluso tenía que acordarse de cerrarlo en el `except`); `with` lo garantiza siempre. `hayArchivo` violaba PEP 8 y envolvía un booleano en un `if` innecesario. Ruff: 8 → 3 (SIM115 ×2, UP015, N802, SIM103). Traza de equivalencia (guardar, cargar, archivo inexistente y corrupto): idéntica. | ✅ 20/20 |

| 6  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R6, nombres descriptivos y snake_case) | `contadorVentas` → `contador_ventas` (gestor y almacen en el mismo cambio); `hacer_cosa` → `formatear_dinero`; `x`/`aux`/`temp2`/`k`/`s`/`t`/`p`/`v` → `producto`, `nuevo_stock`, `reporte`, `valor_total`, `total_dia`, `venta`. Los comentarios de `agregarProducto` y `buscarProducto` pasaron a docstrings; `buscarProducto` y `productos_stock_bajo` usan comprensión de listas sobre `.values()`. Los nombres de `agregarProducto` y `buscarProducto` se conservan porque los usan los tests. | Nombres como `hacer_cosa` o `temp2` obligan a leer el cuerpo para saber qué hacen; el estilo mixto (camelCase y snake_case) viola PEP 8. **Hallazgo:** se decidió *no* cambiar los bucles de suma por `sum()`: desde Python 3.12, `sum()` usa suma compensada y da otro resultado (se comprobó: 10 × 0.1 da `0.9999999999999999` con el bucle y `1.0` con `sum()`). Se dejó un comentario explicándolo. Ruff: 3 → 2 (N816). Traza de equivalencia: idéntica. | ✅ 20/20 |
| 7  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R7, simplificar `mas_vendidos`) | El ordenamiento de burbuja manual (dos bucles anidados con intercambio) se reemplazó por `sorted(..., key=..., reverse=True)`, y el conteo con `if/else` por `dict.get(codigo, 0)`. Se eliminó el `TODO` que ya pedía usar `sorted`. | 17 líneas de algoritmo O(n²) escrito a mano se vuelven 2 instrucciones estándar, más fáciles de leer y sin riesgo de errores de índice. `sorted` es estable, así que los empates conservan el orden de la primera venta, igual que la burbuja con `<`. Se descartó `Counter.most_common(n)`: con `n` negativo regresa `[]`, mientras que el original regresa todos menos los últimos. Se agregaron esos casos a la traza: idéntica. Ruff: se mantiene en 2. | ✅ 20/20 |
| 8  | "Continuamos; haz un commit por cada refactorización" (siguiente paso del plan: R8, dividir `menu()`) | La cadena de 8 `if/elif` de `menu()` se reemplazó por un diccionario de despacho `OPCIONES` (opción → texto y función). Cada opción quedó en su propia función (`opcion_agregar_producto`, `opcion_registrar_venta`, …); el menú en pantalla se genera a partir del mismo diccionario. Se extrajeron `_mostrar_error`, `_mostrar_menu` y `_cargar_datos_iniciales`; se ordenaron los imports y se renombraron `c`/`n`/`p`/`s`/`cant`/`cli`/`v`/`t` y `ARCHIVO` → `ARCHIVO_DATOS`. | `menu()` mezclaba la navegación con la lógica de las 8 opciones (complejidad 17). Ahora agregar o cambiar una opción toca un solo lugar, y el texto del menú no puede desincronizarse de lo que hace cada opción. La traza de equivalencia simula una sesión completa del menú (todas las opciones, opciones inválidas, entradas no numéricas y errores, con y sin archivo de datos) y compara cada línea impresa y cada prompt: idéntica. Ruff: 2 → **0** (C901, I001). | ✅ 20/20 |
| 9  | "Mueve los print a main" (respuesta a la decisión pendiente P4 del plan) | `reporte_inventario` y `resumen_ventas` ya no imprimen: solo arman y regresan el texto. `main.py` es ahora quien lo imprime (`print(reportes.reporte_inventario())`). Se actualizaron los docstrings. | Separa la lógica de la entrada/salida: el módulo de reportes produce datos y la interfaz de consola decide qué mostrar. Así los reportes se pueden reutilizar (guardar en archivo, enviar, probar) sin efectos secundarios en pantalla. La traza mostró exactamente 3 diferencias, todas esperadas: lo que se imprimía al llamar esas funciones directamente; el texto regresado y la sesión completa del menú son idénticos. Ruff: 0. | ✅ 20/20 |

> Agrega más filas si realizas más de 5 refactorizaciones.

## Reflexión final (10-15 líneas)

Responde:

- ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
- ¿Qué propuso la IA que tú no habías notado?
- ¿En qué casos tuviste que corregir o rechazar sus sugerencias?
- ¿Qué aprendiste sobre refactorizar con apoyo de IA?

*(Escribe aquí tu reflexión)*
