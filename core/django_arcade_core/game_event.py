
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

class MarkEvent(GameEvent):
    def __init__(self, id, symbol, x, y):
        super().__init__(id)
        self.symbol = symbol
        self.x = x
        self.y = y

factories = {
    'JoinGameEvent': lambda data: JoinGameEvent(data['id'], data['playerId']),
    'MarkEvent': lambda data: MarkEvent(data['id'], data['symbol'], data['x'], data['y'])
}
