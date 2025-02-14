import logging
from abc import ABC, abstractmethod

from flet import Container

from handlers.state_handler import StateHandler


class BaseUIComponent(Container, ABC):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.state = StateHandler()

    @abstractmethod
    def _register_states(self) -> None:
        """Registra los estados locales específicos del componente."""
        pass

    @abstractmethod
    def _build_ui(self) -> None:
        """Construye la estructura visual del componente."""
        pass

    @abstractmethod
    def _bind_states(self) -> None:
        """Asocia los estados con suscripciones para que reaccionen a cambios."""
        pass

    @abstractmethod
    def _attach_events(self) -> None:
        """Asocia eventos como clics y acciones del usuario."""
        pass

    @abstractmethod
    def _update_ui(self, state_key=None, value=None) -> None:
        """Actualiza elementos del UI cuando cambia un estado."""
        pass
