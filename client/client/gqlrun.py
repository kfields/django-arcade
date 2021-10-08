import asyncio
from contextlib import AsyncExitStack

from loguru import logger

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

class GqlJob:
    def __init__(self, fn, cb):
        self.fn = fn
        self.cb = cb
        self.result = None

class GqlRunner(AsyncExitStack):
    def __init__(self, url):
        super().__init__()

        self.url = url
        self.jobs = []
        self.token = ''

    #It's safe to not call super.  All it does is return self
    async def __aenter__(self):
        self.wsClient = Client(
            transport=WebsocketsTransport(url='ws://' + self.url),
        )
        self.wsSession = await self.enter_async_context(self.wsClient)
        return self

    def add(self, fn, cb):
        self.jobs.append(GqlJob(fn, cb))

    async def step(self):
        while len(self.jobs) != 0:
            job = self.jobs.pop(0)
            task = asyncio.create_task(job.fn())
        await asyncio.sleep(0)

    def execute(self, query, cb, variable_values=None):
        headers=None
        if self.token:
            headers={'Authorization': self.token}
        #logger.debug('execute')
        async def fn():
            client = Client(
                transport=AIOHTTPTransport(url='http://' + self.url, headers=headers),
                fetch_schema_from_transport=True
            )

            async with client as session:
                #logger.debug('execute response')
                result = await session.execute(query, variable_values=variable_values)
                #logger.debug(result)
                cb(result)
        self.add(fn, cb)

    def subscribe(self, query, cb, variable_values=None):
        async def fn(): 
            session = self.wsSession
            async for result in session.subscribe(query, variable_values=variable_values):
                cb(result)
        self.add(fn, cb)

#runner = GqlRunner('localhost:8000/graphql/')
