import asyncio, copy, sys, unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from logica import *
from multimedia import pcm_a_wav, ia_media
import ia as cliente
import httpx

class Reglas(unittest.TestCase):
    def test_quiz_demo_valido(self): self.assertEqual(len(validar_quiz(demo())["preguntas"]), 5)
    def test_puntaje_todo(self): self.assertEqual(puntaje(demo()["preguntas"], [0,1,2,3,0]), 5)
    def test_puntaje_nada(self): self.assertEqual(puntaje(demo()["preguntas"], [1,2,3,0,1]), 0)
    def test_puntaje_parcial(self): self.assertEqual(puntaje(demo()["preguntas"], [0,2]), 1)
    def test_vacio(self):
        with self.assertRaises(ValueError): validar_entrada(" ")
    def test_largo(self):
        with self.assertRaises(ValueError): validar_entrada("a"*501)
    def test_limite(self): self.assertEqual(len(validar_entrada("a"*500)),500)
    def test_telefono(self): self.assertTrue(sensible("Llama al 7123-4567"))
    def test_dui(self): self.assertTrue(sensible("12345678-9"))
    def test_password(self): self.assertTrue(sensible("password=ejemplo"))
    def test_correo(self): self.assertTrue(sensible("persona@example.com"))
    def test_tema_sano(self): self.assertFalse(sensible("Historia de las redes"))
    def test_privacidad(self):
        with self.assertRaises(ValueError): validar_entrada("Mi teléfono es 71234567")
    def test_cinco(self):
        with self.assertRaises(ValueError): validar_quiz({"preguntas":[]})
    def test_booleano_no_es_indice(self):
        d=demo(); d["preguntas"][0]["correcta"]=True
        with self.assertRaises(ValueError): validar_quiz(d)
    def test_opciones_distintas(self):
        d=demo(); d["preguntas"][0]["opciones"]=["a"]*4
        with self.assertRaises(ValueError): validar_quiz(d)
    def test_wav(self):
        self.assertTrue(pcm_a_wav(bytes(320)).startswith(b"RIFF"))
    def test_media_limite(self):
        with self.assertRaises(RuntimeError): ia_media("x",bytes(15_000_001),"image/png")
    def test_clave_faltante(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY":""}):
            with self.assertRaisesRegex(RuntimeError,"clave"): cliente.ia("x","y")
    def test_cuota(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",return_value=httpx.Response(429)):
            with self.assertRaisesRegex(RuntimeError,"cuota"): cliente.ia("x","y")
    def test_red(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",side_effect=httpx.ConnectError("simulado")), patch("ia.descubrir_modelos",return_value=[]), patch("ia.time.sleep"):
            with self.assertRaisesRegex(RuntimeError,"conectar"): cliente.ia("x","y")
    def test_respuesta_rota(self):
        respuesta=httpx.Response(200,json={"candidates":[]})
        with patch.dict("os.environ", {"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",return_value=respuesta):
            with self.assertRaisesRegex(RuntimeError,"incompleta"): cliente.ia("x","y")
    def test_descubrimiento_tras_modelo_no_disponible(self):
        catalogo = httpx.Response(200, json={"models": [
            {"name":"models/gemini-3.8-flash","supportedGenerationMethods":["generateContent"]},
            {"name":"models/gemini-3.8-flash-tts","supportedGenerationMethods":["generateContent"]}]})
        resultado = httpx.Response(200,json={"candidates":[{"content":{"parts":[{"text":"listo"}]}}]})
        with patch.dict("os.environ", {"GEMINI_API_KEY":"ficticia"}), patch.object(cliente, "_url_disponible", None), patch("ia.httpx.get",return_value=catalogo) as obtener, patch("ia.httpx.post",side_effect=[httpx.Response(404),resultado]) as enviar:
            self.assertEqual(cliente.ia("x","y"),"listo")
            self.assertIn("models/gemini-3.8-flash:generateContent",enviar.call_args.args[0])
            self.assertEqual(enviar.call_count,2)
            self.assertNotIn("ficticia",obtener.call_args.args[0])
    def test_catalogo_sin_modelo_compatible(self):
        with patch("ia.httpx.get",return_value=httpx.Response(200,json={"models":[]})):
            with self.assertRaisesRegex(RuntimeError,"compatible"):
                cliente.descubrir_modelo("ficticia")
    def test_error_503_identificable_y_sin_clave(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY":"secreto-ficticio"}), patch("ia.httpx.post",return_value=httpx.Response(503)), patch("ia.descubrir_modelos",return_value=[]), patch("ia.time.sleep"):
            with self.assertRaises(RuntimeError) as error:
                cliente.ia("x","y")
            self.assertIn("Código 503", str(error.exception))
            self.assertNotIn("secreto-ficticio", str(error.exception))
    def test_modelo_retirado_410_descubre_otro(self):
        catalogo=httpx.Response(200,json={"models":[{"name":"models/gemini-3.8-flash","supportedGenerationMethods":["generateContent"]}]})
        resultado=httpx.Response(200,json={"candidates":[{"content":{"parts":[{"text":"listo"}]}}]})
        with patch.dict("os.environ", {"GEMINI_API_KEY":"ficticia"}), patch.object(cliente,"_url_disponible",None), patch("ia.httpx.get",return_value=catalogo), patch("ia.httpx.post",side_effect=[httpx.Response(410),resultado]):
            self.assertEqual(cliente.ia("x","y"),"listo")
    def test_503_recupera_sin_cambiar_modelo(self):
        ok=httpx.Response(200,json={"candidates":[{"content":{"parts":[{"text":"recuperado"}]}}]})
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",side_effect=[httpx.Response(503),ok]) as enviar, patch("ia.time.sleep") as pausa:
            self.assertEqual(cliente.ia("x","y"),"recuperado")
            self.assertEqual(enviar.call_count,2)
            pausa.assert_called_once()
    def test_503_prueba_otro_modelo_y_lo_recuerda(self):
        nuevo="https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"
        ok=httpx.Response(200,json={"candidates":[{"content":{"parts":[{"text":"alternativa"}]}}]})
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch.object(cliente,"_url_disponible",None), patch("ia.httpx.post",side_effect=[httpx.Response(503),httpx.Response(503),ok]) as enviar, patch("ia.descubrir_modelos",return_value=[nuevo]), patch("ia.time.sleep"):
            self.assertEqual(cliente.ia("x","y"),"alternativa")
            self.assertEqual(enviar.call_count,3)
            self.assertEqual(enviar.call_args.args[0],nuevo)
            self.assertEqual(cliente._url_disponible,nuevo)
    def test_503_no_reintenta_indefinidamente(self):
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",return_value=httpx.Response(503)) as enviar, patch("ia.descubrir_modelos",return_value=["https://uno","https://dos","https://tres"]), patch("ia.time.sleep"):
            with self.assertRaisesRegex(RuntimeError,"503"): cliente.ia("x","y")
            self.assertEqual(enviar.call_count,4)
    def test_cuota_no_se_reintenta(self):
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",return_value=httpx.Response(429)) as enviar:
            with self.assertRaisesRegex(RuntimeError,"429"): cliente.ia("x","y")
            self.assertEqual(enviar.call_count,1)
    def test_dictado_rechaza_silencio(self):
        with self.assertRaisesRegex(ValueError,"silencio"):
            validar_audio_pcm(bytes(32000))
    def test_dictado_rechaza_audio_corto(self):
        with self.assertRaisesRegex(ValueError,"corta"):
            validar_audio_pcm(bytes(100))
    def test_dictado_sin_voz_no_inventa_tema(self):
        with self.assertRaises(ValueError):
            validar_transcripcion({"hay_voz":False,"texto":"tema inventado"})
    def test_dictado_acepta_texto_literal(self):
        self.assertEqual(validar_transcripcion({"hay_voz":True,"texto":"animales marinos"}),"animales marinos")
    def test_red_recupera_tras_interrupcion(self):
        ok=httpx.Response(200,json={"candidates":[{"content":{"parts":[{"text":"listo"}]}}]})
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",side_effect=[httpx.ConnectError("simulado"),ok]) as enviar, patch("ia.time.sleep"):
            self.assertEqual(cliente.ia("x","y"),"listo")
            self.assertEqual(enviar.call_count,2)
    def test_timeout_muestra_causa_correcta(self):
        with patch.dict("os.environ",{"GEMINI_API_KEY":"ficticia"}), patch("ia.httpx.post",side_effect=httpx.ReadTimeout("simulado")), patch("ia.descubrir_modelos",return_value=[]), patch("ia.time.sleep"):
            with self.assertRaisesRegex(RuntimeError,"tardó demasiado"): cliente.ia("x","y")
    def test_foto_se_reduce_y_se_conserva_valida(self):
        import io
        from PIL import Image
        from multimedia import preparar_imagen
        entrada=io.BytesIO()
        Image.new("RGB",(2400,1800),"blue").save(entrada,format="PNG")
        datos,mime=preparar_imagen(entrada.getvalue())
        self.assertEqual(mime,"image/jpeg")
        with Image.open(io.BytesIO(datos)) as imagen:
            self.assertEqual(imagen.size,(1600,1200))
            self.assertEqual(imagen.getexif(),{})
    def test_imagen_danada_rechazada(self):
        from multimedia import preparar_imagen
        with self.assertRaises(ValueError): preparar_imagen(b"no es una foto")
    def test_ui_y_juego(self):
        from apps.quiz_infinito import vista
        class Pagina:
            def __init__(self): self.services=[]
            def update(self): pass
        p=Pagina()
        with patch.dict("os.environ", {"GEMINI_API_KEY":""}):
            ui=vista(p)
        def todos(c):
            yield c
            if hasattr(c,"controls"):
                for h in c.controls: yield from todos(h)
            if hasattr(c,"content") and not isinstance(c.content,str) and c.content is not None:
                yield from todos(c.content)
        def boton(texto):
            return next(c for c in todos(ui) if getattr(c,"content",None)==texto)
        # La ruta demo no hace esperas: se prueba sin abrir sockets del bucle Windows.
        ejecucion = boton("✦ Generar 5 preguntas").on_click(None)
        with self.assertRaises(StopIteration):
            ejecucion.send(None)
        for nombre in ["A. Python","B. El acceso al servicio","C. Python","D. Comprobar las reglas","A. Sí"]:
            boton(nombre).on_click(None)
        self.assertTrue(any("5/5" in str(getattr(c,"value","")) for c in todos(ui)))
        boton("👍 Útil").on_click(None); boton("👍 Útil").on_click(None)
        self.assertTrue(any("👍 1" in str(getattr(c,"value","")) for c in todos(ui)))

if __name__=="__main__": unittest.main(verbosity=2)



