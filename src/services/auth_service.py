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
                data = response.json()

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

