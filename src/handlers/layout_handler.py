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
        """Method to handle clearing the current view container content."""
        if self.view_container is not None and hasattr(self.view_container, 'content'):
            try:
                if self.view_container.content:
                    self.logger.debug("Clearing current view_container content")
                    self.logger.info(f"-----> self.view_container.content: {self.view_container.content}")
                    self.logger.info(f"-----> type self.view_container: {type(self.view_container)}")
                    self.logger.info(f"-----> type content: {type(self.view_container.content)}")
                    # Verifica si content tiene clean() antes de llamar
                    if hasattr(self.view_container.content, 'clean') and callable(self.view_container.content.clean):
                        self.view_container.content.clean()
                    else:
                        self.logger.warning("view_container.content no tiene el método 'clean'")
                    self.view_container.update()
            except AttributeError as e:
                self.logger.warning(f"Attempt to clear content failed due to AttributeError: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error while clearing content: {e}")

    def load_layout(self, route, page_func):
        if self.view_container and hasattr(self.view_container, 'content'):
            self.logger.debug(f"view_container controls before update: {self.view_container.content}")

        self.logger.info(f"-------------------> self.view_container: {self.view_container}")
        self.logger.info(f"-------------------> self.view_container.content: {self.view_container.content}")
        self.logger.info(f"-------------------> self.view_container.content: {type(self.view_container.content)}")
        if self.view_container is not None:
            self.logger.info(f"Loading layout for route: {route}")
            route_config = self.app_manager.get_route(route)
            self.logger.info(f"-------------------> route_config: {route_config}")
            layout_class = route_config.get("layout")
            self.logger.info(f"-------------------> layout_class: {layout_class}")

            if layout_class:
                self.logger.info(f"-------------------> self.current_layout is None: {self.current_layout is None}")
                self.logger.info(f"-------------------> not isinstance(self.current_layout, layout_class): {not isinstance(self.current_layout, layout_class)}")
                if self.current_layout is None or not isinstance(self.current_layout, layout_class):
                    self.logger.debug(f"Changing layout to: {layout_class.__name__}")
                    self.current_layout = layout_class(self.app_manager)

                    self._clear_current_content()

                    self.current_layout = layout_class(self.app_manager)
                    self.view_container.content = self.current_layout
                    self.logger.debug(f"New layout set: {layout_class.__name__}")

                    self.logger.info(f"-----> self.view_container: {self.view_container}")
                    self.logger.info(f"-----> self.view_container type: {type(self.view_container)}")
                    self.logger.info(f"-----> self.view_container.content type: {type(self.view_container.content)}")
                    self.logger.info(f"-----> self.view_container.content.content type: {type(self.view_container.content.content)}")

                    for control in self.app_manager.page.controls:
                        self.logger.info(f"-----> self.app_manager.page: {control}")
                        if hasattr(control, "content"):
                            self.logger.info(f"-----> control.content: {control.content}")

                    self.app_manager.page.update()
                    self.logger.info(f"Layout {layout_class.__name__} loaded <----")

            self.logger.info(
                f'-------------------> hasattr(self.current_layout, "render_content"): {hasattr(self.current_layout, "render_content")}')
            if hasattr(self.current_layout, "render_content"):
                self.logger.debug(f"Rendering content for route: {route}")
                content = page_func(self.app_manager) if callable(page_func) else page_func
                self.logger.info(f'-------------------> content: {type(content)} / {content}')
                try:
                    self.current_layout.render_content(content)
                    self.view_container.update()
                    self.logger.info(f"Content rendered for route: {route}")
                except Exception as e:
                    self.logger.error(f"Error rendering content for route {route}: {e}")
        else:
            self.logger.warning("view_container is None; cannot load layout")
