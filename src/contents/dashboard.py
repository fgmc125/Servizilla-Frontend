import flet as ft

class SellerDashboardPage(ft.UserControl):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.services_list = []  # Placeholder for the list of services
        self.build_ui()

    def build_ui(self):
        self.sidebar = self._build_sidebar()
        self.header = self._build_header()
        self.content = self._build_content()

        self.layout = ft.Row(
            controls=[
                self.sidebar,
                ft.Column(
                    controls=[
                        self.header,
                        self.content
                    ],
                    expand=True,
                )
            ],
            expand=True
        )

        self.controls = [self.layout]

    def _build_sidebar(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Servizilla", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Divider(),
                    ft.ListTile(leading=ft.Icon(ft.icons.HOME), title=ft.Text("Resumen")),
                    ft.ListTile(leading=ft.Icon(ft.icons.LIST), title=ft.Text("Mis Servicios")),
                    ft.ListTile(leading=ft.Icon(ft.icons.MESSAGE), title=ft.Text("Mensajes")),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Text(
                            "¿Necesitas ayuda? Puedes visitar el registro de preguntas frecuentes o el asistente de ayuda.",
                            size=12, color="white"
                        ),
                        bgcolor="#7C4DFF",
                        border_radius=8,
                        padding=10,
                        margin=10,
                    ),
                    ft.ElevatedButton("AYUDACIÓN", bgcolor="#7C4DFF", color="white")
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            ),
            width=240,
            bgcolor="#2C2F48",
            padding=20,
        )

    def _build_header(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Servicios", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.ElevatedButton(
                        "Nuevo Servicio",
                        bgcolor="#964BF8",
                        color="white",
                        on_click=self._on_new_service_click,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor="#1A1D2E",
            padding=20
        )

    def _build_content(self):
        # Placeholder for services list
        self.services_column = ft.Column(
            controls=[
                self._build_service_item(index) for index in range(5)  # Example items
            ],
            spacing=10,
        )

        return ft.Container(
            content=self.services_column,
            bgcolor="#1A1D2E",
            padding=20,
            border_radius=8,
            expand=True
        )

    def _build_service_item(self, index):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(src="https://via.placeholder.com/80", width=80, height=80),
                    ft.Column(
                        controls=[
                            ft.Text(f"Servicio de ejemplo {index}", size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Descripción del servicio", size=14, color="white")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Editar", bgcolor="#964BF8", color="white"),
                            ft.ElevatedButton("Desactivar", bgcolor="#FF5252", color="white")
                        ],
                        spacing=10
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor="#2C2F48",
            border_radius=8,
            padding=10,
            margin=5
        )

    def _on_new_service_click(self, event):
        print("Nuevo servicio creado")

    def build(self):
        return self.layout


def seller_dashboard_page(app_manager):
    return SellerDashboardPage(app_manager)
