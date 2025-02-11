import asyncio
import logging

import flet as ft

from contents.content import PageContainer
from controllers.dashboard_controller import ServicesController

from utils.style_helper import input_text_style, input_label_style, button_style_submit


class ServicesTablePage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self._app_manager = app_manager
        self.controller = ServicesController(app_manager)

        self.elements_by_page = ft.Dropdown(
            label="Cantidad de Elementos",
            hint_text="SELECCIONE CANTIDAD",
            options=[
                ft.dropdown.Option(key="5", text="5"),
                ft.dropdown.Option(key="10", text="10"),
                ft.dropdown.Option(key="15", text="15"),
            ],
            value=self.state.get("elements_by_page") or "5",
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=1,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            label_style=input_label_style,
        )
        self.category_filter = ft.Dropdown(
            label="Filto por Categoría",
            hint_text="SELECCIONE UN FILTRO",
            options=[
                ft.dropdown.Option(key="T", text="TODOS"),
                ft.dropdown.Option(key="A", text="ACTIVOS"),
                ft.dropdown.Option(key="I", text="INACTIVOS"),
            ],
            value="T",
            text_style=input_text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=1,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color=ft.Colors.PURPLE_300,
            label_style=input_label_style,
        )
        self.search = ft.TextField(
            label="Buscar Servicio",
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
            expand=1,
        )
        self.new_service_button = ft.FilledButton(
            "Nuevo Servicio",
            style=button_style_submit,
            height=42,
            on_click=lambda e: self._app_manager.page.go("/services/new")
        )

        self.table_content = self._build_table()

        self.state.register("is_processing", False)
        self.state.register("field_errors", {})
        self.state.register("general_error", None)

        self.state.register("services", {})
        self.state.register("elements_by_page", self.elements_by_page.value or "5")
        self.state.register("category_filter", self.category_filter.value or "T")
        self.state.register("search_query", self.search.value or None)

        self.state.register("current_page", 1)
        self.state.register("total_pages", 0)

        self.state.subscribe("is_processing", self._update_ui)
        self.state.subscribe("field_errors", self._update_ui)
        self.state.subscribe("general_error", self._update_ui)

        self.state.subscribe("services", self._update_ui)
        self.state.subscribe("elements_by_page", self._update_ui)
        self.state.subscribe("category_filter", self._update_ui)
        self.state.subscribe("search_query", self._update_ui)

        self.state.subscribe("total_pages", self._update_ui)

        self.state.subscribe("current_page", self._fetch_services)

        self._fetch_services()
        self._build_ui()

    def _build_ui(self):
        filter_row = ft.Row(
            controls=[
                self.elements_by_page,
                self.category_filter,
                self.search,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        pagination = self._build_pagination()

        layout = ft.Column(
            controls=[
                ft.Text(
                    "Gestión de Servicios",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="black",
                ),
                ft.Row(
                    controls=[
                        self.new_service_button
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                filter_row,
                self.table_content,
                pagination,
            ],
            spacing=20,
            tight=False,
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )

        container = ft.Container(
            content=layout,
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            bgcolor="white",
            border_radius=10
        )

        self.content = container

    def _build_table(self):
        table_header = ft.Row(
            controls=[
                ft.Text("Nombre", weight=ft.FontWeight.BOLD, width=200, color="black"),
                ft.Text("Categoría", weight=ft.FontWeight.BOLD, width=100, color="black"),
                ft.Text("Estado", weight=ft.FontWeight.BOLD, width=100, color="black"),
                ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=300, color="black"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        table_rows = []
        self.logger.info(f": [services] {len(self.state.get("services")) if self.state.get("services") else []}")
        if self.state.get("services") and len(self.state.get("services")) > 0:
            self.logger.info(f": [services] {self.state.get("services")[0].keys()}")
            table_rows = [
                self._build_table_row(service) for service in self.state.get("services")
            ]

        return ft.Column(
            controls=[table_header] + table_rows,
            spacing=10,
        )

    def _build_table_row(self, service):
        self.logger.info(f": [TABLE] {service}")
        return ft.Row(
            controls=[
                ft.Text(service["title"], width=200, color="black"),
                ft.Text(service["category"], width=100, color="black"),
                ft.Text(service["is_archived"], width=100, color="black"),
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.VISIBILITY, icon_color="white", bgcolor="#64B5F6"),
                        ft.IconButton(icon=ft.icons.EDIT, icon_color="white", bgcolor="#FFD54F"),
                        ft.IconButton(icon=ft.icons.DELETE, icon_color="white", bgcolor="#FF5252"),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_pagination(self):
        current_page = self.state.get("current_page", 1)
        total_pages = self.state.get("total_pages", 0)

        if total_pages == 0:
            return ft.Row(controls=[], spacing=5, alignment=ft.MainAxisAlignment.CENTER)

        prev_button = ft.ElevatedButton(
            "<", bgcolor="#2C2F48", color="white",
            disabled=current_page == 1,
            on_click=lambda e: self.state.set("current_page", max(1, current_page - 1))
        )

        page_buttons = [
            ft.ElevatedButton(
                text=str(page),
                color="white" if page == current_page else "black",
                bgcolor="#2C2F48" if page == current_page else "#E0E0E0",
                on_click=lambda e, p=page: self.state.set("current_page", p)
            )
            for page in range(1, total_pages + 1)
        ]

        next_button = ft.ElevatedButton(
            ">", bgcolor="#2C2F48", color="white",
            disabled=current_page == total_pages,
            on_click=lambda e: self.state.set("current_page", min(total_pages, current_page + 1))
        )

        return ft.Row(
            controls=[prev_button] + page_buttons + [next_button],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        )

    def _update_ui(self, state_key=None, value=None):

        if state_key == "services":
            self.logger.info(f"[update_ui] value: services -> {value}")

            self.table_content = self._build_table()
            self.table_content.update()

    def on_new_service_click(self, e):
        print("Nuevo servicio creado")

    def on_search_click(self, e):
        self._fetch_services()

    def _fetch_services(self):
        self.state.set("is_processing", True)
        asyncio.run(self.controller.fetch_services(self.state))
        self.state.set("is_processing", False)

    def _register_states(self) -> None:
        pass

    def _bind_states(self) -> None:
        pass

    def _attach_events(self) -> None:
        pass


def seller_dashboard_page(app_manager):
    app_manager.page.title_text = "Gestión de Servicios"
    return ServicesTablePage(app_manager)
