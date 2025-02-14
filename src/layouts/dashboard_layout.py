from layouts.layout import Layout


class DashboardLayout(Layout):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.state = {}

    def _register_states(self) -> None:
        pass

    def _build_ui(self) -> None:
        pass

    def _bind_states(self) -> None:
        pass

    def _attach_events(self) -> None:
        pass

    def _update_ui(self, state_key=None, value=None) -> None:
        pass

    def render_content(self, content):
        self.content = content