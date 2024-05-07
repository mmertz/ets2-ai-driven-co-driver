import logging
import threading
from collections import defaultdict, deque
from typing import Any, Callable, Dict, List

from src.shared.helpers.constants import EventCategory, EventType


class EventBus:
    """
    Manages events within the plugin with support for categorized event handling.
    Includes a mechanism to prevent event overlap by using state management.
    """

    def __init__(self) -> None:
        self.handlers: Dict[EventType, List[Callable[[Any], None]]] = defaultdict(list)
        self.queues: Dict[EventCategory, deque] = defaultdict(deque)
        self.locks: Dict[EventCategory, threading.Lock] = defaultdict(threading.Lock)
        self.active_threads: Dict[EventCategory, threading.Thread] = {}
        self.state_flags: Dict[EventType, bool] = defaultdict(bool)
        self.telemetry_handlers_blocked: bool = False

        self.block_emit_on_states: List[EventType] = [
            EventType.USER_SPEECH_START,
        ]

    def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[Any], None],
    ) -> None:
        """
        Subscribes a handler to a specific type of event with an optional cooldown for rate limiting.
        """
        self.handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Unsubscribes a handler from a specific type of event."""
        self.handlers[event_type] = [
            (h, c) for h, c in self.handlers[event_type] if h != handler
        ]

    def emit(
        self,
        event_type: EventType,
        data: Any,
        category: EventCategory = EventCategory.GENERIC,
    ):
        with self.locks[category]:
            self.queues[category].append((event_type, data))
            if (
                category not in self.active_threads
                or not self.active_threads[category].is_alive()
            ):
                self.active_threads[category] = threading.Thread(
                    target=self.process_queue, args=(category,)
                )
                self.active_threads[category].start()

    def process_event(self, event_type: EventType, data: Any, category: EventCategory):
        """Processes the event and invokes registered handlers."""
        with self.locks[category]:
            if (
                category not in self.active_threads
                or not self.active_threads[category].is_alive()
            ):
                thread = threading.Thread(
                    target=self._handle_event, args=(event_type, data)
                )
                thread.start()
                self.active_threads[category] = thread

    def process_queue(self, category: EventCategory):
        while self.queues[category]:
            with self.locks[category]:
                event_type, data = self.queues[category].popleft()
            self._handle_event(event_type, data)

    def _handle_event(self, event_type: EventType, data: Any):
        for handler in self.handlers[event_type]:
            try:
                handler(data)
            except Exception as e:
                logging.error(f"[EventBus] Error handling event {event_type}: {e}")

    def is_blocked(self) -> bool:
        """Checks if any critical event is currently active that should block other events."""
        return any(
            self.state_flags[event_type] for event_type in self.block_emit_on_states
        )

    def block_telemetry_handlers(self):
        self.telemetry_handlers_blocked = True

    def unblock_telemetry_handlers(self):
        self.telemetry_handlers_blocked = False

    def set_state(self, event_type: EventType, active: bool):
        """Sets the active state for a given type of event."""
        self.state_flags[event_type] = active

    def shutdown(self) -> None:
        """Ensures all threads have completed before shutting down."""
        for thread in self.active_threads.values():
            thread.join()
