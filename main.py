#!/usr/bin/env python3
"""LogCrew CLI entrypoint."""

import asyncio
import sys

from logcrew.collector import CollectorAgent
from logcrew.config import LOG_GATEWAY_URL


async def main() -> int:
    print("LogCrew agent system starting...")
    collector = CollectorAgent(LOG_GATEWAY_URL)
    incidents = await collector.ingest([])
    print(f"Flushed {len(incidents)} incidents.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
