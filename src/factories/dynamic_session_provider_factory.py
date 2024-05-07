from src.application.event_bus import EventBus
from src.application.model.session_model import Session
from src.application.session_management import SessionManagement
from src.domain.service.dynamic_session_providers.openai_dynamic_session_provider import \
    OpenAIDynamicSessionProvider
from src.domain.service.dynamic_session_providers.spacy_dynamic_session_provider import \
    SpacyDynamicSession


class DynamicSessionProviderFactory:
    @staticmethod
    def get_provider(event_bus: EventBus, session_manager: SessionManagement):
        session = session_manager.get_current_session()
        config = session.co_driver.config.dynamic_session

        if config is None:
            raise ValueError(
                "Configuration for dynamic session service is not defined in the co-driver's profile."
            )

        history_size = config.history_size if config.history_size else 5
        interaction_interval = (
            config.interaction_interval if config.interaction_interval else 3
        )

        if config.provider == "openai":
            return OpenAIDynamicSessionProvider(
                event_bus=event_bus,
                session_manager=session_manager,
                model=config.model_id,
                params=config.params,
                history_size=history_size,
                interaction_interval=interaction_interval,
            )
        if config.provider == "spacy":
            return SpacyDynamicSession(
                event_bus=event_bus,
                session_manager=session_manager,
                model=config.model_id,
                params=config.params,
                history_size=history_size,
                interaction_interval=interaction_interval,
            )

        raise ValueError(f"Unsupported AI provider: {config.provider}")
