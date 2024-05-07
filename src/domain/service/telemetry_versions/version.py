from abc import ABC, abstractmethod
from typing import Any, Dict


class TelemetryVersion(ABC):
    """
    Abstract base class defining the interface for telemetry version handlers.
    """

    @property
    @abstractmethod
    def version_number(self) -> int:
        """Return the version number associated with this telemetry version."""
        pass

    @abstractmethod
    def is_same_version(self, data: bytes) -> bool:
        """Check if the provided data buffer corresponds to this telemetry version."""
        pass

    @abstractmethod
    def parse_data(self, data: bytes) -> Dict[str, Any]:
        """Parse the data buffer according to the telemetry version's specifications."""
        pass
