import flet as ft
import httpx

API_BASE = "https://json.casabaldini.eu/api/v1"
IMG_BASE = "https://json.casabaldini.eu/static/img"

async def main(page: ft.Page):
    page.title = "CasaBaldini Test"
    page.theme_mode = ft.ThemeMode.DARK

    status = ft.Text("Caricamento...", color="orange", size=18)
    lista = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    page.add(status, lista)
    page.update()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f"{API_BASE}/slider?dir=index")
            response.raise_for_status()
            data = response.json()

        status.value = f"SUCCESSO! {len(data)} elementi. Carico prima immagine..."
        page.update()

        primo = data[0]
        img_url = f"{IMG_BASE}/index/{primo.get('img')}"

        # In Flet le immagini da URL si caricano direttamente — niente download manuale!
        img = ft.Image(src=img_url, width=400, fit=ft.BoxFit.CONTAIN)
        
        lista.controls.append(img)
        lista.controls.append(ft.Text(primo.get("titolo", ""), size=20, weight=ft.FontWeight.BOLD))
        lista.controls.append(ft.Text(primo.get("caption", ""), size=14, color="grey"))

        for item in data[1:]:
            lista.controls.append(ft.Text(item.get("titolo", ""), size=16))

        status.value = f"SUCCESSO TOTALE! {len(data)} elementi"
        status.color = "green"
        page.update()

    except Exception as e:
        status.value = f"ERRORE: {e}"
        status.color = "red"
        page.update()

#ft.run(main, view=ft.AppView.WEB_BROWSER)
ft.run(main)