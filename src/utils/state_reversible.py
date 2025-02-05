from abc import ABC, abstractmethod


class StateReversible(ABC):

    @abstractmethod
    def save_state_to_session(self) -> None:
        """
        Método que debe guardar el estado del componente en sessionStorage.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def load_state_from_session(self) -> None:
        """
        Método que debe cargar el estado del componente desde sessionStorage.
        Debe ser implementado por las clases hijas.
        """
        pass
