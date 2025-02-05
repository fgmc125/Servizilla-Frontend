import flet as ft
from contents.content import PageContainer


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
        self.state.register("is_view_loading", False)
        self.state.register("products", [])
        self.state.register("current_page", 1)

        self.build_ui()

    def build_ui(self):
        search_bar = ft.TextField(
            label="Search here...",
            prefix_icon=ft.icons.SEARCH,
            width=300
        )

        categories = ft.Column(
            controls=[
                ft.Text("CATEGORIES", weight=ft.FontWeight.W_600),
                ft.Divider(),
                ft.TextButton("Brand One"),
                ft.TextButton("Brand Two"),
                ft.TextButton("Mobile"),
                ft.TextButton("Tab"),
                ft.TextButton("Watch"),
                ft.TextButton("Head Phone"),
                ft.TextButton("Memory"),
                ft.TextButton("Accessories"),
                ft.TextButton("Top Brands"),
                ft.TextButton("Jewelry"),
            ],
            spacing=5
        )

        products_grid = ft.GridView(
            expand=True,
            runs_count=3,
            child_aspect_ratio=1,
            spacing=10,
            controls=[
                ProductCard(
                    image="https://via.placeholder.com/150",
                    name="PRODUCT NAME",
                    price="869.00",
                    rating=4
                ) for _ in range(9)
            ]
        )

        pagination = ft.Row(
            controls=[
                ft.TextButton("<"),
                ft.TextButton("01"),
                ft.TextButton("02"),
                ft.TextButton("03"),
                ft.TextButton("04"),
                ft.TextButton("05"),
                ft.TextButton(">"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Layout assembly
        container_wrapper = ft.Row(
            controls=[
                categories,
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                search_bar,
                                ft.IconButton(icon=ft.icons.VIEW_MODULE, tooltip="Grid View"),
                                ft.IconButton(icon=ft.icons.VIEW_LIST, tooltip="List View"),
                                ft.Text("Sort by:", size=12),
                                ft.Dropdown(
                                    options=[
                                        ft.dropdown.Option("Newest items"),
                                        ft.dropdown.Option("Price: Low to High"),
                                        ft.dropdown.Option("Price: High to Low")
                                    ],
                                    width=150
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        products_grid,
                        pagination
                    ],
                    tight=True,
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=10
                )
            ],
            expand=True,
            tight=True,
            alignment=ft.MainAxisAlignment.START
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
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        container = ft.Container(
            content=layout,
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            bgcolor="white",
            border_radius=10
        )

        self.content = container


def product_catalog_page(app_manager):
    app_manager.page.title_text = "Product Catalog"
    return ProductCatalogPage(app_manager)
