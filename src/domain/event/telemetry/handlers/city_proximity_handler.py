import logging
import math

from src.domain.event.telemetry.handlers.telemetry_event_handlers import \
    TelemetryEventHandlers
from src.domain.model.telemetry_data import TelemetryData
from src.shared.helpers.constants import EventType


class CityProximityHandler(TelemetryEventHandlers):
    """
    Handles events related to the truck nearing a city based on telemetry data.
    """

    subscriptions = ["truck.speed"]
    proximity_threshold = 5000  # meters within which a city is considered 'near'

    def handle(self, telemetry_data: TelemetryData):
        """
        Check if the truck is nearing any city and trigger appropriate events.
        """


        logging.info(telemetry_data.truck.speed)

        if (
            not telemetry_data.truck
            or not telemetry_data.navigation
            or not telemetry_data.navigation.nearest_cities
        ):
            logging.info(
                "[CityProximityHandler] No truck data or nearest cities information available."
            )
            return False

        truck_position = (
            telemetry_data.truck.coordinate_x,
            telemetry_data.truck.coordinate_y,
        )
        logging.info(f"[CityProximityHandler] Current truck position: {truck_position}")

        nearest_city = self.find_nearest_city(
            telemetry_data.navigation.nearest_cities, truck_position
        )

        if nearest_city and nearest_city["distance"] <= self.proximity_threshold:
            self.notify_approaching_city(nearest_city, nearest_city["distance"])
            return True
        logging.info("[CityProximityHandler] No city within proximity threshold.")
        return False

    def find_nearest_city(self, cities, truck_position):
        """
        Find the nearest city to the truck's current position.
        """
        nearest_city = None
        min_distance = float("inf")
        for city in cities:
            distance = self.calculate_distance(truck_position, (city["X"], city["Y"]))
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
                nearest_city["distance"] = distance
        logging.info(
            f"[CityProximityHandler] Nearest city: {nearest_city['Name']} at distance: {min_distance}"
        )
        return nearest_city

    @staticmethod
    def calculate_distance(pos1, pos2):
        """
        Calculate the Euclidean distance between two points.
        """
        distance = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        logging.debug(f"[CityProximityHandler] Calculated distance: {distance}")
        return distance

    def notify_approaching_city(self, city, distance):
        """
        Notify that the truck is approaching a city.
        """
        message = f"Generate a CONVERSATIONAL message that we are approaching {city['Name']}"
        self.emit_event(
            event_type=EventType.DIALOGUE_RESPONSE_REQUEST,
            message=message,
        )
        logging.info(
            f"[CityProximityHandler] Approaching {city['Name']} at {distance:.2f} meters."
        )
