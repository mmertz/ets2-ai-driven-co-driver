import random
from datetime import datetime

from pytz import utc

from src.application.event_bus import EventBus
from src.application.model.session_model import CoDriverProfile, Session
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventType


class PersonalStoryTimeHandler(TelemetryEventHandlers):
    """
    Handler that generates context-aware stories based on the co-driver's profile and current telemetry data,
    enhancing the in-game experience with personalized and engaging narratives.
    """

    def __init__(self, event_bus: EventBus, session: Session):
        super().__init__(
            event_bus=event_bus, session=session, cooldown=1800, chance=0.5
        )  # Cooldown set to 30 minutes
        self.possible_stories = [
            "childhood",
            "career",
            "travel",
            "hobby",
            "fun_fact",
        ]  # Example story themes

    def handle(self, telemetry_data: TelemetryData):
        """
        Decides whether to initiate a story based on the current driving conditions and the co-driver's state.
        """
        if self.is_opportune_moment(telemetry_data):
            story = self.compose_story(telemetry_data, self.session)
            if story:
                self.emit_event(
                    event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                    message=story,
                )
                return True
        return False

    def is_opportune_moment(self, telemetry_data: TelemetryData) -> bool:
        """
        Checks if current driving conditions are suitable for a story, e.g., long highway stretches.
        """
        if telemetry_data.truck.speed > 60 and not telemetry_data.game.game_paused:
            # Assume suitable conditions if speed is above 60 km/h and game is not paused
            return True
        return False


    def compose_story(self, telemetry_data: TelemetryData, session: Session) -> str:
        """
        Generate a story instruction integrating mood, personality, and recent interactions.
        """
        co_driver = session.co_driver
        dynamic_profile = co_driver.dynamic_profile
        static_profile = co_driver.static_profile

        mood = dynamic_profile.state.mood
        topic = random.choice(static_profile.preferences.get('topics_of_interest', []))

        # Start the instruction
        instruction = f"Generate a PERSONAL REALISTIC SHORT story about {topic}, where the you felt {mood}. "

        # Include personality traits in storytelling
        personality_traits = f"with humor at level {dynamic_profile.personality.humor} and confidence at level {dynamic_profile.personality.confidence}"
        instruction += f"The story should reflect these traits {personality_traits}. "

        # Adjust storytelling based on the journey context
        if telemetry_data.navigation.distance > 100000:
            instruction += "As we have a long drive ahead, ensure the story is captivating for the duration. "

        # Conclude with a question to engage the user
        instruction += "Base your story on YOUR personality (co-driver) profile and conversation with the user."

        return instruction
