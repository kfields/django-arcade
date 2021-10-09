#from django.core.serializers.json import DjangoJSONEncoder
import json

factories = None

empty_board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

class GameState:
    def __init__(self, board) -> None:
        self.board = board

    @property
    def typename(self):
        return self.__class__.__name__

    def wire(self):
        return {
            '__typename': self.typename,
            'board': self.board
        }

class WaitState(GameState):
    pass

class ActiveState(GameState):
    pass

class GameStateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GameState):
            return o.wire()
        return super().encode(o)

class GameStateDecoder(json.JSONDecoder):
    def decode(self, s):
        data = super().decode(s)
        if isinstance(data, dict) and '__typename' in data:
            return factories[data['__typename']](data)
        return data

def default_state():
    encoder = GameStateEncoder()
    state = GameState(empty_board)
    return encoder.default(state)

factories = {
    'GameState': lambda data: GameState(data['board']),
    'WaitState': lambda data: WaitState(data['board']),
    'ActiveState': lambda data: ActiveState(data['board']),
}
