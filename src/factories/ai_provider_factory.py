from src.application.model.session_model import Session
from src.application.session_management import SessionManagement
from src.domain.service.ai_providers.microsoft_edge_provider import \
    MicrosoftEdgeProvider
from src.domain.service.ai_providers.nlpcloud_provider import NLPCloudProvider
from src.domain.service.ai_providers.openai_provider import OpenAIProvider
from src.domain.service.ai_providers.replicate_provider import \
    ReplicateProvider
from src.shared.helpers.constants import AIProviderType


class AIProviderFactory:
    @staticmethod
    def get_provider(service_type: AIProviderType, session: Session):
        config_map = {
            AIProviderType.TEXT_TO_TEXT: session.co_driver.config.text_to_text,
            AIProviderType.IMAGE_TO_TEXT: session.co_driver.config.image_to_text,
            AIProviderType.TEXT_TO_AUDIO: session.co_driver.config.text_to_audio,
        }

        config = config_map.get(service_type)
        if config is None:
            raise ValueError(
                "Configuration for AI service is not defined in the co-driver's profile."
            )

        history_size = config.history_size if config.history_size else 5
        is_stream = config.is_stream if config.is_stream else False

        if config.provider == "openai":
            return OpenAIProvider(
                model_id=config.model_id,
                params=config.params,
                is_stream=is_stream,
                history_size=history_size,
            )
        if config.provider == "replicate":
            return ReplicateProvider(
                model_id=config.model_id,
                params=config.params,
                is_stream=is_stream,
                history_size=history_size,
            )

        if config.provider == "nlpcloud":
            return NLPCloudProvider(
                model_id=config.model_id,
                params=config.params,
                is_stream=is_stream,
                history_size=history_size,
            )
        if config.provider == "microsoft_edge":
            return MicrosoftEdgeProvider(
                model_id=config.model_id,
                params=config.params,
                is_stream=is_stream,
                history_size=history_size,
            )

        raise ValueError(f"Unsupported AI provider: {config.provider}")
