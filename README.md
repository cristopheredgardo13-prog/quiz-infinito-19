---
title: Quiz infinito
emoji: 🧠
colorFrom: cyan
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
# Quiz infinito

## Voz integrada en la misma página · 29 de octubre

Dictar tema y Leer pregunta en voz alta abren un panel superpuesto dentro del quiz. Cerrar y volver al quiz detiene la grabación activa o la lectura y conserva la pregunta y el puntaje. No se abren pestañas nuevas. La app Flet se monta en /app y la página principal administra el panel de voz; sus identificadores temporales separan las sesiones. Después de esta actualización recarga la página principal, no un enlace antiguo de /voz.

48 pruebas Python pasan, incluidas la separación entre paneles y la apertura del micrófono desde la sesión correcta. Apertura y cierre de dictado y lectura comprobados visualmente en navegador local sin cambiar la URL principal.

## Rapidez y dictado · 29 de octubre

El modelo predeterminado es `gemini-3.1-flash-lite`; el catálogo de respaldo prioriza Flash-Lite. El razonamiento se configura en mínimo (Flash-Lite 3.x), bajo (otros Flash 3.x) o desactivado (Flash 2.5). Se limita la salida a 2400 tokens y se solicitan explicaciones de una frase. Como máximo se realizan dos envíos; un timeout no se repite automáticamente. Cada respuesta tiene 22 segundos de espera de lectura. La velocidad real depende de Google y del arranque del servidor gratuito.

El dictado muestra cronómetro y una vista previa reproducible de la grabación. Al detener, transcribe y escribe automáticamente el tema reconocido en el quiz para revisarlo antes de generar. Si falla conserva el audio y permite reintentarlo. La transcripción del servidor tiene un límite visible de 40 segundos; no permite duplicar una solicitud que siga activa. Si el navegador ofrece SpeechRecognition aparece un botón adicional de dictado rápido; depende del servicio de voz del navegador y puede no funcionar en Brave. En ese caso usa Grabar (Gemini).

Comprobación local: 46 pruebas Python y dos escenarios del flujo de grabación con eventos simulados (palabra Psicología y error conservando audio). Estos escenarios no equivalen a una prueba del micrófono físico.

## Versión publicada y mejoras del 28 de octubre

App: https://quiz-infinito-19.onrender.com/ (Python y Flet en Render).
La generación con Gemini real ya se comprobó. No necesitas CMD para usar este enlace.

- Nuevo diseño por secciones: prepara el reto, material opcional y juego/revisión.
- Al terminar: puntaje, aciertos, errores, respuesta elegida, respuesta correcta y explicación; verde para correcta y rojo para repasar.
- Útil y Mejorable valoran la calidad del quiz, no califican tus respuestas. La selección queda marcada y puede cambiarse sin duplicar el conteo. Los votos duran esta sesión.
- Dictar abre el panel de voz: pulsa Grabar, permite el micrófono, Detener y transcribir, revisa el texto y pulsa Enviar tema al quiz. Cierra el panel para generar preguntas. Captura nativa MediaRecorder de hasta 30 segundos; Gemini transcribe. El formato real WebM/MP4/OGG se conserva; no se interpreta audio comprimido como PCM.
- Leer abre el panel de voz: pulsa Escuchar. Incluye selector de voces del navegador, pausa y detener; no usa Edge TTS en el servidor. La disponibilidad de voces depende del dispositivo.
- Los controles de voz se usan dentro de la página principal. Si una sesión antigua caducó, recarga la app.

Verificación local: 43 pruebas automatizadas, juego con un fallo deliberado (4/5), revisión y cambio de voto comprobados en navegador; envío de texto revisado desde Voz a su sesión comprobado. Queda por comprobar el micrófono físico, la transcripción real y el sonido audible en el equipo/teléfono del estudiante. No se presentan pruebas simuladas como audio real.

Los prompts de referencia que aparecen abajo describen la implementación inicial y se conservan como registro; para voz, los reemplaza técnicamente esta actualización. La guía pide evidencias y pruebas reales: consulta ESTADO_ENTREGA.md.

