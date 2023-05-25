#!/usr/bin/env python

import asyncio
import os
import json
from loguru import logger
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.websockets import WebsocketsTransport

DEFAULT_ENDPOINT='ws://44.210.191.88:9080/v1/graphql' # TODO update to wss

class RedoubtEventsStream:
    def __init__(self, endpoint=DEFAULT_ENDPOINT, api_key=None):
        if api_key is None:
            api_key = os.environ.get('REDOUBT_API_KEY', None)
        assert api_key is not None, "API key not found"
        self.transport = WebsocketsTransport(
            url=endpoint, ping_interval=1, pong_timeout=1, headers={
                'X-API-Key': api_key
                }
            )
    
    async def subscribe(self, handler, scope=None, event_type=None):
        subscription = gql("""
            subscription GetEventsStreamStreamingSubscription {
                redoubt_events_stream (
                    cursor:{initial_value: {time: now}},
                    batch_size:1) {
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
        """)
        async with Client(transport=self.transport, fetch_schema_from_transport=False) as session:
            async for result in session.subscribe(subscription):
                for event in result['redoubt_events_stream']:
                    if event_type is not None and event['event_type'] != event_type:
                        continue
                    event['data'] = json.loads(event['data'])
                    handler(event)
