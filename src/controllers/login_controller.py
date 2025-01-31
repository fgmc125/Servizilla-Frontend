import asyncio
from services.auth_service import AuthService

class LoginController:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.auth_service = AuthService()

    async def login(self, username, password):
        error_data = {
            "success": False,
            "field_errors": {},
            "general_error": None
        }

        if not username:
            error_data["field_errors"]["username"] = "El usuario es obligatorio."

        if not password:
            error_data["field_errors"]["password"] = "La contraseña es obligatoria."

        if password and len(password) < 8:
            error_data["field_errors"]["password"] = "La contraseña debe tener al menos 6 caracteres."

        if error_data["field_errors"]:
            return error_data

        response = await self.auth_service.login(username, password)

        if response["success"]:
            access_token = response["access_token"]
            refresh_token = response["refresh_token"]

            self.app_manager.state_handler.set("access_token", access_token)
            self.app_manager.state_handler.set("refresh_token", refresh_token)
            self.app_manager.state_handler.set("is_authenticated", True)

            return {"success": True}

        else:
            if response["status_code"] == 401:
                error_data["field_errors"] = {
                    "username": "Credenciales inválidas.",
                    "password": "Credenciales inválidas."
                }
            else:
                error_data["general_error"] = response["error"]

            return error_data
