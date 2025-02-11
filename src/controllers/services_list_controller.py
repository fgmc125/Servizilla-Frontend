import logging

from services.api_services import APIService


class ServicesListController:
    def __init__(self, app_manager):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._app_manager = app_manager

    async def get_categories(self, state):
        try:
            token = self._app_manager.state_handler.get("access_token")
            categories = await APIService.get_categories(token)

            if categories:
                state.set("categories", categories)
            else:
                self.logger.error("No se encontraron categorías.")
                state.set("general_error", "No se encontraron categorías.")

        except Exception as e:
            error_msg = f"Error al obtener las categorías: {str(e)}"
            self.logger.error(error_msg)
            state.set("general_error", error_msg)