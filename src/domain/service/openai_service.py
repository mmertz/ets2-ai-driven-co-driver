# openai_service.py
import json
import logging
from typing import Any, Dict, List, Optional

from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.shared.exceptions import AIProcessingError

client = OpenAI(api_key=OPENAI_API_KEY)


class OpenAIService:
    @staticmethod
    def text_to_text(
        input_text: str,
        system_text: str,
        user_messages: List[dict],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 4096,
        temperature: float = 0.8,
    ) -> str:
        try:
            combined_messages = [
                {"role": "system", "content": system_text},
                *user_messages,
                {"role": "user", "content": input_text},
            ]

            response = client.chat.completions.create(
                model=model,
                messages=combined_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            if response.choices:
                return response.choices[0].message.content
            else:
                logging.error("OpenAI API returned no choices.")
                return "I'm sorry, I couldn't process your request."
        except Exception as e:
            logging.error(f"Failed to generate text-to-text with OpenAI: {str(e)}")
            raise AIProcessingError(f"OpenAI text-to-text processing failed: {str(e)}")

    @staticmethod
    def text_to_audio(
        text: str,
        model: str = "tts-1",
        voice: Optional[str] = "alloy",
    ) -> bytes:
        try:
            response = client.audio.speech.create(model=model, input=text, voice=voice)
            return response.content
        except Exception as e:
            logging.error(f"Failed to generate text-to-audio with OpenAI: {str(e)}")
            raise AIProcessingError(f"OpenAI text-to-audio processing failed: {str(e)}")

    @staticmethod
    def text_to_json(
        input_text: str,
        system_text: str,
        params: Dict[str, Any],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 4096,
        temperature: float = 0.8,
    ) -> Dict[str, Any]:
        try:
            combined_messages = [
                {"role": "system", "content": system_text},
                {"role": "user", "content": input_text},
            ]

            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                temperature=temperature,
                messages=combined_messages,
                max_tokens=max_tokens,
                **params,
            )

            if response.choices:
                json_response = json.loads(response.choices[0].message.content)
                return json_response
            else:
                logging.error("OpenAI API returned no choices.")
                return {}
        except Exception as e:
            logging.error(f"Failed to generate text-to-json with OpenAI: {str(e)}")
            raise AIProcessingError(f"OpenAI text-to-json processing failed: {str(e)}")
