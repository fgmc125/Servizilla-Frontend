import logging
import asyncio

import flet as ft

from contents.content import PageContainer
from controllers.services_list_controller import ServicesListController
from utils.style_helper import input_label_style, input_text_style, primary_button_style


class ProductCard(ft.Container):
    def __init__(self, image, name, price, rating):
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Image(src=image, height=150, fit=ft.ImageFit.CONTAIN),
                    ft.Text(value=name, weight=ft.FontWeight.W_600, size=14, color="#7C89B0"),
                    ft.Text(value=f"$ {price}", weight=ft.FontWeight.W_500, size=12, color="#101213"),
                    ft.Row(
                        controls=[
                            ft.Text(value="\u2605" * int(rating), color="#FFB400", size=12),
                            ft.Text(value="\u2606" * (5 - int(rating)), color="#CCCCCC", size=12),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            padding=10,
            border_radius=8,
            bgcolor="#FFFFFF",
            shadow=ft.BoxShadow(
                blur_radius=3,
                spread_radius=0.5,
                color="#E0E0E0",
            )
        )


class ProductCatalogPage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self._app_manager = app_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        self.controller = ServicesListController(app_manager)

        self.aside = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Categorías",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color="#54647F",
                        font_family="Rubik",
                        selectable=True
                    ),
                    ft.TextButton(
                        text="Todas",
                        data={}
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                alignment=ft.MainAxisAlignment.START
            ),
            width=250,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                offset=ft.Offset(2, 2),
                color=ft.Colors.with_opacity(0.08, '#22303e'),
                blur_radius=6,
                spread_radius=2
            ),
            padding=ft.padding.symmetric(20, 20),
            margin=ft.margin.only(right=6, left=6),
            alignment=ft.alignment.top_left
        )

        self.products_grid = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                offset=ft.Offset(2, 2),
                color=ft.Colors.with_opacity(0.08, '#22303e'),
                blur_radius=6,
                spread_radius=2
            ),
            padding=ft.padding.symmetric(12, 20),
            margin=ft.margin.only(right=6, left=6),
            expand=True
        )

        self.search_bar = ft.TextField(
            label="Search here...",
            prefix_icon=ft.Icons.SEARCH,
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
            # expand=True,
            data={"state": "service_search"}
        )

        self.pagination = []

        self._register_states()
        self._build_ui()
        self._attach_events()
        self._bind_states()
        self._invoke_service()

    def _register_states(self) -> None:
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("field_errors", {})
        self.state.register("general_error", None)

        self.state.register("categories", [])

    def _build_ui(self):
        wrapper_layout = ft.Column(
            controls=[
                self.search_bar,
                self.products_grid
            ],
            alignment=ft.MainAxisAlignment.START
        )

        wrapper = ft.Container(
            content=wrapper_layout,
            expand=True
        )

        layout = ft.Row(
            controls=[self.aside, wrapper],
            # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        container = ft.Container(
            content=layout,
        )

        self.content = container
        self.update()
        self.logger.warning("self.aside: ADDED")

    def _bind_states(self) -> None:
        self.state.subscribe("categories", self._update_ui)

    def _attach_events(self) -> None:
        pass

    def _update_ui(self, state_key=None, value=None) -> None:
        if state_key == "categories":
            self._build_aside_controls()

        self.update()

    def _invoke_service(self) -> None:
        self.state.set("is_processing", True)
        asyncio.run(self.controller.get_categories(self.state))
        self.state.set("is_processing", False)

    def _build_aside_controls(self):
        self.logger.warning("_build_aside_controls: in")
        menu = [
            ft.TextButton(
                text=category["name"],
                data={}
            )
            for category in self.state.get("categories", [])
        ]

        if len(self.aside.content.controls) == 2:
            self.aside.content.controls = self.aside.content.controls + menu
        else:
            item_1 = ft.Text(
                value="Categorías",
                size=14,
                weight=ft.FontWeight.W_600,
                color="#54647F",
                font_family="Rubik",
                selectable=True
            )

            item_2 = ft.TextButton(
                text="Todas",
                data={}
            )

            self.aside.content.controls = [item_1, item_2] + menu

        self.aside.content.update()

    def on_resized(self, event: ft.ControlEvent):
        if self.app_manager.page.width < 1200:
            pass
        else:
            pass

def product_catalog_page(app_manager):
    app_manager.page.title_text = "Product Catalog"
    return ProductCatalogPage(app_manager)


def main(page: ft.Page):
    page.title = "Nav Example"
    page.padding = 0
    page.bgcolor = "#F5F5F9"

    page.add(product_catalog_page(None))


if __name__ == "__main__":
    ft.app(target=main)
