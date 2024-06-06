import flet as ft
import scripts.settings as settings
import scripts.graph_calculations as gc


class UI(ft.Column):
    def __init__(self):
        super().__init__(
            expand=True,
            #alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        
        self.graph_view = ft.Image(
            visible=False,
            src="graph.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            filter_quality=ft.FilterQuality.HIGH,
        )
        self.cooler_graph_view = ft.Image(
            visible=False,
            src="cooler_graph.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            filter_quality=ft.FilterQuality.NONE
        )
        
        self.graph_display = ft.Container(
            expand=1,
            border_radius=ft.border_radius.all(10),
            content=ft.Row(
                scroll=ft.ScrollMode.ALWAYS,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.MainAxisAlignment.START,
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            self.graph_view,
                            self.cooler_graph_view,
                        ]
                    ),
                ]
            ),
        )
        
        self.data_table = ft.DataTable(
            expand=5,
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        )
        
        self.controls = [
            self.graph_display,
            ft.Column(
                expand=1,
                controls=[
                ft.Row(
                    expand=1,
                    controls=[
                        ft.ElevatedButton(
                            expand=1,
                            text="Сгенерировать график",
                            on_click=self.generate_graph 
                        ),
                        ft.ElevatedButton(
                            expand=1,
                            text="Поменять график",
                            on_click=self.change_shown_graph 
                        ),
                        ft.ElevatedButton(
                            expand=1,
                            text="Показать график",
                            on_click=self.show_graph
                        ),
                    ]
                ),
                ft.Row(
                    expand=5,
                    controls=[
                        self.data_table
                    ]
                ),
            ]
            )
            
            # ft.Row(
            #     expand=1,
            #     controls=[
            #         ft.TextField(
            #             expand=1,
            #             label="Путь к файлу"
            #         ),
            #     ]
            # ),
        ]


    def generate_graph(self, e):
        gc.generate_graph(*gc.get_optimal_path(settings.input_file, settings.year))
        gc.resize_graphs()
        self.update()

    def change_shown_graph(self, e):
        if self.graph_view.visible == True:
            self.graph_view.visible = False
            self.cooler_graph_view.visible = True
        elif self.cooler_graph_view.visible == True:
            self.graph_view.visible = True
            self.cooler_graph_view.visible = False
        self.update()

    def show_graph(self, e):
        self.graph_view.visible = True
        self.update()


def main_page(page: ft.Page):
    page.title = settings.page_title
    page.window_resizable = True
    page.window_min_width = 1200
    page.window_min_height = 600
    page.expand = True
    page.add(UI())
   