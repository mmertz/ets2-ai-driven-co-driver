import logging
import time

from src.application.event_bus import EventBus
from src.application.model.session_model import CoDriverProfile, Session
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventCategory, EventType


class SpeedingHandler(TelemetryEventHandlers):
    """
    Monitors vehicle speed and provides commentary if the vehicle exceeds highway speed limits.
    """

    cooldown = 1800
    chance = 1

    def register(self):
        self.subscribe_to_fields(["truck.speed"])

    def handle(self, telemetry_data: TelemetryData):
        truck_data = telemetry_data.truck
        speed_limit_highway = 90  # km/h
        if truck_data.speed > speed_limit_highway:
            message = f"Comment about the user speeding. Current speed: {truck_data.speed} km/h, limit: {speed_limit_highway} km/h."

            self.emit_event(
                event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                message=message,
            )
            logging.info("[SpeedingHandler] Speeding event reported to AI.")

            return True
        else:
            return False
