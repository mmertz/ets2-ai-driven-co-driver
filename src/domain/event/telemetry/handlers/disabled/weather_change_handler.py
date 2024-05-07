import logging

from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import TelemetryData, TruckData
from src.shared.helpers.constants import EventType


class WeatherChangeHandler(TelemetryEventHandlers):
    """
    Handles dynamic commentary on changes in weather conditions based on the truck's telemetry data.
    """

    subscriptions = ["truck.wipers", "truck.lights_fog"]
    last_weather_condition = None
    cooldown = 3600
    chance = 0.5

    def handle(self, telemetry_data: TelemetryData):
        """
        Generates commentary based on changes in the truck's wipers and fog lights indicating weather conditions.
        """
        result = self.comment_on_weather(telemetry_data.truck)
        return result

    def comment_on_weather(self, truck_data: TruckData):
        """
        Generates a weather-related comment if conditions change to indicate rain or fog, or if it clears up.
        """
        current_condition = self.determine_weather_condition(truck_data)

        if current_condition != self.last_weather_condition:
            if (
                current_condition != "clear"
            ):  # Comment only on changes to rainy or foggy
                message = f"Generate a comment on the changing weather conditions: now it's {current_condition}."
                self.emit_event(
                    event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                    message=message,
                )
                logging.info("[WeatherChangeHandler] Weather prompt sent to AI.")
                self.last_weather_condition = current_condition
                return True
        return False

    def determine_weather_condition(self, truck_data: TruckData):
        """
        Determines the weather condition based on truck data.
        """
        if truck_data.wipers:
            return "rainy"
        elif truck_data.lights_fog:
            return "foggy"
        else:
            return "clear"
