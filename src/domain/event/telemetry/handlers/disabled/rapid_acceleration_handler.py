import logging

from src.application.event_bus import EventBus
from src.application.model.session_model import CoDriverProfile, Session
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventCategory, EventType


class RapidAccelerationHandler(TelemetryEventHandlers):
    def __init__(self, event_bus: EventBus, session: Session):
        super().__init__(
            event_bus=event_bus, session=session, cooldown=1800, chance=0.4
        )

    def handle(self, telemetry_data: TelemetryData):
        self.inform_about_acceleration(telemetry_data.truck)

    def inform_about_acceleration(self, truck_data: TruckData):
        if truck_data.acceleration > 2.5:
            instruction = "Generate a comment on rapid acceleration."
            self.emit_event(
                event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                message=instruction,
            )
            logging.info(
                "[RapidAccelerationHandler] Prompt for rapid acceleration sent to AI."
            )
