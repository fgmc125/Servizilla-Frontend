import re
import logging
from urllib.parse import urlparse, parse_qs
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
        full_route = e.route
        self.logger.info(f"Route change detected: {full_route}")
        is_authenticated = self.app_manager.is_authenticated()

        parsed_url = urlparse(full_route)
        route_path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if route_path in self.routes:
            route_info = self.routes[route_path]
            if route_info["protected"] and not is_authenticated:
                self.logger.info(f"Access denied for protected route '{route_path}', redirecting to login")
                self.app_manager.page.go("/auth/login")
                return

            self.logger.debug(f"Loading exact route: {route_path}")
            self._load_route(route_path, route_info["page"], query_params)
            return

        for route_pattern, route_info in self.routes.items():
            dynamic_regex = self._convert_route_to_regex(route_pattern)
            match = re.match(f"^{dynamic_regex}$", route_path)

            if match:
                extracted_params = self._extract_params_from_route(route_pattern, match)
                self.logger.info(f"Detected dynamic route '{route_pattern}' with params: {extracted_params}")

                if route_info["protected"] and not is_authenticated:
                    self.logger.info(f"Access denied for protected route '{route_path}', redirecting to login")
                    self.app_manager.page.go("/auth/login")
                    return

                self._load_route(route_path, route_info["page"], {**extracted_params, **query_params})
                return

        self.logger.warning(f"Route '{route_path}' not found, redirecting to 404")
        self.app_manager.page.go("/404")

    def _convert_route_to_regex(self, route_pattern):
        type_map = {
            "int": r"\d+",
            "str": r"\w+",
            "slug": r"[-\w]+",
            "uuid": r"[0-9a-fA-F\-]+",
            "path": r".+",
        }

        # Expresión regular para detectar "<tipo:nombre>"
        param_pattern = re.compile(r"<(int|str|slug|uuid|path):(\w+)>")

        # Función de reemplazo que transforma los parámetros en regex
        def replace_param(match):
            param_type, param_name = match.groups()
            return rf"(?P<{param_name}>{type_map[param_type]})"

        # Reemplaza todos los parámetros encontrados en la ruta
        regex_pattern = param_pattern.sub(replace_param, route_pattern)

        # Agrega los delimitadores de inicio y fin para evitar coincidencias parciales
        regex_pattern = f"^{regex_pattern}$"

        return regex_pattern

    def _extract_params_from_route(self, route_pattern, match):
        param_names = re.findall(r"<(\w+:\w+)>", route_pattern)
        extracted_params = match.groupdict()

        for param in param_names:
            param_type, param_name = param.split(":")
            if param_type == "int":
                extracted_params[param_name] = int(extracted_params[param_name])
            elif param_type == "str":
                extracted_params[param_name] = str(extracted_params[param_name])

        return extracted_params

    def _load_route(self, route, page_func, params=None):
        self.logger.debug(f"Loading page function for route: {route} with params: {params}")

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

