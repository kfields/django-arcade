#from django.core.serializers.json import DjangoJSONEncoder
import json
from asgiref.sync import async_to_sync

from django_arcade_core.game_event import JoinEvent, StartEvent, TurnEvent, MarkEvent, EndEvent

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
    'turn': None
}

class GameState:
    def __init__(self, data) -> None:
        self.board = data['board']
        self.turn = data['turn']

    @property
    def typename(self):
        return self.__class__.__name__

    def wire(self):
        return {
            '__typename': self.typename,
            'board': self.board,
            'turn': self.turn
        }

    def enter(self, game):
        pass

    def exit(self):
        pass

    def join(self, game, user):
        if Player.objects.filter(user=user, game=game).exists():
            player = Player.objects.get(user=user, game=game)
        return { 'ok': True, 'message': 'Player joined', 'player': player}

    def ready(self, game, player_id):
        return { 'ok': False, 'message': 'Not time to start!'}

    def mark(self, game, user, x, y):
        return { 'ok': False, 'message': 'Illegal move!'}
    '''
    def check_win_rows(self, symbol):
        for i in range(3):
            count = 0
            for j in range(3):
                if self.board[i][j] == symbol:
                    count += 1
                    if count == 3:
                        return True
    '''
    def check_win_rows(self, symbol):
        for i in range(3):
            if ''.join(self.board[i]) == symbol * 3:
                return True
        return False

    def check_win_cols(self, symbol):
        for j in range(3):
            if self.board[0][j] + self.board[1][j] + self.board[2][j] == symbol * 3:
                return True
        return False

    def check_win_diag(self, symbol):
        if self.board[0][0] + self.board[1][1] + self.board[2][2] == symbol * 3:
            return True
        if self.board[0][2] + self.board[1][1] + self.board[2][0] == symbol * 3:
            return True
        return False

    def check_win(self, symbol):
        return self.check_win_rows(symbol) or self.check_win_cols(symbol) or self.check_win_diag(symbol)

class InitState(GameState):
    def join(self, game, user):
        if Player.objects.filter(user=user, game=game).exists():
            player = Player.objects.get(user=user, game=game)
        elif len(Player.objects.filter(game=game)) == 0:
            player = Player.objects.create(user=user, game=game, symbol='X')
            self.turn = player.id
            async_to_sync(hub.send)(JoinEvent(game.id, player.id))
        else:
            last_player = Player.objects.get(game=game, next=None)
            player = Player.objects.create(user=user, game=game, symbol='O', prev=last_player)
            async_to_sync(hub.send)(JoinEvent(game.id, player.id))
            game.enter(StartState(self.__dict__))

        return { 'ok': True, 'message': 'Player joined', 'player': player}

class StartState(GameState):
    def enter(self, game):
        async_to_sync(hub.send)(StartEvent(game.id))

    def ready(self, game, user):
        player = Player.objects.get(user=user, game=game)
        player.ready()
        player_count = Player.objects.filter(game=game).count()
        ready_count = Player.objects.filter(game=game, status=Player.Status.READY).count()
        if player_count == ready_count:
            game.enter(TurnState(self.__dict__))
        return { 'ok': True, 'message': 'Time to start!'}

class TurnState(GameState):
    def enter(self, game):
        async_to_sync(hub.send)(TurnEvent(game.id, self.turn))

    def mark(self, game, user, x, y):
        player = Player.objects.get(user=user, game=game)
        if player.id != self.turn:
            return { 'ok': False, 'message': 'Not your turn!'}
        if self.board[x][y] != ' ':
            return { 'ok': False, 'message': 'Illegal Move!'}

        self.board[x][y] = player.symbol
        async_to_sync(hub.send)(MarkEvent(game.id, player.symbol, x, y))

        if self.check_win(player.symbol):
            game.enter(EndState(self.__dict__))
            return { 'ok': True, 'message': 'Match!'}

        if hasattr(player, 'next'):
            self.turn = player.next.id
        else:
            self.turn = Player.objects.get(game=game, prev=None).id

        game.enter(TurnState(self.__dict__))
        return { 'ok': True, 'message': ''}

class EndState(GameState):
    def enter(self, game):
        async_to_sync(hub.send)(EndEvent(game.id, self.turn))


class GameStateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GameState):
            return o.wire()
        return super().default(o)

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
    'StartState': lambda data: StartState(data),
    'TurnState': lambda data: TurnState(data),
    'EndState': lambda data: EndState(data),
}
