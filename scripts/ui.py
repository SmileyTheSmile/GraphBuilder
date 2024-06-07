import flet as ft
import scripts.settings as settings
import scripts.graph_calculations as gc

control = gc.Control()


class TableTab(ft.Tab):
    def __init__(self):
        super().__init__(
            text="Таблица",
        )
        
        self.login_field = ft.TextField(
            label="Логин",
            hint_text="Введите логин",
            value=settings.login,
        )
        self.password_field = ft.TextField(
            label="Пароль",
            hint_text="Введите пароль",
            value=settings.password,
        )
        self.login_button = ft.TextButton(
            text="Подключиться",
            on_click=self.connect_to_db,
        )
        
        self.progress_ring = ft.ProgressRing(
            tooltip="Подключаемся к PostgreSQL...",
            visible=False,
        )
        
        self.login_box = ft.Container(
            alignment=ft.alignment.center,
            width=500,
            height=200,
            bgcolor=ft.colors.GREY_900,
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, ft.colors.BLACK),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self.login_field,
                    self.password_field,
                    self.login_button,
                    self.progress_ring,
                ]
            )
        )
        
        self.table_view = ft.Container(
            expand=1,
            alignment=ft.alignment.center,
            visible=False,
            content=ft.DataTable(
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
            ), 
        )
        
        self.content = ft.Column(
            expand=1,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    expand=1,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        self.login_box,
                        self.table_view,
                    ],
                )
            ],
        )
        
    def connect_to_db(self, e):
        self.login_field.visible = False
        self.password_field.visible = False
        self.login_button.visible = False
        self.progress_ring.visible = True
        self.update()
        
        control.connect_to_db(
            login=self.login_field.value,
            password=self.password_field.value,
            database=settings.database,
            server=settings.server,
            port=settings.port,
        )
        
        self.progress_ring.tooltip = "Получаем данные..."
        self.update()
        
        control.get_data_db()
        
        self.progress_ring.visible = False
        self.table_view.visible = True
        self.login_box.visible = False
        self.update()


        
class GraphTab(ft.Tab):
    def __init__(self):
        super().__init__(
            text="График",
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
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            filter_quality=ft.FilterQuality.NONE
        )
        
        self.progress_ring = ft.ProgressRing(
            visible=True,
        )
        
        self.graph_display = ft.Container(
            visible=False,
            border_radius=ft.border_radius.all(10),
            content=ft.Row(
                scroll=ft.ScrollMode.ALWAYS,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    self.progress_ring,
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
        
        self.buttons_row = ft.Row(
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
        )
        
        self.content = ft.Column(
            expand=1,
            controls=[
                self.buttons_row,
                self.graph_display,
            ],
        )

    def generate_graph(self, e):
        self.graph_display.visible = True
        self.progress_ring.visible = True
        self.graph_view.visible = False
        self.update()
        
        gc.get_graphs()
        
        self.graph_view.visible = True
        self.progress_ring.visible = False
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


class UI(ft.Column):
    def __init__(self):
        super().__init__(
            expand=True,
        )
        
        self.controls = [
            ft.Tabs(
                selected_index=1,
                animation_duration=300,
                expand=1,
                tabs=[
                    TableTab(),
                    GraphTab(),
                ],
            )
        ]


def main_page(page: ft.Page):
    page.title = settings.page_title
    page.window_resizable = True
    page.window_min_width = 1200
    page.window_min_height = 600
    page.expand = True
    page.add(UI())
   