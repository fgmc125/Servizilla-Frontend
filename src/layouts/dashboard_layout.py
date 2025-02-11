from layouts.layout import Layout


class DashboardLayout(Layout):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.state = {}

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state.update(state)

    def render_content(self, content):
        self.content = content