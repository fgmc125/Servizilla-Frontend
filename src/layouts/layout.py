import logging
from abc import ABC, abstractmethod

from handlers.state_handler import StateHandler
from core.base_ui_component import BaseUIComponent


class LayoutInterface(ABC):
    @abstractmethod
    def render_content(self, content):
        pass


class Layout(BaseUIComponent, LayoutInterface, ABC):
    def __init__(self):
        super().__init__()
