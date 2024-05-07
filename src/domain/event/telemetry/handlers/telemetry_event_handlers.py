import logging
import random
import time
from typing import Any, List

from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.domain.event.telemetry.telemetry_subscription_manager import \
    TelemetrySubscriptionManager
from src.domain.model.telemetry_data import TelemetryData
from src.shared.helpers.constants import EventCategory, EventType


class TelemetryEventHandlers:
    """
    Base class for telemetry handlers that supports dynamic cooldowns, state tracking,
    and probabilistic event triggering with synchronized access to a shared block flag.
    """

    cooldown: int = 0
    chance: float = 1
    subscriptions: List[str] = []
    minimum_wait_time: int = 0

    def __init__(
        self,
        event_bus: EventBus,
        session: Session,
        telemetry_subscription_manager: TelemetrySubscriptionManager,
        only_once: bool = False,
    ):
        self.event_bus = event_bus
        self.last_emit_time = None
        self.session = session
        self.only_once = only_once
        self.has_triggered_once = False
        self.telemetry_subscription_manager = telemetry_subscription_manager
        self.previous_data = {}
        self.current_data = {}
        self.start_time = time.time()  # Record the start time

        self.subscribe_to_fields()

    def handle_telemetry_data(self, telemetry_data: TelemetryData):
        """
        Entry point for handling telemetry data. It checks if execution should proceed
        based on the global blocking state and minimum wait time.
        """
        logging.debug(
            f"[Module][{self.__class__.__name__}] Handling telemetry data"
        )

        if self.has_triggered_once and self.only_once:
            return

        if self.is_execution_blocked():
            logging.debug(
                f"[Module][{self.__class__.__name__}] Execution blocked, skipping handler."
            )
            return

        if not self.has_minimum_wait_time_passed():
            logging.info(
                f"[Module][{self.__class__.__name__}] Minimum wait time not passed, skipping handler."
            )
            return

        if self.has_cooled_down() and self.meets_chance():
            self.event_bus.block_telemetry_handlers()
            has_passed = self.handle(telemetry_data)
            self.has_triggered_once = True

            if has_passed is False:
                self.event_bus.unblock_telemetry_handlers()
                logging.info(
                    f"[Module][{self.__class__.__name__}] Has not passed conditions, unblocking telemetry handlers."
                )
        else:
            self.event_bus.unblock_telemetry_handlers()

    def handle(self, telemetry_data: TelemetryData):
        """
        This method should be implemented by subclasses to handle telemetry data specifically.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def emit_event(
        self,
        event_type: EventType,
        message: str,
    ):
        """
        Attempts to emit an event if the conditions (cooldown and chance) are met, considers prompt_type for specific handling.
        """
        self.last_emit_time = time.time()
        self.event_bus.emit(event_type, message, EventCategory.TELEMETRY)
        logging.info(f"[Module][{self.__class__.__name__}] Emitting: {message}")

    def is_execution_blocked(self):
        """
        Checks if the execution of the handler should be blocked.
        """
        return self.event_bus.telemetry_handlers_blocked

    def has_minimum_wait_time_passed(self):
        """
        Checks if the minimum wait time has passed since the start time.
        """
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.minimum_wait_time

    def has_cooled_down(self):
        """
        Checks if the handler has cooled down.
        """
        will_cooldown_in_seconds = (
            (self.last_emit_time + self.cooldown) - time.time()
            if self.last_emit_time is not None
            else None
        )
        has_cooled_down = (
            self.last_emit_time is None
            or (time.time() - self.last_emit_time) > self.cooldown
        )
        logging.debug(
            f"[Module][{self.__class__.__name__}] Has cooled down: {has_cooled_down}, will cool down in: {will_cooldown_in_seconds} seconds"
        )

        return has_cooled_down

    def meets_chance(self):
        """
        Checks if the handler meets the chance.
        """
        meets_chance = random.random() < self.chance
        logging.debug(
            f"[Module][{self.__class__.__name__}] Meets chance: {meets_chance}"
        )

        return meets_chance

    def subscribe_to_fields(self):
        """Subscribe to a list of telemetry fields."""
        self.telemetry_subscription_manager.subscribe(self.subscriptions, self)

    def register(self):
        """
        Register this handler for telemetry events.
        """
        self.event_bus.subscribe(
            EventType.TELEMETRY_RECEIVED, self.handle_telemetry_data
        )

    def unregister(self):
        """
        Unregister this handler from telemetry events and unsubscribe from all fields.
        """
        self.event_bus.unsubscribe(
            EventType.TELEMETRY_RECEIVED, self.handle_telemetry_data
        )
        for field in self.subscriptions:
            self.telemetry_subscription_manager.unsubscribe(field, self)
