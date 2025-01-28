import logging

import flet as ft

from handlers.RouteHandler import RouteHandler
from handlers.LayoutHandler import LayoutHandler
from handlers.SessionHandler import SessionHandler
from handlers.ResizeHandler import ResizeHandler
from handlers.StateHandler import StateHandler


class AppManager:
    def __init__(self):
        self.safe_area = None
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.debug("Initializing AppManager")
            self.page = None
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
        self.page.title = "Mi App Prototipo"
        self.page.spacing = 0
        self.page.padding = ft.padding.all(0)
        self.page.bgcolor = '#F5F5F9'
        self.page.expand = True

        self.logger.debug("Configuring AppBar and view container")
        self.page.appbar = ft.AppBar(
            toolbar_height=5,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self.safe_area = ft.SafeArea(content=self.view_container, expand=True)

        self.page.add(self.safe_area)
        self.page.update()

        self.logger.debug("Setting up route change listener")

        self.page.on_resized = self.resize_handler.on_resized

        self.page.on_route_change = self.route_handler.route_change
        self.route_handler.start()

    # ------------------------------------------------------------------------------------------------------------------
    # MANEJO DE EVENTOS
    # ------------------------------------------------------------------------------------------------------------------

    def go(self, route: str):
        self.logger.info(f"Navigating to route: {route}")
        self.page.go(route)

    def load_layout(self, route: str, callback):
        self.logger.debug(f"Loading layout for route: {route}")
        self.layout_handler.load_layout(route, callback)

    def is_authenticated(self) -> bool:
        return self.session_handler.is_authenticated

    def get_route(self, route: str) -> ft.Container:
        self.logger.debug(f"Retrieving route configuration for: {route}")
        return self.route_handler.routes.get(route, {})

    def authenticate(self, user: str, password: str):
        return True
