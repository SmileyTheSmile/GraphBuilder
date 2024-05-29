import flet as ft
import settings


class UI(ft.Column):
    def __init__(self):
        super().__init__(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        self.graph_view = ft.Image(
            visible=False,
            src="graph.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
            filter_quality=ft.FilterQuality.NONE
        )
        self.cooler_graph_view = ft.Image(
            visible=False,
            src="cooler_graph.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
            filter_quality=ft.FilterQuality.NONE
        )
        
        self.controls = [
            ft.Row(
                controls=[
                    ft.TextField(label="Путь к файлу"),
                ]
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Сгенерировать график",
                        on_click=self.button_clicked 
                    ),
                ]
            ),
            ft.Row(
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    self.graph_view,
                ]
            ),
            ft.Row(
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    self.cooler_graph_view,
                ]
            ),
        ]

    def button_clicked(self, e):
        self.graph_view.visible = True
        self.cooler_graph_view.visible = True
        self.update()


def main_page(page: ft.Page):
    page.title = settings.page_title
    page.window_resizable = True
    page.window_min_width = 1200
    page.window_min_height = 600
    page.expand = True
    
    page.add(UI())
   
    
if __name__ == "__main__":
    ft.app(target=main_page)