from loguru import logger

from channels.db import database_sync_to_async

from schema.base import query

from .models import Game
from .schema import GameConnection

@query.field("allGames")
@database_sync_to_async
def resolve_all_games(root, info):
    # return Game.objects.all()
    games = [p for p in Game.objects.all()]
    connection = GameConnection(games)
    result = connection.wire()
    return result


@query.field("game")
@database_sync_to_async
def resolve_game(*_, id):
    return Game.objects.get(id=id)
