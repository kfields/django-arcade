from queue import Queue
from threading import Thread, Event
from sys import stdout, stderr
from time import sleep

import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

class GqlJob:
    def __init__(self, fn, cb):
        self.fn = fn
        self.cb = cb
        self.result = None

class GqlRunner:
    def __init__(self, url):
        super().__init__()

        self.url = url
        self.jobs = []
        self.results = []
        '''
        self.httpClient = Client(
            transport=AIOHTTPTransport(url='http://' + url),
            fetch_schema_from_transport=True
        )
        '''
        self.wsClient = Client(
            transport=WebsocketsTransport(url='ws://' + url),
        )

    async def start(self):
        self.wsSession = await self.wsClient.__aenter__()

    async def stop(self):
        #TODO:This is not working well at all
        #await self.wsClient.__aexit__(None, None, None)
        pass

    def add(self, fn, cb):
        self.jobs.append(GqlJob(fn, cb))

    def do_callbacks(self):
        while len(self.results) != 0:
            result = self.results.pop(0)
            result[0](result[1])

    def step(self):
        while len(self.jobs) != 0:
            job = self.jobs.pop(0)
            task = asyncio.create_task(job.fn())

        self.do_callbacks()

    def execute(self, query, cb, variable_values=None):
        #logger.debug('execute')
        async def fn():
            client = Client(
                transport=AIOHTTPTransport(url='http://' + self.url),
                fetch_schema_from_transport=True
            )

            async with client as session:
                #logger.debug('execute response')
                result = await session.execute(query, variable_values=variable_values)
                #logger.debug(result)
                cb(result)
        self.add(fn, cb)

    def subscribe(self, query, cb):
        async def fn(): 
            session = self.wsSession
            async for result in session.subscribe(query):
                cb(result)
        self.add(fn, cb)

runner = GqlRunner('localhost:8000/graphql/')
