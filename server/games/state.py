#from django.core.serializers.json import DjangoJSONEncoder
import json

from django_arcade_core.game_event import JoinGameEvent, MarkEvent

from players.models import Player

from .hub import hub

factories = None

empty_board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

empty_state = {
    'board': empty_board,
    'rotation': []
}

class GameState:
    def __init__(self, data) -> None:
        self.board = data['board']
        self.rotation = data['rotation']

    @property
    def typename(self):
        return self.__class__.__name__

    def wire(self):
        return {
            '__typename': self.typename,
            'board': self.board,
            'rotation': self.rotation
        }

    def enter(self):
        pass

    def exit(self):
        pass

    def join(self, game, user):
        pass

    def mark(self, game, user, x, y):
        pass

class InitState(GameState):
    def join(self, game, user):
        if Player.objects.filter(user=user, game=game).exists():
            player = Player.objects.get(user=user, game=game)
        #else
        elif len(Player.objects.filter(game=game)) == 0:
            player = Player.objects.create(user=user, game=game, symbol='X')
        else:
            player = Player.objects.create(user=user, game=game, symbol='O')
            game.enter(TurnState(self.__dict__))
        if not player in self.rotation:
            self.rotation.append(player.id)
        return { 'ok': True, 'message': '', 'player': player}

class TurnState(GameState):
    def enter(self):
        pass

    def mark(self, game, user, x, y):
        player = Player.objects.get(user=user, game=game)
        if player.id != self.rotation[0]:
            return { 'ok': False, 'message': 'Not your turn!'}, None
        self.board[x][y] = player.symbol
        return { 'ok': True, 'message': ''}, MarkEvent(game.id, player.symbol, x, y)


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
    state = InitState(empty_state)
    return encoder.default(state)

factories = {
    'InitState': lambda data: InitState(data),
    'TurnState': lambda data: TurnState(data),
}
