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
| 3  |              |                  |               |          |
| 4  |              |                  |               |          |
| 5  |              |                  |               |          |

> Agrega más filas si realizas más de 5 refactorizaciones.

## Reflexión final (10-15 líneas)

Responde:

- ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
- ¿Qué propuso la IA que tú no habías notado?
- ¿En qué casos tuviste que corregir o rechazar sus sugerencias?
- ¿Qué aprendiste sobre refactorizar con apoyo de IA?

*(Escribe aquí tu reflexión)*
