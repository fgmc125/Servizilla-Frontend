import asyncio

import flet as ft

from contents.content import PageContainer
from utils.style_helper import label_style, text_style, primary_button_style
from controllers.signup_controller import SignupController


class SignupPage(PageContainer):
    def __init__(self, app_manager):
        super().__init__()
        self._app_manager = app_manager
        self.controller = SignupController(app_manager)


def signup_page(app_manager):
    app_manager.page.title = "Signup Page"
    return SignupPage(app_manager)