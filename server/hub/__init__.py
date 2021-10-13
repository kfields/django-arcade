import asyncio

from loguru import logger

class Message:
    def resolve_type(self):
        return self.__class__.__name__

class Event(Message):
    def __init__(self, id):
        self.id = id

class Subscriber:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.active = True

    def send(self, msg):
        logger.debug(f'Subscriber:send: {msg}')

    async def receive(self):
        msg = await self.queue.get()
        logger.debug(f'Subscriber:receive: {msg}')
        return msg


class Hub:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def send(self, msg):
        logger.debug(f'Hub:send: {msg}')
        asyncio.create_task(self.publish(msg))

    async def publish(self, msg):
        logger.debug(f'Hub:publish: {msg}')
        for subscriber in self.subscribers:
            await subscriber.send(msg)
