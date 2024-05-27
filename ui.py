import flet as ft


class UI(ft.UserControl):
    def build(self):
        self.image_view = ft.Image(
            visible=False,
            src="output.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
            filter_quality=ft.FilterQuality.NONE
        )

        return ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
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
                self.image_view,
            ],
        )

    def button_clicked(self, e):
        self.image_view.visible = True
        self.update()


def main(page: ft.Page):
    page.expand = True
    page.add(UI())
   
    
ft.app(target=main)