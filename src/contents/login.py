import flet as ft


def _build_header(title, subtitle):
    text_title = ft.Text(
        value=title,
        size=32,
        weight=ft.FontWeight.W_600,
        color="#7C89B0",
        font_family="Urbanist",
        selectable=True
    )

    text_subtitle = ft.Text(
        value=subtitle,
        size=14,
        weight=ft.FontWeight.W_500,
        color="#7C89B0",
        font_family="Plus Jakarta Sans",
        selectable=True,
    )

    text_title_container = ft.Container(
        content=text_title,
        padding=ft.padding.only(top=50),
        alignment=ft.alignment.center_left
    )

    text_subtitle_cotainer = ft.Container(
        content=text_subtitle,
        padding=ft.padding.only(top=12, bottom=24),
        alignment=ft.alignment.center_left
    )

    layout = ft.Column(
        controls=[
            text_title_container,
            text_subtitle_cotainer
        ]
    )
    return layout


def _build_component(app_manager):
    def on_login_click(event):
        if not validate_fields():
            app_manager.page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, completa todos los campos obligatorios."),
                bgcolor="red"
            )
            app_manager.page.snack_bar.open = True
            app_manager.page.update()
            return

        username = email_address_input.content.value.strip()
        password = password_input.content.value.strip()

        app_manager.page.snack_bar.open = True
        app_manager.page.update()

    def validate_fields():
        error_color = "#BA1A1A"
        success_color = "#45BE88"
        has_error = False

        user_value = email_address_input.content.value.strip()
        if not user_value:
            email_address_input.content.error_text = "El usuario es obligatorio."
            email_address_input.content.fill_color = ft.colors.with_opacity(1, "#f1f4f8")
            has_error = True
        else:
            email_address_input.content.error_text = None
            email_address_input.content.suffix = ft.Icon(
                name=ft.icons.CHECK,
                color=success_color,
                size=18,
            )
            email_address_input.content.fill_color = ft.colors.with_opacity(0.16, success_color)

        email_address_input.content.update()

        password_value = password_input.content.value.strip()
        if not password_value:
            password_input.content.error_text = "La contraseña es obligatoria."
            password_input.content.fill_color = ft.colors.with_opacity(1, "#f1f4f8")
            has_error = True
        else:
            password_input.content.error_text = None
            password_input.content.suffix = ft.Icon(
                name=ft.icons.CHECK,
                color=success_color,
                size=18,
            )
            password_input.content.fill_color = ft.colors.with_opacity(0.16, success_color)

        password_input.content.update()

        return not has_error

    email_address_input = ft.Container(
        content=ft.TextField(
            label="Usuario",
            color="#57636c",
            label_style=ft.TextStyle(
                color="#7C89B0",
                weight=ft.FontWeight.W_500,
                font_family="Plus Jakarta Sans",
            ),
            max_lines=1,
            text_size=16,
            text_style=ft.TextStyle(
                color="#101213",
                weight=ft.FontWeight.W_500,
                font_family="Plus Jakarta Sans",
            ),
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color="#45BE88",
        ),
        padding=ft.padding.only(bottom=10),
        margin=ft.margin.all(0),
    )

    password_input = ft.Container(
        content=ft.TextField(
            label="Contraseña",
            password=True,
            color="#57636c",
            label_style=ft.TextStyle(
                color="#7C89B0",
                weight=ft.FontWeight.W_500,
                font_family="Plus Jakarta Sans",
            ),
            border_radius=12,
            border_color="#f1f4f8",
            border_width=2,
            filled=True,
            fill_color="#f1f4f8",
            focused_border_color="#45BE88",
            can_reveal_password=True,
        ),
        padding=ft.padding.only(bottom=10),
        margin=ft.margin.all(0),
    )

    remember_me = ft.Checkbox(
        label="Recordarme",
        label_style=ft.TextStyle(color="#7C89B0", size=15)
    )

    btn_forgot_password = ft.TextButton(
        text="¿Olvidaste tu contraseña?",
        style=ft.ButtonStyle(color="#45BE88"),
    )

    remember_and_forgot_password_row = ft.Container(
        content=ft.Row(
            controls=[remember_me, btn_forgot_password],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        margin=ft.margin.only(bottom=12),
    )

    login_button = ft.ElevatedButton(
        text="Acceder",
        on_click=on_login_click,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DISABLED: "#f1f4f8",
                # ft.ControlState.HOVERED: "ft.Colors.WHITE",
                ft.ControlState.DEFAULT: "#45BE88"
            },
            color={
                ft.ControlState.DISABLED: "#7C89B0",
                # ft.ControlState.HOVERED: "#45BE88",
                ft.ControlState.DEFAULT: ft.colors.WHITE,
            },
            text_style=ft.TextStyle(
                size=16,
                weight=ft.FontWeight.W_500,
                font_family="Plus Jakarta Sans",
            ),
            side=ft.BorderSide(
                color=ft.colors.TRANSPARENT,
                width=1,
            ),
            shape=ft.RoundedRectangleBorder(radius=16),
        ),
        expand=True,
        height=42,
    )

    login_button_layout = ft.Row([login_button],expand=True)

    signup_text_hint = ft.Text(
        value="¿No tienes una cuenta?",
        color="#7C89B0",
        size=14,
        weight=ft.FontWeight.W_600,
        selectable=True
    )

    btn_signup_text = ft.TextButton(
        text="Regístrate aquí",
        on_click=lambda e: app_manager.page.go("/auth/signup"),
        style=ft.ButtonStyle(color="#45BE88")
    )

    signup_text = ft.Container(
        content=ft.Row(
            [signup_text_hint, btn_signup_text],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(bottom=8),
    )

    column_child = ft.Column(
        controls=[
            _build_header("¡Bienvenido!👋", "Ingrese su Usuario y su contraseña para acceder a la plataforma."),
            email_address_input,
            password_input,
            remember_and_forgot_password_row,
            login_button_layout,
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

    container = ft.Container(
        content=ft.SafeArea(content=container_child),
        width=430,
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

    return container


def login_page(app_manager):
    app_manager.page.title = "Login Page"

    def unfocused(event: ft.ControlEvent):
        for control in app_manager.page.controls:
            if isinstance(control, ft.TextField):
                control.blur()
        app_manager.page.update()

    gesture_detector = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.BASIC,
        on_tap=unfocused,
        content=_build_component(app_manager),
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
    return container


def main(page: ft.Page):
    page.padding = ft.padding.all(0)
    page.add(login_page(page))
    page.expand = True


if __name__ == "__main__":
    ft.app(target=main)
