import asyncio
import flet as ft
import logging

from contents.content import PageContainer
from controllers.add_service_controller import AddServiceController
from utils.style_helper import input_text_style, input_label_style, button_style_submit, text_button_style, outlined_button_style


class AddServicePage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self._app_manager = app_manager
        self.controller = AddServiceController(app_manager)

        self.title_text = ft.Text(
            value="Agregar nuevo servicio",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="black"
        )

        self.title_input = ft.TextField(
            label="Nombre del Servicio",
            value="",
            color="#57636c",
            label_style=input_label_style,
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            expand=True,
            data={"state": "service_name"}
        )
        self.description_input = ft.TextField(
            label="Descripción",
            value="",
            color="#57636c",
            label_style=input_label_style,
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            multiline=True,
            expand=True,
            data={"state": "service_description"}
        )
        self.duration_input = ft.TextField(
            label="Duración (min)",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="30",
            color="#57636c",
            label_style=input_label_style,
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            expand=True,
            data={"state": "duration"}
        )

        self.category_dropdown = ft.Dropdown(
            label="Categoría",
            label_style=input_label_style,
            # hint_text="SELECCIONE UNA CATEGORÍA",
            # hint_style=input_text_style,
            color="#57636c",
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            expand=True,
            data={"state": "service_category_id"}
        )

        self.days_selected = {
            day: ft.Checkbox(
                label=day.capitalize(),
                value=day not in ["Sábado", "Domingo"],
                active_color=ft.Colors.PURPLE_300,
                check_color=ft.Colors.WHITE,
                hover_color="#d1d5db",
                label_style=input_label_style,
                splash_radius=8,
            ) for day in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        }

        self.start_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            data={"state": "start_time_picker"}
        )

        self.end_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            data={"state": "end_time_picker"}
        )

        self.start_time_picker_button = ft.OutlinedButton(
            text="Desde",
            # style=outlined_button_style
        )

        self.end_time_picker_button = ft.OutlinedButton(
            text="Hasta",
            # style=outlined_button_style
        )

        self.all_day_switch = ft.Switch(
            label="Disponible 24h",
            value=False,
            active_color=ft.Colors.PURPLE,
            thumb_color=ft.Colors.WHITE,
            inactive_track_color="#d1d5db",
            inactive_thumb_color="green",
            label_style=input_label_style,
            data={"state": "available_all_day"}
        )

        self.save_button = ft.FilledButton(
            "Guardar",
            style=button_style_submit
        )

        self.cancel_button = ft.TextButton(
            "Cancelar",
            style=text_button_style
        )

        self._register_states()
        self._build_ui()
        self._attach_events()
        self._bind_states()
        self._invoke_service()

    def _build_ui(self) -> None:
        availability_section = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.all_day_switch,
                        self.start_time_picker_button,
                        self.end_time_picker_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Column(
                    controls=list(self.days_selected.values()),
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )

        column_child = ft.Column(
            controls=[
                self.title_text,
                self.title_input,
                self.description_input,
                self.duration_input,
                self.category_dropdown,
                availability_section,
                ft.Row(
                    controls=[self.save_button, self.cancel_button],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.HIDDEN,
        )

        container_child = ft.Container(
            content=column_child,
            alignment=ft.alignment.top_center,
            expand=True
        )

        container_wrapper = ft.Container(
            content=ft.SafeArea(content=container_child),
            bgcolor="#FFFFFF",
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            expand=True,
        )

        layout = ft.Row(
            controls=[container_wrapper],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        container = ft.Container(
            content=layout,
            bgcolor="#FFFFFF",
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            expand=True,
            border_radius=10
        )

        self.content = container
        self._app_manager.page.update()

    def _update_ui(self, state_key=None, value=None) -> None:
        if state_key == "categories":
            options = [
                ft.dropdown.Option(key=category["id"], text=category["name"])
                for category in value
            ]
            self.category_dropdown.options = options

    def _attach_events(self) -> None:
        self.title_input.on_change = self.handle_input_change
        self.description_input.on_change = self.handle_input_change
        self.duration_input.on_change = self.handle_input_change
        self.category_dropdown.on_change = self.handle_category_change
        self.start_time_picker.on_change = self.handle_input_change
        self.end_time_picker.on_change = self.handle_input_change

        self.start_time_picker_button.on_click = lambda _: self._app_manager.page.open(self.start_time_picker)
        self.end_time_picker_button.on_click = lambda _: self._app_manager.page.open(self.end_time_picker)
        self.all_day_switch.on_change = self.toggle_24_hours
        self.save_button.on_click = self.handle_click
        self.cancel_button.on_click = lambda _: self._app_manager.page.go("/dashboard")

        for checkbox in self.days_selected.values():
            checkbox.on_change = self.update_days_state

    def _register_states(self) -> None:
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("field_errors", {})
        self.state.register("general_error", None)

        self.state.register("categories", [])
        self.state.register("service_name", None)
        self.state.register("service_description", None)
        self.state.register("service_category_id", None)
        self.state.register("duration", None)
        self.state.register("start_time_picker", None)
        self.state.register("end_time_picker", None)
        self.state.register("days", {
            day: checkbox.value for day, checkbox in self.days_selected.items()
        })

        self.state.register("available_all_day", self.all_day_switch.value)

    def _bind_states(self) -> None:
        self.state.subscribe("is_processing", self._update_ui)
        self.state.subscribe("field_errors", self._update_ui)
        self.state.subscribe("general_error", self._update_ui)

        self.state.subscribe("categories", self._update_ui)

        self.state.subscribe("start_time_picker", self._update_ui)
        self.state.subscribe("end_time_picker", self._update_ui)

    def _invoke_service(self) -> None:
        self.state.set("is_processing", True)
        asyncio.run(self.controller.get_categories(self.state))
        self.state.set("is_processing", False)

    def toggle_24_hours(self, event: ft.ControlEvent) -> None:
        # disabled = self.all_day_switch.value
        self.start_time_picker_button.disabled = not self.start_time_picker_button.disabled
        self.end_time_picker_button.disabled = not self.end_time_picker_button.disabled
        self.start_time_picker_button.update()
        self.end_time_picker_button.update()

    def update_days_state(self, event: ft.ControlEvent):
        day = event.control.label
        days = self.state.get("days", {}).copy()
        days[day] = event.control.value
        self.state.set("days", days)

    async def handle_click(self, event: ft.ControlEvent):
        await self.controller.add_service(self.state)

    def handle_input_change(self, event: ft.ControlEvent):
        self.state.set(event.control.data["state"], event.control.value)

    def handle_category_change(self, event: ft.ControlEvent):
        self.state.set(event.control.data["state"], event.control.value)


def add_service_page(app_manager):
    app_manager.page.title_text = "Agregar Servicio"
    return AddServicePage(app_manager)
