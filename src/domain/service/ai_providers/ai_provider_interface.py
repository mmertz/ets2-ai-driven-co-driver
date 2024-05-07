
from abc import ABC, abstractmethod
from typing import Any


class AIProviderInterface(ABC):
    """
    Interface for AI providers. All AI provider classes must implement these methods.
    """

    @abstractmethod
    def text_to_text(self, input_text: str) -> str:
        """
        Process text and return the transformed text.
        """
        pass

    @abstractmethod
    def image_to_text(self, image_path: str) -> str:
        """
        Analyze an image and return the extracted text.
        """
        pass

    @abstractmethod
    def text_to_audio(self, text: str) -> bytes:
        """
        Convert text to audio and return the audio file bytes.
        """
        pass
