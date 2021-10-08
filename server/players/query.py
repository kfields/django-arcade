from loguru import logger

from channels.db import database_sync_to_async

from schema.base import query

from .models import Player
from .schemata import PlayerConnection

@query.field("allPlayers")
@database_sync_to_async
def resolve_all_players(root, info, after='', before='', first=0, last=0):
    players = [p for p in Player.objects.all()]
    connection = PlayerConnection(players)
    result = connection.wire()
    return result


@query.field("player")
@database_sync_to_async
def resolve_player(*_, id):
    return Player.objects.get(id=id)
