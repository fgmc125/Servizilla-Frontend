import httpx
import socket

BASE_URL = "http://127.0.0.1:8000/auth"


class AuthService:
    def __init__(self):
        self.device_info = "unknown_device"
        self.user_agent = "unknown_user_agent"
        self.ip_address = self.get_ip_address()

    def get_ip_address(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.error:
            return "0.0.0.0"

    async def login(self, username: str, password: str) -> dict:
        url = f"{BASE_URL}/login/"
        payload = {"username": username, "password": password}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                data = response.json()

                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Login exitoso",
                        "data": {
                            "access_token": data.get("access_token"),
                            "refresh_token": data.get("refresh_token")
                        }
                    }

                return {"success": False, "message": data.get("error", "Error en la autenticación")}

            except httpx.RequestError as e:
                return {"success": False, "message": f"Error de conexión: {str(e)}"}

    async def refresh(self, refresh_token: str) -> dict:
        if not refresh_token:
            return {"success": False, "message": "No hay refresh token disponible."}

        url = f"{BASE_URL}/token/refresh/"
        payload = {"refresh": refresh_token}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                data = response.json()

                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Token renovado",
                        "data": {
                            "access_token": data.get("access"),
                            "refresh_token": data.get("refresh"),
                        }
                    }

                return {"success": False, "message": data.get("message", "Error al renovar el token.")}

            except httpx.RequestError as e:
                return {"success": False, "message": f"Error de conexión: {str(e)}"}

    async def logout(self, access_token: str) -> dict:
        url = f"{BASE_URL}/logout/"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers)
                data = response.json()

                if response.status_code == 200:
                    return {"success": True, "message": data.get("message", "Sesión cerrada exitosamente.")}

                return {"success": False, "message": data.get("message", "Error al cerrar sesión.")}

            except httpx.RequestError as e:
                return {"success": False, "message": f"Error de conexión: {str(e)}"}
