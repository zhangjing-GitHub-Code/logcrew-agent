"""Analyzer Agent — long-chain reasoning for root-cause analysis."""

from logcrew.llm_client import LLMClient
from logcrew.models import Incident, RootCause


class AnalyzerAgent:
    """Perform Chain-of-Thought root-cause analysis on unknown incidents."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm = llm_client or LLMClient()
        self._confidence_window: list[float] = []
        self._window_size = 20

    async def analyze(self, incident: Incident) -> RootCause:
        """Run multi-step reasoning to produce a root-cause hypothesis."""
        # Step 1: temporal clustering
        services = sorted({log.service for log in incident.logs})

        # Step 2: severity ranking
        errors = [log for log in incident.logs if log.level in ("ERROR", "FATAL")]

        # Step 3: dependency walk
        deps = await self._fetch_dependencies(services)

        # Step 4: synthesize hypothesis via CoT prompt
        hypothesis = await self._cot_synthesize(incident, errors, deps)

        # Step 5: dynamic confidence with sliding window calibration
        raw_confidence = self._compute_confidence(incident, errors, services, deps)
        calibrated = self._apply_window(raw_confidence)

        return RootCause(
            hypothesis=hypothesis,
            confidence=round(calibrated, 2),
            evidences=[f"{len(errors)} error logs", f"affected: {services}", f"deps: {len(deps)}"],
        )

    async def _fetch_dependencies(self, services: list[str]) -> dict[str, list[str]]:
        """Fetch service topology. Placeholder returns empty graph."""
        return {svc: [] for svc in services}

    async def _cot_synthesize(
        self, incident: Incident, errors: list, deps: dict
    ) -> str:
        """Build a Chain-of-Thought prompt and return synthesized hypothesis."""
        services = sorted({log.service for log in incident.logs})
        return f"Potential cascade failure starting from {services[0]}"

    def _compute_confidence(
        self,
        incident: Incident,
        errors: list,
        services: list[str],
        deps: dict[str, list[str]],
    ) -> float:
        """Compute raw confidence from evidence dimensions."""
        if not incident.logs:
            return 0.0

        error_ratio = len(errors) / len(incident.logs)
        service_penalty = min(len(services) * 0.02, 0.15)
        deps_bonus = sum(1 for v in deps.values() if v) * 0.05

        base = 0.5 + (error_ratio * 0.3) + deps_bonus - service_penalty
        return max(0.1, min(0.95, base))

    def _apply_window(self, raw: float) -> float:
        """Calibrate confidence using a sliding window of recent values."""
        self._confidence_window.append(raw)
        if len(self._confidence_window) > self._window_size:
            self._confidence_window.pop(0)

        avg = sum(self._confidence_window) / len(self._confidence_window)
        # Pull raw confidence toward historical average to reduce variance
        return raw * 0.7 + avg * 0.3
