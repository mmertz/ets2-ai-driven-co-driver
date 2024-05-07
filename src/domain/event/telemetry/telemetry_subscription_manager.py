import fnmatch
import logging
from collections import defaultdict


class TelemetrySubscriptionManager:
    def __init__(self):
        # This will store subscriptions with handlers interested in specific patterns
        self.subscriptions = defaultdict(list)
        # Store the last known values for comparison
        self.last_known_values = {}

    def subscribe(self, patterns, handler):
        """Subscribe a handler to changes in specific telemetry fields or patterns."""
        if isinstance(patterns, str):
            patterns = [patterns]
        for pattern in patterns:
            self.subscriptions[pattern].append(handler)

    def unsubscribe(self, patterns, handler):
        """Unsubscribe a handler from specific telemetry fields or patterns."""
        if isinstance(patterns, str):
            patterns = [patterns]
        for pattern in patterns:
            if handler in self.subscriptions[pattern]:
                self.subscriptions[pattern].remove(handler)
                if not self.subscriptions[pattern]:
                    del self.subscriptions[pattern]

    def notify_handlers(self, telemetry_data):
        """Notify handlers if their subscribed fields have changed."""
        changed_fields = self._find_changed_fields(telemetry_data)
        for field in changed_fields:
            for pattern, handlers in self.subscriptions.items():
                if fnmatch.fnmatch(field, pattern):
                    for handler in handlers:
                        handler.handle_telemetry_data(telemetry_data)

    def _find_changed_fields(self, telemetry_data):
        """Detect changes in telemetry data and update last known values."""
        current_values = self._extract_values(telemetry_data)
        changed_fields = []
        for field, value in current_values.items():
            if self.last_known_values.get(field) != value:
                self.last_known_values[field] = value
                changed_fields.append(field)
        return changed_fields

    def _extract_values(self, telemetry_data, prefix=''):
        """Extract values recursively from telemetry data."""
        values = {}
        for attr, val in vars(telemetry_data).items():
            full_path = f"{prefix}.{attr}".strip('.')
            if hasattr(val, '__dict__') or isinstance(val, dict):
                values.update(self._extract_values(val, prefix=full_path))
            else:
                values[full_path] = val
        return values
