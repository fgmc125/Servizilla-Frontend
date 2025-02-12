import flet as ft

from flet import Container

from core.base_ui_component import BaseUIComponent

try:
    from handlers.state_handler import StateHandler
    from utils.style_helper import primary_button_style, outlined_button_style
except:
    from src.handlers.state_handler import StateHandler


primary_button_style_re = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.DISABLED: "#f1f4f8",
        ft.ControlState.DEFAULT: "#964BF8",
    },
    color={
        ft.ControlState.DISABLED: "#7C89B0",
        ft.ControlState.DEFAULT: ft.Colors.WHITE,
    },
    text_style=ft.TextStyle(
        size=12,
        weight=ft.FontWeight.W_500,
        font_family="Plus Jakarta Sans",
    ),
    side=ft.BorderSide(
        color=ft.Colors.TRANSPARENT,
        width=1,
    ),
    elevation=1,
    shape=ft.RoundedRectangleBorder(radius=8),
    padding=ft.padding.symmetric(horizontal=20)
)

outlined_button_style_re = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
        ft.ControlState.HOVERED: "#964BF8",
        ft.ControlState.PRESSED: "#964BF8",
        ft.ControlState.DISABLED: ft.Colors.TRANSPARENT
    },
    color={
        ft.ControlState.DEFAULT: "#964BF8",
        ft.ControlState.HOVERED: "#FFFFFF",
        ft.ControlState.PRESSED: "#964BF8",
        ft.ControlState.DISABLED: ft.Colors.GREY_400
    },
    text_style=ft.TextStyle(
        size=12,
        weight=ft.FontWeight.W_500,
        font_family="Plus Jakarta Sans",
    ),
    side=ft.BorderSide(
        color="#964BF8",
        width=1,
    ),
    shape=ft.RoundedRectangleBorder(radius=8),
    padding=ft.padding.symmetric(horizontal=20)
)

