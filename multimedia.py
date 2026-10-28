import base64, io, wave
from ia import solicitar
def pcm_a_wav(pcm, tasa=16000, canales=1):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(canales); w.setsampwidth(2); w.setframerate(tasa); w.writeframes(pcm)
    return buf.getvalue()
def ia_media(instruccion, datos, mime, texto="", como_json=False, adicionales=None):
    archivos = [(datos, mime)] + list(adicionales or [])
    if sum(len(d) for d, _ in archivos) > 15_000_000:
        raise RuntimeError("Los archivos superan 15 MB. Usa archivos más pequeños.")
    partes = [{"text": instruccion + "\n" + texto}]
    partes += [{"inline_data": {"mime_type": m, "data": base64.b64encode(d).decode()}} for d, m in archivos]
    return solicitar(partes, como_json)



def preparar_imagen(datos):
    """Reduce el tamaño de subida y elimina metadatos de la foto."""
    from PIL import Image, ImageOps, UnidentifiedImageError
    if not datos or len(datos) > 10_000_000:
        raise ValueError("Elige una imagen de hasta 10 MB.")
    try:
        with Image.open(io.BytesIO(datos)) as imagen:
            if imagen.width * imagen.height > 25_000_000:
                raise ValueError("La foto tiene demasiados píxeles. Reduce su tamaño antes de subirla.")
            imagen = ImageOps.exif_transpose(imagen)
            imagen.thumbnail((1600, 1600))
            if imagen.mode != "RGB":
                imagen = imagen.convert("RGB")
            salida = io.BytesIO()
            imagen.save(salida, format="JPEG", quality=85, optimize=True)
            return salida.getvalue(), "image/jpeg"
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise ValueError("El archivo no es una imagen válida o está dañado.") from None
