#!/usr/bin/env python3
"""LogCrew CLI entrypoint."""

import asyncio
import sys

from logcrew.analyzer import AnalyzerAgent
from logcrew.classifier import ClassifierAgent
from logcrew.collector import CollectorAgent
from logcrew.config import LOG_GATEWAY_URL
from logcrew.remediator import RemediatorAgent


async def main() -> int:
    print("LogCrew agent system starting...")

    collector = CollectorAgent(LOG_GATEWAY_URL)
    classifier = ClassifierAgent()
    analyzer = AnalyzerAgent()
    remediator = RemediatorAgent()

    # Demo: ingest empty batch
    incidents = await collector.ingest([])
    print(f"Flushed {len(incidents)} incidents.")

    for inc in incidents:
        label, conf = await classifier.classify(inc)
        print(f"  {inc.id} -> {label} ({conf})")

        if label == "unknown":
            rc = await analyzer.analyze(inc)
            plan = await remediator.remediate(inc, rc)
            print(f"  RCA: {rc.hypothesis} (confidence {rc.confidence})")
            print(f"  Remediation: {plan['commands']}")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
