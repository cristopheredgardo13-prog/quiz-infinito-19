import os
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
    ft.run(main, view=None if os.getenv("RENDER") else ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.getenv("PORT", "7860")), assets_dir="assets")


