from loguru import logger

from channels.db import database_sync_to_async

from django_arcade_core.game_event import GameEvent, JoinEvent, MarkEvent

from schema.base import mutation
from users.jwt import load_user
from .models import Game
from .hub import hub


@mutation.field("createGame")
@database_sync_to_async
def resolve_create_game(_, info):
    user = info.context["user"]
    game = Game.objects.create()
    return game

@mutation.field("joinGame")
@database_sync_to_async
def sync_resolve_join_game(_, info, gameId):
    game = Game.objects.get(id=gameId)
    user = info.context["user"]
    result = game.join(user)
    logger.debug(f'resolve_join_game:result:  {result}')
    if result['ok']:
        game.save()
    return result

@database_sync_to_async
def sync_resolve_mark(_, info, gameId, x, y):
    game = Game.objects.get(id=gameId)
    user = info.context["user"]
    result, event = game.mark(user, x, y)
    logger.debug(f'resolve_mark:result:  {result}')
    if result['ok']:
        game.save()
    return result, event

@mutation.field("mark")
async def resolve_mark(_, info, gameId, x, y):
    result, event = await sync_resolve_mark(_, info, gameId, x, y)
    if result['ok']:
        await hub.send(event)
    return result
