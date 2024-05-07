from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AIProviderConfig(BaseModel):
    provider: str
    model_id: Optional[str] = None
    params: Dict[str, Any] = {}
    history_size: Optional[int] = None
    is_stream: Optional[bool] = False


class DynamicSessionProviderConfig(BaseModel):
    provider: str
    model_id: Optional[str] = None
    params: Dict[str, Any] = {}
    history_size: Optional[int] = None
    interaction_interval: Optional[int] = None


class CoDriverProfileConfig(BaseModel):
    text_to_text: Optional[AIProviderConfig] = None
    text_to_audio: Optional[AIProviderConfig] = None
    image_to_text: Optional[AIProviderConfig] = None
    dynamic_session: Optional[DynamicSessionProviderConfig] = None


class StaticProfile(BaseModel):
    name: str
    age: int
    background: Dict[str, str]
    personality: Dict[str, float]  # Added personality directly into StaticProfile
    preferences: Dict[str, List[str]]


class LastInteraction(BaseModel):
    date: str
    topic: str
    user_mood: str
    interaction_quality: int


class Relationship(BaseModel):
    rapport: int
    trust_level: int
    familiarity: int


class State(BaseModel):
    mood: str
    fatigue_level: int
    stress_level: int
    interest_level: int
    satisfaction: int
    optimism: int
    last_interaction: LastInteraction
    relationship: Relationship
    important_memories: List  # Added important_memories list


class DynamicProfile(BaseModel):
    state: State


class CoDriverProfile(BaseModel):
    static_profile: StaticProfile
    dynamic_profile: DynamicProfile
    config: CoDriverProfileConfig


class Session(BaseModel):
    session_id: str
    user_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    interaction_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    profile_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    co_driver: Optional[CoDriverProfile] = None

    def get_co_driver_context(self):
        return (
            f"Name: {self.co_driver.static_profile.name}\n"
            f"Age: {self.co_driver.static_profile.age}\n"
            f"Personality: {self.co_driver.static_profile.personality}\n"
            f"Preferences: {self.co_driver.static_profile.preferences}\n"
            f"Background: {self.co_driver.static_profile.background}\n"
            f"State: {self.co_driver.dynamic_profile.state}\n"
        )