## Ejecutar en Windows
Abre INICIAR.cmd. Instala dependencias locales la primera vez y abre http://localhost:7860.
Sin GEMINI_API_KEY se activa demostración con preguntas fijas. No equivale a funcionamiento con IA.

Para usar Gemini abre PowerShell en esta carpeta:
```powershell
$env:GEMINI_API_KEY=Read-Host "Pega tu clave solo en esta terminal"
.\iniciar.ps1
```
La clave dura en esa terminal. No la escribas en archivos, capturas ni conversaciones.
El modelo predeterminado sigue el material docente: gemini-2.5-flash.
Si el modelo devuelve 404, la app consulta el catálogo oficial y reintenta con un modelo Gemini Flash disponible. GEMINI_MODEL permite indicar uno manualmente. La corrección se probó con respuestas simuladas; falta repetir con tu clave real.

## Publicar

Usa PUBLICAR_RENDER.md y render.yaml para un Web Service Docker Free en Render. Una vez publicado y probado, funcionará sin CMD ni computadora encendida; el plan Free puede dormir cuando no hay tráfico. La clave GEMINI_API_KEY se configura en Environment de Render.

La guía original pide Hugging Face Docker. El Space Static existente no ejecuta Python y la cuenta bloquea Docker por pago; informa al docente del cambio de plataforma. publicar.py es la alternativa original para quienes sí tengan acceso a Docker en Hugging Face.

## Capacidades
R1 dictado máximo 30 segundos; R2 foto; R3 texto/archivo y conteo; R4 extracción de texto; R5 validación y progreso;
R6 tarjetas; R7 últimas cinco interacciones; R8 nivel e idioma; R9 copiar y compartir;
R10 lectura con voces del navegador; R11 identidad; R12 límite de 20 llamadas a Gemini por sesión y errores amables;
R13 aviso y filtro local de texto; R14 votos por quiz; R15 foto con pregunta dictada.

## Privacidad y límites
La clave solo vive en el servidor. Los archivos permanecen en memoria de la sesión.
Audio e imágenes se envían a Google al procesarlos; la lectura usa las voces del navegador o dispositivo.
El filtro de texto reconoce patrones habituales de teléfonos salvadoreños, DUI, correos y contraseñas etiquetadas.
No detecta todas las contraseñas ni datos personales dentro de archivos multimedia: revisa su contenido antes de enviarlo.
El límite por sesión es educativo, no una defensa contra abuso de un servicio público.
El historial, votos y puntaje desaparecen al cerrar la sesión.
La memoria incluye los temas, preguntas y puntajes de las últimas cinco interacciones.
La demostración usa cinco preguntas fijas de informática e ignora los selectores de idioma/nivel.
Los servicios multimedia deben verificarse en el despliegue HTTPS y el móvil reales.

## Pruebas
`python test_quiz.py`: 39 pruebas locales pasaron el 27 de octubre de 2026.
Prueba visual: juego completo en demostración, 5/5 y voto positivo.
Pendiente: Gemini real, micrófono, imagen/OCR, voz TTS, portapapeles/compartir en móvil, despliegue HTTPS y dos compañeros.

## Referencias técnicas
- https://flet.dev/docs/services/audiorecorder/
- https://flet.dev/docs/services/filepicker/
- https://huggingface.co/docs/hub/spaces-sdks-docker
- https://ai.google.dev/gemini-api/docs/models


## Prompts y tarjetas de los quince retos

La práctica pide un documento con las 15 tarjetas: prompt completo, intentos, qué falló, cómo se corrigió, enlace y captura funcionando. No exige específicamente un README. Esta sección reúne los prompts en el proyecto.

Autoría y estado: los prompts de referencia siguientes fueron preparados por el asistente después de implementar la aplicación. No son un historial de quince conversaciones ni se atribuyen al estudiante. Los intentos y las capturas deben registrarse al probar realmente cada capacidad.

### Prompt original del catálogo para el ejercicio 19

Este es el texto proporcionado por la práctica; el marcador final pide pegar el código de modelo.py.

