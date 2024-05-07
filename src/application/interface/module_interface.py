# src/application/module_interface.py

from abc import ABC, abstractmethod

from src.application.event_bus import EventBus


class ModuleInterface(ABC):
    """
    Interface for dynamic modules within the ETS2 AI Plugin system.
    Each module must be capable of registering and unregistering itself with the event bus.
    """

    @abstractmethod
    def register(self, event_bus: EventBus) -> None:
        """
        Register this module with the event bus, subscribing to necessary events.
        """
        pass

    @abstractmethod
    def unregister(self, event_bus: EventBus) -> None:
        """
        Unregister this module from the event bus, removing all subscriptions.
        """
        pass
