
from abc import ABC, abstractmethod


class EventHandlerInterface(ABC):
    """
    Interface for all event handlers. Each event handler must implement this interface.
    """

    @abstractmethod
    def handle_event(self, event_data: dict) -> None:
        """
        Handle an event with the given data.
        """
        pass