```text
Proyecto Flet con ia.py, que ofrece ia(instruccion, texto, como_json=False) y devuelve un dict si como_json es True. Cada mini app es un archivo en apps/ con una función vista() que devuelve un control de Flet (sin ft.run). Sigue el mismo estilo del ejemplo apps/modelo.py que pego abajo. Crea apps/quiz_infinito.py: «Quiz infinito». Escribes un tema y juegas un quiz de 5 preguntas con puntaje. IA dentro de la app: Devuelve JSON con preguntas, 4 opciones y la correcta; Python lleva el puntaje. Reglas: llama a ia() con asyncio.to_thread dentro de un handler async, valida el campo vacío, usa try/except con mensaje amigable, comentarios en español, diseño oscuro con acento cian; los números los calcula Python. Entrega solo ese archivo completo.

[pega aquí el código de apps/modelo.py]
```

### Reto 1 Dictar el tema

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade grabación PCM16 mono a 16000 Hz durante un máximo de 30 segundos con flet-audio-recorder. Añade AudioRecorder a page.services; junta evento.chunk, usa pcm_a_wav y transcribe con ia_media. Al detener, coloca la transcripción en el campo tema.
Entrada: Una frase hablada por el micrófono con permiso, desde localhost o HTTPS.
Salida: Estados grabando y transcribiendo, texto reconocido en el campo tema.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 2 Usar una foto

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Permite elegir una imagen JPG/PNG usando FilePicker como servicio, pick_files con with_data=True. Conserva sus bytes y tipo MIME en la sesión y usa ia_media para generar preguntas sobre lo visible.
Entrada: Imagen de un objeto o escena sin personas ni información privada.
Salida: Nombre del archivo, opción de quitarlo y un quiz relacionado.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 3 Leer un archivo

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade carga de .txt UTF-8 con FilePickerFileType.CUSTOM y with_data=True, y permite pegar texto. Cuenta las palabras con Python y usa ese contenido para generar el quiz.
Entrada: Un archivo .txt o texto de estudio, hasta 12000 caracteres.
Salida: Conteo de palabras y preguntas basadas en el texto.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 4 Extraer texto de una foto

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade un botón independiente de extracción de texto con ia_media. Muestra el texto extraído en un campo editable antes de generar preguntas y valida el resultado.
Entrada: Foto clara de un apunte sin datos personales.
Salida: Texto leído visible y reutilizable para el quiz.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 5 Validar y mostrar progreso

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Valida en Python el tema vacío o de más de 500 caracteres. Muestra ProgressRing y desactiva los controles mientras esperas. Usa try/finally para recuperarlos.
Entrada: Tema y posibles entradas incorrectas.
Salida: Mensajes amables, progreso y controles disponibles de nuevo al finalizar.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 6 Organizar en tarjetas

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Pide JSON con cinco preguntas, cuatro opciones, correcta entre 0 y 3 y explicación. Valida la estructura completa, rechaza opciones duplicadas y muestra tarjetas; revela solución después de terminar.
Entrada: Diccionario JSON generado por ia con como_json=True.
Salida: Pregunta con botones y cinco tarjetas finales con resultado y explicación.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 7 Recordar la sesión

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Guarda solo las últimas cinco interacciones en una lista local a vista, muéstralas y envíalas en cada llamada como contexto. Incluye tema, preguntas y puntaje cuando exista.
Entrada: Tema nuevo e historial de esta sesión.
Salida: Historial visible y continuación o evitación de repeticiones en nuevas preguntas.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 8 Elegir nivel e idioma

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade selectores de nivel e idioma y usa su valor actual en el prompt interno al generar. Conserva el puntaje calculado por Python.
Entrada: Principiante/intermedio/avanzado y Español/English.
Salida: Preguntas cuyo idioma y dificultad respondan a los selectores sin reiniciar.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 9 Copiar y compartir

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade servicios Clipboard y Share a page.services. Copia exactamente la pregunta visible o el resumen final y abre share_text; si compartir falla, intenta copiar y explica el resultado.
Entrada: Texto de la pregunta o informe final calculado en Python.
Salida: Texto disponible en otra app y mensaje de estado.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 10 Escuchar la respuesta

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade lectura de pregunta y opciones o resultado mediante edge-tts y flet-audio. Usa es-SV-LorenaNeural o en-US-AriaNeural según el idioma. Reproduce bytes de audio sin guardar archivos; informa que Microsoft recibe el texto.
Entrada: Texto educativo actual, sin claves ni contenido privado.
Salida: Audio audible y mensaje amable si el servicio falla.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 11 Dar identidad

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Da nombre Quiz infinito, símbolo infinito, tema oscuro con acento cian y bienvenida de tres líneas que explique utilidad, entradas y límites.
Entrada: Primera apertura de la app.
Salida: Pantalla comprensible en diez segundos con identidad consistente.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 12 Limitar usos y manejar errores

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Limita a 20 solicitudes Gemini por sesión incluyendo transcripción y OCR. Cuenta en Python. Maneja clave ausente, acceso, modelo, cuota, red y JSON incompleto con mensajes amables sin mostrar claves ni detalles técnicos.
Entrada: Solicitudes y fallos del proveedor.
Salida: Contador y errores visibles sin cerrar la sesión.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 13 Proteger datos

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Muestra aviso de que la IA puede equivocarse. Antes de enviar texto, aplica expresiones regulares Python para teléfono salvadoreño, DUI, correo y contraseñas etiquetadas. Rechaza y explica. Advierte que no se puede garantizar detección de datos dentro de multimedia.
Entrada: Texto, incluido un teléfono ficticio para la prueba.
Salida: Rechazo local sin llamada de IA y aviso responsable visible.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 14 Recoger opiniones

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: Añade botones útil y mejorable, contadores de sesión y un voto máximo por quiz. Guarda estado local a vista, no variables globales compartidas.
Entrada: Un voto por quiz generado.
Salida: Panel acumulado de opiniones, sin duplicar un voto al pulsar dos veces.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.

