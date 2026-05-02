import pytest
from datetime import datetime
from logcrew.classifier import ClassifierAgent
from logcrew.models import Incident, LogEntry


@pytest.mark.asyncio
async def test_classify_unknown_incident():
    clf = ClassifierAgent()
    inc = Incident(
        id="inc-1",
        trace_id="unknown-trace",
        logs=[
            LogEntry(
                timestamp=datetime.utcnow(),
                service="svc",
                level="ERROR",
                trace_id="unknown-trace",
                message="boom",
            )
        ],
    )
    label, conf = await clf.classify(inc)
    assert label == "unknown"


@pytest.mark.asyncio
async def test_classify_known_incident():
    clf = ClassifierAgent()
    clf.register_known("known-tr", "restart redis")
    inc = Incident(
        id="inc-2",
        trace_id="known-trace",
        logs=[
            LogEntry(
                timestamp=datetime.utcnow(),
                service="svc",
                level="ERROR",
                trace_id="known-trace",
                message="oom",
            )
        ],
    )
    label, conf = await clf.classify(inc)
    assert label == "known"
    assert conf > 0.9
