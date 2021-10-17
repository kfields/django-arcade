
from .message import Event

factories = None

class GameEvent(Event):
    def __init__(self, id):
        super().__init__(id)

    @classmethod
    def produce(self, data):
        return factories[data['__typename']](data)

class JoinEvent(GameEvent):
    def __init__(self, id, playerId):
        super().__init__(id)
        self.player_id = playerId

class TurnEvent(GameEvent):
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
    'JoinEvent': lambda data: JoinEvent(data['id'], data['playerId']),
    'TurnEvent': lambda data: TurnEvent(data['id'], data['playerId']),
    'MarkEvent': lambda data: MarkEvent(data['id'], data['symbol'], data['x'], data['y'])
}
