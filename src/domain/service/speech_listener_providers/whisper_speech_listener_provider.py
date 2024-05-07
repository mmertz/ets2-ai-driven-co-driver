import logging
from typing import Any

import numpy as np
import sounddevice as sd
import torch
from scipy.io.wavfile import write
from whisper import load_model

from src.application.event_bus import EventBus
from src.interfaces.speech_listener_interface import SpeechListenerInterface
from src.shared.helpers.constants import EventCategory, EventType


class WhisperSpeechListenerProvider(SpeechListenerInterface):
    """
    Manages real-time speech recognition using the Whisper model to enhance user interaction by accurately capturing and processing spoken commands.
    It coordinates with the system's event bus to manage audio input states efficiently.
    """

    def __init__(
        self,
        event_bus: EventBus,
        input_device_index: int,
        model_name: str = "base",
        temp_directory: str = "/tmp",
    ) -> None:
        self.event_bus = event_bus
        self.input_device_index = input_device_index
        self.model = load_model(
            model_name, device="cuda" if torch.cuda.is_available() else "cpu"
        )
        self.temp_directory = temp_directory
        self.fs = 44100
        self.silent_threshold = 1.3
        self.grace_period = 2
        self.buffer = []
        self.recording = []
        self.silence_duration = 0.0
        self.speech_detected = False
        self.recording_finished = False
        self.stream = None

        logging.debug(
            "[WhisperSpeechListenerProvider] Initialized with model %s on device %s",
            model_name,
            input_device_index,
        )

    def start_listening(self):
        """Start listening to audio input."""
        logging.debug("[WhisperSpeechListenerProvider] start_listening called")
        if self.stream is not None and self.stream.active:
            logging.debug(
                "[WhisperSpeechListenerProvider] Existing stream is active, stopping first."
            )
            self.stop_listening()

        self.recording = []
        self.silence_duration = 0.0
        self.speech_detected = False
        self.stream = sd.InputStream(
            callback=self._audio_callback,
            device=self.input_device_index,
            channels=1,
            samplerate=self.fs,
            dtype="float32",
        )
        self.stream.start()
        logging.info(
            "[WhisperSpeechListenerProvider] Listening started on device index: %s",
            self.input_device_index,
        )

    def stop_listening(self):
        logging.debug("[WhisperSpeechListenerProvider] stop_listening called")
        if self.stream and self.stream.active:
            self.stream.stop()
            self.stream.close()
        self.stream = None
        logging.info("[WhisperSpeechListenerProvider] Listening stopped.")

    def _audio_callback(
        self, indata: np.ndarray, frames: int, time: Any, status: sd.CallbackFlags
    ) -> None:
        """
        Handles the incoming audio stream by detecting speech and managing recording states.

        Args:
        indata (np.ndarray): The buffer containing the captured audio data.
        frames (int): The number of frames in the buffer.
        time (Any): Timestamp information for the buffer.
        status (sd.CallbackFlags): Flags indicating the status of the audio stream.
        """
        if status:
            logging.error(
                "[WhisperSpeechListenerProvider] Audio callback error: %s", status
            )
        volume_norm = np.linalg.norm(indata) * 10
        is_loud = volume_norm > self.silent_threshold

        logging.debug("[WhisperSpeechListenerProvider] is_loud: %s", is_loud)

        if is_loud:
            logging.debug(
                "[WhisperSpeechListenerProvider] Speech detected, silence duration: %s",
                self.silence_duration,
            )

            self.silence_duration = 0
            self.speech_detected = True
            self.recording.extend(indata[:, 0])
        else:
            if self.speech_detected:
                self.silence_duration += frames / self.fs
                if self.silence_duration <= self.grace_period:
                    logging.debug(
                        "[WhisperSpeechListenerProvider] Still in grace period, recording extended. Current length: %s",
                        len(self.recording),
                    )
                    self.recording.extend(indata[:, 0])
                else:
                    logging.debug(
                        "[WhisperSpeechListenerProvider] Recording finished, silence duration: %s",
                        self.silence_duration,
                    )

                    self.event_bus.emit(
                        EventType.USER_SPEECH_END, None, category=EventCategory.AUDIO
                    )
                    self.event_bus.emit(
                        EventType.AUDIO_INPUT_PAUSE, None, category=EventCategory.AUDIO
                    )
                    self.event_bus.emit(
                        EventType.REQUEST_IN_PROGRESS, None, category=EventCategory.GENERIC
                    )

                    self.recording_finished = True
                    self.silence_duration = 0
                    self.speech_detected = False
                    self._process_audio()
                    self.stop_listening()
                    logging.debug(
                        "[WhisperSpeechListenerProvider] Recording finished and stream stopped"
                    )

    def _process_audio(self):
        """
        Processes the recorded audio data by transcribing it and handling the response.
        """
        logging.debug("[WhisperSpeechListenerProvider] Processing recorded audio data")
        if self.recording:
            output_wav = f"{self.temp_directory}/temp_recording.wav"
            write(output_wav, self.fs, np.array(self.recording, dtype=np.float32))
            logging.info("[WhisperSpeechListenerProvider] Transcribing...")
            result = self.model.transcribe(output_wav)
            transcription = result.get("text", "")
            if transcription:
                logging.info(
                    "[WhisperSpeechListenerProvider] Transcription successful: %s",
                    transcription,
                )
                self.event_bus.emit(
                    EventType.TRANSCRIPTION_COMPLETE,
                    transcription,
                    category=EventCategory.AUDIO,
                )

            else:
                logging.error(
                    "[WhisperSpeechListenerProvider] No transcription returned."
                )
            self.recording = []  # Clear recording after processing
        else:
            logging.error("[WhisperSpeechListenerProvider] No recording data found.")
