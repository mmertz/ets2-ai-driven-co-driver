# src/domain/service/speech_listener_interface.py

from abc import ABC, abstractmethod


class SpeechListenerInterface(ABC):
    """
    Interface that all speech listeners must implement to be used with AudioInputService.
    """
    @abstractmethod
    def start_listening(self):
        """
        Start listening to the audio input.
        """
        pass

    @abstractmethod
    def stop_listening(self):
        """
        Stop listening to the audio input.
        """
        pass

    @abstractmethod
    def _process_audio(self):
        """
        Process captured audio and return the transcription or result.
        """
        pass