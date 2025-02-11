import flet as ft

from layouts.layout import Layout
from components.nav import Nav
from handlers.state_handler import StateHandler


class BasicLayout(Layout):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager

        self.header = ft.Container(
            content=Nav(app_manager, self.state)
        )
        self.main_content = ft.Container(
            expand=True
        )
        self.footer = ft.Container()

        self._register_states()
        self._build_ui()
        self._attach_events()
        self._bind_states()

    def _register_states(self) -> None:
        pass

    def _build_ui(self) -> None:
        footer_nav_items = [
            ft.TextButton(
                text=item,
                style=ft.ButtonStyle(
                    color="#8392AB",
                    text_style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_400,
                        font_family="Rubik",
                    ),
                ),
            )
            for item in ["Empresa", "Nosotros", "Equipo", "Politicas de privacidad", "Térmnos y condiciones de uso", "Contacto",]
        ]

        footer_nav_content = ft.Row(
            controls=footer_nav_items,
            alignment=ft.MainAxisAlignment.CENTER
        )

        footer_social_items = [
            ft.IconButton(
                icon=icon,
                style=ft.ButtonStyle(
                    color="#8392AB",
                    text_style=ft.TextStyle(
                        size=18,
                        weight=ft.FontWeight.W_400,
                        font_family="Rubik",
                    ),
                ),
            )
            for icon in [ft.Icons.FACEBOOK]
        ]

        footer_social_content = ft.Row(
            controls=footer_social_items,
            alignment=ft.MainAxisAlignment.CENTER
        )

        footer_content = ft.Column(
            controls=[footer_nav_content, footer_social_content],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.footer.content = footer_content

        layout = ft.Column(
            controls=[self.header, self.main_content, self.footer],
        )

        container = ft.Container(
            content=layout,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(
                offset=ft.Offset(2, 2),
                color=ft.Colors.with_opacity(0.08, '#22303e'),
                blur_radius=6,
                spread_radius=2
            ),
            padding=ft.padding.symmetric(12, 20),
            margin=ft.margin.only(right=6, left=6),
        )

        self.content = container

    def _bind_states(self) -> None:
        pass

    def _attach_events(self) -> None:
        pass

    def _update_ui(self, state_key=None, value=None) -> None:
        pass

    def render_content(self, content):
        self.main_content.content = content