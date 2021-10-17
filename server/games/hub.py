from ariadne import InterfaceType

from loguru import logger

from hub import Hub, Subscriber

hub = Hub()

game_event = InterfaceType("GameEvent")

@game_event.type_resolver
def resolve_game_event_type(obj, *_):
    return obj.typename

class GameSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = str(id)

    async def send(self, msg):
        logger.debug(f'GameSubscriber:send:  {msg.__dict__}')
        if msg.id != self.id:
            logger.debug(f'GameSubscriber:send:no match:self:  {self.__dict__}')
            return
        await self.queue.put(msg)
