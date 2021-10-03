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

class GqlRunner(Thread):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        self.jobs = Queue()
        self.results = Queue()
        super().__init__(*args, **kwargs)

    def add(self, fn, cb):
        self.jobs.put(GqlJob(fn, cb))

    def do_callbacks(self):
        while not self.results.empty():
            result = self.results.get()
            result[0](result[1])

    async def main(self):
        while True:
            job = self.jobs.get()
            await job.fn()
            self.jobs.task_done()

    def run(self):
        asyncio.run(self.main())

    def execute(self, query, cb):
        async def fn(): 
            async with self.client as session:
                result = await session.execute(query)
                self.results.put( (cb, result) )
        self.add(fn, cb)

    def subscribe(self, query, cb):
        async def fn(): 
            async with self.client as session:
                async for result in session.subscribe(query):
                    self.results.put( (cb, result) )
        self.add(fn, cb)


transport = WebsocketsTransport(url='ws://localhost:8000/graphql/')

client = Client(
    transport=transport,
    #fetch_schema_from_transport=True, #TODO:Ariadne problem?
)

runner = GqlRunner(client)

getMessageQuery = gql("""
query {
  getMessage
}
""")

counterQuery = gql("""
subscription {
  counter
}
""")


def main():
    runner.start()

    def cb(data):
        print(data)

    #runner.subscribe(counterQuery, cb)
    while True:
        print('running ...')
        runner.execute(getMessageQuery, cb)
        runner.do_callbacks()
        sleep(2)

if __name__ == "__main__":
    main()