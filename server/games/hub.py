from loguru import logger

from hub import Hub, Subscriber, Event

hub = Hub()

class GameEvent(Event):
    def __init__(self, id):
        super().__init__(id)

class JoinEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
        self.playerId = playerId

class GameSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        logger.debug(f'GameSubscriber:send:  {msg}')
        if msg.id != self.id:
            logger.debug(f'no match:  {msg}')
            return
        await self.queue.put(msg)
