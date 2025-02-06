import asyncio
import requests
import flet as ft

from contents.content import PageContainer
from utils.style_helper import label_style, text_style

class ServiceDetailPage(PageContainer):
    def __init__(self, app_manager, service_id):
        super().__init__()
        self._app_manager = app_manager
        self.service_id = service_id

        self.state.register("is_loading", True)
        self.state.register("service", None)
        self.state.subscribe("is_loading", self.update_ui)
        self.state.subscribe("service", self.update_ui)

        self.build_ui()
        self.load_service_data()

    def build_ui(self):
        self.service_image = ft.Image(src="", height=200, fit=ft.ImageFit.CONTAIN)
        self.service_name = ft.Text(value="Cargando...", size=20, weight=ft.FontWeight.BOLD, text_style=text_style)
        self.service_description = ft.Text(value="", size=14, text_style=text_style)
        self.service_price = ft.Text(value="", size=14, text_style=text_style)
        self.service_category = ft.Text(value="", size=12, color="#7C89B0")
        self.service_oferente = ft.Text(value="", size=12, color="#7C89B0")
        self.loading_indicator = ft.ProgressRing(visible=True)

        column_child = ft.Column(
            controls=[
                self.service_image,
                self.service_name,
                self.service_description,
                self.service_price,
                self.service_category,
                self.service_oferente,
                self.loading_indicator
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        container_wrapper = ft.Container(
            content=ft.SafeArea(content=column_child),
            width=400,
            bgcolor="#FFFFFF",
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            expand=True,
        )

        self.content = container_wrapper

    def load_service_data(self):
        base_url = "https://playground5.pythonanywhere.com/"
        url = f"{base_url}{self.service_id}/"

        headers = {"Authorization": f"Bearer {self._app_manager.token}"}

        async def fetch_service():
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.state.set("service", response.json())
            else:
                self.state.set("service", None)
            self.state.set("is_loading", False)

        asyncio.run(fetch_service())

    def update_ui(self, state_key=None, value=None):
        service = self.state.get("service")
        is_loading = self.state.get("is_loading")

        if is_loading:
            self.loading_indicator.visible = True
            return

        self.loading_indicator.visible = False

        if service:
            #self.service_image.src = service.get("image", "https://via.placeholder.com/200")
            self.service_name.value = service.get("name", "Nombre no disponible")
            self.service_description.value = service.get("description", "Sin descripción")
            self.service_price.value = f"Precio: ${service.get('price', 'N/A')}"
            self.service_category.value = f"Categoría: {service['category']['name']}"
            self.service_oferente.value = f"Oferente: {service['oferente']['username']}"

        self.service_image.update()
        self.service_name.update()
        self.service_description.update()
        self.service_price.update()
        self.service_category.update()
        self.service_oferente.update()

def service_detail_page(app_manager, service_id):
    return ServiceDetailPage(app_manager, service_id)
