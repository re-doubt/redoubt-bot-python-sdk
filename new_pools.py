#!/usr/bin/env python

import asyncio
from loguru import logger
from redoubt_api import RedoubtEventsStream

def handler(obj, session):
    # logger.info(obj)
    logger.info(f"Got new pool: {obj['data']['pool_name']} with TVL {obj['data']['tvl_ton']}")

async def run_bot():
    logger.info("Running new pools bot")
    stream = RedoubtEventsStream()
    await stream.subscribe(handler, event_type='NewPool')

if __name__ == "__main__":
    asyncio.run(run_bot())