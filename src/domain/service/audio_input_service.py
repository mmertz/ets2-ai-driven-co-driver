import logging

from pynput.keyboard import Key

from src.application.event_bus import EventBus
from src.infrastructure.input_output.keyboard_manager import KeyboardManager
from src.interfaces.speech_listener_interface import SpeechListenerInterface
from src.shared.helpers.constants import EventType


class AudioInputService:
    """
    Controls speech listening activation via a hotkey, using a centralized keyboard manager.
    """

    def __init__(
        self,
        event_bus: EventBus,
        speech_listener: SpeechListenerInterface,
        keyboard_manager: KeyboardManager,
        hotkey: str = "alt",
    ):
        """
        Initializes the service with necessary components to manage speech input control.
        """
        self.event_bus: EventBus = event_bus
        self.speech_listener: SpeechListenerInterface = speech_listener
        self.keyboard_manager: KeyboardManager = keyboard_manager
        self.hotkey: str = hotkey
        self.listening: bool = False
        self.ignore_input: bool = False

    def pause_listening(self, _data=None):
        self.ignore_input = True
        logging.debug("[AudioInputService] Ignoring input as co-driver is speaking.")

    def resume_listening(self, _data=None):
        self.ignore_input = False
        logging.debug(
            "[AudioInputService] Resuming input as co-driver has stopped speaking."
        )

    def on_press(self, key: Key):
        """
        Responds to hotkey presses to toggle listening.
        """
        try:
            if self._is_hotkey(key):
                self.toggle_listening()
        except AttributeError:
            pass

    def _is_hotkey(self, key: Key) -> bool:
        """
        Checks if a key matches the predefined hotkey.
        """
        return key == Key.alt

    def register(self):
        """
        Starts listening for the hotkey.
        """
        self.keyboard_manager.register_callback(self.on_press)
        self.event_bus.subscribe(EventType.CO_DRIVER_SPEECH_START, self.pause_listening)
        self.event_bus.subscribe(EventType.CO_DRIVER_SPEECH_END, self.resume_listening)

        self.event_bus.subscribe(EventType.AUDIO_INPUT_PAUSE, self.pause_listening)
        self.event_bus.subscribe(EventType.AUDIO_INPUT_RESUME, self.resume_listening)

        logging.info(
            "[AudioInputService] Hotkey for toggling listening set to %s", self.hotkey
        )

    def unregister(self):
        """
        Stops listening for the hotkey.
        """
        self.keyboard_manager.unregister_callback(self.on_press)
        self.event_bus.unsubscribe(
            EventType.CO_DRIVER_SPEECH_START, self.pause_listening
        )
        self.event_bus.unsubscribe(
            EventType.CO_DRIVER_SPEECH_END, self.resume_listening
        )
        logging.info("[AudioInputService] Hotkey unregistered")

    def toggle_listening(self):
        """
        Toggles the speech listening state.
        """
        if self.ignore_input:
            self.listening = False
            self.event_bus.set_state(EventType.USER_SPEECH_START, False)
            self.event_bus.unblock_telemetry_handlers()
            logging.info("[AudioInputService] Unblocking telemetry handlers")
            self.speech_listener.stop_listening()
            logging.info("[AudioInputService] Listening ignored.")
            return

        if self.listening:
            self.listening = False
            self.event_bus.set_state(EventType.USER_SPEECH_START, False)
            self.event_bus.unblock_telemetry_handlers()
            logging.info("[AudioInputService] Unblocking telemetry handlers")
            self.speech_listener.stop_listening()
            logging.info("[AudioInputService] Listening stopped.")
        else:
            self.listening = True
            self.event_bus.set_state(EventType.USER_SPEECH_START, True)
            self.event_bus.block_telemetry_handlers()
            logging.info("[AudioInputService] Blocking telemetry handlers")
            self.speech_listener.start_listening()
            logging.info("[AudioInputService] Listening started.")
