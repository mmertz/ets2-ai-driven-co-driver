from abc import ABC, abstractmethod
from typing import Dict

from src.application.session_management import SessionManagement


class TextToTextProvider(ABC):
    def __init__(self, model_id: str, params: Dict, is_stream: bool = False, history_size: int = 5):
        self.model_id = model_id
        self.params = params
        self.is_stream = is_stream
        self.history_size = history_size

    @abstractmethod
    def text_to_text(
        self,
        input_text: str,
        system_text: str,
        session: SessionManagement,
    ) -> str:
        pass


class ImageToTextProvider(ABC):
    def __init__(self, model_id: str, params: Dict, is_stream: bool = False, history_size: int = 5):
        self.model_id = model_id
        self.params = params
        self.is_stream = is_stream
        self.history_size = history_size

    @abstractmethod
    def image_to_text(self, image_path: str) -> str:
        pass


class TextToAudioProvider(ABC):
    def __init__(self, model_id: str, params: Dict, is_stream: bool = False, history_size: int = 5):
        self.model_id = model_id
        self.params = params
        self.is_stream = is_stream
        self.history_size = history_size

    @abstractmethod
    def text_to_audio(self, text: str) -> bytes:
        pass
