# Reflexión final

**Nombre:** Arturo Guzmán Yonemoto

Reflexión sobre el reto de refactorización asistida por IA con Claude Code. El
detalle de cada cambio está en [`bitacora.md`](bitacora.md) y el plan en
[`PLAN.md`](../PLAN.md).

## ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?

Claude Code fue muy útil; en pocos minutos analizó el proyecto completo, identificó los code smells y propuso un plan priorizado antes de modificar el código. Con ese plan se aplicaron 9 refactorizaciones en commits atómicos, y ruff pasó de 20 errores a 0 sin romper ninguna prueba.

## ¿Qué propuso la IA que yo no había notado?

Además de los tests, la IA construyó una validación propia (una traza de ~1 500 casos comparada contra el código original), y con ella detectó detalles que yo no habría visto, por ejemplo: sum() redondea distinto que un bucle desde Python 3.12, una venta sin descuento guarda 0 entero y no 0.0, y un permiso en settings.json contenía una ruta personal que no debía subirse al repositorio.

## ¿En qué casos tuve que corregir o rechazar sus sugerencias?

Rechacé agregar type hints, decidí separar los print de los reportes y ajusté el flujo de trabajo: avanzar fase por fase según el plan creado, hacer push al final de cada fase, indicar la fase en cada commit y pedir que me explicara cada comando antes de ejecutarlo. Trabajé en modo PLAN para analizar los requerimientos y crear un plan, posteriormente pasé a trabajar en modo auto, sin embargo eso provocó que se agregaran unos settings que yo no pude validar en su momento, por lo cual opté por cambiar a un modo manual que me permitió validar cada paso antes de aprobarlo.

## ¿Qué aprendí sobre refactorizar con apoyo de IA?

La IA reduce drásticamente el tiempo de refactorización, pero el resultado depende del contexto: un buen prompt, un CLAUDE.md con reglas claras y un plan acordado evitan que tome decisiones por su cuenta fuera de lo esperado. El riesgo que veo es usarla para que haga todo el trabajo sin entender lo que hizo. Para mí es una herramienta, no un reemplazo: la IA propone, y el desarrollador valida, entiende y aprueba cada cambio, lo que exige conocer la tecnología. Vivimos un cambio profundo en la forma de desarrollar, y aprender a trabajar con IA ya es parte de nuestro oficio.

## Técnicas de prompting: qué funcionó y qué no

### Lo que funcionó

- **Prompt estructurado antes de tocar código.** El prompt inicial
  ([`prompt_base.md`](../prompt_base.md)) definía el contexto, un orden
  explícito (README → proyecto → plan → preguntas), el formato de cada
  actividad y restricciones claras ("no modifiques ningún archivo"). El
  resultado fue un diagnóstico completo y un plan revisable, no cambios
  precipitados.
- **Plan primero, ejecución después.** Usar el modo plan para el análisis y
  pedir que las decisiones importantes quedaran como preguntas pendientes
  evitó que la IA eligiera por su cuenta, por ejemplo si eliminar funciones
  públicas o corregir el bug de ruta.
- **Avanzar fase por fase con instrucciones cortas.** Una vez aprobado el plan,
  bastaban prompts breves como "continuamos" o "elimina el código muerto",
  porque el contexto ya estaba fijado. Sin el plan, esos mismos prompts habrían
  sido ambiguos.
- **Contexto persistente en `CLAUDE.md`.** Las reglas (no tocar tests,
  comportamiento idéntico, un cambio por commit) y las "trampas conocidas" que
  se fueron descubriendo quedaron escritas para toda la sesión, no solo en un
  prompt.
- **Restricciones técnicas, no solo escritas.** `.claude/settings.json` bloquea
  la edición de `tests/` y `pyproject.toml`, así que la regla más importante
  del reto no dependía de que la IA la recordara.
- **Pedir validación más allá de los tests.** Exigir que el comportamiento
  fuera idéntico llevó a comparar contra el código original, y eso detectó
  casos que los 20 tests no cubrían.
- **Reglas de trabajo explícitas.** Indicar cómo quería los commits, cuándo
  hacer push y que explicara cada comando antes de ejecutarlo hizo el proceso
  predecible y me permitió aprender de él.

### Lo que no funcionó o generó fricción

- **Pedir cambios estando en modo plan.** Al pedir que editara un archivo
  mientras seguía activo el modo plan, la IA no podía hacerlo y hubo que salir
  del modo primero. Conviene tener claro en qué modo se está antes de pedir
  una acción.
- **Aprobar permisos de forma permanente sin revisar dónde se guardan.**
  Aprobar un comando con "no volver a preguntar" agregó reglas al
  `settings.json` compartido del proyecto, una de ellas con una ruta personal.
  Esos permisos pertenecen a `settings.local.json`.
- **Instrucciones del curso contradictorias.** El README y los documentos de
  entrega no coincidían (destino del PR, ubicación de la bitácora). La IA no
  podía resolverlo sola: hubo que detectarlo y decidirlo explícitamente.
- **Confiar solo en "los tests pasan".** Las pruebas existentes no habrían
  detectado cambios en el redondeo, en los mensajes o en el formato de los
  tickets. Un prompt que solo pidiera "que pasen los tests" habría dado una
  falsa seguridad.

## Conclusión

La IA en el desarrollo de código es una herramienta invaluable que ayuda a reducir drásticamente los tiempos de desarrollo. Sin embargo, el éxito de los resultados depende en gran medida de las indicaciones que le demos. Dedicar tiempo a construir un buen prompt es crucial para que la IA ejecute las tareas con precisión; de hecho, podemos apoyarnos en la misma IA para perfeccionar estas instrucciones.

En este proceso, trazar un plan es fundamental. Con una estrategia clara podemos dar seguimiento a las acciones y evitar que la IA se desvíe del objetivo debido a un exceso de "creatividad". Por otro lado, aunque el tiempo de codificación disminuya, es vital invertir tiempo en validar y aprobar cada cambio. Si la IA no cuenta con el contexto adecuado, puede devolver un resultado visualmente correcto, pero respaldado por decisiones automáticas que choquen con el comportamiento esperado del negocio.

Sin duda alguna, el desarrollo de software actual está fuertemente influenciado por la IA. Esto ha traído un riesgo que ya estamos viviendo; muchos desarrolladores se limitan a pedirle código, arquitecturas o migraciones a la herramienta sin entender qué hace realmente detrás de escena, enfocándose solo en que el programa "funcione". Esto suele ocurrir cuando se dan instrucciones incompletas o al vuelo, sin un contexto profundo ni un plan de acción.

Desde mi punto de vista, la IA es una tecnología increíble, pero debe usarse como lo que es; una herramienta de asistencia, no un sustituto del pensamiento crítico. El desarrollador debe validar constantemente y sobre todo, comprender el código generado. Para lograr esto, se requiere un equipo con conocimientos técnicos sólidos. Estamos ante una revolución informática impresionante, y para nosotros los desarrolladores es indispensable aprender a desenvolvernos en este nuevo ecosistema, ya que el presente y el futuro de nuestra profesión están completamente ligados a la IA.
