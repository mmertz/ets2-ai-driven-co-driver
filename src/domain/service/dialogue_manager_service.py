import logging

import spacy

from src.application.event_bus import EventBus
from src.application.session_management import Session, SessionManagement
from src.config import MOCK_AI_RESPONSES, SYSTEM_PROMPT
from src.interfaces.ai_provider_interface import TextToTextProvider
from src.shared.helpers.constants import EventCategory, EventType


class DialogueManager:
    """
    Manages dialogues within the system by generating responses based on user input and prior interaction history.
    Attributes:
        session_manager (SessionManagement): Manages user sessions, storing interaction history and user data.
        event_bus (EventBus): The event bus for subscribing to and emitting events.
    """

    def __init__(
        self,
        event_bus: EventBus,
        session_manager: SessionManagement,
        text_to_text_provider: TextToTextProvider,
    ):
        """
        Initializes the DialogueManager with required services for managing sessions and handling events.
        """
        self.nlp = spacy.load("en_core_web_sm")  # Load the spaCy model

        self.text_to_text_provider = text_to_text_provider
        self.event_bus = event_bus
        self.session_manager = session_manager

    def handle_event(self, event_type: EventType, data: str):
        """
        General event handler that routes events based on type.
        """
        if event_type == EventType.TRANSCRIPTION_COMPLETE:
            self.handle_transcription(data)
        elif event_type == EventType.DIALOGUE_RESPONSE_REQUEST:
            self.generate_response(data)

    def handle_transcription(self, transcription: str):
        """
        Processes transcriptions using NLP, updates the session, and generates responses.
        Args:
            transcription (str): The transcription text from audio input.
        """
        logging.info("[DialogueManager] Handling transcription: %s", transcription)

        # Process transcription with spaCy for entity recognition
        doc = self.nlp(transcription)
        entities = {ent.label_: ent.text for ent in doc.ents}

        # Update session data with recognized entities
        session = self.session_manager.get_current_session()
        if session:
            session.profile_data.update(entities)

        self.generate_response(transcription)

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response based on the current prompt and the context from the session's interaction history.
        """

        session = self.session_manager.get_current_session()

        if not session:
            logging.error("[DialogueManager] No active session found.")
            return "I'm sorry, I seem to have lost our thread. Can you remind me what we were talking about?"

        context = self.prepare_context(session)
        system_text = SYSTEM_PROMPT + " " + context

        logging.info("[DialogueManager] Sending crafted prompt")
        logging.debug("[DialogueManager] Sending prompt: %s", prompt)
        logging.debug("[DialogueManager] Sending system text: %s", system_text)

        response = "This is a mock response"

        if MOCK_AI_RESPONSES is False:
            response = self.text_to_text_provider.text_to_text(
                prompt, system_text, session
            )

        self.session_manager.add_interaction({"role": "user", "content": prompt})
        self.session_manager.add_interaction({"role": "assistant", "content": response})

        self.event_bus.emit(
            EventType.DIALOGUE_RESPONSE_COMPLETE, response, EventCategory.TEXT
        )

        logging.info("[DialogueManager] Generated response for session: %s", response)

    def prepare_context(self, session: Session):
        """
        Prepares contextual information based on the user's profile data for the AI model.
        """
        user_profile_context_items = []

        if session.profile_data:
            for key, value in session.profile_data.items():
                user_profile_context_items.append(f"Key: {key} Value: {value}")

        user_profile_context = ", ".join(user_profile_context_items)

        return (
            f"[USER_PROFILE] {user_profile_context} [/USER_PROFILE] \n"
            f"[CO_DRIVER_PROFILE (AI)] {session.get_co_driver_context()} [/CO_DRIVER_PROFILE]"
        )

    def register(self):
        """
        Register the manager to listen to specific events on the event bus.
        """
        self.event_bus.subscribe(
            EventType.TRANSCRIPTION_COMPLETE, self.handle_transcription
        )
        self.event_bus.subscribe(
            EventType.DIALOGUE_RESPONSE_REQUEST, self.generate_response
        )

    def unregister(self):
        """
        Unregister the manager from listening to specific events on the event bus.
        """
        self.event_bus.unsubscribe(
            EventType.TRANSCRIPTION_COMPLETE, self.handle_transcription
        )
        self.event_bus.unsubscribe(
            EventType.DIALOGUE_RESPONSE_REQUEST, self.generate_response
        )
