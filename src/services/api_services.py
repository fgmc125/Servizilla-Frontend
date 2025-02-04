import httpx

BASE_URL = "https://playground5.pythonanywhere.com/api"


class APIService:
    @staticmethod
    async def get_categories() -> dict:
        """Obtiene la lista de categorías."""
        url = f"{BASE_URL}/categories/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return APIService._handle_response(response)

    @staticmethod
    async def get_request_status_list() -> dict:
        """Obtiene la lista de estados posibles de las solicitudes."""
        url = f"{BASE_URL}/requests/status/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return APIService._handle_response(response)

    @staticmethod
    async def list_services(
            token: str, search: str = "", category_id: int = None,
            created_at_min: str = None, created_at_max: str = None,
            updated_at_min: str = None, updated_at_max: str = None,
            page: int = 1, page_size: int = 10, only_owner:bool =False,
            oferente_id:int=None
    ) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{BASE_URL}/services/"
        params = {
            "search": search.strip() if search else None,
            "category_id": category_id if category_id else None,
            "created_at_min": created_at_min,
            "created_at_max": created_at_max,
            "updated_at_min": updated_at_min,
            "updated_at_max": updated_at_max,
            "page": page,
            "page_size": page_size,
            "only_owner": only_owner,
            "oferente_id": oferente_id
        }
        params = {k: v for k, v in params.items() if v is not None}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP Error {e.response.status_code}: {e.response.text}"}
            except httpx.RequestError as e:
                return {"error": f"Error en la solicitud: {str(e)}"}

    @staticmethod
    async def get_service_detail(service_id: int, token: str) -> dict:
        """Obtiene los detalles de un servicio específico."""
        url = f"{BASE_URL}/services/{service_id}/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def create_service(data: dict, token: str) -> dict:
        """Crea un nuevo servicio."""
        url = f"{BASE_URL}/services/create/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def update_service(service_id: int, data: dict, token: str) -> dict:
        """Actualiza un servicio existente."""
        url = f"{BASE_URL}/services/{service_id}/update/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def partial_update_service(service_id: int, data: dict, token: str) -> dict:
        """Realiza una actualización parcial de un servicio."""
        url = f"{BASE_URL}/services/{service_id}/partial_update/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def delete_service(service_id: int, token: str) -> dict:
        """Elimina (archiva) un servicio."""
        url = f"{BASE_URL}/services/{service_id}/delete/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def list_requests(token: str) -> dict:
        """Obtiene la lista de solicitudes del usuario autenticado."""
        url = f"{BASE_URL}/requests/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def get_request_detail(request_id: int, token: str) -> dict:
        """Obtiene los detalles de una solicitud específica."""
        url = f"{BASE_URL}/requests/{request_id}/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def update_request(request_id: int, data: dict, token: str) -> dict:
        """Actualiza completamente una solicitud."""
        url = f"{BASE_URL}/requests/{request_id}/update/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def partial_update_request(request_id: int, data: dict, token: str) -> dict:
        """Realiza una actualización parcial de una solicitud."""
        url = f"{BASE_URL}/requests/{request_id}/partial_update/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def delete_request(request_id: int, token: str) -> dict:
        """Elimina (archiva) una solicitud."""
        url = f"{BASE_URL}/requests/{request_id}/delete/"
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    async def create_request(service_id: int, content: str, token: str) -> dict:
        """Crea una nueva solicitud de servicio."""
        url = f"{BASE_URL}/requests/create/"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "service_id": service_id,
            "content": content
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            return APIService._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> dict:
        """Manejo de respuestas HTTP, incluyendo errores."""
        try:
            data = response.json()
        except ValueError:
            return {"success": False, "error": "Respuesta no válida del servidor.", "status_code": response.status_code}

        if response.status_code in [200, 201]:
            return {"success": True, "data": data}

        return {
            "success": False,
            "error": data.get("message", data.get("error", "Error desconocido.")),
            "status_code": response.status_code
        }
