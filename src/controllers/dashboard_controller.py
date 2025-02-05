import asyncio
import logging
from services.api_services import APIService


class ServicesController:
    def __init__(self, app_manager):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._app_manager = app_manager

    async def fetch_services(self, state):
        search_query = state.get("search_query", "").strip()
        category_filter = state.get("category_filter", None)
        elements_by_page = int(state.get("elements_by_page", 10))
        current_page = int(state.get("current_page", 1))

        category_id = None if category_filter == "T" else category_filter
        token = self._app_manager.state_handler.get("access_token")
        try:
            response = await APIService.list_services(
                search=search_query,
                category_id=category_id,
                page=current_page,
                page_size=elements_by_page,
                token=token,
                only_owner=True
            )

            if "error" in response:
                self.logger.error(f"Error en API: {response['error']}")
                state.set("general_error", response["error"])
            else:
                services = response.get("results", [])
                total_pages = max(1, (response.get("count", 0) // elements_by_page))

                state.set("services", services)
                state.set("total_pages", total_pages)
                state.set("general_error", None)

        except Exception as e:
            error_msg = f"Error en la solicitud: {str(e)}"
            self.logger.error(error_msg)
            state.set("general_error", error_msg)
            state.set("services", [])
