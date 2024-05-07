from typing import Any, Dict

from src.domain.service.dynamic_session_providers.dynamic_session_interface import \
    DynamicSessionInterface
from src.domain.service.spacy_nlp_service import SpacyNLPService


class SpacyDynamicSession(DynamicSessionInterface):
    def __init__(self, model_name: str = "en_core_web_lg"):
        self.spacy_service = SpacyNLPService(model_name)

    def process_text(self, text: str) -> Dict[str, Any]:
        response = self.spacy_service.process_text(text)
        keywords = [
            token.lemma_ for token in response if not token.is_stop and token.is_alpha
        ]
        return {
            "entities": response["entities"],
            "keywords": keywords,
        }
