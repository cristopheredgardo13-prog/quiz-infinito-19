# Publicar Quiz infinito sin depender de CMD

Esta ruta conserva Python, Flet y Gemini. Cambia el alojamiento de Hugging Face Docker por Render porque el Space creado en la cuenta iud220 es Static y no puede ejecutar Python. El uso de una plataforma distinta debe comunicarse al docente.

## Resultado esperado
Un enlace HTTPS de Render que abre el quiz en cualquier teléfono. No requiere que la computadora permanezca encendida ni que haya una ventana CMD abierta.
El plan Free puede dormir tras 15 minutos sin tráfico y tardar aproximadamente un minuto en despertar. No es una garantía de disponibilidad permanente.

## Pasos de publicación
1. Crea un repositorio en tu cuenta GitHub llamado quiz-infinito-19. El código puede ser público; no contiene la clave.
2. Sube los archivos de esta carpeta respetando apps/ como carpeta. No subas .dependencias, .temporal, .env, claves ni credenciales.
3. En https://dashboard.render.com crea una cuenta o inicia sesión. Acepta tú las condiciones y completa las verificaciones.
4. Crea un New Web Service a partir del repositorio. Elige Docker y el plan Free. No elijas Static Site.
5. En Environment añade GEMINI_API_KEY con tu clave de Google AI Studio. No la escribas en el código.
6. Añade FLET_FORCE_WEB_SERVER con valor true. Render proporciona PORT automáticamente.
7. Despliega y espera Live. Conserva el enlace que Render asigne; no se puede conocer hasta crear el servicio.
8. Abre ese enlace desde tu celular, permite el micrófono cuando quieras usar voz y prueba el quiz con demostración desactivada.
Si usas Blueprints, render.yaml ya declara Docker, plan Free, comprobación de salud y las variables; GEMINI_API_KEY se solicita al configurar.

## Archivos principales
main.py, ia.py, multimedia.py, logica.py, requirements.txt, Dockerfile, .dockerignore, render.yaml, README.md y apps/ con __init__.py y quiz_infinito.py.
test_quiz.py permite ejecutar las pruebas. Los archivos .cmd y .ps1 solo ayudan a iniciar localmente.

## Antes de dar la entrega por terminada
- No basta con que Render diga Live: la IA debe generar preguntas de verdad.
- Prueba texto, imagen, archivo y voz en el teléfono con HTTPS.
- Confirma copiar/compartir y lectura audible.
- Captura pruebas reales y registra intentos, fallos y correcciones.
- Haz las pruebas cruzadas con dos compañeros.
- Presenta la demo de 60 segundos.
- Completa las 15 tarjetas; los prompts de referencia fueron redactados por el asistente y la práctica pide autoría propia.

Fuentes consultadas el 27 de octubre de 2026:
https://render.com/docs/free
https://render.com/docs/web-services
https://huggingface.co/docs/hub/spaces-overview

