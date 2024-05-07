from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import (GameData, JobData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventType


class FuelReminderHandler(TelemetryEventHandlers):
    """
    Monitors the truck's fuel level and consumption rate to provide timely suggestions or reminders
    about refueling, considering the journey's progress and known preferences for fuel stops.
    """

    def __init__(self, event_bus: EventBus, session: Session):
        super().__init__(
            event_bus=event_bus, session=session, cooldown=7200, chance=1.0
        )  # Cooldown set to 2 hours, always checks

    def handle(self, telemetry_data: TelemetryData):
        """
        Evaluates the need for a fuel reminder based on the current fuel level, consumption rate, and journey progress.
        """
        if self.need_to_refuel(telemetry_data):
            message = self.generate_fuel_reminder(telemetry_data.truck)
            if message:
                self.emit_event(
                    event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
                    message=message,
                )
                return True
        return False

    def need_to_refuel(self, telemetry_data: TelemetryData) -> bool:
        """
        Determines whether it's appropriate to remind about refueling based on fuel levels, consumption rate, distance to next destination, and next mandatory rest stop.
        """
        truck_data = telemetry_data.truck
        navigation_data = telemetry_data.navigation
        game_data = telemetry_data.game

        # Calculate the estimated range left with the current fuel
        estimated_range_left = (
            truck_data.fuel / truck_data.fuel_rate
        ) * 100  # Convert fuel rate to km/L if necessary

        # Check if the remaining fuel is enough to reach the next destination or mandatory rest stop
        if estimated_range_left < navigation_data.distance:
            return True

        # Consider next mandatory rest as a point to refuel if close to fuel exhaustion
        if game_data.next_rest_stop * (truck_data.speed / 60) > estimated_range_left:
            return True

        # Regular low fuel level check
        fuel_threshold = truck_data.fuel_capacity * 0.25
        if truck_data.fuel < fuel_threshold:
            return True

        return False

    def generate_fuel_reminder(self, truck_data: TruckData) -> str:
        """
        Generates a user-friendly reminder about refueling, based on current fuel levels and the journey context.
        """
        remaining_fuel_percent = (truck_data.fuel / truck_data.fuel_capacity) * 100
        if remaining_fuel_percent < 25:
            return f"Generate a message about low fuel level. Current fuel: {truck_data.fuel}. Capacity: {truck_data.fuel_capacity}. Percentage: {remaining_fuel_percent}"
        return None
