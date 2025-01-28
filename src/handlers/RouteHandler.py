import logging

from routes.urls import routes


class RouteHandler:
    def __init__(self, app_manager):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.debug("Initializing RouteManager")

            self.app_manager = app_manager
            self.routes = routes
            self.history = []
            self.current_route = None
            self.view_container = app_manager.view_container
            self.initialized = True
            self.logger.debug("RouteManager initialized with routes")

    def start(self):
        self.logger.info("Starting navigation")
        self.app_manager.go(self.app_manager.page.route or "/dashboard")

    def route_change(self, e):
        route = e.route
        self.logger.info(f"Route change detected: {route}")
        is_authenticated = self.app_manager.is_authenticated()

        if route not in self.routes:
            self.logger.warning(f"Route '{route}' not found, redirecting to 404")
            self.app_manager.page.go("/404")
            return

        if route == '/auth/logout':
            log = self.app_manager.session_handler.logout()
            print(log)
            self.app_manager.page.go("/auth/login")
            return

        if self.routes[route]["protected"] and not is_authenticated:
            self.logger.info(f"Access denied for protected route '{route}', redirecting to login")
            self.app_manager.page.go("/auth/login")
            return

        self.logger.debug(f"Loading route: {route}")
        self._load_route(route)

    def _load_route(self, route):
        page_func = self.routes[route]["page"]
        self.logger.debug(f"Loading page function for route: {route} of type {type(page_func)}")

        if hasattr(self.view_container, 'content'):
            self.logger.debug(
                f"Current view_container content before loading route: {self.view_container.content}")

        if self.view_container is not None:
            self.history.append(route)
            self.current_route = route
            self.logger.info(f"[RouteManager] Route '{route}' loaded, updating layout")
            try:
                self.app_manager.load_layout(route, page_func)
            except Exception as e:
                self.logger.error(f"Error loading layout for route {route}: {e}")
        else:
            self.logger.warning("view_container is None; cannot load route")

