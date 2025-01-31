from services.auth_service import AuthService


class SignupController:
    def __init__(self, app_manager):
        self.app_manager = app_manager

    async def signup(self, username, password, email):
        validation_errors = self._validate_fields(username, password, email)
        if validation_errors:
            return validation_errors

        response = await AuthService.signup(username, password, email)

        if response["success"]:
            return {"success": True}

        return self._handle_api_error(response)

    def _validate_fields(self, username, password, email):
        error_data = {"success": False, "field_errors": {}, "general_error": None}

        if not username:
            error_data["field_errors"]["username"] = "El usuario es obligatorio."

        if not password:
            error_data["field_errors"]["password"] = "La contraseña es obligatoria."
        elif len(password) < 8:
            error_data["field_errors"]["password"] = "La contraseña debe tener al menos 8 caracteres."

        if not email:
            error_data["field_errors"]["email"] = "El correo electrónico es obligatorio."

        return error_data if error_data["field_errors"] else None

    def _handle_api_error(self, response):
        error_data = {"success": False, "field_errors": {}, "general_error": None}

        if response["status_code"] == 409:
            # Si el error es "usuario ya existe" o "correo ya registrado"
            if "usuario ya existe" in response["error"].lower():
                error_data["field_errors"]["username"] = response["error"]
            elif "correo ya está registrado" in response["error"].lower():
                error_data["field_errors"]["email"] = response["error"]
            else:
                error_data["general_error"] = response["error"]

        elif response["status_code"] == 422:
            error_data["field_errors"] = response.get("field_errors", {})

        else:
            error_data["general_error"] = response["error"]

        return error_data
