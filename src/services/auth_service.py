import httpx

BASE_URL = "https://playground5.pythonanywhere.com/auth"


class AuthService:
    @staticmethod
    async def login(username: str, password: str) -> dict:
        url = f"{BASE_URL}/login/"
        payload = {
            "username": username,
            "password": password
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)

                try:
                    data = response.json()
                except ValueError:
                    return {
                        "success": False,
                        "error": "Error inesperado en el servidor.",
                        "status_code": response.status_code
                    }

                if response.status_code == 200:
                    return {
                        "success": True,
                        "access_token": data["access_token"],
                        "refresh_token": data["refresh_token"]
                    }

                elif response.status_code == 400:
                    return {
                        "success": False,
                        "error": "El nombre de usuario y la contraseña son obligatorios.",
                        "status_code": 400
                    }

                elif response.status_code == 401:
                    return {
                        "success": False,
                        "error": "Credenciales inválidas. Verifique su nombre de usuario y contraseña.",
                        "status_code": 401
                    }

                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Error desconocido."),
                        "status_code": response.status_code
                    }

            except httpx.RequestError as e:
                return {
                    "success": False,
                    "error": f"Error de conexión: {str(e)}",
                    "status_code": 0
                }

    @staticmethod
    async def signup(username: str, password: str, email: str) -> dict:
        url = f"{BASE_URL}/register/"
        payload = {
            "username": username,
            "password": password,
            "email": email
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)

                try:
                    data = response.json()
                except ValueError:
                    return {
                        "success": False,
                        "error": "Error inesperado en el servidor.",
                        "status_code": response.status_code
                    }

                if response.status_code == 201:
                    return {
                        "success": True,
                        "message": "Registro exitoso"
                    }

                elif response.status_code == 409:
                    return {
                        "success": False,
                        "error": data.get("error", "Error desconocido."),
                        "status_code": 409
                    }

                elif response.status_code == 422:
                    return {
                        "success": False,
                        "field_errors": data,
                        "status_code": 422
                    }

                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Error desconocido."),
                        "status_code": response.status_code
                    }

            except httpx.RequestError as e:
                return {
                    "success": False,
                    "error": f"Error de conexión: {str(e)}",
                    "status_code": 0
                }

    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        url = f"{BASE_URL}/userinfo/"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)

                try:
                    data = response.json()
                except ValueError:
                    return {
                        "success": False,
                        "error": "Error inesperado en el servidor.",
                        "status_code": response.status_code
                    }

                if response.status_code == 200:
                    return {
                        "success": True,
                        "user": data
                    }

                elif response.status_code == 401:
                    return {
                        "success": False,
                        "error": "Token inválido o expirado.",
                        "status_code": 401
                    }

                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Error desconocido."),
                        "status_code": response.status_code
                    }

            except httpx.RequestError as e:
                return {
                    "success": False,
                    "error": f"Error de conexión: {str(e)}",
                    "status_code": 0
                }

    @staticmethod
    async def logout(access_token: str) -> dict:
        url = f"{BASE_URL}/token/revoke/"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers)

                try:
                    data = response.json()
                except ValueError:
                    return {
                        "success": False,
                        "error": "Error inesperado en el servidor.",
                        "status_code": response.status_code
                    }

                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Logout exitoso."
                    }

                elif response.status_code == 401:
                    return {
                        "success": False,
                        "error": "Token inválido o expirado.",
                        "status_code": 401
                    }

                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Error desconocido."),
                        "status_code": response.status_code
                    }

            except httpx.RequestError as e:
                return {
                    "success": False,
                    "error": f"Error de conexión: {str(e)}",
                    "status_code": 0
                }