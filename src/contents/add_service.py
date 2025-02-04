import asyncio
import flet as ft
import logging

from contents.content import PageContainer
from controllers.dashboard_controller import ServicesController
from utils.style_helper import input_text_style, input_label_style, button_style_submit


class AddServicePage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self._app_manager = app_manager
        self.controller = ServicesController(app_manager)

        self.title_input = ft.TextField(label="Nombre del Servicio", expand=True)
        self.description_input = ft.TextField(label="Descripción", multiline=True, expand=True)
        self.duration_input = ft.TextField(label="Duración (min)", keyboard_type=ft.KeyboardType.NUMBER, expand=True)

        self.category_dropdown = ft.Dropdown(
            label="Categoría",
            options=[],
        )

        self.days_selected = {
            day: ft.Checkbox(label=day.capitalize(), value=False) for day in
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        }

        self.start_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
        )
        self.end_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
        )
        self.all_day_switch = ft.Switch(label="Disponible 24h", value=False, on_change=self.toggle_24_hours)

        # Sección de disponibilidad
        self.availability_section = ft.Column(
            controls=[
                self.all_day_switch,
                ft.Row(
                    controls=[
                        self.start_time_picker,
                        self.end_time_picker
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Column(
                    controls=list(self.days_selected.values()),
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )

        # Botones de acción
        self.save_button = ft.FilledButton("Guardar", style=button_style_submit)
        self.cancel_button = ft.TextButton("Cancelar")

        self.build_ui()

    def build_ui(self):
        """Construye la interfaz gráfica de la página"""
        form_layout = ft.Column(
            controls=[
                ft.Text("Agregar nuevo servicio", size=24, weight=ft.FontWeight.BOLD, color="black"),
                self.title_input,
                self.description_input,
                self.duration_input,
                self.category_dropdown,
                self.availability_section,
                ft.Row(
                    controls=[self.save_button, self.cancel_button],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            spacing=10,
            expand=False,
        )

        container = ft.Container(
            content=form_layout,
            padding=ft.padding.all(20),
            bgcolor="white",
            border_radius=10
        )

        self.content = container

        self._app_manager.page.update()

        self.save_button.on_click = self.submit_service
        self.cancel_button.on_click = self.go_back
        self.load_categories()

    def toggle_24_hours(self, e):
        """Activa o desactiva los selectores de hora si se elige la opción 24h"""
        disabled = self.all_day_switch.value
        self.start_time_picker.disabled = disabled
        self.end_time_picker.disabled = disabled
        self.start_time_picker.update()
        self.end_time_picker.update()

    def submit_service(self, e):
        """Recoge los valores del formulario y envía la petición"""
        availability = {
            "days": {
                day.lower(): [] if not self.days_selected[day].value else
                [{"start": self.start_time_picker.value, "end": self.end_time_picker.value}]
                for day in self.days_selected
            },
            "hours": {"24_hours": self.all_day_switch.value}
        }

        service_data = {
            "title": self.title_input.value,
            "description": self.description_input.value,
            "duration": int(self.duration_input.value) if self.duration_input.value else 0,
            "availability": availability,
            "category": int(self.category_dropdown.value) if self.category_dropdown.value else None
        }

        if not service_data["title"] or not service_data["description"] or not service_data["category"]:
            self._app_manager.page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
            self._app_manager.page.snack_bar.open = True
            self._app_manager.page.update()
            return

        asyncio.run(self.controller.create_service(service_data))
        self._app_manager.page.snack_bar = ft.SnackBar(ft.Text("Servicio creado con éxito!"))
        self._app_manager.page.snack_bar.open = True
        self._app_manager.page.update()
        self.go_back(None)

    def go_back(self, e):
        """Regresa a la pantalla anterior"""
        self._app_manager.page.go("/dashboard")

    async def load_categories(self):
        CATEGORIES = [
            {"id": 1, "name": "Reparaciones del hogar"},
            {"id": 2, "name": "Servicios de limpieza"},
            {"id": 3, "name": "Mudanzas y transporte"},
        ]

        self.category_dropdown.options = [
            ft.dropdown.Option(text=cat["name"], key=cat["id"]) for cat in CATEGORIES
        ]

        self.category_dropdown.update()


def add_service_page(app_manager):
    app_manager.page.title = "Agregar Servicio"
    return AddServicePage(app_manager)
