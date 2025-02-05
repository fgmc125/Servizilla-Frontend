import asyncio
import logging
from services.api_services import APIService


class AddServiceController:
    def __init__(self, app_manager):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._app_manager = app_manager

    async def add_service(self, state):
        service_name = state.get("service_name", "").strip()
        service_description = state.get("service_description", "").strip()
        service_duration = state.get("duration", None)
        service_category = state.get("service_category_id", None)
        start_time_picker = state.get("start_time_picker", None)
        end_time_picker = state.get("end_time_picker", None)
        days = state.get("days", {})
        service_available_all_day = state.get("available_all_day", False)

        availability = {
            "days": {},
            "hours": {"24_hours": service_available_all_day}
        }

        for day, is_selected in days.items():
            if is_selected:
                availability["days"][self.__get_day_in_english(day)] = [
                    {
                        "start": "00:00" if service_available_all_day else start_time_picker,
                        "end": "24:00" if service_available_all_day else end_time_picker
                    }
                ]

        token = self._app_manager.state_handler.get("access_token")

        service_data = {
            "title": service_name,
            "description": service_description,
            "duration": service_duration,
            "availability": availability,
            "category": service_category
        }

        state.set("is_processing", True)

        try:
            response = await APIService.create_service(data=service_data, token=token)

            if "error" in response:
                self.logger.error(f"Error al agregar servicio: {response['error']}")
                state.set("general_error", response["error"])
            else:
                state.set("general_error", None)
                state.set("service_added", True)
                state.set("new_service", response.get("service", {}))

        except Exception as e:
            error_msg = f"Error en la solicitud: {str(e)}"
            self.logger.error(error_msg)
            state.set("general_error", error_msg)

        state.set("is_processing", False)

    def __get_day_in_english(self, day):
        days_translation = {
            "Lunes": "monday",
            "Martes": "tuesday",
            "Miércoles": "wednesday",
            "Jueves": "thursday",
            "Viernes": "friday",
            "Sábado": "saturday",
            "Domingo": "sunday"
        }
        return days_translation.get(day, "")

    async def get_categories(self, state):
        try:
            token = self._app_manager.state_handler.get("access_token")
            categories = await APIService.get_categories(token)

            if categories:
                state.set("categories", categories)
            else:
                self.logger.error("No se encontraron categorías.")
                state.set("general_error", "No se encontraron categorías.")

        except Exception as e:
            error_msg = f"Error al obtener las categorías: {str(e)}"
            self.logger.error(error_msg)
            state.set("general_error", error_msg)


