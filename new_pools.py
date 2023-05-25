#!/usr/bin/env python

import asyncio
from loguru import logger
from redoubt_api import RedoubtEventsStream

def handler(obj):
    print(obj)

async def run_bot():
    logger.info("Running new pools bot")
    stream = RedoubtEventsStream()
    await stream.subscribe(handler)

if __name__ == "__main__":
    asyncio.run(run_bot())