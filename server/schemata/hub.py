import asyncio


class Message:
    pass


class Event(Message):
    def __init__(self, id, kind='default', ok=True):
        self.id = id
        self.kind = kind
        self.ok = ok


class Subscriber:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.active = True

    def send(self, msg):
        pass

    async def receive(self):
        await self.queue.get()

class Hub:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def send(self, msg):
        asyncio.create_task(self.publish(msg))

    async def publish(self, msg):
        for subscriber in self.subscribers:
            await subscriber.send(msg)
