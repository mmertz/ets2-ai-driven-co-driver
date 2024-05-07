from typing import Dict, Optional

import requests

from src.application.session_management import SessionManagement
from src.domain.service.replicate_service import make_replicate_prediction
from src.interfaces.ai_provider_interface import (TextToAudioProvider,
                                                  TextToTextProvider)


class ReplicateProvider(TextToTextProvider, TextToAudioProvider):
    def text_to_text(
        self, input_text: str, system_text: str, session: SessionManagement
    ) -> Optional[Dict]:
        """Convert text to text using a specific voice and language."""
        parsed_params = self.params
        for key, value in parsed_params.items():
            if value == "{{text}}":
                parsed_params[key] = input_text
            if value == "{{system}}":
                parsed_params[key] = system_text

        history = session.interaction_history
        last_user_messages = history[-self.history_size :]

        conversation_history = ""

        for message in last_user_messages:
            role = "Co-driver" if message["role"] == "assistant" else "User"
            conversation_history += f"{role}: {message['content']}\n"

        parsed_params["conversation_history"] = conversation_history

        return make_replicate_prediction(
            model_version=self.model_id,
            input_data=parsed_params,
            is_stream=self.is_stream,
        )

    def text_to_audio(self, text: str) -> bytes:
        """Convert text to audio using a specific voice and language."""
        parsed_params = self.params
        for key, value in parsed_params.items():
            if value == "{{text}}":
                parsed_params[key] = text

        url = make_replicate_prediction(
            self.model_id, parsed_params, is_stream=self.is_stream
        )

        return requests.get(url=url, timeout=200).content
