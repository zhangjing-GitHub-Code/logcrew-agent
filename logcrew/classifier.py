"""Classifier Agent — vectorize incidents and match against known issue DB."""

from logcrew.models import Incident


class ClassifierAgent:
    """Classify incidents as known or unknown using vector similarity."""

    def __init__(self, threshold: float = 0.85) -> None:
        self.threshold = threshold
        self._known: dict[str, str] = {}  # embedding_key -> resolution

    async def classify(self, incident: Incident) -> tuple[str, float]:
        """Return (label, confidence). label='known'|'unknown'."""
        # Placeholder: real impl would query Qdrant vector DB
        key = incident.trace_id[:8]
        if key in self._known:
            return "known", 0.92
        return "unknown", 0.0

    def register_known(self, signature: str, resolution: str) -> None:
        """Register a known issue signature and its resolution."""
        self._known[signature] = resolution
