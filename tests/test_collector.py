import pytest
from datetime import datetime
from logcrew.collector import CollectorAgent
from logcrew.models import Incident


@pytest.mark.asyncio
async def test_ingest_creates_incident_for_error_trace():
    collector = CollectorAgent("http://fake")
    raw = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "payment",
            "level": "ERROR",
            "trace_id": "abc123",
            "message": "connection timeout",
            "meta": {},
        }
    ]
    incidents = await collector.ingest(raw)
    assert len(incidents) == 1
    assert incidents[0].trace_id == "abc123"
    assert incidents[0].logs[0].service == "payment"


@pytest.mark.asyncio
async def test_ingest_skips_info_only_trace():
    collector = CollectorAgent("http://fake")
    raw = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "order",
            "level": "INFO",
            "trace_id": "xyz789",
            "message": "order created",
            "meta": {},
        }
    ]
    incidents = await collector.ingest(raw)
    assert len(incidents) == 0
