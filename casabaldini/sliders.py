import flet as ft
import httpx
from api import API_BASE, IMG_BASE

async def build_sliders(page: ft.Page, dir: str = "index") -> ft.Column:
    """Scarica gli slider e restituisce una Column con tutte le immagini."""
    
    status = ft.Text("Caricamento slider...", color="orange", size=14)
    colonna = ft.Column(
        controls=[status],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f"{API_BASE}/slider?dir={dir}")
            response.raise_for_status()
            data = response.json()

        status.value = f"Caricati {len(data)} elementi"
        status.color = "green"

        for item in data:
            img_url = f"{IMG_BASE}/{dir}/{item.get('img')}"
            colonna.controls.append(
                ft.Column(controls=[
                    ft.Image(
                        src=img_url,
                        width=page.width * 0.4,
                        height=page.height * 0.4,
                        fit=ft.BoxFit.COVER,
                    ),
                    ft.Text(item.get("titolo", ""), size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(item.get("caption", ""), size=12, color="grey"),
                    ft.Divider(),
                ])
            )

        page.update()

    except Exception as e:
        status.value = f"ERRORE: {e}"
        status.color = "red"
        page.update()

    return colonna