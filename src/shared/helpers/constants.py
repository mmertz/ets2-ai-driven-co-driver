
from enum import Enum, auto


class EventCategory(Enum):
    AUDIO = auto()
    TEXT = auto()
    UI = auto()
    GENERIC = auto()
    TRANSCRIPTION = auto()
    TELEMETRY = auto()


class AIProviderType(Enum):
    TEXT_TO_TEXT = auto()
    IMAGE_TO_TEXT = auto()
    TEXT_TO_AUDIO = auto()


class DynamicSessionProviderType(Enum):
    OPENAI = auto()
    NLP = auto()


class EventType(Enum):
    # Audio events
    USER_SPEECH_START = auto()  # Triggered when the user starts speaking
    USER_SPEECH_END = auto()  # Triggered when the user stops speaking
    CO_DRIVER_SPEECH_START = auto()  # Triggered when the co-driver starts speaking
    CO_DRIVER_SPEECH_END = auto()  # Triggered when the co-driver stops speaking

    AUDIO_INPUT_PAUSE = auto()
    AUDIO_INPUT_RESUME = auto()

    REQUEST_IN_PROGRESS = auto()
    REQUEST_COMPLETE = auto()

    # Transcription events
    TRANSCRIPTION_COMPLETE = auto()  # Triggered when speech transcription is completed

    # Dialogue events
    DIALOGUE_RESPONSE_REQUEST = auto()  # Request for generating a dialogue response
    DIALOGUE_RESPONSE_COMPLETE = auto() # Triggered when a dialogue response is generated

    # Telemetry events
    TELEMETRY_RECEIVED = auto()  # Triggered when new telemetry data is received
