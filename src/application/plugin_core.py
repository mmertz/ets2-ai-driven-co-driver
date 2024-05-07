import asyncio
import importlib
import logging
import os
import sys
import time

from src.application.event_bus import EventBus
from src.application.interface.module_interface import ModuleInterface
from src.application.session_management import SessionManagement
from src.application.setup_management import SetupManagement
from src.domain.event.telemetry.telemetry_subscription_manager import \
    TelemetrySubscriptionManager
from src.domain.service.audio_input_service import AudioInputService
from src.domain.service.dialogue_manager_service import DialogueManager
from src.domain.service.speech_output_service import SpeechOutputService
from src.domain.service.telemetry_client_service import TelemetryClientService
from src.factories.ai_provider_factory import AIProviderFactory
from src.factories.dynamic_session_provider_factory import \
    DynamicSessionProviderFactory
from src.factories.speech_listener_factory import SpeechListenerFactory
from src.infrastructure.input_output.keyboard_manager import KeyboardManager
from src.shared.helpers.constants import AIProviderType


class PluginCore:
    """
    Core class for the ETS2 AI Plugin. Initializes the system and manages core components.
    This is the entry point for the plugin, responsible for setting up services and event handling.
    """

    def __init__(self, listener_type="whisper"):
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Initializing PluginCore with all components.")

        self.event_bus = EventBus()
        self.session_manager = SessionManagement()
        self.setup_manager = SetupManagement(
            profile_path="src/co_driver_profiles.json",
            session_directory="./data/sessions",
            session_manager=self.session_manager,
        )

        self.setup_manager.setup_initial_session()

        self.session = self.session_manager.get_current_session()

        self.keyboard_manager = KeyboardManager()

        self.text_to_text_provider = AIProviderFactory.get_provider(
            service_type=AIProviderType.TEXT_TO_TEXT, session=self.session
        )
        self.text_to_audio_provider = AIProviderFactory.get_provider(
            service_type=AIProviderType.TEXT_TO_AUDIO, session=self.session
        )

        self.dynamic_session_provider = DynamicSessionProviderFactory.get_provider(
            event_bus=self.event_bus, session_manager=self.session_manager
        )

        self.dialogue_manager = DialogueManager(
            event_bus=self.event_bus,
            session_manager=self.session_manager,
            text_to_text_provider=self.text_to_text_provider,
        )

        self.speech_listener = SpeechListenerFactory.create_speech_listener(
            listener_type=listener_type, event_bus=self.event_bus
        )
        self.audio_service = AudioInputService(
            event_bus=self.event_bus,
            speech_listener=self.speech_listener,
            keyboard_manager=self.keyboard_manager,
        )
        self.speech_output_service = SpeechOutputService(
            event_bus=self.event_bus,
            text_to_audio_provider=self.text_to_audio_provider,
            audio_output_path="./",
        )

        self.telemetry_subscription_manager = TelemetrySubscriptionManager()
        self.telemetry_client = TelemetryClientService(
            telemetry_subscription_manager=self.telemetry_subscription_manager
        )

        self.register_services()
        self.register_telemetry_handlers()

        self.running = True

    async def start(self) -> None:
        """
        Starts the core components of the plugin. This method initializes all services
        and begins the event listening and processing loop.
        """
        logging.info("Starting all core services.")
        await self.telemetry_client.start()

        logging.info("Starting the main event loop. Press Ctrl+C to stop.")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Stopping the plugin.")
            self.stop()

    def stop(self) -> None:
        """
        Stops the plugin and cleans up resources.
        """
        logging.info("Stopping all services and cleaning up resources.")
        self.running = False

    def register_services(self):
        """
        Register all necessary services and modules with the event bus.
        """
        logging.info("Registering all modules and services with the event bus.")
        self.keyboard_manager.start_listener()
        self.audio_service.register()
        self.dialogue_manager.register()
        self.speech_output_service.register()
        self.dynamic_session_provider.register()

    def register_telemetry_handlers(self):
        """
        Automatically registers all telemetry handlers found in the handlers directory.
        """

        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )  # Adjust path to match the project structure
        logging.debug("Base directory: %s", base_dir)
        handlers_directory = os.path.join(
            base_dir, "src", "domain", "event", "telemetry", "handlers"
        )
        logging.debug("Loading handlers from: %s", handlers_directory)
        for filename in os.listdir(handlers_directory):
            if (
                filename.endswith("_handler.py")
                and filename != "telemetry_event_handlers.py"
            ):
                module_name = filename[:-3]  # Strip the .py extension
                module_path = f"src.domain.event.telemetry.handlers.{module_name}"

                handler_module = importlib.import_module(module_path)

                class_name = "".join(
                    word.capitalize() for word in module_name.split("_")
                )
                handler_class = getattr(handler_module, class_name)

                # Instantiate and register the handler
                handler_instance = handler_class(
                    self.event_bus, self.session, self.telemetry_subscription_manager
                )
                handler_instance.register()

    def register_module(self, module: ModuleInterface) -> bool:
        """
        Dynamically registers a new module to expand functionality.
        Modules should interface with the event bus to receive or emit events.
        This method now returns a boolean indicating success or failure.
        """
        try:
            module.register(self.event_bus)
            return True
        except Exception as e:
            logging.error("Failed to register module: %s", e)
            return False

    def unregister_module(self, module: ModuleInterface) -> bool:
        """
        Dynamically unregisters a module.
        Modules should cleanly remove themselves from the event bus.
        """
        try:
            module.unregister(self.event_bus)
            return True
        except Exception as e:
            logging.error("Failed to unregister module: %s", e)
            return False


if __name__ == "__main__":
    core = PluginCore()
    asyncio.run(core.start())
