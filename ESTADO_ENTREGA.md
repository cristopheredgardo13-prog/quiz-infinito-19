# Revisión de la práctica y siguiente paso

Ejercicio 19: Quiz infinito. Revisión del 27 de octubre de 2026 a partir de los dos HTML docentes y las capturas compartidas.

## Lo comprobado
- El quiz generó preguntas reales con Gemini en la computadora, según la captura compartida por el estudiante.
- Se probó el juego completo en demostración con 5/5, el puntaje Python y el voto.
- La selección de foto funcionó: la captura muestra una imagen lista. La solicitud a Gemini falló después, por lo que R2 no está confirmado de extremo a extremo.
- Se corrigió la recuperación de errores transitorios y de red; no se ha demostrado todavía que el error de la foto esté resuelto con Gemini real.
- Se añadió optimización de imágenes a JPEG de hasta 1600 píxeles, con eliminación de metadatos.
- Pasaron 39 pruebas automatizadas locales, con respuestas de Google simuladas para los fallos de servicio. Estas pruebas no sustituyen al móvil real.
- La guía requiere publicación y prueba desde celular; el Space Static creado aún no ejecuta este proyecto.

## Estado por reto
| Reto | Implementación | Falta confirmar |
| --- | --- | --- |
| R1 Voz | Grabadora, 30 s, transcripción literal, rechazo de silencio | Dictado fiel y micrófono en HTTPS desde celular |
| R2 Foto | Selección y optimización de imagen | Quiz real basado en la foto |
| R3 Texto | Archivo UTF-8, campo y conteo Python | Carga y quiz real desde archivo en celular |
| R4 OCR | Extracción y texto editable | Lectura de un apunte real y uso como entrada |
| R5 Validación | Vacío, 500 caracteres, progreso, bloqueo de controles | Evidencia del flujo publicado |
| R6 Tarjetas | Pregunta y revisión final en tarjetas | Captura final real en el celular |
| R7 Memoria | Cinco interacciones enviadas como contexto | Segunda respuesta que demuestre recuerdo |
| R8 Preferencias | Nivel e idioma | Cambio real de idioma/dificultad |
| R9 Compartir | Clipboard y Share | Pegar el mismo texto en otra app del celular |
| R10 Voz de salida | Lectura con Microsoft TTS | Audio audible; registrar tres intentos si falla |
| R11 Identidad | Nombre, colores y bienvenida | Comprensión por otra persona en 10 segundos |
| R12 Errores | Límite de sesión, mensajes y reintentos acotados | Pruebas de fallos en la app publicada |
| R13 Responsable | Aviso y expresiones regulares en texto | Captura del rechazo local en la app publicada |
| R14 Votos | Un voto por quiz y contadores | Evidencia con varios quizzes reales |
| R15 Multimodal | Foto más pregunta dictada | Prueba integrada real en el celular |

## Orden a seguir
1. Terminar la publicación en Render usando GitHub y guardar Gemini como variable privada. Requiere iniciar sesión y crear la cuenta Render; no se ha desplegado todavía.
2. Abrir el enlace HTTPS en el teléfono y comprobar un quiz por texto.
3. Completar R1 a R5 y guardar cinco tarjetas con capturas.
4. Hacer la prueba cruzada con dos compañeros; completar R6 a R10.
5. Completar R11 a R15, reunir las 15 tarjetas y ensayar la demo de 60 segundos.
6. Entregar el enlace público, documento de tarjetas, demo y lista de logro.
La publicación alternativa en Render debe comunicarse al docente porque la guía pide un Space Docker.

## Condiciones de la entrega según el documento
- 15 % en total, 5 % por bloque de cinco retos, con posibles ajustes del docente.
- Cada reto completo requiere función publicada y prompt propio.
- Las tarjetas contienen prompt completo, número de intentos, fallo inicial, cómo se mejoró, enlace y captura.
- No se deben inventar intentos ni atribuir al estudiante los prompts redactados por el asistente.
- Dos compañeros deben probar la app y dejar comentarios reales.
- La fecha final contiene una contradicción: el documento dice viernes 29; el 29 de octubre de 2026 es jueves. Confirmar la fecha con el docente.

