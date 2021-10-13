from ariadne import InterfaceType

from loguru import logger

#from hub import Hub, Subscriber, Event
from hub import Hub, Subscriber

hub = Hub()

game_event = InterfaceType("GameEvent")

@game_event.type_resolver
def resolve_game_event_type(obj, *_):
    #return obj.resolve_type()
    return obj.typename

'''
class GameEvent(Event):
    def __init__(self, id):
        super().__init__(id)
    def resolve_type(self):
        return self.__class__.__name__

class JoinGameEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
        self.player_id = playerId

class StartGameEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
'''

class GameSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        logger.debug(f'GameSubscriber:send:  {msg.__dict__}')
        if msg.id != self.id:
            logger.debug(f'GameSubscriber:send:no match:self:  {self.__dict__}')
            return
        await self.queue.put(msg)