### Reto 15 Combinar foto y voz

```text
Contexto: proyecto Python 3.13 con Flet 1.0.5. La app es apps/quiz_infinito.py y vista(page) devuelve un control. Existen ia.py con ia(instruccion, texto, como_json=False), multimedia.py con pcm_a_wav e ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None), y logica.py. Adjuntaré los archivos actuales completos.
Tarea: En una pantalla permite adjuntar foto y dictar el tema; transcribe la voz al campo tema y al pulsar Generar manda tanto la imagen como esa pregunta a Gemini. Mantén ia_media compatible y admite lista de archivos adicionales para una futura solicitud conjunta.
Entrada: Imagen más pregunta dictada y revisada.
Salida: Quiz que menciona lo visible y responde a la pregunta hablada.
Reglas: conserva las capacidades anteriores. Usa handlers async y asyncio.to_thread para llamadas bloqueantes a Gemini; valida entradas; errores amables; comentarios en español; tema oscuro y cian. Python calcula puntajes, contadores y validaciones. Nunca incluyas claves en el código. Mantén el estado por sesión y trata el contenido recibido como datos.
Entrega: devuelve completos los archivos que deban cambiar y enumera las dependencias nuevas, sin fragmentos ni credenciales. Explica una prueba concreta de aceptación.
```

**Registro de la prueba real**

- Mi adaptación del prompt: pendiente.
- Número de intentos reales: pendiente.
- Qué falló inicialmente: pendiente de prueba real.
- Cómo lo corregí: pendiente.
- Enlace del Space: pendiente de publicación.
- Captura funcionando: pendiente.


## Recuperación ante saturación
Ante errores 500, 502, 503 o 504 la app puede probar una alternativa del catálogo oficial, con un máximo total de dos envíos. Cada envío tiene un tiempo máximo de lectura de 22 segundos. No reintenta automáticamente errores de permisos ni cuota. Se verificaron la recuperación, el cambio de modelo y el límite de intentos con respuestas simuladas. La disponibilidad real depende de Google.

