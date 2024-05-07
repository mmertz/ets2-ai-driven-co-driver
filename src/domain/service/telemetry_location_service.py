import json
import math
import os
from typing import Dict, List

from src.domain.model.telemetry_data import TelemetryData


class TelemetryLocationService:
    def __init__(self):
        self.cities_data = []

        self.load_cities_data()

    def load_cities_data(self) -> List[Dict]:
        file_path = os.path.join("./src", "cities.json")
        with open(file_path, "r") as file:
            cities = json.load(file)
            self.cities_data = cities

    def find_nearest_cities(
        self, telemetry_data: TelemetryData, limit: int = 5
    ) -> List[Dict]:
        """
        Find the nearest cities based on the current location from telemetry data.
        """
        player_position = (
            telemetry_data.truck.coordinate_x,
            telemetry_data.truck.coordinate_y,
        )

        if not player_position:
            return []

        nearest_cities = sorted(
            self.cities_data,
            key=lambda city: self.calculate_distance(
                player_position, city["X"], city["Y"]
            ),
        )[:limit]

        return nearest_cities

    @staticmethod
    def calculate_distance(player_position, city_x, city_y) -> float:
        """
        Calculate the distance between the player's position and a city's coordinates.
        """
        x1, y1 = player_position
        x2, y2 = city_x, city_y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
