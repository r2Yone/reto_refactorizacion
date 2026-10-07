# Plan de trabajo: refactorización asistida por IA

Este documento recoge el plan que se diseñó con Claude Code **antes de modificar
el código** y cómo se fue ejecutando. El análisis inicial se pidió con el prompt
de [`prompt_base.md`](prompt_base.md), que exigía analizar el README y el
proyecto, proponer un plan por fases y no cambiar nada hasta que el plan fuera
aprobado. El detalle de cada refactorización (prompt, cambio, justificación y
resultado de pruebas) está en [`BITACORA.md`](BITACORA.md).

## Resumen

| Fase | Objetivo | Estado |
|------|----------|--------|
| 0 | Preparar el entorno y medir la línea base | ✅ Completada |
| 1 | Configurar el proyecto para Claude Code | ✅ Completada |
| 2 | Refactorizar `src/` en pasos atómicos | ✅ Completada (9 refactorizaciones) |
| 3 | Validación final, reflexión y Pull Request | ✅ Completada |

| Métrica | Inicio | Final |
|---------|--------|-------|
| `pytest` | 20/20 | 20/20 (después de **cada** cambio) |
| `ruff check src` | 20 errores | **0 errores** |
| Archivos de `tests/` y `pyproject.toml` modificados | — | 0 |

## 1. Análisis previo

### Requisitos del README

- Crear `CLAUDE.md` y `.claudeignore`.
- Aplicar al menos 5 refactorizaciones significativas, una a la vez.
- Validar con `pytest` y `ruff check src` después de cada una.
- Documentar cada prompt en `BITACORA.md` y cerrar con una reflexión.
- Entregar por Pull Request con commits atómicos.
- **Restricciones:** no modificar `tests/` ni `pyproject.toml`; conservar los
  nombres `agregarProducto` y `buscarProducto`; mantener el comportamiento
  observable idéntico.

### Code smells detectados

| Archivo | Problemas principales |
|---------|-----------------------|
| `gestor.py` | `registrar_venta` gigante (6 responsabilidades, complejidad 12); lógica de descuento e IVA duplicada con `cotizar`; números mágicos; `if` anidados hasta 4 niveles; nombres crípticos (`x`, `aux`, `temp2`); `contadorVentas` en camelCase; código muerto |
| `almacen.py` | Archivos abiertos sin `with`; `hayArchivo` fuera de PEP 8 con un `if/else` innecesario |
| `reportes.py` | Import sin uso; `hacer_cosa` como nombre; ordenamiento de burbuja manual; número mágico duplicado; función obsoleta `reporteViejoCSV` |
| `main.py` | `menu()` con 8 `elif` y lógica de E/S en línea (complejidad 17); imports desordenados |

### Riesgos identificados antes de empezar

1. **Precisión flotante:** los tests comparan totales exactos, así que hay que
   conservar el orden de las operaciones y los puntos de redondeo.
2. **`cotizar` y `registrar_venta` no son idénticas** (VIP, validación de
   stock, orden y texto de los errores): solo se puede compartir el cálculo
   común.
3. **Estado global:** los tests leen `gestor.INVENTARIO` y `gestor.VENTAS`
   directamente, así que no se pueden encapsular.
4. **Formato de texto:** los montos se imprimen con `str(round(v, 2))`
   (`185.0`, no `185.00`).
5. **Estabilidad del orden** en `mas_vendidos` cuando hay empates.

## 2. Ejecución por fases

### Fase 0: Preparación del entorno

| Actividad | Resultado | Commit |
|-----------|-----------|--------|
| Repositorio y rama de trabajo `feature/refactorizacion` | Configurados | — |
| Entorno virtual con `pytest` y `ruff` | Instalados | — |
| Línea base | 20 pruebas pasan; 20 errores de ruff | — |
| `.gitignore` (cachés, `.DS_Store`, configuración local de Claude) | Completado | `5b8beaf`, `7c34da6` |
| Versionar el prompt de análisis | `prompt_base.md` | `025a87a` |

### Fase 1: Configuración para Claude Code

Un solo commit (`aad3ccc`) con:

- **`CLAUDE.md`:** contexto, comandos, reglas obligatorias y "trampas
  conocidas" que se fueron ampliando durante la Fase 2.
- **`.claudeignore`:** entorno virtual, cachés, `.git/` y datos generados.
- **`.claude/settings.json`:** prohíbe a Claude editar `tests/` y
  `pyproject.toml`, de modo que la regla del reto es una restricción técnica y
  no solo una instrucción escrita.
