#!/usr/bin/env python

import asyncio
from loguru import logger
from redoubt_api import RedoubtEventsStream
from gql import gql

class JettonTransfersBot:
    def __init__(self):
        self.stream =  RedoubtEventsStream()

    async def handler(self, obj, session):
        # logger.info(obj)
        res = await session.execute(gql("""
            query jetton {
                redoubt_jetton_master(where: {address: {_eq: "%s"}}) {
                    address
                    symbol
                    decimals
                    admin_address
                }
            }
        """ % obj['data']['master']))
        if len(res['redoubt_jetton_master']) == 0:
            logger.info("Jetton master info not found")
        jetton = res['redoubt_jetton_master'][0]
        decimals = jetton.get("decimals", 9)
        if not decimals:
            decimals = 9
        logger.info(f"{obj['data']['source_owner']} => {obj['data']['destination_owner']} {obj['data']['amount'] / pow(10, decimals)} {jetton['symbol']}")

    async def run_bot(self):
        logger.info("Running jetton transfer bot")
        await self.stream.subscribe(self.handler, event_type='Transfer')

if __name__ == "__main__":
    bot = JettonTransfersBot()
    asyncio.run(bot.run_bot())