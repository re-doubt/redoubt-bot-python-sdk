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

DEFAULT_DATA_ENDPOINT = 'https://graphql.redoubt.online/v1/graphql'
DEFAULT_EVENTS_ENDPOINT = 'wss://graphql.redoubt.online/events'


class RedoubtEventsStream:
    def __init__(self, api_key=None, data_endpoint=DEFAULT_DATA_ENDPOINT, events_endpoint=DEFAULT_EVENTS_ENDPOINT):
        if api_key is None:
            api_key = os.environ.get('REDOUBT_API_KEY', None)
        assert api_key is not None, "API key not found"
        self.events_transport = WebsocketsTransport(
            url=events_endpoint, ping_interval=1, pong_timeout=1, headers={
                'X-API-Key': api_key
            }
        )
        self.data_transport = AIOHTTPTransport(
            url=data_endpoint, headers={
                'X-API-Key': api_key
            }
        )

    async def execute(self, query):
        async with Client(transport=self.data_transport, fetch_schema_from_transport=False) as session:
            return await session.execute(gql(query))

    async def subscribe(self, handler, scope=None, event_type=None, event_target=None):
        logger.info(f"Starting streaming events for filter scope={scope}, type={event_type}, target={event_target}")
        filters = []
        if scope is not None:
            filters.append("""event_scope: "%s" """ % scope)
        if event_type is not None:
            filters.append("""event_type: "%s" """ % event_type)
        if event_target is not None:
            filters.append("""event_target: "%s" """ % event_target)
        if len(filters) == 0:
            filters = ""
        else:
            filters = ",".join(filters)

        subscription = gql("""
            subscription GetEvents {
                events (%s
                    ) {
                    data
                    event_id
                    event_scope
                    event_target
                    finding_type
                    event_type
                    severity
                }
            }
        """ % (filters))
        async with Client(transport=self.events_transport, fetch_schema_from_transport=False) as session:
            async for result in session.subscribe(subscription):
                event = result['events']
                if event_type is not None and event['event_type'] != event_type:
                    logger.info(event_type)
                    continue
                event['data'] = json.loads(event['data'])
                if inspect.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)