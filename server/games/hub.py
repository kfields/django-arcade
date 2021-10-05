from hub import Hub, Subscriber, Event

hub = Hub()

class GameEvent(Event):
    def __init__(self, id, kind):
        super().__init__(id, kind)

class GameSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        print('put in queue')
        if msg.id != self.id:
            return
        await self.queue.put(msg)
