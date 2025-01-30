import logging
from abc import ABC, abstractmethod

from flet import Container
from handlers.state_handler import StateHandler


class LayoutInterface(ABC):
    """
    Interfaz que define el contrato que deben implementar todos los layouts.
    """
    @abstractmethod
    def get_state(self):
        """Devuelve el estado del layout."""
        pass

    @abstractmethod
    def set_state(self, state):
        """Establece el estado del layout."""
        pass

    @abstractmethod
    def render_content(self, content):
        """Renderiza el contenido dentro del layout."""
        pass


class Layout(Container, LayoutInterface):
    """
    Clase abstracta que implementa la lógica común para todos los layouts.
    Extiende de LayoutInterface y agrega un atributo StateHandler.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._state_handler = StateHandler()

    @property
    def state_manager(self):
        """Devuelve el StateHandler asociado a este layout."""
        return self._state_handler

    @state_manager.setter
    def state_manager(self, state_manager):
        """Permite establecer un nuevo StateHandler para este layout."""
        if not isinstance(state_manager, StateHandler):
            raise TypeError("state_manager debe ser una instancia de StateHandler")
        self._state_handler = state_manager

    def get_state(self):
        """Devuelve el StateHandler asociado a este layout."""
        return self.state_manager

    def set_state(self, state):
        """Actualiza el estado en el StateHandler."""
        for key, value in state.items():
            self.state_manager.set(key, value)

    @abstractmethod
    def render_content(self, content):
        """Debe ser implementado por los layouts concretos para renderizar contenido."""
        pass
