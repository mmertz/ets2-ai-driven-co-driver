import asyncio
import logging

import httpx

from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.domain.model.telemetry_data import (GameData, JobData, NavigationData,
                                             TelemetryData, TruckData)
from src.shared.helpers.constants import EventCategory, EventType


class TelemetryClientService:
    """
    Manages fetching telemetry data from a server and broadcasting it via an event bus.
    """

    def __init__(
        self,
        event_bus: EventBus,
        session: Session,
        server_url: str = "http://localhost:8000/api/telemetry",
    ):
        """
        Initializes the client with an event bus and a server URL.
        """
        self.event_bus = event_bus
        self.server_url = server_url
        self.session = session
        self.client = httpx.AsyncClient()

    async def fetch_telemetry_data(self):
        """
        Fetches telemetry data from the server and dispatches it through the event bus.
        """
        try:
            response = await self.client.get(self.server_url)
            response.raise_for_status()
            data = response.json()

            # Unpack JSON into data class instances
            truck_data = TruckData(**data["truck"])
            game_data = GameData(**data["game"])
            navigation_data = NavigationData(**data["navigation"])
            job_data = JobData(**data["job"]) if "job" in data else None

            telemetry_data = TelemetryData(
                truck=truck_data,
                game=game_data,
                navigation=navigation_data,
                job=job_data,
            )

            self.event_bus.emit(
                EventType.TELEMETRY_RECEIVED, telemetry_data, EventCategory.GENERIC
            )
        except httpx.HTTPError as e:
            logging.error(f"Failed to fetch telemetry data: {e}")

    async def start_telemetry_loop(self):
        """
        Continuously fetches telemetry data at regular intervals.
        """
        try:
            while True:
                await self.fetch_telemetry_data()
                await asyncio.sleep(5)  # Delay to pace the fetching
        except asyncio.CancelledError:
            logging.info(
                "[TelemetryClientService] Telemetry fetching loop has been cancelled."
            )

    async def start(self):
        """
        Initiates the asynchronous telemetry data fetching loop.
        """
        await self.start_telemetry_loop()
