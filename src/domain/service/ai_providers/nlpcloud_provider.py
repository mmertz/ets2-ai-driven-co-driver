import logging
from typing import Dict

import nlpcloud

from src.application.session_management import SessionManagement
from src.domain.service.nlpc_cloud_service import NLPCloudService
from src.interfaces.ai_provider_interface import (ImageToTextProvider,
                                                  TextToTextProvider)
from src.shared.exceptions import AIProcessingError


class NLPCloudProvider(TextToTextProvider):
    """
    Provides functionality to interact with NLPCloud's API for different AI-driven tasks.
    """

    def __init__(self, model_id: str, params: Dict, is_stream: bool, history_size: int):
        super().__init__(model_id, params, is_stream, history_size)
        self.client = NLPCloudService(model_id)

    def text_to_text(
        self,
        input_text: str,
        system_text: str,
        session: SessionManagement,
    ) -> str:
        """
        Generates text based on input text using the specified NLPCloud model.
        """
        try:
            history = session.interaction_history
            last_messages = history[-self.history_size :]

            response = self.client.chatbot(
                input_text=input_text,
                context=system_text,
                history=last_messages,
            )

            return response["response"]
        except Exception as e:
            logging.error(f"Failed to generate text-to-text with NLPCloud: {str(e)}")
            raise AIProcessingError(
                f"NLPCloud text-to-text processing failed: {str(e)}"
            )
