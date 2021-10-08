from ariadne import InterfaceType

from loguru import logger

from hub import Hub, Subscriber, Event

hub = Hub()

game_event = InterfaceType("GameEvent")

@game_event.type_resolver
def resolve_game_event_type(obj, *_):
    return obj.resolve_type()

class GameEvent(Event):
    def __init__(self, id):
        super().__init__(id)
    def resolve_type(self):
        return self.__class__.__name__

class JoinGameEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
        self.player_id = playerId
 
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
