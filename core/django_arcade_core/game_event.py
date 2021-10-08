
from .message import Event

factories = None

class GameEvent(Event):
    def __init__(self, id):
        super().__init__(id)

    @classmethod
    def produce(self, data):
        return factories[data['__typename']](data)

class JoinGameEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
        self.player_id = playerId

class StartGameEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)

factories = {
    'JoinGameEvent': lambda data: JoinGameEvent(data['id'], data['playerId']),
    'StartGameEvent': lambda data: StartGameEvent()
}
