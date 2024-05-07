import logging
import uuid
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import Any, Dict, Optional, Type, TypeVar

from src.application.model.session_model import CoDriverProfile, Session
from src.infrastructure.storage.json_storage import JsonStorage

T = TypeVar('T')

def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    """Recursively convert a dictionary to a dataclass."""
    if not isinstance(data, dict):
        return data  # Not a dict, no conversion needed, pass as is (handles simple types)

    fieldtypes = {f.name: f.type for f in fields(cls)}
    kwargs = {}
    for field_name, field_type in fieldtypes.items():
        field_value = data.get(field_name)

        # Check if the field is itself a dataclass and field_value is dict
        if is_dataclass(field_type) and isinstance(field_value, dict):
            field_value = from_dict(field_type, field_value)
        elif isinstance(field_value, dict) and hasattr(field_type, '__args__'):  # Handle Optional[SomeDataClass]
            actual_type = next((t for t in field_type.__args__ if t is not type(None)), None)
            if is_dataclass(actual_type):
                field_value = from_dict(actual_type, field_value)

        kwargs[field_name] = field_value

    return cls(**kwargs)


class SessionManagement:
    """
    Manages sessions for users, providing capabilities to create, retrieve, update,
    and delete sessions. Utilizes JSON-based storage for session data.
    """

    def __init__(self) -> None:
        self.sessions: Dict[str, Session] = {}
        self.storage = JsonStorage(storage_dir="./data/sessions")
        self.active_session: Optional[Session] = None
        logging.info("[SessionManagement] SessionManagement initialized")

    def create_session(self) -> Session:
        """Creates a new session with a unique identifier and stores it."""
        session_id = str(uuid.uuid4())
        new_session = Session(session_id=session_id)
        self.sessions[session_id] = new_session
        self.active_session = new_session
        self.storage.save_data(session_id, new_session.model_dump_json())
        return new_session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieves a session by its ID, converting stored data to dataclass instances."""
        session = self.sessions.get(session_id)
        if not session:
            session_data = self.storage.load_data(session_id)
            if session_data:
                session = from_dict(Session, session_data)
                self.sessions[session_id] = session
            else:
                session = self.create_session()
        return session

    def get_current_session(self) -> Optional[Session]:
        return self.active_session

    def set_current_session(self, session_id: str) -> None:
        self.active_session = self.get_session(session_id)

    def add_interaction(self, interaction: Dict[str, str]) -> bool:
        """
        Adds an interaction to the session's interaction history.
        """
        session = self.get_current_session()
        if session:
            session.interaction_history.append(interaction)
            self.storage.save_data(session.session_id, session.model_dump_json())
            logging.info(
                "[SessionManagement] Interaction added to session %s",
                session.session_id,
            )
            return True
        return False

    def delete_session(self, session_id: str) -> bool:
        """
        Deletes a session based on its ID.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            # self.storage.delete_data(session_id)
            logging.info("[SessionManagement] Session deleted: %s", session_id)
            return True
        return False

    def load_co_driver_profile(self, session_id: str, profile_data: Dict) -> None:
        """
        Loads co-driver profile data into the session.
        """
        session = self.get_session(session_id)
        if session:
            session.co_driver = CoDriverProfile(**profile_data)
            self.storage.save_data(session.session_id, session.model_dump_json())

    def update_co_driver_dynamic_profile(
        self, session_id: str, new_state: Dict[str, any]
    ) -> None:
        """
        Updates the dynamic profile of the co-driver in the session.
        """
        session = self.get_session(session_id)
        if session:
            session.co_driver.dynamic_profile.update(new_state)
            self.storage.save_data(session.session_id, session.model_dump_json())
