class UserData:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.last_name = kwargs.get("last_name")
        self.document_number = kwargs.get("document_number")
        self.gender = kwargs.get("gender")

        self.access_token = kwargs.get("access_token")
        self.refresh_token = kwargs.get("refresh_token")


class SessionHandler:
    def __init__(self, app_manager):
        self.listeners = []
        self._on_session_change = None
        self._is_authenticated = None

        self.app_manager = app_manager

        self.user_data: UserData or None = None


    @property
    def is_authenticated(self):
        self.load_token()
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        if isinstance(value, bool):
            self._is_authenticated = value
            self.save_token()
            self._notify_listeners()

    def add_listener(self, callback):
        self.listeners.append(callback)

    def _notify_listeners(self):
        for listener in self.listeners:
            listener(self._is_authenticated)

    def authenticate(self, cuil, password):
        pass

    def save_token(self):
        pass

    def signup(self, **user_data):
       pass

    def load_token(self):
        pass

    def logout(self):
        pass

    def clear_token(self):
        pass

    def get_user_data(self):
        pass

    def update_user_data(self, updated_profile):
        pass
