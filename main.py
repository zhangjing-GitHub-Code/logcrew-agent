#!/usr/bin/env python3
"""LogCrew CLI entrypoint."""

import asyncio
import sys


async def main() -> int:
    print("LogCrew agent system starting...")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
