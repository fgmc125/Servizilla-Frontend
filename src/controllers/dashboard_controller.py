import httpx
import asyncio
import logging


class ServicesController:
    def __init__(self, app_manager):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.app_manager = app_manager
        self.base_url = "https://playground5.pythonanywhere.com/api/services/"
        self.access_token = self.app_manager.get_state("access_token")

    async def fetch_services(self, page=1, filters=None, search=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        self.logger.info(f"[CONTROLLER] access_token: {self.access_token}")
        params = {"page": page}
        if filters:
            params.update(filters)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, headers=headers, params=params)

                self.logger.info(f"[CONTROLLER] response: {response.json()}")

                if response.status_code == 200:
                    data = response.json()
                    services = data.get("results", [])

                    self.app_manager.state_handler.set("services_data", {
                        "services": services,
                        "next": data.get("next"),
                        "previous": data.get("previous"),
                        "count": data.get("count"),
                    })

                    return {"success": True}

                elif response.status_code == 401:
                    return {"success": False, "error": "No autorizado. Por favor, inicie sesión."}

                return {"success": False, "error": "Error al cargar los servicios."}

            except httpx.RequestError as e:
                return {"success": False, "error": f"Error de conexión: {str(e)}"}