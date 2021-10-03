from queue import Queue
from threading import Thread, Event
from sys import stdout, stderr
from time import sleep

import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

class GqlJob:
    def __init__(self, fn, cb):
        self.fn = fn
        self.cb = cb
        self.result = None

class GqlRunner(Thread):
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = url
        self.jobs = Queue()
        self.results = Queue()

        self.httpClient = Client(
            #transport=RequestsHTTPTransport(url='http://' + url),
            transport=AIOHTTPTransport(url='http://' + url),
            fetch_schema_from_transport=True
        )
        self.wsClient = Client(
            transport=WebsocketsTransport(url='ws://' + url),
        )


    def add(self, fn, cb):
        self.jobs.put(GqlJob(fn, cb))

    def do_callbacks(self):
        while not self.results.empty():
            result = self.results.get()
            result[0](result[1])

    async def main(self):
        while True:
            job = self.jobs.get()
            logger.debug('job:  ', job)
            await job.fn()
            self.jobs.task_done()

    def run(self):
        asyncio.run(self.main())

    def execute(self, query, cb):
        logger.debug('execute')
        async def fn(): 
            async with self.httpClient as session:
                logger.debug('execute response')
                result = await session.execute(query)
                logger.debug(result)
                self.results.put( (cb, result) )
        self.add(fn, cb)

    def subscribe(self, query, cb):
        async def fn(): 
            async with self.wsClient as session:
                async for result in session.subscribe(query):
                    self.results.put( (cb, result) )
        self.add(fn, cb)


runner = GqlRunner('localhost:8000/graphql/')

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