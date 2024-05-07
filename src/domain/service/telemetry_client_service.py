import asyncio
import logging
import time
from abc import ABC, abstractmethod
from multiprocessing import shared_memory

from src.application.event_bus import EventBus
from src.config import MOCK_TELEMETRY_DATA
from src.domain.event.telemetry.telemetry_subscription_manager import \
    TelemetrySubscriptionManager
from src.domain.model.telemetry_data import MockTelemetry, TelemetryData
from src.domain.service.telemetry_location_service import \
    TelemetryLocationService
from src.domain.service.telemetry_versions import version_1_10, version_1_12
from src.shared.helpers.constants import EventType


class ITelemetryClient(ABC):
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_version_number(self):
        pass

    @abstractmethod
    def close(self):
        pass


class TelemetryClientService(ITelemetryClient):
    def __init__(self, telemetry_subscription_manager: TelemetrySubscriptionManager):
        self.telemetry_subscription_manager = telemetry_subscription_manager
        self.mock_telemetry = MockTelemetry()
        self.location_service = TelemetryLocationService()
        self.shared_memory = None
        self.telemetry_version = None
        self.previous_data = None
        self.running = False
        self.init()

    def init(self):
        """Initialize telemetry data source based on configuration."""
        if MOCK_TELEMETRY_DATA:
            logging.info("Initializing mock telemetry data.")
            self.telemetry_version = self.mock_telemetry_version
        else:
            try:
                self.shared_memory = shared_memory.SharedMemory(
                    name="Local\\SCSTelemetry", create=False
                )
                for version in [version_1_10, version_1_12]:
                    if version.is_same_version(self.shared_memory.buf):
                        self.telemetry_version = version
                        break
                if not self.telemetry_version:
                    raise ValueError("Unsupported telemetry SDK version")
            except FileNotFoundError:
                logging.error("Shared memory segment not found.")
                raise ConnectionError("Shared memory segment not found.")

    def emit_data(self, data):
        """Emit telemetry data."""
        self.telemetry_subscription_manager.notify_handlers(data)

    def get_data(self):
        """Return telemetry data from the appropriate source."""
        data = None

        if not self.telemetry_version:
            raise ValueError("Telemetry version is not set.")
        if MOCK_TELEMETRY_DATA:
            data = self.mock_telemetry.get_telemetry_data()
        else:
            data = self.telemetry_version.parse_data(self.shared_memory.buf)

        nearest_cities = self.location_service.find_nearest_cities(data)
        data.navigation.nearest_cities = nearest_cities

        return data

    def get_version_number(self):
        """Return the telemetry version number."""
        if self.telemetry_version:
            return self.telemetry_version.get_version_number()
        return 0

    def close(self):
        """Clean up the telemetry data source."""
        self.running = False
        if self.shared_memory:
            self.shared_memory.close()
            self.shared_memory = None
        self.telemetry_version = None

    @staticmethod
    def mock_telemetry_version():
        """Simulate telemetry version when in mock mode."""
        return 12

    async def start_telemetry_loop(self):
        """
        Continuously fetches telemetry data at regular intervals.
        """
        try:
            while True:
                current_data = self.get_data()
                telemetry_data = TelemetryData(
                    truck=current_data.truck,
                    game=current_data.game,
                    navigation=current_data.navigation,
                    job=current_data.job
                )
                self.emit_data(telemetry_data)

                await asyncio.sleep(1)  # Delay to pace the fetching
        except asyncio.CancelledError:
            logging.info(
                "[TelemetryClientService] Telemetry fetching loop has been cancelled."
            )

    async def start(self):
        """
        Initiates the asynchronous telemetry data fetching loop.
        """
        await self.start_telemetry_loop()
