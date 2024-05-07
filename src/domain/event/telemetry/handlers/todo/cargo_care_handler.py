import logging

from src.domain.event.telemetry.handlers.telemetry_event_handlers import TelemetryEventHandlers
from src.domain.model.telemetry_data import TelemetryData
from src.shared.helpers.constants import EventType


class CargoCareHandler(TelemetryEventHandlers):
    """
    Cargo care
    """

    def handle(self, telemetry_data: TelemetryData):
        # Implement the logic for handling the event based on telemetry data
        pass
