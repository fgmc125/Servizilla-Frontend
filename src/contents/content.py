from core.base_ui_component import BaseUIComponent


class PageContainer(BaseUIComponent):
    def __init__(self):
        super().__init__()
        self.__register_default_states()

    def __register_default_states(self):
        self.state.register("is_view_loading", False)
        self.state.register("is_processing", False)
        self.state.register("error_message", None)
        self.state.register("success_message", None)
