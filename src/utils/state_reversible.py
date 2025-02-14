from abc import ABC, abstractmethod


class StateReversible(ABC):

    @abstractmethod
    def save_state_to_session(self) -> None:
        pass

    @abstractmethod
    def load_state_from_session(self) -> None:
        pass
