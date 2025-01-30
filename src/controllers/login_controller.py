import asyncio
from services.auth_service import AuthService


class LoginController:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.auth_service = AuthService()

    async def login(self, username, password):
        response = await self.auth_service.login(username, password)

        if response["success"]:
            access_token = response["data"]["access_token"]
            refresh_token = response["data"]["refresh_token"]

            self.app_manager.state_handler.set("access_token", access_token)
            self.app_manager.state_handler.set("refresh_token", refresh_token)
            self.app_manager.state_handler.set("is_authenticated", True)

            return {"success": True}
        else:
            return {
                "success": False,
                "field_errors": response.get("field_errors", {}),
                "general_error": response.get("message", "Error inesperado."),
            }
