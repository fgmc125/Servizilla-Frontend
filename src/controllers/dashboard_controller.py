import httpx
import asyncio


class ServicesController:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.base_url = "https://playground5.pythonanywhere.com/api/services/"
        self.session = self.app_manager.state_handler.get("access_token")

    async def fetch_services(self, page=1, filters=None):
        headers = {
            "Authorization": f"Bearer {self.session.get('access_token')}"
        }

        params = {"page": page}
        if filters:
            params.update(filters)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "services": data.get("results", []),
                        "next": data.get("next"),
                        "previous": data.get("previous"),
                        "count": data.get("count"),
                    }
                elif response.status_code == 401:
                    return {"success": False, "error": "No autorizado. Por favor, inicie sesión."}
                else:
                    return {"success": False, "error": "Error al cargar los servicios."}

            except httpx.RequestError as e:
                return {"success": False, "error": f"Error de conexión: {str(e)}"}
