import flet as ft
import scripts.settings as settings
import scripts.graph_calculations as gc

control = gc.Control()


class TableTab(ft.Column):
    def __init__(self):
        super().__init__(
            scroll=ft.ScrollMode.ADAPTIVE,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        
        self.select_db_button = ft.TextButton(
            text="Получить данные из БД",
            on_click=self.show_db_connection_screen,
        )
        self.select_csv_button = ft.TextButton(
            text="Получить данные из CSV",
            on_click=self.show_csv_connection_screen,
        )
        
        self.connection_selection = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.select_db_button,
                self.select_csv_button,
            ]
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
        
        self.progress_ring = ft.ProgressRing()
        
        self.db_connection = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.login_field,
                self.password_field,
                ft.Row(
                    controls=[
                        self.login_button,
                        self.select_csv_button,
                    ]
                ),
            ]
        )
        
        self.csv_file_field = ft.TextField(
            label="Путь к файлу",
            hint_text="Введите путь к файлу CSV",
            value=settings.input_file,
        )
        self.connect_to_csv_button = ft.TextButton(
            text="Открыть файл",
            on_click=self.connect_to_csv,
        )
        self.csv_connection = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.csv_file_field,
                ft.Row(
                    controls=[
                        self.connect_to_csv_button,
                        self.select_db_button,
                    ]
                ),
            ]
        )
        
        self.login_box = ft.Container(
            width=500,
            height=300,
            bgcolor=ft.colors.GREY_900,
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, ft.colors.BLACK),
            content=self.connection_selection,
        )
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(settings.id_label)),
                ft.DataColumn(ft.Text(settings.id_parent_label)),
                ft.DataColumn(ft.Text(settings.year_label)),
                ft.DataColumn(ft.Text(settings.earnings_label)),
                ft.DataColumn(ft.Text(settings.probability_label)),
                ft.DataColumn(ft.Text(settings.final_probability_label)),
                ft.DataColumn(ft.Text(settings.discount_sum_label)),
                ft.DataColumn(ft.Text(settings.final_discount_sum_label)),
                ft.DataColumn(ft.Text(settings.final_sum_label)),
            ],
        )
        
        self.table_view = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Row(
                        height=50,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.TextButton(
                                expand=1,
                                text="Обновить данные",
                                on_click=self.update_data,
                            ),
                            ft.TextButton(
                                expand=1,
                                text="Подключиться заново",
                                on_click=self.change_connection,
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            self.data_table,
                        ]
                    ),
                ]
            )
        )
        
        self.controls=[
            self.login_box,
        ]
        
    def update_data(self, e):
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.progress_ring,
                ],
            )
        ]
        self.update()
        
        if control.connection_type == 'db':
            control.get_data_db()
        else:
            control.get_data_csv()
            
        self.update_data_table()
        
    def change_connection(self, e):
        self.login_box.content = self.connection_selection
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.login_box,
                ],
            )
        ]
        self.update()
        
    def show_db_connection_screen(self, e):
        self.login_box.content = self.db_connection
        self.update()
        
    def show_csv_connection_screen(self, e):
        self.login_box.content = self.csv_connection
        self.update()
        
    def connect_to_csv(self, e):
        self.login_box.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.progress_ring
            ]
        )
        self.update()
        
        control.get_data_csv()
        self.update_data_table()
        
    def connect_to_db(self, e):
        self.login_box.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.progress_ring
            ]
        )
        self.update()
        
        control.connect_to_db(
            login=self.login_field.value,
            password=self.password_field.value,
            database=settings.database,
            server=settings.server,
            port=settings.port,
        )
        control.get_data_db()
        
        self.update_data_table()

    def update_data_table(self):
        self.data_table.rows = []
        for _, row in control.data.iterrows():
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[settings.id_row])),
                        ft.DataCell(ft.Text(row[settings.id_parent_row])),
                        ft.DataCell(ft.Text(row[settings.year_row])),
                        ft.DataCell(ft.Text(row[settings.earnings_row])),
                        ft.DataCell(ft.Text(row[settings.probability_row])),
                        ft.DataCell(ft.Text(row[settings.final_probability_row])),
                        ft.DataCell(ft.Text(row[settings.discount_sum_row])),
                        ft.DataCell(ft.Text(row[settings.final_discount_sum_row])),
                        ft.DataCell(ft.Text(row[settings.final_sum_row])),
                    ],
                ),
            )
        
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self.table_view,
                ],
            )
        ]
        self.update()
        
        
class GraphTab(ft.Column):
    def __init__(self, page):
        super().__init__(
            alignment=ft.MainAxisAlignment.START,
        )
        self.page = page
        
        self.graph_image = ft.Image(
            visible=False,
            src="graph.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            filter_quality=ft.FilterQuality.HIGH,
        )
        self.cooler_graph_image = ft.Image(
            visible=False,
            src="cooler_graph.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            filter_quality=ft.FilterQuality.NONE
        )
        
        self.progress_ring = ft.ProgressRing()
        
        self.graph_view = ft.Row(
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.MainAxisAlignment.START,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        self.graph_image,
                        self.cooler_graph_image,
                    ]
                ),
            ]
        )
        
        self.graph_display = ft.Container(
            visible=False,
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(2, ft.colors.GREY),
            alignment=ft.alignment.center,
            content=self.progress_ring,
        )
        
        self.controls = [ 
            ft.Row(
                height=50,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
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
                ]
            ),
            self.graph_display,
        ]

    def generate_graph(self, e):
        if control.data is None:
            self.page.snack_bar = ft.SnackBar(
                bgcolor=ft.colors.RED_300,
                
                content=ft.Text("Не загружены данные."),
                action="Ок",
                open=True,
            )
            self.page.update()
            return
        
        self.graph_display.visible = True
        self.graph_display.content = self.progress_ring
        self.update()
        
        control.generate_graphs()
        control.resize_graphs()
        
        self.graph_display.content = self.graph_view
        self.graph_image.visible = True
        self.update()

    def change_shown_graph(self, e):
        if control.data is None:
            self.page.snack_bar = ft.SnackBar(
                bgcolor=ft.colors.RED_300,
                
                content=ft.Text("Не загружены данные."),
                action="Ок",
                open=True,
            )
            self.page.update()
            return
        
        if self.graph_image.visible == True:
            self.graph_image.visible = False
            self.cooler_graph_image.visible = True
        elif self.cooler_graph_image.visible == True:
            self.graph_image.visible = True
            self.cooler_graph_image.visible = False
        self.update()


class UI(ft.Column):
    def __init__(self, page):
        super().__init__(
            expand=True,
        )
        self.page = page
        
        self.controls = [
            ft.Tabs(
                selected_index=0,
                animation_duration=300,
                expand=1,
                tabs=[
                    ft.Tab(
                        text="Таблица",
                        content=ft.Container(
                            alignment=ft.alignment.center,
                            expand=1,
                            content=TableTab()
                        ),
                    ),
                    ft.Tab(
                        text="График",
                        content=ft.Container(
                            alignment=ft.alignment.center,
                            expand=1,
                            content=GraphTab(page),
                        ),
                    ),
                    
                ],
            )
        ]


def main_page(page: ft.Page):
    page.title = settings.page_title
    page.window_resizable = True
    page.window_min_width = 1200
    page.window_min_height = 600
    page.expand = True
    page.window_maximized = True
    page.theme_mode = "dark"
    page.add(UI(page))
   