"""Collector Agent — ingest and correlate logs by trace_id."""

import asyncio
from collections import defaultdict
from datetime import datetime

from logcrew.models import LogEntry, Incident


class CollectorAgent:
    """Pull logs from gateway and group them into incidents by trace_id."""

    def __init__(self, gateway_url: str) -> None:
        self.gateway_url = gateway_url
        self._buffer: dict[str, list[LogEntry]] = defaultdict(list)

    async def ingest(self, raw_logs: list[dict]) -> list[Incident]:
        """Ingest raw log dicts, buffer by trace_id, then flush incidents."""
        for raw in raw_logs:
            entry = LogEntry(
                timestamp=datetime.fromisoformat(raw["timestamp"]),
                service=raw["service"],
                level=raw["level"],
                trace_id=raw["trace_id"],
                message=raw["message"],
                meta=raw.get("meta", {}),
            )
            self._buffer[entry.trace_id].append(entry)

        # Flush any trace with error/fatal level as an incident
        incidents: list[Incident] = []
        for trace_id, entries in list(self._buffer.items()):
            if any(e.level in ("ERROR", "FATAL") for e in entries):
                incident = Incident(
                    id=f"inc-{trace_id[:8]}",
                    trace_id=trace_id,
                    logs=entries,
                )
                incidents.append(incident)
                del self._buffer[trace_id]

        return incidents

    async def fetch_from_gateway(self) -> list[dict]:
        """Placeholder for real HTTP fetch from Vector/Kafka gateway."""
        await asyncio.sleep(0.1)
        return []
