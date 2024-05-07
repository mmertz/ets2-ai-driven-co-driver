import logging
from typing import Dict

from src.application.session_management import SessionManagement
from src.domain.service.openai_service import OpenAIService
from src.interfaces.ai_provider_interface import (ImageToTextProvider,
                                                  TextToTextProvider)
from src.shared.exceptions import AIProcessingError


class OpenAIProvider(TextToTextProvider, ImageToTextProvider):
    """
    Provides functionality to interact with OpenAI's API for different AI-driven tasks,
    """

    def __init__(self, model_id: str, params: Dict, is_stream: bool, history_size: int):
        super().__init__(model_id, params, is_stream, history_size)
        self.client = OpenAIService()

    def text_to_text(
        self,
        input_text: str,
        system_text: str,
        session: SessionManagement,
    ) -> str:
        """
        Generates text based on input text using the specified OpenAI model.
        """
        try:
            history = session.interaction_history
            last_user_messages = history[-self.history_size:]
            temperature = self.params.get("temperature", 0.8)

            user_messages = [
                {"role": message["role"], "content": message["content"]}
                for message in last_user_messages
            ]

            response = self.client.text_to_text(
                input_text=input_text,
                system_text=system_text,
                user_messages=user_messages,
                model=self.model_id,
                max_tokens=4096,
                temperature=temperature,
            )

            return response
        except Exception as e:
            logging.error(f"Failed to generate text-to-text with OpenAI: {str(e)}")
            raise AIProcessingError(f"OpenAI text-to-text processing failed: {str(e)}")

    def image_to_text(self, image_path: str) -> str:
        """
        Converts an image to text.
        """
        # Hypothetical implementation, as OpenAI does not provide this directly
        return "Extracted text from image at " + image_path

    def text_to_audio(
        self,
        text: str,
    ) -> bytes:
        """
        Converts text to spoken audio using OpenAI's text-to-speech API.
        """
        try:
            voice = self.params.get("voice", "alloy")

            response = self.client.text_to_audio(
                model=self.model_id, text=text, voice=voice
            )
            return response
        except Exception as e:
            logging.error(f"Failed to generate text-to-audio with OpenAI: {str(e)}")
            raise AIProcessingError(f"OpenAI text-to-audio processing failed: {str(e)}")
