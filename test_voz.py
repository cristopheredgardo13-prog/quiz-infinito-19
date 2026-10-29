import unittest
from unittest.mock import patch
import httpx
from fastapi import FastAPI
import voz

class Voz(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        voz.sesiones.clear()
        app = FastAPI()
        voz.registrar_rutas(app)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        voz.sesiones.clear()

    async def test_sesion_aislada_y_caducidad(self):
        token = voz.crear_sesion("leer", "Pregunta de prueba", "Español")
        r = await self.client.get("/api/voz/" + token)
        self.assertEqual(r.json()["texto"], "Pregunta de prueba")
        self.assertNotIn("recibir", r.json())
        self.assertEqual((await self.client.get("/api/voz/desconocido")).status_code, 410)
        voz.sesiones[token]["vence"] = 0
        self.assertEqual((await self.client.get("/api/voz/" + token)).status_code, 410)

    async def test_tema_revisado_llega_solo_a_su_quiz(self):
        uno, dos = [], []
        a = voz.crear_sesion("dictar", "", "Español", uno.append)
        voz.crear_sesion("dictar", "", "Español", dos.append)
        r = await self.client.post(f"/api/voz/{a}/texto", json={"texto":"redes informáticas"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(uno, ["redes informáticas"])
        self.assertEqual(dos, [])
        self.assertEqual((await self.client.post(f"/api/voz/{a}/texto", json={"texto":"x"*501})).status_code,400)

    async def test_audio_real_usa_mime_y_devuelve_transcripcion_revisable(self):
        token = voz.crear_sesion("dictar", "", "Español", lambda _:None)
        with patch("voz.ia_media", return_value={"hay_voz":True,"texto":"sistema solar"}) as ia:
            r = await self.client.post(f"/api/voz/{token}/audio", content=b"audio de prueba"*100, headers={"Content-Type":"audio/webm;codecs=opus"})
            self.assertEqual(r.json(), {"texto":"sistema solar"})
            self.assertEqual(ia.call_args.args[2], "audio/webm")
        self.assertEqual((await self.client.post(f"/api/voz/{token}/audio",content=b"x"*200,headers={"Content-Type":"text/html"})).status_code,400)

    async def test_audio_rechaza_silencio_y_limita_uso(self):
        token = voz.crear_sesion("dictar", "", "Español", lambda _:None)
        with patch("voz.ia_media", return_value={"hay_voz":False,"texto":""}):
            r = await self.client.post(f"/api/voz/{token}/audio",content=b"x"*200,headers={"Content-Type":"audio/mp4"})
            self.assertEqual(r.status_code,400)
        voz.sesiones[token]["usos"] = 5
        self.assertEqual((await self.client.post(f"/api/voz/{token}/audio",content=b"x"*200,headers={"Content-Type":"audio/mp4"})).status_code,429)

if __name__ == "__main__": unittest.main()
