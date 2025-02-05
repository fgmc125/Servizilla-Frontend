from flet import Container

from handlers.state_handler import StateHandler

from utils.state_reversible import StateReversible


class PageContainer(Container):
    def __init__(self):
        super().__init__()
        self.state = StateHandler()
        self.__register_default_states()

    def __register_default_states(self):
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("error_message", None)
        self.state.register("success_message", None)

    def get_state(self):
        return self.state

    def set_state(self, key, value):
        self.state.set(key, value)

    def _build_ui(self) -> None:
        pass

    def _update_ui(self, state_key=None, value=None) -> None:
        pass

    def _attach_events(self) -> None:
        pass

    def _register_states(self) -> None:
        pass

    def _bind_states(self) -> None:
        pass

    def _invoke_service(self) -> None:
        pass

