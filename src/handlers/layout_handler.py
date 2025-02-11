import logging


class LayoutHandler:
    def __init__(self, app_manager):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.debug("Initializing LayoutManager")

            self.app_manager = app_manager
            self.current_layout = None
            self.view_container = self.app_manager.view_container
            self.initialized = True
            self.logger.debug("LayoutManager initialized")

    def _clear_current_content(self):
        if self.view_container is not None and hasattr(self.view_container, 'content'):
            try:
                if self.view_container.content:
                    self.logger.debug("Clearing current view_container content")
                    self.logger.info(f"-----> self.view_container.content: {self.view_container.content}")
                    self.logger.info(f"-----> type self.view_container: {type(self.view_container)}")
                    self.logger.info(f"-----> type content: {type(self.view_container.content)}")

                    if hasattr(self.view_container.content, 'clean') and callable(self.view_container.content.clean):
                        self.view_container.content.clean()
                    else:
                        self.logger.warning("view_container.content no tiene el método 'clean'")
                    self.view_container.update()
            except AttributeError as e:
                self.logger.warning(f"Attempt to clear content failed due to AttributeError: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error while clearing content: {e}")

    def load_layout(self, route, page_func, params=None):
        self.logger.info(f"Inside LayoutHandler.load_layout() - Received params: {params} (type: {type(params)})")
        self.logger.info(f"Ejecutando LayoutHandler.load_layout() para {route} con params {params}")

        if self.view_container and hasattr(self.view_container, 'content'):
            self.logger.debug(f"view_container controls before update: {self.view_container.content}")

        self.logger.info(f"Loading layout for route: {route} with params: {params}")
        route_config = self.app_manager.get_route(route)
        layout_class = route_config.get("layout")

        if layout_class:
            if self.current_layout is None or not isinstance(self.current_layout, layout_class):
                self.logger.debug(f"Changing layout to: {layout_class.__name__}")
                self.current_layout = layout_class(self.app_manager)

                self._clear_current_content()

                self.current_layout = layout_class(self.app_manager)
                self.view_container.content = self.current_layout
                self.logger.debug(f"New layout set: {layout_class.__name__}")

                self.app_manager.page.update()

        if hasattr(self.current_layout, "render_content"):
            self.logger.debug(f"Rendering content for route: {route}")

            content = page_func(self.app_manager, **params) if params else page_func(self.app_manager)

            try:
                self.current_layout.render_content(content)
                self.view_container.update()
                self.logger.info(f"Content rendered for route: {route}")
            except Exception as e:
                self.logger.error(f"Error rendering content for route {route}: {e}")

