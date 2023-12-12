import flet as ft

def main(page: ft.Page):
    page.title = "Web-Crawler"

    domain = ft.TextField(label="Enter the domain address", autofocus=True, width=350)
    ssl_verify = ft.Checkbox(label="Verify SSL?", value=False, )

    page.add(
        ft.Row(
            [
                domain,
                ft.FilledTonalButton("Crawl", )
            ],
            alignment=ft.MainAxisAlignment.START,
        )
    )