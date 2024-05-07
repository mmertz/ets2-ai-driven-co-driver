import logging
import random

from src.application.event_bus import EventBus
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, JobData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventCategory, EventType


class MusicSuggestionHandler(TelemetryEventHandlers):
    """
    Suggests music based on current conditions and user preferences, dynamically crafting music suggestions
    that resonate with the user's tastes or inquiring about them if unknown.
    """

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus=event_bus, cooldown=3600, chance=1)  # Adjust cooldown and chance as needed

    def handle(self, telemetry_data: TelemetryData):
        """
        Generates a music suggestion based on time of day, weather conditions, or directly from user preferences,
        always considering user profile data.
        """
        truck_data = telemetry_data.truck
        game_data = telemetry_data.game
        suggestion = self.generate_music_suggestion(truck_data, game_data)

        if suggestion:
            self.emit_event(
                event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                message=suggestion,
            )
            return True
        return False

    def generate_music_suggestion(self, truck_data: TruckData, game_data: GameData) -> str:
        """
        Crafts a music suggestion based on environmental factors and includes instructions to check user preferences.
        """
        weather_condition = self.get_weather_condition(truck_data)
        time_of_day = self.get_time_of_day(game_data)
        context = f"Check user profile for music preferences. If not available, ask what their music tastes are. "

        if weather_condition or time_of_day:
            condition_description = weather_condition if weather_condition else time_of_day
            return f"{context}Suggest {condition_description} music based on the user's interest."
        else:
            return None

    def get_weather_condition(self, truck_data: TruckData) -> str:
        """
        Returns a descriptive string for the current weather condition based on the truck's data.
        """
        if truck_data.wipers:
            return "cozy rainy day"
        elif truck_data.lights_fog:
            return "misty morning"
        return None

    def get_time_of_day(self, game_data: GameData) -> str:
        """
        Returns a time-of-day specific string for music suggestion.
        """
        current_hour = int(game_data.time.split(':')[0])
        if 6 <= current_hour < 12:
            return "energetic morning"
        elif 12 <= current_hour < 18:
            return "upbeat afternoon"
        elif 18 <= current_hour < 24 or 0 <= current_hour < 6:
            return "relaxing evening"
        return None