- **`BITACORA.md`:** creada a partir de la plantilla, con la línea base.

### Fase 2: Refactorizaciones

Se ordenaron de menor a mayor riesgo y cada una se validó con:

1. `pytest`.
2. `ruff check src`.
3. **Una traza de equivalencia:** un script auxiliar, fuera del repositorio,
   que ejecuta unos 1 500 casos (ventas, cotizaciones, errores, reportes,
   persistencia y una sesión completa del menú) sobre el código original y
   sobre el refactorizado, y compara las salidas.

| # | Refactorización | Ruff | Commit |
|---|-----------------|------|--------|
| R1 | Eliminar código muerto e imports sin uso | 20 → 13 | `171f3f6` |
| R2 | Constantes en lugar de números mágicos | 13 | `a50b934` |
| R3 | Extraer el cálculo de descuento e IVA duplicado | 13 → 11 | `0360149` |
| R4 | Dividir `registrar_venta` en funciones | 11 → 8 | `445f136` |
| R5 | Persistencia con `with` y nombres PEP 8 | 8 → 3 | `04e1fc0` |
| R6 | Nombres descriptivos y snake_case | 3 → 2 | `fde85b5` |
| R7 | `sorted` en lugar del bubble sort | 2 | `e60cde0` |
| R8 | Dividir `menu()` con un diccionario de despacho | 2 → **0** | `e6d7841` |
| R9 | Separar la impresión de los reportes (los `print` pasan a `main.py`) | 0 | `f8fee3b` |

### Fase 3: Cierre

| Actividad | Estado |
|-----------|--------|
| Validación final: 20/20 pruebas, ruff en 0, `tests/` y `pyproject.toml` sin cambios desde el commit inicial, prueba manual del menú | ✅ |
| Reflexión en `BITACORA.md` | ✅ |
| `PLAN.md` (este documento) | ✅ |
| Push y Pull Request `feature/refactorizacion` → `main` | ⏳ Pendiente de autorización |

## 3. Decisiones tomadas durante el plan

El plan dejó abiertas varias preguntas para que el desarrollador las decidiera
antes de cada fase, en lugar de que la IA las resolviera por su cuenta:

| Pregunta | Decisión |
|----------|----------|
| ¿Eliminar funciones públicas sin uso (`reporteViejoCSV`, `calcular_descuento_viejo`)? | Sí, se eliminaron (R1) |
| ¿Corregir el bug de ruta de `datos_ejemplo.json` al ejecutar desde `src/`? | No: cambiaría el comportamiento; se documentó en `CLAUDE.md` |
| ¿Mover los `print` de los reportes a `main.py`? | Sí (R9) |
| ¿Agregar type hints? | No |
| ¿Commits por archivo o por fase? | Un commit por refactorización, con la fase en el mensaje |
| ¿Cuándo hacer push? | Al final de cada fase |
| ¿Ignorar toda la carpeta `.claude/`? | No, solo `settings.local.json`; `settings.json` se versiona |

## 4. Desviaciones del plan original

- **R9:** el plan proponía agregar type hints. Se descartó por decisión del
  desarrollador y en su lugar se aplicó la separación de E/S en los reportes,
  que era otra decisión pendiente del plan.
- **Validación reforzada:** el plan solo contemplaba `pytest` y `ruff`. Se
  agregó la traza de equivalencia porque las 20 pruebas no cubren casos como
  el formato de los tickets, los mensajes de error o el menú.

## 5. Hallazgos que cambiaron decisiones de implementación

La traza de equivalencia y la revisión detectaron casos que los tests no cubren
y que obligaron a descartar soluciones aparentemente más limpias:

- **`sum()` no es equivalente a un bucle de suma** desde Python 3.12, porque
  usa suma compensada: 10 × 0.1 da `1.0` con `sum()` y `0.9999999999999999`
  con el bucle. Se conservaron los bucles.
- **Sin descuento, la venta guarda el entero `0` y no `0.0`.** Esto se ve en el
  JSON guardado y en el `$0` del resumen, así que se preservó.
- **`Counter.most_common(n)` no es equivalente** con `n` negativo; se usó
  `sorted`, que además es estable en los empates.

Estos hallazgos se agregaron a `CLAUDE.md` como reglas para futuros cambios.
