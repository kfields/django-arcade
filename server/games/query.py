from loguru import logger

from channels.db import database_sync_to_async

from schema.base import query
from players.models import Player

from .models import Game
from .schemata import GameConnection
from schema.types import game

@query.field("allGames")
@database_sync_to_async
def resolve_all_games(root, info, after='', before='', first=0, last=0):
    games = [p for p in Game.objects.all()]
    connection = GameConnection(games)
    result = connection.wire()
    return result


@query.field("game")
@database_sync_to_async
def resolve_game(*_, id):
    return Game.objects.get(id=id)

@game.field("players")
@database_sync_to_async
def resolve_game_players(obj, *_):
    players = list(Player.objects.filter(game=obj['id']))
    return players

@game.field('state')
@database_sync_to_async
def resolve_game_state(obj, *_):
    #obj:  Game instance
    #return obj.wire()
    logger.debug(f'resolve_game_state:game:  {obj}')
    game = Game.objects.get(id=obj['id'])
    state = game.state
    return state.wire()