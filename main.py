import os
from pathlib import Path
import flet as ft
from apps.quiz_infinito import vista
def main(page: ft.Page):
    page.title = "Quiz infinito · AppLab IA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#08111F"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.add(vista(page))
if __name__ == "__main__":
    import uvicorn
    from flet_web.fastapi import FastAPI
    from flet_web.fastapi import app as flet_app
    from voz import registrar_rutas
    app = FastAPI()
    registrar_rutas(app)
    app.mount("/", flet_app(main, assets_dir=str(Path(__file__).parent / "assets")))
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "7860")), access_log=False)


