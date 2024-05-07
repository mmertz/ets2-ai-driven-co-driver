from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import NavigationData, TelemetryData
from src.shared.helpers.constants import EventType


class CulturalTriviaHandler(TelemetryEventHandlers):
    """
    Provides cultural trivia based on the truck's current location during the journey.
    """

    subscriptions = ["navigation.distance"]

    minimum_wait_time: int = 60

    def handle(self, telemetry_data: TelemetryData):
        """
        Generates cultural trivia based on the truck's navigation data.
        """

        self.provide_cultural_trivia(telemetry_data.navigation)

    def provide_cultural_trivia(self, navigation_data: NavigationData):
        """
        Generates a cultural trivia prompt about the current location.
        """

        message = "Resume the conversation by providing a trivia based on either your profile data or the user's profile data."
        self.emit_event(
            event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
            message=message,
        )
