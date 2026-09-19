import flet as ft
from sliders import build_sliders

async def main(page: ft.Page):
    page.title = "CasaBaldini"
    page.theme_mode = ft.ThemeMode.DARK

    slider_view = await build_sliders(page, dir="index")
    page.add(slider_view)
    page.update()

#ft.run(main)

ft.run(main, view=ft.AppView.WEB_BROWSER)