class Nav(BaseUIComponent):
    def __init__(self, app_manage, parent_state):
        super().__init__()
        self._app_manage = app_manage
        self.parent_state = parent_state

        self.brand_image = ft.Image(
            src=f"/brand.png",
            width=32,
            height=32,
            fit=ft.ImageFit.CONTAIN,
        )
        self.brand_name = ft.Text(
            value="Servizilla",
            size=18,
            weight=ft.FontWeight.W_600,
            color="#54647F",
            font_family="Rubik",
            selectable=True
        )

        menu = ["Inicio", "Servicios", "Contacto"]

        self.menu_list = [
            ft.TextButton(
                text=item,
                style=ft.ButtonStyle(
                    color="#54647F",
                    text_style = ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_400,
                        font_family="Rubik",
                    ),
                ),
            )
            for item in menu
        ]

        self.login_button = ft.FilledButton(
            text="ACCEDER",
            style=primary_button_style_re,
            height=32,
        )

        self.signup_button = ft.OutlinedButton(
            text="REGISTRARSE",
            style=outlined_button_style_re,
            height=32,
        )

        avatar_url = f"/male_default_avatar.png"
        self.avatar_me = Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src=avatar_url,
                        width=40,
                        height=40,
                        border_radius=20,
                        fit=ft.ImageFit.COVER,
                    ),
                    Container(
                        width=10,
                        height=10,
                        bgcolor="#71dd37",
                        border_radius=5,
                        alignment=ft.alignment.bottom_right,
                        offset=ft.Offset(2.9, 2.75),
                    )
                ]
            ),
            height=40,
            alignment=ft.alignment.center,
        )

        self.avatar_button = ft.PopupMenuButton(
            content=Container(
                content=self.avatar_me,
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(left=10)
            ),
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            Container(
                                content=ft.Row(
                                    controls=[
                                        self.avatar_me,
                                        ft.Column(
                                            controls=[
                                                ft.Text("Usuario", color='#384551'),
                                                ft.Text("Paciente", color='#a7acb2')],
                                            width=210,
                                            spacing=0
                                        )
                                    ]
                                ),
                                padding=ft.padding.only(top=10, bottom=14)
                            )
                        ]
                    ),
                    # on_click=self.on_click_profile,
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            Container(
                                height=1,
                                expand=True,
                                border=ft.border.only(bottom=ft.border.BorderSide(0.5, "#e4e6e8")),
                                margin=ft.margin.only(top=4, bottom=4)
                            )
                        ]
                    ),
                    padding=ft.padding.all(0),
                    height=1
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.PERSON_OUTLINED, color="#384551", size=22),
                            ft.Text(value="Mi Perfil", color="#384551", size=15, weight=ft.FontWeight.W_400)
                        ]
                    ),
                    # on_click=self.on_click_profile,
                    height=39.5
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.SETTINGS_OUTLINED, color="#384551", size=22),
                            ft.Text(value="Configuraciones", color="#384551", size=15, weight=ft.FontWeight.W_400)
                        ]
                    ),
                    # on_click=self.on_click_settings,
                    height=39.5
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            Container(
                                height=1,
                                expand=True,
                                border=ft.border.only(bottom=ft.border.BorderSide(0.5, "#e4e6e8")),
                                margin=ft.margin.only(top=4, bottom=4)
                            ),
                        ]
                    ),
                    padding=ft.padding.all(0),
                    height=1
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.HELP_OUTLINE_ROUNDED, color="#384551", size=22),
                            ft.Text(value="¿Necesitas ayuda?", color="#384551", size=15, weight=ft.FontWeight.W_400)
                        ],
                    ),
                    # on_click=self.on_click_help,
                    height=39.5
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            Container(
                                height=1,
                                expand=True,
                                border=ft.border.only(bottom=ft.border.BorderSide(0.5, "#e4e6e8")),
                                margin=ft.margin.only(top=4, bottom=4)
                            )
                        ]
                    ),
                    padding=ft.padding.all(0),
                    height=1
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.LOGOUT_OUTLINED, color="#384551", size=22),
                            ft.Text(value="Cerrar sesión", color="#384551", size=15, weight=ft.FontWeight.W_400)
                        ]
                    ),
                    # on_click=self.on_click_logout,
                    height=39.5
                ),
            ],
            menu_position=ft.PopupMenuPosition.UNDER,
            bgcolor="white",
        )
        self.notifications_button = ft.IconButton(
            icon=ft.Icons.NOTIFICATIONS,
            icon_color="blue400",
            icon_size=20,
            tooltip="Notificaciones",
        )

        self.actions = ft.Row(
            controls=[]
        )

        self._register_states()
        self._build_ui()
        self._attach_events()
        self._bind_states()

    def _register_states(self) -> None:
        self.state.register("is_loading", False)
        self.state.register("is_processing", False)
        self.state.register("errors", {})

        self.state.register("name", "")
        self.state.register("lastname", "")
        self.state.register("rol", "user")

    def _build_ui(self) -> None:
        brand = ft.Row(
            controls=[self.brand_image, self.brand_name],
        )

        nav = ft.Row(
            controls=self.menu_list
        )

        self._build_actions()

        layout = ft.Row(
            controls=[brand, nav, self.actions],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        container = ft.Container(
            content=layout,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
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
        self._app_manage.subscribe_state("is_authenticated", self._update_ui)

    def _attach_events(self) -> None:
        self.login_button.on_click=lambda e: self._app_manage.go("/auth/login")
        self.signup_button.on_click = lambda e: self._app_manage.go("/auth/signup")

        callbacks = [
            lambda e: self._app_manage.go("/home"),
            lambda e: self._app_manage.go("/services"),
            lambda e: self._app_manage.go("/contact"),
        ]

        for item, callback in zip(self.menu_list, callbacks):
            item.on_click = callback

    def _update_ui(self, state_key=None, value=None) -> None:
        if state_key == "is_authenticated":
            self._build_actions()
            self.update()

    def _build_actions(self):
        if self._app_manage.get_state("is_authenticated"):
            self.actions.controls = [self.notifications_button, self.avatar_button]
        else:
            self.actions.controls = [self.signup_button, self.login_button]


def main(page: ft.Page):
    page.title = "Nav Example"
    page.padding = 0
    page.bgcolor = "#F5F5F9"

    page.add(Nav())


if __name__ == "__main__":
    ft.app(target=main)
