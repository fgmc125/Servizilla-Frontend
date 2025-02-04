from flet import Container

from handlers.state_handler import StateHandler


class PageContainer(Container):
    def __init__(self):
        super().__init__()
        self.state = StateHandler()
        self._register_default_states()

    def _register_default_states(self):
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("error_message", None)
        self.state.register("success_message", None)

    def get_state(self):
        return self.state

    def set_state(self, key, value):
        self.state.set(key, value)

    def build_ui(self):
        pass

    def build_ui(self):
        pass
