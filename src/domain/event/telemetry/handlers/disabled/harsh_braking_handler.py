# harsh_braking_commentary_handler.py
import logging

from src.application.event_bus import EventBus
from src.domain.event.handlers.base_telemetry_handler import \
    TelemetryEventHandlers
from src.domain.model.ets2_telemetry_data import TelemetryData, TruckData
from src.shared.helpers.constants import EventCategory, EventType


class HarshBrakingHandler(TelemetryEventHandlers):
    def handle(self, telemetry_data: TelemetryData):
        self.inform_about_braking(telemetry_data.truck)

    def inform_about_braking(self, truck_data: TruckData):
        if truck_data.brake > 0.5:
            instruction = "Generate a comment on harsh braking."
            self.emit_event(
                event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                message=instruction,
                prompt_type="braking",
                cooldown=1800,
                chance=0.3,
            )
            logging.info(
                "[HarshBrakingCommentaryHandler] Prompt for harsh braking sent to AI."
            )
