#!/usr/bin/env python

import asyncio

from loguru import logger
from redoubt_agent import RedoubtEventsStream

async def run_query():
    logger.info("Running GraphQL query")
    stream = RedoubtEventsStream()
    res = await stream.execute("""
    query nft {
        redoubt_nft_deals(order_by: {deal_time: desc}, limit: 1) {
            sale_address
            address
            deal_time
            seller
            buyer
            price
        }
    }
    """)
    logger.info(f"Got last NFT deals: {res}")

if __name__ == "__main__":
    asyncio.run(run_query())