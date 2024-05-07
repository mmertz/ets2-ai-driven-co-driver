import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.application.session_management import SessionManagement
from src.shared.helpers.constants import EventType


class DynamicSessionInterface(ABC):
    """
    Interface for dynamic session providers. All dynamic session provider classes must implement these methods.
    """

    def __init__(
        self,
        event_bus: EventBus,
        session_manager: SessionManagement,
        model: str,
        params: Dict[str, Any],
        history_size: int,
        interaction_interval: int,
    ):
        self.session_manager = session_manager
        self.session = self.session_manager.get_current_session()
        self.model = model
        self.params = params
        self.history_size = history_size
        self.interaction_interval = interaction_interval
        self.event_bus = event_bus
        self.total_interactions_after_last_update = 0

    def update_profiles(self, _):
        """
        Update the co-pilot and user profile based on the given text.
        """

        logging.info("[DynamicSessionProvider] Attempting to update profiles")
        if self.total_interactions_after_last_update >= self.interaction_interval:
            logging.info("[DynamicSessionProvider] Interaction interval reached, updating profiles")
            self.process()
            self.total_interactions_after_last_update = 0

        logging.info("[DynamicSessionProvider] Incrementing total interactions after last update")
        self.total_interactions_after_last_update += 1

    def register(self) -> None:
        """
        Registers the service with the event bus to respond to dialogue completion events.
        """
        self.event_bus.subscribe(EventType.REQUEST_COMPLETE, self.update_profiles)

    def unregister(self) -> None:
        """
        Unregisters the service from the event bus, ceasing its response to dialogue events.
        """
        self.event_bus.unsubscribe(EventType.REQUEST_COMPLETE, self.update_profiles)

    @abstractmethod
    def process(self):
        """
        Process the given text and dynamically update the co-pilot and user profile.
        Returns a dictionary with processed results and any state changes.
        """
        raise NotImplementedError("This method must be implemented by a subclass.")
