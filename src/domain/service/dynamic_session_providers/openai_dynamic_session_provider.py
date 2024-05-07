import json
import logging
from typing import Any, Dict, List

from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.application.session_management import SessionManagement
from src.domain.service.dynamic_session_providers.dynamic_session_interface import \
    DynamicSessionInterface
from src.domain.service.openai_service import OpenAIService


class OpenAIDynamicSessionProvider(DynamicSessionInterface):
    def __init__(
        self,
        event_bus: EventBus,
        session_manager: SessionManagement,
        model: str = "gpt-3.5-turbo-0125",
        params: dict = {},
        history_size: int = 5,
        interaction_interval: int = 3,
    ):
        super().__init__(event_bus, session_manager, model, params, history_size, interaction_interval)
        self.openai_provider = OpenAIService()

    def process(self) -> Session:
        conversation_history = self.session.interaction_history[
            -self.interaction_interval :
        ]
        dynamic_profile = self.session.co_driver.dynamic_profile
        system_prompt = "You are an AI assistant designed to analyze conversation history and update the co-driver's dynamic profile."
        input_text = f"Conversation History:\n{conversation_history}\n\nCurrent Dynamic Profile:\n{dynamic_profile}\n\nPlease analyze the conversation history and current input, and suggest updates to the dynamic profile in JSON format."

        logging.info(f"[Module][{self.__class__.__name__}] Processing session")

        json_response = OpenAIService.text_to_json(
            input_text=input_text,
            system_text=system_prompt,
            model=self.model,
            params=self.params,
        )

        self.session_manager.update_co_driver_dynamic_profile(json_response)

        return self.session_manager.get_current_session()

    def _construct_prompt(
        conversation_history: List[Dict[str, str]],
        current_input: str,
        dynamic_profile: Dict[str, Any],
    ) -> str:
        prompt = f"Conversation History:\n{conversation_history}\n\nCurrent Input: {current_input}\n\nCurrent Dynamic Profile:\n{dynamic_profile}\n\nPlease analyze the conversation history and current input, and suggest updates to the dynamic profile in JSON format."
        return prompt

    def _parse_response(response_text: str) -> Dict[str, Any]:
        updated_profile = json.loads(response_text)
        return updated_profile
