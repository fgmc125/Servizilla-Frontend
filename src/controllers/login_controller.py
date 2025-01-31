from services.auth_service import AuthService


class LoginController:
    def __init__(self, app_manager):
        self.app_manager = app_manager

    async def login(self, username, password):
        validation_errors = self._validate_fields(username, password)
        if validation_errors:
            return validation_errors

        response = await AuthService.login(username, password)

        if response["success"]:
            self._store_tokens(response)
            return {"success": True}

        return self._handle_api_error(response)

    def _validate_fields(self, username, password):
        error_data = {"success": False, "field_errors": {}, "general_error": None}

        if not username:
            error_data["field_errors"]["username"] = "El usuario es obligatorio."

        if not password:
            error_data["field_errors"]["password"] = "La contraseña es obligatoria."
        elif len(password) < 8:
            error_data["field_errors"]["password"] = "La contraseña debe tener al menos 8 caracteres."

        return error_data if error_data["field_errors"] else None

    def _handle_api_error(self, response):
        error_data = {"success": False, "field_errors": {}, "general_error": None}

        if response["status_code"] == 401:
            error_data["field_errors"] = {
                "username": "Credenciales inválidas.",
                "password": "Credenciales inválidas."
            }
        else:
            error_data["general_error"] = response["error"]

        return error_data

    def _store_tokens(self, response):
        self.app_manager.state_handler.set("access_token", response["access_token"])
        self.app_manager.state_handler.set("refresh_token", response["refresh_token"])
        self.app_manager.state_handler.set("is_authenticated", True)
