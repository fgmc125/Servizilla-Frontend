import logging
import asyncio

import flet as ft

from handlers.route_handler import RouteHandler
from handlers.layout_handler import LayoutHandler
from handlers.session_handler import SessionHandler
from handlers.resize_handler import ResizeHandler
from handlers.state_handler import StateHandler
from services.auth_service import AuthService

class AppManager:
    def __init__(self):
        self.safe_area = None
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.debug("Initializing AppManager")
            self.page: ft.Page or None = None
            self.view_container = None

            self.build_view_container()

            self.logger.debug("Creating RouteHandler, SessionHandler, and LayoutHandler")
            self.route_handler = RouteHandler(self)
            self.session_handler = SessionHandler(self)
            self.layout_handler = LayoutHandler(self)

            self.state_handler = StateHandler()
            self.resize_handler = ResizeHandler()

            self.initialized = True
            self.logger.debug("AppManager ha sido inicializada e instanciada")

    def build_view_container(self):
        self.view_container = ft.AnimatedSwitcher(
            content=ft.Container(
                expand=True,
                padding=ft.padding.all(0),
                margin=ft.margin.all(0),
            ),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=500,
            expand=True
        )

    def initialize_app(self):
        self.logger.info("Initializing the application")
        self.page.title_text = "Mi App Prototipo"
        self.page.spacing = 0
        self.page.padding = ft.padding.all(0)
        self.page.bgcolor = '#F4F5F6'
        self.page.expand = True

        self.logger.debug("Configuring AppBar and view container")
        self.page.appbar = ft.AppBar(
            toolbar_height=5,
            bgcolor=ft.Colors.SURFACE
        )
        self.safe_area = ft.SafeArea(content=self.view_container, expand=True)

        self.page.add(self.safe_area)
        self.page.update()

        self.logger.debug("Setting up route change listener")

        self.page.on_resized = self.resize_handler.on_resized

        asyncio.run(self._get_token_stored())
        self.state_handler.subscribe("access_token", self._token_store)
        self.state_handler.subscribe("refresh_token", self._token_store)

        self.page.on_route_change = self.route_handler.route_change
        self.route_handler.start()

    # ------------------------------------------------------------------------------------------------------------------
    # MANEJO DE EVENTOS
    # ------------------------------------------------------------------------------------------------------------------

    def go(self, route: str):
        self.logger.info(f"Navigating to route: {route}")
        self.page.go(route)

    def load_layout(self, route: str, callback, params=None):
        self.logger.info(f"Received params in LayoutHandler: {params} (type: {type(params)})")
        self.logger.debug(f"Loading layout for route: {route} with params: {params}")

        self.logger.info(f"Passing params to LayoutHandler.load_layout(): {params} (type: {type(params)})")
        self.layout_handler.load_layout(route, callback, params=params)

    def is_authenticated(self) -> bool:
        self.logger.debug(f"[IS AUTHENTICATED?]{self.state_handler.get("is_authenticated")}")
        return self.state_handler.get("is_authenticated")

    def get_route(self, route: str) -> ft.Container:
        self.logger.debug(f"Retrieving route configuration for: {route}")
        return self.route_handler.routes.get(route, {})

    def authenticate(self, user: str, password: str):
        self.logger.debug(f"[IS AUTHENTICATED?]{self.state_handler.get("is_authenticated")}")
        return self.state_handler.get("is_authenticated")

    # ------------------------------------------------------------------------------
    # StateHandler Events
    # ------------------------------------------------------------------------------

    def get_state(self, key):
        return self.state_handler.get(key)

    def set_state(self, key: str, value):
        self.state_handler.set(key, value)

    def subscribe_state(self, key: str, callback):
        self.state_handler.subscribe(key, callback)

    def _token_store(self, key, value):
        self.page.client_storage.set(f"servizilla.{key}", value)

    async def _get_token_stored(self):
        self.logger.info(f"access_token 2: {
        self.page.client_storage.contains_key('servizilla.access_token')
        }")

        success = False

        access_token = None
        refresh_token = None

        if self.page.client_storage.contains_key("servizilla.access_token"):
            access_token = self.page.client_storage.get("servizilla.access_token")

        if self.page.client_storage.contains_key("servizilla.refresh_token"):
            refresh_token = self.page.client_storage.get("servizilla.refresh_token")

        if access_token and refresh_token:
            user_info = await AuthService.get_user_info(access_token)

            if user_info.get("success"):
                success = True
                self.state_handler.register("user_info", user_info["user"])
            else:
                self.logger.warning("Token inválido o expirado, el usuario no está autenticado")

        self.state_handler.register("is_authenticated", success)

        self.logger.info(f"access_token: {access_token}, refresh_token: {refresh_token}")
        self.logger.info(f"KEYS: {self.page.client_storage.get_keys('servizilla.')}")

        self.state_handler.register("access_token", access_token)
        self.state_handler.register("refresh_token", refresh_token)
