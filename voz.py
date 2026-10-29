"""Puente efímero entre la sesión Flet y los controles de voz del navegador."""
import secrets
import time
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from multimedia import ia_media
from logica import validar_entrada, validar_transcripcion
import asyncio

sesiones = {}

def crear_sesion(modo, texto, idioma, recibir=None, reservar=None):
    ahora = time.monotonic()
    for clave in list(sesiones):
        if sesiones[clave]["vence"] < ahora:
            sesiones.pop(clave, None)
    if len(sesiones) >= 500:
        raise ValueError("Hay demasiadas sesiones de voz. Intenta más tarde.")
    token = secrets.token_urlsafe(32)
    sesiones[token] = dict(modo=modo, texto=texto, idioma=idioma, recibir=recibir, reservar=reservar,
                           vence=ahora + 600, usos=0, ocupado=False)
    return token

def registrar_rutas(app: FastAPI):
    def obtener(token):
        s = sesiones.get(token)
        if not s or s["vence"] < time.monotonic():
            raise HTTPException(410, "Esta ventana caducó. Ábrela otra vez desde el quiz.")
        return s

    @app.get("/voz", response_class=HTMLResponse)
    async def pagina():
        return HTMLResponse(Path(__file__).with_name("voz.html").read_text(encoding="utf-8"),
                            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    @app.get("/api/voz/{token}")
    async def datos(token: str):
        s = obtener(token)
        return {k: s[k] for k in ("modo", "texto", "idioma")}

    @app.post("/api/voz/{token}/texto")
    async def texto(token: str, request: Request):
        s = obtener(token)
        if s["modo"] != "dictar" or not s["recibir"]: raise HTTPException(400)
        if int(request.headers.get("content-length", "0")) > 4000: raise HTTPException(413)
        body = await request.body()
        if len(body) > 4000: raise HTTPException(413)
        try:
            import json
            valor = validar_entrada(json.loads(body)["texto"])
            s["recibir"](valor)
        except (ValueError, KeyError, TypeError):
            raise HTTPException(400, "Revisa el tema: máximo 500 caracteres y sin datos personales.")
        return {"ok": True}

    @app.post("/api/voz/{token}/audio")
    async def audio(token: str, request: Request):
        s = obtener(token)
        if s["modo"] != "dictar" or s["usos"] >= 5 or s["ocupado"]:
            raise HTTPException(429, "Límite de esta ventana. Vuelve al quiz.")
        mime = request.headers.get("content-type", "").split(";")[0]
        if mime not in ("audio/webm", "audio/mp4", "audio/ogg", "audio/wav"):
            raise HTTPException(400, "Formato de audio no compatible.")
        contenido = bytearray()
        async for chunk in request.stream():
            contenido.extend(chunk)
            if len(contenido) > 2_000_000: raise HTTPException(413, "Graba menos de 30 segundos.")
        if len(contenido) < 100: raise HTTPException(400, "No se recibió audio.")
        s["ocupado"] = True
        s["usos"] += 1
        try:
            if s["reservar"]: s["reservar"]()
            resultado = await asyncio.to_thread(ia_media,
                'Transcribe literalmente la voz, sin responder ni completar. Si no hay voz inteligible devuelve '
                '{"hay_voz":false,"texto":""}. En otro caso devuelve JSON {"hay_voz":true,"texto":"transcripción literal"}.',
                bytes(contenido), mime, "", True)
            return {"texto": validar_transcripcion(resultado)}
        except (ValueError, RuntimeError) as error:
            raise HTTPException(400, str(error))
        finally:
            s["ocupado"] = False
