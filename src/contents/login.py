import asyncio

import flet as ft

from contents.content import PageContainer
from utils.style_helper import label_style, text_style, primary_button_style
from controllers.login_controller import LoginController


class LoginPage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self._app_manager = app_manager
        self.controller = LoginController(app_manager)

        self.text_title = ft.Text(
            value="¡Bienvenido!👋",
            size=32,
            weight=ft.FontWeight.W_600,
            color="#964BF8",
            font_family="Urbanist",
            selectable=True
        )

        self.text_subtitle = ft.Text(
            value="Ingrese su Usuario y su contraseña para acceder a la plataforma.",
            size=14,
            weight=ft.FontWeight.W_500,
            color="#7C89B0",
            font_family="Plus Jakarta Sans",
            selectable=True,
        )

        self.username_input = ft.TextField(
            label="Nombre de Usuario",
            color="#57636c",
            label_style=label_style,
            max_lines=1,
            text_size=16,
            text_style=text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color="#964BF8",
        )

        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            color="#57636c",
            label_style=label_style,
            text_style=text_style,
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color="#964BF8",
            can_reveal_password=True,
        )

        self.remember_me = ft.Checkbox(
            label="Recordarme",
            label_style=ft.TextStyle(color="#7C89B0", size=15)
        )

        self.forgot_password_button = ft.TextButton(
            text="¿Olvidaste tu contraseña?",
            style=ft.ButtonStyle(color="#964BF8"),
        )

        self.login_button = ft.FilledButton(
            text="Acceder",
            style=primary_button_style,
            expand=True,
            height=42,
        )

        self.signup_text_hint = ft.Text(
            value="¿No tienes una cuenta?",
            color="#7C89B0",
            size=14,
            weight=ft.FontWeight.W_600,
            selectable=True
        )

        self.signup_text_button = ft.TextButton(
            text="Regístrate aquí",
            style=ft.ButtonStyle(color="#964BF8")
        )

        self._register_states()
        self._build_ui()
        self._attach_events()
        self._bind_states()

    def _register_states(self) -> None:
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("field_errors", {})
        self.state.register("general_error", None)

    def _build_ui(self) -> None:
        text_title = ft.Container(
            content=self.text_title,
            padding=ft.padding.only(top=50),
            alignment=ft.alignment.center_left
        )

        text_subtitle = ft.Container(
            content=self.text_subtitle,
            padding=ft.padding.only(top=12, bottom=24),
            alignment=ft.alignment.center_left
        )

        header_layout = ft.Column(
            controls=[
                text_title,
                text_subtitle
            ]
        )

        username_input = ft.Container(
            content=self.username_input,
            padding=ft.padding.only(bottom=10),
            margin=ft.margin.all(0),
        )
        password_input = ft.Container(
            content=self.password_input,
            padding=ft.padding.only(bottom=10),
            margin=ft.margin.all(0),
        )

        remember_and_forgot_password_row = ft.Container(
            content=ft.Row(
                controls=[self.remember_me, self.forgot_password_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            margin=ft.margin.only(bottom=12),
        )

        login_button = ft.Row([self.login_button], expand=True)

        signup_text = ft.Container(
            content=ft.Row(
                [self.signup_text_hint, self.signup_text_button],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(bottom=8),
        )

        column_child = ft.Column(
            controls=[
                header_layout,
                username_input,
                password_input,
                remember_and_forgot_password_row,
                login_button,
                signup_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.HIDDEN,
        )

        container_child = ft.Container(
            content=column_child,
            alignment=ft.alignment.center,
            expand=True
        )

        container_wrapper = ft.Container(
            content=ft.SafeArea(content=container_child),
            width=400,
            bgcolor="#FFFFFF",
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            expand=True,
            col={
                'xs': 12,
                "sm": 12,
                'md': 6,
                'lg': 5,
                'xl': 4,
                'xxl': 4,
            },
        )

        def unfocused(event: ft.ControlEvent):
            for control in self._app_manager.page.controls:
                if isinstance(control, ft.TextField):
                    control.blur()
            self._app_manager.page.update()

        gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.BASIC,
            on_tap=unfocused,
            content=container_wrapper,
        )

        layout = ft.Row(
            controls=[gesture_detector],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        container = ft.Container(
            content=layout,
            bgcolor="#FFFFFF",
            margin=ft.margin.all(0),
            padding=ft.padding.all(0),
            expand=True,
        )

        self.content = container

    def _bind_states(self) -> None:
        self.state.subscribe("is_processing", self._update_ui)
        self.state.subscribe("field_errors", self._update_ui)
        self.state.subscribe("general_error", self._update_ui)

    def _attach_events(self) -> None:
        self.login_button.on_click = self.__on_login_click
        self.signup_text_button.on_click = lambda e: self._app_manager.go("/auth/signup")

    def _update_ui(self, state_key=None, value=None) -> None:
        if state_key is None or state_key not in ["is_processing", "field_errors"]:
            self.login_button.disabled = self.state.get("is_processing")
            self.login_button.text = "Verificando..." if self.state.get("is_processing") else "Acceder"

            self.username_input.error_text = self.state.get("field_errors").get("username", None)
            self.password_input.error_text = self.state.get("field_errors").get("password", None)

        else:
            if state_key == "is_processing":
                self.login_button.disabled = value
                self.login_button.text = "Verificando..." if value else "Acceder"

            elif state_key == "field_errors":
                self.username_input.error_text = value.get("username", None)
                self.password_input.error_text = value.get("password", None)

        self.username_input.update()
        self.password_input.update()
        self.login_button.update()

    def __on_login_click(self, event: ft.ControlEvent):
        self.state.set("is_processing", True)

        async def process_login():
            response = await self.controller.login(
                self.username_input.value.strip(),
                self.password_input.value.strip()
            )

            if not response["success"]:
                self.state.set("is_processing", False)
                self.state.set("field_errors", response.get("field_errors", {}))
                self.state.set("general_error", response.get("general_error"))
                return

            self.state.set("is_processing", False)
            self.state.set("field_errors", {})
            self.state.set("general_error", None)
            self._app_manager.page.go("/home")

        asyncio.run(process_login())

    def on_resized(self, event: ft.ControlEvent):
        if self.app_manager.page.width < 1200:
            pass
        else:
            pass


def login_page(app_manager):
    app_manager.page.title_text = "Login Page"
    return LoginPage(app_manager)
