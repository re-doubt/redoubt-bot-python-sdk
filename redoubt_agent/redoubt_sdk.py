#!/usr/bin/env python

import asyncio
import inspect
import json
import os
from datetime import datetime, timezone

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.websockets import WebsocketsTransport
from loguru import logger

DEFAULT_ENDPOINT = 'wss://graphql.redoubt.online/v1/graphql'


class RedoubtEventsStream:
    def __init__(self, api_key=None, endpoint=DEFAULT_ENDPOINT):
        if api_key is None:
            api_key = os.environ.get('REDOUBT_API_KEY', None)
        assert api_key is not None, "API key not found"
        self.transport = WebsocketsTransport(
            url=endpoint, ping_interval=1, pong_timeout=1, headers={
                'X-API-Key': api_key
            }
        )

    async def execute(self, query):
        async with Client(transport=self.transport, fetch_schema_from_transport=False) as session:
            return await session.execute(gql(query))

    async def subscribe(self, handler, scope=None, event_type=None, event_target=None):
        now = datetime.now().astimezone(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S")  # "2023-05-29 12:10:16.051"# int(time.time())
        logger.info(f"Starting from cursor {now}")
        filters = []
        if scope is not None:
            filters.append("""{event_scope: {_eq: "%s"}}""" % scope)
        if event_type is not None:
            filters.append("""{event_type: {_eq: "%s"}}""" % event_type)
        if event_target is not None:
            filters.append("""{event_target: {_eq: "%s"}}""" % event_target)
        if len(filters) == 0:
            filters = ""
        else:
            filters = "," + ",".join(filters)

        subscription = gql("""
            subscription GetEventsStreamStreamingSubscription {
                redoubt_events (
                    where: {_and: [
                        {time: {_gte: "%s"}}
                        %s
                    ]}
                    ) {
                    event_id
                    event_scope
                    event_target
                    finding_type
                    event_type
                    severity
                    data
                    time
                }
            }
        """ % (now, filters))
        async with Client(transport=self.transport, fetch_schema_from_transport=False) as session:
            async for result in session.subscribe(subscription):
                for event in result['redoubt_events']:
                    if event_type is not None and event['event_type'] != event_type:
                        logger.info(event_type)
                        continue
                    event['data'] = json.loads(event['data'])
                    if inspect.iscoroutinefunction(handler):
                        await handler(event, session)
                    else:
                        handler(event, session)
