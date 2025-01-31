from flet import (
    BorderSide, ButtonStyle, Column, Container, CrossAxisAlignment, ElevatedButton, FontWeight,
    MainAxisAlignment, Page, RoundedRectangleBorder, Row, Text, TextAlign, TextButton, TextStyle,
    alignment, app, Colors, margin, padding
)


#success page falta


def create_error_page(app_manager, code, title, message):
    app_manager.page.title = f"{title}"
    app_manager.page.vertical_alignment = MainAxisAlignment.CENTER
    app_manager.page.horizontal_alignment = CrossAxisAlignment.CENTER

    error_code = Container(
        content=Text(
            str(code),
            size=96,
            weight=FontWeight.BOLD,
            color='#384551',
            font_family="Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif",
            selectable=True
        ),
        alignment=alignment.center
    )

    error_alert = Container(
        content=Text(
            title,
            size=23,
            weight=FontWeight.BOLD,
            color="#384551",
            font_family="Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif",
            selectable=True
        ),
        alignment=alignment.center,
    )

    error_message = Container(
        content=Text(
            message,
            size=15,
            color="#646E78",
            font_family="Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif",
            text_align=TextAlign.CENTER,
            selectable=True
        ),
        alignment=alignment.center,
    )

    btn_back_to_home = Container(
        content=ElevatedButton(
            text="Volver al Inicio",
            on_click=lambda e: app_manager.page.go("/home"),
            style=ButtonStyle(
                bgcolor="#964BF8",
                color=Colors.WHITE,
                padding=padding.only(bottom=8, top=8, left=20, right=20),
                text_style=TextStyle(
                    size=16,
                    weight=FontWeight.W_500,
                    font_family="Plus Jakarta Sans",
                ),
                side=BorderSide(
                    color=Colors.TRANSPARENT,
                    width=1,
                ),
                elevation=3,
                shape=RoundedRectangleBorder(radius=12),
            ),
            expand=True,
            height=44,
        )
    )

    return Container(
        content=Column(
            controls=[
                error_code,
                error_alert,
                error_message,
                btn_back_to_home
            ],
            spacing=20,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        margin=margin.all(34),
        alignment=alignment.center,
        expand=True,
    )


def code_401(app_manager):
    return create_error_page(
        app_manager, 401, "¡No estás autorizado! 🔐",
        "No tienes permiso para acceder a esta página. ¡Vuelve a la página principal!"
    )


def code_404(app_manager):
    return create_error_page(
        app_manager, 404, "Página No Encontrada ⚠️",
        "No pudimos encontrar lo que estás buscando."
    )


def code_500(app_manager):
    return create_error_page(
        app_manager, 500, "¡Oops! Algo salió mal 🔧",
        "Parece que estamos experimentando problemas técnicos. Nuestro equipo está trabajando para resolverlo. Por favor, intenta nuevamente en unos momentos."
    )


def code_503(app_manager):
    return create_error_page(
        app_manager, 503, "¡Servicio No Disponible! 🚧",
        "Disculpa las molestias, estamos realizando mantenimiento en este momento."
    )


def main(page: Page):
    page.spacing = 0
    page.padding = 0
    page.margin = 0
    page.window.width = 450
    page.bgcolor = "#F5F5F9"
    page.add(code_401(page))


if __name__ == "__main__":
    app(target=main)
