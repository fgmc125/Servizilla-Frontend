import flet as ft

label_style = ft.TextStyle(
    color="#7C89B0",
    weight=ft.FontWeight.W_500,
    font_family="Plus Jakarta Sans",
)

text_style = ft.TextStyle(
    color="#101213",
    weight=ft.FontWeight.W_500,
    font_family="Plus Jakarta Sans",
)

primary_button_style = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.DISABLED: "#f1f4f8",
        ft.ControlState.DEFAULT: "#964BF8",
    },
    color={
        ft.ControlState.DISABLED: "#7C89B0",
        ft.ControlState.DEFAULT: ft.Colors.WHITE,
    },
    text_style=ft.TextStyle(
        size=16,
        weight=ft.FontWeight.W_500,
        font_family="Plus Jakarta Sans",
    ),
    side=ft.BorderSide(
        color=ft.Colors.TRANSPARENT,
        width=1,
    ),
    elevation=1,
    shape=ft.RoundedRectangleBorder(radius=12),
)

input_label_style = ft.TextStyle(
    color="#7C89B0",
    weight=ft.FontWeight.W_500,
    font_family="Plus Jakarta Sans",
)

input_text_style = ft.TextStyle(
    color="#101213",
    weight=ft.FontWeight.W_500,
    font_family="Plus Jakarta Sans",
)

button_style_submit = ft.ButtonStyle(
    bgcolor={ft.ControlState.DEFAULT: ft.Colors.PURPLE_300},
    color={ft.ControlState.DEFAULT: ft.colors.WHITE},
    text_style=ft.TextStyle(
        size=16,
        weight=ft.FontWeight.W_500,
        font_family="Plus Jakarta Sans"
    ),
    side=ft.BorderSide(color=ft.colors.TRANSPARENT, width=1),
    shape=ft.RoundedRectangleBorder(radius=8),
)
