import logging
import os
import subprocess

from src.application.event_bus import EventBus
from src.config import MOCK_AI_RESPONSES
from src.interfaces.ai_provider_interface import TextToAudioProvider
from src.shared.helpers.constants import EventType


class SpeechOutputService:
    """
    Handles speech output by converting text responses to audio and managing the playback.
    The service interacts with an event bus to listen for complete dialogue responses
    and controls audio output to ensure user interactions are handled in sequence.
    """

    def __init__(
        self,
        event_bus: EventBus,
        text_to_audio_provider: TextToAudioProvider,
        audio_output_path: str,
    ):
        """
        Initializes the SpeechOutputService with necessary components for audio management.

        Args:
        event_bus (EventBus): The system's event bus for subscribing to and emitting events.
        text_to_audio_provider (TextToAudioProvider): Provider for converting text to audio.
        audio_output_path (str): Path where audio files are stored temporarily.
        """
        self.event_bus: EventBus = event_bus
        self.text_to_audio_provider: TextToAudioProvider = text_to_audio_provider
        self.audio_output_path: str = audio_output_path

    def register(self) -> None:
        """
        Registers the service with the event bus to respond to dialogue completion events.
        """
        self.event_bus.subscribe(
            EventType.DIALOGUE_RESPONSE_COMPLETE, self.handle_dialogue_response
        )

    def unregister(self) -> None:
        """
        Unregisters the service from the event bus, ceasing its response to dialogue events.
        """
        self.event_bus.unsubscribe(
            EventType.DIALOGUE_RESPONSE_COMPLETE, self.handle_dialogue_response
        )

    def handle_dialogue_response(self, dialogue_response: str) -> None:
        """
        Processes the completed dialogue response by converting it to audio, playing it,
        and managing audio output events.

        Args:
        dialogue_response (str): The text response from dialogue processing to be spoken.
        """
        logging.debug("[SpeechOutputService] Handling dialogue response")
        try:

            if MOCK_AI_RESPONSES:
                audio_file_path: str = './mock_output.wav'
            else:
                audio_data: bytes = self.text_to_audio_provider.text_to_audio(dialogue_response)
                audio_file_path: str = self._save_audio_data(audio_data)

            self.event_bus.emit(EventType.CO_DRIVER_SPEECH_START, None)
            self._play_audio_file(audio_file_path)
            self.event_bus.emit(EventType.CO_DRIVER_SPEECH_END, None)
            self.event_bus.emit(EventType.AUDIO_INPUT_RESUME, None)
            self.event_bus.emit(EventType.REQUEST_COMPLETE, None)

            logging.debug("[SpeechOutputService] Unblocking telemetry handlers")
            self.event_bus.unblock_telemetry_handlers()


        except Exception as e:
            logging.error("[SpeechOutputService] Error in handling transcription: %s", str(e))

    def _save_audio_data(self, audio_data: bytes) -> str:
        """
        Saves the generated audio data to a file.

        Args:
        audio_data (bytes): Binary audio data to be saved.

        Returns:
        str: The path to the saved audio file.
        """
        audio_file_path = os.path.join(self.audio_output_path, "response_audio.wav")
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_data)
        return audio_file_path

    def _play_audio_file(self, file_path: str) -> None:
        """
        Plays the specified audio file using the system's default audio player.

        Args:
        file_path (str): The path to the audio file to be played.
        """
        cmd = ["afplay", file_path]
        logging.debug("[SpeechOutputService] Executing command to play audio: %s", " ".join(cmd))
        subprocess.call(cmd)
        self._cleanup_temp_files(file_path)

    def _cleanup_temp_files(self, file_path: str) -> None:
        """
        Removes the temporary audio file after playing it.

        Args:
        file_path (str): The path to the audio file to be removed.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.debug("[SpeechOutputService] Cleaned up temporary audio file: %s", file_path)
