"""Reglas de privacidad, validación y puntaje, sin conexión."""
import re
def sensible(texto):
    patrones = [r"(?<!\d)\d{8}-\d(?!\d)", r"(?<!\d)(?:\+503[\s-]?)?[267]\d{3}[\s-]?\d{4}(?!\d)",
        r"(?i)\b(?:contrase[nñ]a|password|clave)\s*[:=]\s*\S+", r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"]
    return any(re.search(p, texto) for p in patrones)
def validar_entrada(texto, maximo=500):
    if not texto.strip(): raise ValueError("Escribe un tema o añade contenido.")
    if len(texto) > maximo: raise ValueError(f"La entrada permite hasta {maximo} caracteres.")
    if sensible(texto): raise ValueError("Detectamos posibles datos personales. Elimínalos; no se enviaron a la IA.")
    return texto.strip()
def validar_quiz(datos):
    if not isinstance(datos, dict) or not isinstance(datos.get("preguntas"), list) or len(datos["preguntas"]) != 5:
        raise ValueError("La IA debe devolver cinco preguntas. Genera otro quiz.")
    for p in datos["preguntas"]:
        if not isinstance(p, dict) or not isinstance(p.get("pregunta"), str) or not p["pregunta"].strip():
            raise ValueError("Una pregunta llegó incompleta.")
        ops = p.get("opciones")
        if not isinstance(ops, list) or len(ops) != 4 or not all(isinstance(o, str) and o.strip() for o in ops) or len(set(ops)) != 4:
            raise ValueError("Cada pregunta necesita cuatro opciones diferentes.")
        if type(p.get("correcta")) is not int or p["correcta"] not in range(4):
            raise ValueError("Una respuesta correcta llegó dañada.")
        if not isinstance(p.get("explicacion"), str): raise ValueError("Falta una explicación.")
    return datos
def puntaje(preguntas, respuestas):
    return sum(r == p["correcta"] for p, r in zip(preguntas, respuestas))
def demo():
    ejemplos = [
        ("¿Qué lenguaje usa este proyecto?", ["Python", "Latín", "Solo HTML", "Francés"], 0),
        ("¿Qué protege una clave API?", ["El color", "El acceso al servicio", "La fuente", "El archivo"], 1),
        ("¿Quién calcula el puntaje?", ["La foto", "El micrófono", "Python", "El teclado"], 2),
        ("¿Qué significa validar?", ["Publicar", "Compartir claves", "Ignorar errores", "Comprobar las reglas"], 3),
        ("¿Puede equivocarse una IA?", ["Sí", "Nunca", "Solo sin pantalla", "Solo de noche"], 0)]
    return {"preguntas": [{"pregunta": q, "opciones": o, "correcta": c, "explicacion": "Respuesta: " + o[c]} for q, o, c in ejemplos]}



def validar_audio_pcm(pcm):
    """Descarta grabaciones vacías, demasiado cortas o prácticamente silenciosas."""
    import struct
    if len(pcm) < 16000:
        raise ValueError("La grabación fue muy corta. Pulsa Dictar, espera Grabando y habla durante al menos un segundo.")
    if len(pcm) % 2:
        pcm = pcm[:-1]
    muestras = [x[0] for x in struct.iter_unpack("<h", pcm)]
    rms = (sum(x*x for x in muestras) / len(muestras)) ** 0.5
    if rms < 40:
        raise ValueError("El audio llegó casi en silencio. Revisa el micrófono y habla más cerca.")
    return pcm

def validar_transcripcion(datos):
    if not isinstance(datos, dict) or datos.get("hay_voz") is not True:
        raise ValueError("No se distinguió una frase. Tu tema no se cambió; vuelve a grabar hablando claramente.")
    texto = datos.get("texto")
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("No se reconoció texto. Tu tema no se cambió.")
    return validar_entrada(texto)
