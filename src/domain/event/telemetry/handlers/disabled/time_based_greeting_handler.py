# time_based_greeting_handler.py
import logging

from src.application.event_bus import EventBus
from src.application.model.session_model import CoDriverProfile, Session
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventCategory, EventType


class TimeBasedGreetingHandler(TelemetryEventHandlers):
    """
    Provides greetings to the driver based on the time of day, enhancing the sense of realism in the simulation.
    """

    def __init__(self, event_bus: EventBus, session: Session):
        super().__init__(
            event_bus=event_bus,
            session=session,
            cooldown=7200,
            chance=1,
            only_once=True,
        )

    def handle(self, telemetry_data: TelemetryData):
        """
        Generates time-specific greetings based on the in-game time.
        """

        self.greet_based_on_time(telemetry_data.game)

        return True

    def greet_based_on_time(self, game_data: GameData):
        """
        Generates a greeting based on the current in-game time.
        """
        current_hour = int(game_data.time.split(":")[0])
        if 6 <= current_hour < 12:
            message = "Generate a good morning greeting."
        elif 12 <= current_hour < 18:
            message = "Generate a good afternoon greeting."
        else:
            message = "Generate a good evening greeting."

        self.emit_event(
            event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
            message=message + "\n IMPORTANT: Generate BASED on YOUR co-driver profile.",
        )

        logging.info(
            "[TimeBasedGreetingHandler] Time-specific greeting prompt sent to AI."
        )
